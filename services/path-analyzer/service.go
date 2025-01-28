package main

import (
	"context"
	"fmt"
	"net"
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/hashicorp/golang-lru/v2/expirable"
	"go-simpler.org/env"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"

	pb "github.com/marinoandrea/hoppipolla/pkg/proto/path_analyzer/v1"
	policypb "github.com/marinoandrea/hoppipolla/pkg/proto/policy_manager/v1"

	"github.com/scionproto/scion/pkg/addr"
	"github.com/scionproto/scion/pkg/daemon"
	"github.com/scionproto/scion/pkg/snet"
)

type config struct {
	Port              int    `env:"PORT" default:"27001"`
	SciondAddr        string `env:"SCIOND_ADDR" default:"127.0.0.1:30255"`
	CacheSize         int    `env:"CACHE_SIZE" default:"1000"`
	PolicyManagerAddr string `env:"POLICY_MANAGER_ADDR" default:"127.0.0.1:27002"`
}

type server struct {
	pb.UnimplementedPathAnalyzerServer
	config              config
	daemon              *daemon.Service
	conn                daemon.Connector
	cache               *expirable.LRU[addr.IA, []snet.Path]
	policyManagerConn   *grpc.ClientConn
	policyManagerClient policypb.PolicyManagerClient
}

func newServer(cfg config) server {
	return server{
		config: cfg,
		daemon: &daemon.Service{Address: cfg.SciondAddr},
		cache:  expirable.NewLRU[addr.IA, []snet.Path](cfg.CacheSize, nil, 0),
	}
}

func (s *server) init(ctx context.Context) error {
	conn, err := grpc.NewClient(s.config.PolicyManagerAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return err
	}

	s.policyManagerConn = conn
	s.policyManagerClient = policypb.NewPolicyManagerClient(conn)

	// subscribe to policy manager updates to keep cache consistency
	var req emptypb.Empty
	_, err = s.policyManagerClient.SubscribePathAnalyzer(context.Background(), &req)
	if err != nil {
		return err
	}

	dconn, err := s.daemon.Connect(ctx)
	if err != nil {
		return err
	}
	s.conn = dconn

	return nil
}

func (s *server) shutdown() error {
	err := s.policyManagerConn.Close()
	return err
}

func (s *server) Refresh(ctx context.Context, req *emptypb.Empty) (*emptypb.Empty, error) {
	var res emptypb.Empty
	s.cache.Purge()
	return &res, nil
}

func (s *server) GetPath(ctx context.Context, req *pb.GetPathRequest) (*pb.GetPathResponse, error) {
	var res pb.GetPathResponse

	src, err := s.conn.LocalIA(ctx)
	if err != nil {
		return nil, err
	}

	dst := addr.IA(req.Destination)
	now := time.Now()

	// check in-memory caches
	paths, ok := s.cache.Get(dst)
	if ok {
		for _, path := range paths {
			if path.Metadata().Expiry.After(now) {
				res.Path = convertPathToMsg(path)
				return &res, nil
			}
		}
	}
	s.cache.Remove(dst)

	// retrieve new candidates from sciond
	candidates, err := s.conn.Paths(ctx, dst, src, daemon.PathReqFlags{})
	if err != nil {
		return nil, err
	}

	pathToLinks := make(map[snet.Path][]*policypb.Link)
	for _, path := range candidates {
		idfs := path.Metadata().Interfaces
		links := make([]*policypb.Link, 0)
		for i := range len(idfs) {
			idfA := idfs[i]
			idfB := idfs[i+1]
			// NOTE(andrea): we have to convert to string here cause our
			// reasoner in the policy-manager service only supports 32-bit
			links = append(links, &policypb.Link{
				AsA: idfA.IA.String(),
				IfA: idfA.ID.String(),
				AsB: idfB.IA.String(),
				IfB: idfB.ID.String()})
		}
		pathToLinks[path] = links
	}

	// obtain valid paths from policy-manager
	graph := make([]*policypb.Link, 0)
	for _, links := range pathToLinks {
		for _, link := range links {
			graph = append(graph, link)
		}
	}

	policyRes, err := s.policyManagerClient.FindPaths(ctx, &policypb.FindPathsRequest{
		Src:   src.String(),
		Dst:   dst.String(),
		Links: graph})
	if err != nil {
		return nil, err
	}

	// NOTE(andrea): inefficient operation, but allows to preserve snet.Path
	// metadata without leaking SCION abstractions into the policy-manager which
	// should be somewhat dataplane agnostic
	paths = make([]snet.Path, 0)
	for _, policyPath := range policyRes.Paths {
		found := true
		for _, path := range candidates {
			if len(path.Metadata().Interfaces) != len(policyPath.Links) {
				continue
			}
			for i := range len(policyPath.Links) {
				if pathToLinks[path][i].AsA != policyPath.Links[i].AsA || pathToLinks[path][i].AsB != policyPath.Links[i].AsB || pathToLinks[path][i].IfA != policyPath.Links[i].IfA || pathToLinks[path][i].IfB != policyPath.Links[i].IfB {
					found = false
					break
				}
			}
			if found {
				paths = append(paths, path)
			}
		}
	}

	s.cache.Add(dst, paths)

	if len(paths) > 0 {
		res.Path = convertPathToMsg(paths[0])
	}

	return &res, nil
}

func convertPathToMsg(path snet.Path) *pb.Path {
	out := pb.Path{
		SrcIsdAs: uint64(path.Source()),
		DstIsdAs: uint64(path.Destination()),
		Hops:     make([]*pb.Hop, 0, len(path.Metadata().Interfaces)),
	}

	for _, idf := range path.Metadata().Interfaces {
		out.Hops = append(out.Hops, &pb.Hop{
			IsdAs: uint64(idf.IA),
			IfId:  uint64(idf.ID)})
	}

	return &out
}

func main() {
	var cfg config
	if err := env.Load(&cfg, nil); err != nil {
		log.Fatalf("failed to load env vars: %v", err)
	}

	server := newServer(cfg)
	if err := server.init(context.Background()); err != nil {
		log.Fatalf("failed to initialize server: %v", err)
	}
	defer server.shutdown()

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", &server.config.Port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	grpcServer := grpc.NewServer()
	pb.RegisterPathAnalyzerServer(grpcServer, &server)

	log.Printf("server listening at %v", lis.Addr())

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
