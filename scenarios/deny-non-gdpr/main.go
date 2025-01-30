package main

import (
	"context"
	"log"
	"os"
	"time"

	papb "github.com/marinoandrea/hoppipolla/pkg/proto/path_analyzer/v1"
	pmpb "github.com/marinoandrea/hoppipolla/pkg/proto/policy_manager/v1"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"
)

var policy string
var results [2]*papb.GetPathsResponse

var paClient papb.PathAnalyzerClient
var pmClient pmpb.PolicyManagerClient

func main() {
	setup()
	start := time.Now()
	execute()
	elapsed := time.Since(start)
	log.Printf("Elapsed %s", elapsed)
	clean()
	log.Println(results)
}

func execute() {
	paReq := papb.GetPathsRequest{Destination: "16-ffaa:0:1002"}
	pmReq := pmpb.CreatePolicyRequest{Source: policy}

	// retrieve valid paths for destination
	paRes1, err := paClient.GetPaths(context.TODO(), &paReq)
	if err != nil {
		log.Fatalln(err)
	}

	// publish policy denying non-GDPR countries
	_, err = pmClient.CreatePolicy(context.TODO(), &pmReq)
	if err != nil {
		log.Fatalln(err)
	}
	results[0] = paRes1

	// retrieve valid paths for destination
	paRes2, err := paClient.GetPaths(context.TODO(), &paReq)
	if err != nil {
		log.Fatalln(err)
	}
	results[1] = paRes2
}

func setup() {
	// load policy
	f, err := os.Open("./policy.lp")
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()

	info, err := f.Stat()
	if err != nil {
		log.Fatalln(err)
	}

	buf := make([]byte, info.Size())

	_, err = f.Read(buf)
	if err != nil {
		log.Fatalln(err)
	}

	policy = string(buf)

	// initialize connection to path-analyzer service
	paConn, err := grpc.NewClient("127.0.0.1:27001", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalln(err)
	}
	defer paConn.Close()

	paClient = papb.NewPathAnalyzerClient(paConn)

	// initialize connection to policy-manager service
	pmConn, err := grpc.NewClient("127.0.0.1:27002", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalln(err)
	}
	defer pmConn.Close()

	pmClient = pmpb.NewPolicyManagerClient(pmConn)
}

func clean() {
	pmClient.ResetPolicies(context.TODO(), &emptypb.Empty{})
	paClient.Refresh(context.TODO(), &emptypb.Empty{})
}
