package main

import (
	"context"
	"log"
	"time"

	"github.com/scionproto/scion/pkg/addr"
	"github.com/scionproto/scion/pkg/daemon"
	"github.com/scionproto/scion/pkg/snet"
)

var policy string
var results [2][]snet.Path

var scionDaemon *daemon.Service
var scionDaemonConn daemon.Connector

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
	src, err := scionDaemonConn.LocalIA(context.TODO())
	if err != nil {
		log.Fatalln(err)
	}

	dst, err := addr.ParseIA("16-ffaa:0:1002")
	if err != nil {
		log.Fatalln(err)
	}

	candidates, err := scionDaemonConn.Paths(context.TODO(), dst, src,
		daemon.PathReqFlags{Refresh: true})
	if err != nil {
		log.Fatalln(err)
	}
	results[0] = candidates

	candidates, err = scionDaemonConn.Paths(context.TODO(), dst, src,
		daemon.PathReqFlags{Refresh: true})
	if err != nil {
		log.Fatalln(err)
	}
	results[1] = candidates
}

func setup() {
	scionDaemon = &daemon.Service{Address: "127.0.0.1:30255"}
	conn, err := scionDaemon.Connect(context.TODO())
	if err != nil {
		log.Fatalln(err)
	}
	scionDaemonConn = conn
}

func clean() {
	scionDaemonConn.Close()
}
