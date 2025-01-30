package main

import (
	"context"
	"log"
	"time"

	papb "github.com/marinoandrea/hoppipolla/pkg/proto/path_analyzer/v1"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"
)

var results [1]*papb.GetPathsResponse

var paClient papb.PathAnalyzerClient

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

	paRes, err := paClient.GetPaths(context.TODO(), &paReq)
	if err != nil {
		log.Fatalln(err)
	}
	results[0] = paRes
}

func setup() {
	paConn, err := grpc.NewClient("127.0.0.1:27001", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalln(err)
	}
	defer paConn.Close()

	paClient = papb.NewPathAnalyzerClient(paConn)
}

func clean() {
	paClient.Refresh(context.TODO(), &emptypb.Empty{})
}
