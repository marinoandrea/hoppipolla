package main

import (
	"log"
	"time"

	papb "github.com/marinoandrea/hoppipolla/pkg/proto/path_analyzer/v1"
	pmpb "github.com/marinoandrea/hoppipolla/pkg/proto/policy_manager/v1"
	"github.com/scionproto/scion/pkg/daemon"
	"google.golang.org/grpc"
)

const N_TEST = 5
const N_RUNS = 100

const DST = "16-ffaa:0:1002"
const ADDR_SCIOND = "127.0.0.1:30255"
const ADDR_PATH_ANALYZER = "127.0.0.1:27001"
const ADDR_POLICY_MANAGER = "127.0.0.1:27002"

const OUTPUT_FILE = "perftest_cache.csv"

var results [N_TEST][N_RUNS]time.Duration

var scionDaemon *daemon.Service
var scionDaemonConn daemon.Connector

var paClient papb.PathAnalyzerClient
var pmClient pmpb.PolicyManagerClient

var paConn *grpc.ClientConn
var pmConn *grpc.ClientConn

func main() {
	log.Println("Executing base performance test")
	executeBasePerftest()
	log.Println("Executing cached performance test")
	executeCachedPerftest()
}
