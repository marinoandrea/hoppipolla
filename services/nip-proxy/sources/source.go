package sources

import (
	"context"

	pb "github.com/marinoandrea/hoppipolla/pkg/proto/nip_proxy/v1"
)

type Link struct {
	AsA string
	IfA string
	AsB string
	IfB string
}

type MetadataRequest struct {
	Src      string
	Dst      string
	Topology []*Link
}

type LinkMetadata struct {
	Name        string
	Link        Link
	ValueBool   *bool
	ValueInt32  *int32
	ValueString *string
}

type NodeMetadata struct {
	Name        string
	As          string
	ValueBool   *bool
	ValueInt32  *int32
	ValueString *string
}

type Metadata struct {
	LinkInfo []LinkMetadata
	NodeInfo []NodeMetadata
}

// Represents a Network Information Plane (NIP) data source.
// It is an external service which provides network metadata based on
// a topology and optionally a source and destination node for path search.
type NipSource interface {
	GetMetadata(ctx context.Context, req *pb.GetMetadataRequest) (*Metadata, error)
	Init(ctx context.Context) error
	Close(ctx context.Context) error
}

func MergeMetadata(ress []*Metadata) *Metadata {
	var out Metadata
	for _, res := range ress {
		for _, nodeInfo := range res.NodeInfo {
			out.NodeInfo = append(out.NodeInfo, nodeInfo)
		}
		for _, linkInfo := range res.LinkInfo {
			out.LinkInfo = append(out.LinkInfo, linkInfo)
		}
	}
	return &out
}
