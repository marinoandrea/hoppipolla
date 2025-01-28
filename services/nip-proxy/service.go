package main

import (
	"context"
	"fmt"
	"log"
	"net"

	"go-simpler.org/env"
	"google.golang.org/grpc"

	pb "github.com/marinoandrea/hoppipolla/pkg/proto/nip_proxy/v1"
	"github.com/marinoandrea/hoppipolla/services/nip-proxy/sources"
)

type config struct {
	Port             int    `env:"PORT" default:"27003"`
	SciondAddr       string `env:"SCIOND_ADDR" default:"127.0.0.1:30255"`
	CacheSize        int    `env:"CACHE_SIZE" default:"1000"`
	GoogleMapsApiKey string `env:"GOOGLE_MAPS_API_KEY"`
}

type server struct {
	pb.UnimplementedNipProxyServer
	config  config
	sources []sources.NipSource
}

func newServer(cfg config) server {
	nipSources := make([]sources.NipSource, 0)

	// more sources can be added here
	nipSources = append(nipSources, sources.NewScionNipSource(sources.ScionNipSourceConfig{
		SciondAddress:    cfg.SciondAddr,
		GoogleMapsApiKey: cfg.GoogleMapsApiKey,
		CacheSize:        cfg.CacheSize,
	}))

	return server{
		config:  cfg,
		sources: nipSources,
	}
}

func (s *server) init(ctx context.Context) error {
	for _, source := range s.sources {
		err := source.Init(ctx)
		if err != nil {
			return err
		}
	}

	return nil
}

func (s *server) shutdown(ctx context.Context) error {
	for _, source := range s.sources {
		err := source.Close(ctx)
		if err != nil {
			return err
		}
	}
	return nil
}

func (s *server) GetMetadata(ctx context.Context, req *pb.GetMetadataRequest) (*pb.GetMetadataResponse, error) {
	var out pb.GetMetadataResponse

	results := make([]*sources.Metadata, 0)
	for _, source := range s.sources {
		metadata, err := source.GetMetadata(ctx, req)
		if err != nil {
			// NOTE(andrea): maybe we should not fail on source retrieval
			return nil, err
		}
		results = append(results, metadata)
	}

	mergedResults := sources.MergeMetadata(results)
	for _, metadata := range mergedResults.NodeInfo {
		out.NodeInfo = append(out.NodeInfo, FromNodeMetadataToPB(metadata))
	}
	for _, metadata := range mergedResults.LinkInfo {
		out.LinkInfo = append(out.LinkInfo, FromLinkMetadataToPB(metadata))
	}

	return &out, nil
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
	defer server.shutdown(context.Background())

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", &server.config.Port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	grpcServer := grpc.NewServer()

	log.Printf("server listening at %v", lis.Addr())

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
