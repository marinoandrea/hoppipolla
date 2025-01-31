package sources

import (
	"context"
	"encoding/json"
	"log"
	"os"

	pb "github.com/marinoandrea/hoppipolla/pkg/proto/nip_proxy/v1"
)

type LocalNipSourceConfig struct{}

// Local metadata source for mocks and manually recorded data
type LocalNipSource struct {
	isInit   bool
	config   LocalNipSourceConfig
	metadata *Metadata
}

func NewLocalNipSource(cfg LocalNipSourceConfig) *LocalNipSource {
	return &LocalNipSource{config: cfg}
}

func (s *LocalNipSource) Init(ctx context.Context) error {
	entries, err := os.ReadDir("/var/lib/hoppipolla/data")
	if err != nil {
		return err
	}

	metadatas := make([]*Metadata, 0)
	for _, entry := range entries {
		var metadata Metadata

		f, err := os.Open("/var/lib/hoppipolla/data/" + entry.Name())
		if err != nil {
			return err
		}
		stats, err := f.Stat()
		if err != nil {
			return err
		}

		buf := make([]byte, stats.Size())
		_, err = f.Read(buf)
		if err != nil {
			return err
		}
		defer f.Close()

		err = json.Unmarshal(buf, &metadata)
		if err != nil {
			log.Printf("ERROR: failed to parse file '%s'\n", f.Name())
			continue
		}

		metadatas = append(metadatas, &metadata)
	}

	s.metadata = MergeMetadata(metadatas)

	return nil
}

func (s LocalNipSource) Close(ctx context.Context) error {
	return nil
}

func (s LocalNipSource) GetMetadata(ctx context.Context, req *pb.GetMetadataRequest) (*Metadata, error) {
	return s.metadata, nil
}
