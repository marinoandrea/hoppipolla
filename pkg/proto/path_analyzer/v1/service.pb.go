// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.36.4
// 	protoc        v3.12.4
// source: path_analyzer/v1/service.proto

package path_analyzer

import (
	empty "github.com/golang/protobuf/ptypes/empty"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
	unsafe "unsafe"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

// A SCION network path
type Path struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// Source ISD-AS address
	Src string `protobuf:"bytes,1,opt,name=src,proto3" json:"src,omitempty"`
	// Destination ISD-AS address
	Dst string `protobuf:"bytes,2,opt,name=dst,proto3" json:"dst,omitempty"`
	// String representation of the path
	Sequence string `protobuf:"bytes,3,opt,name=sequence,proto3" json:"sequence,omitempty"`
	// List of hops in the path (excluding src and dst)
	Hops          []*Hop `protobuf:"bytes,4,rep,name=hops,proto3" json:"hops,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Path) Reset() {
	*x = Path{}
	mi := &file_path_analyzer_v1_service_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Path) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Path) ProtoMessage() {}

func (x *Path) ProtoReflect() protoreflect.Message {
	mi := &file_path_analyzer_v1_service_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Path.ProtoReflect.Descriptor instead.
func (*Path) Descriptor() ([]byte, []int) {
	return file_path_analyzer_v1_service_proto_rawDescGZIP(), []int{0}
}

func (x *Path) GetSrc() string {
	if x != nil {
		return x.Src
	}
	return ""
}

func (x *Path) GetDst() string {
	if x != nil {
		return x.Dst
	}
	return ""
}

func (x *Path) GetSequence() string {
	if x != nil {
		return x.Sequence
	}
	return ""
}

func (x *Path) GetHops() []*Hop {
	if x != nil {
		return x.Hops
	}
	return nil
}

// A hop in a SCION network path
type Hop struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// ISD-AS address
	As string `protobuf:"bytes,1,opt,name=as,proto3" json:"as,omitempty"`
	// Interface ID
	If            string `protobuf:"bytes,2,opt,name=if,proto3" json:"if,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Hop) Reset() {
	*x = Hop{}
	mi := &file_path_analyzer_v1_service_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Hop) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Hop) ProtoMessage() {}

func (x *Hop) ProtoReflect() protoreflect.Message {
	mi := &file_path_analyzer_v1_service_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Hop.ProtoReflect.Descriptor instead.
func (*Hop) Descriptor() ([]byte, []int) {
	return file_path_analyzer_v1_service_proto_rawDescGZIP(), []int{1}
}

func (x *Hop) GetAs() string {
	if x != nil {
		return x.As
	}
	return ""
}

func (x *Hop) GetIf() string {
	if x != nil {
		return x.If
	}
	return ""
}

type GetPathRequest struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// ISD-AS destination target
	Destination   string `protobuf:"bytes,1,opt,name=destination,proto3" json:"destination,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *GetPathRequest) Reset() {
	*x = GetPathRequest{}
	mi := &file_path_analyzer_v1_service_proto_msgTypes[2]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *GetPathRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetPathRequest) ProtoMessage() {}

func (x *GetPathRequest) ProtoReflect() protoreflect.Message {
	mi := &file_path_analyzer_v1_service_proto_msgTypes[2]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetPathRequest.ProtoReflect.Descriptor instead.
func (*GetPathRequest) Descriptor() ([]byte, []int) {
	return file_path_analyzer_v1_service_proto_rawDescGZIP(), []int{2}
}

func (x *GetPathRequest) GetDestination() string {
	if x != nil {
		return x.Destination
	}
	return ""
}

type GetPathResponse struct {
	state protoimpl.MessageState `protogen:"open.v1"`
	// Optional SCION network path to reach destination if there is a valid one
	Paths         []*Path `protobuf:"bytes,1,rep,name=paths,proto3" json:"paths,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *GetPathResponse) Reset() {
	*x = GetPathResponse{}
	mi := &file_path_analyzer_v1_service_proto_msgTypes[3]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *GetPathResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetPathResponse) ProtoMessage() {}

func (x *GetPathResponse) ProtoReflect() protoreflect.Message {
	mi := &file_path_analyzer_v1_service_proto_msgTypes[3]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetPathResponse.ProtoReflect.Descriptor instead.
func (*GetPathResponse) Descriptor() ([]byte, []int) {
	return file_path_analyzer_v1_service_proto_rawDescGZIP(), []int{3}
}

func (x *GetPathResponse) GetPaths() []*Path {
	if x != nil {
		return x.Paths
	}
	return nil
}

var File_path_analyzer_v1_service_proto protoreflect.FileDescriptor

var file_path_analyzer_v1_service_proto_rawDesc = string([]byte{
	0x0a, 0x1e, 0x70, 0x61, 0x74, 0x68, 0x5f, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2f,
	0x76, 0x31, 0x2f, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x12, 0x21, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x68, 0x6f, 0x70, 0x70, 0x69, 0x70, 0x6f, 0x6c,
	0x6c, 0x61, 0x2e, 0x70, 0x61, 0x74, 0x68, 0x5f, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72,
	0x2e, 0x76, 0x31, 0x1a, 0x1b, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2f, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x62, 0x75, 0x66, 0x2f, 0x65, 0x6d, 0x70, 0x74, 0x79, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x22, 0x82, 0x01, 0x0a, 0x04, 0x50, 0x61, 0x74, 0x68, 0x12, 0x10, 0x0a, 0x03, 0x73, 0x72, 0x63,
	0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x03, 0x73, 0x72, 0x63, 0x12, 0x10, 0x0a, 0x03, 0x64,
	0x73, 0x74, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x03, 0x64, 0x73, 0x74, 0x12, 0x1a, 0x0a,
	0x08, 0x73, 0x65, 0x71, 0x75, 0x65, 0x6e, 0x63, 0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x08, 0x73, 0x65, 0x71, 0x75, 0x65, 0x6e, 0x63, 0x65, 0x12, 0x3a, 0x0a, 0x04, 0x68, 0x6f, 0x70,
	0x73, 0x18, 0x04, 0x20, 0x03, 0x28, 0x0b, 0x32, 0x26, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e,
	0x68, 0x6f, 0x70, 0x70, 0x69, 0x70, 0x6f, 0x6c, 0x6c, 0x61, 0x2e, 0x70, 0x61, 0x74, 0x68, 0x5f,
	0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2e, 0x76, 0x31, 0x2e, 0x48, 0x6f, 0x70, 0x52,
	0x04, 0x68, 0x6f, 0x70, 0x73, 0x22, 0x25, 0x0a, 0x03, 0x48, 0x6f, 0x70, 0x12, 0x0e, 0x0a, 0x02,
	0x61, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x02, 0x61, 0x73, 0x12, 0x0e, 0x0a, 0x02,
	0x69, 0x66, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x02, 0x69, 0x66, 0x22, 0x32, 0x0a, 0x0e,
	0x47, 0x65, 0x74, 0x50, 0x61, 0x74, 0x68, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x20,
	0x0a, 0x0b, 0x64, 0x65, 0x73, 0x74, 0x69, 0x6e, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x18, 0x01, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x0b, 0x64, 0x65, 0x73, 0x74, 0x69, 0x6e, 0x61, 0x74, 0x69, 0x6f, 0x6e,
	0x22, 0x50, 0x0a, 0x0f, 0x47, 0x65, 0x74, 0x50, 0x61, 0x74, 0x68, 0x52, 0x65, 0x73, 0x70, 0x6f,
	0x6e, 0x73, 0x65, 0x12, 0x3d, 0x0a, 0x05, 0x70, 0x61, 0x74, 0x68, 0x73, 0x18, 0x01, 0x20, 0x03,
	0x28, 0x0b, 0x32, 0x27, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x68, 0x6f, 0x70, 0x70, 0x69,
	0x70, 0x6f, 0x6c, 0x6c, 0x61, 0x2e, 0x70, 0x61, 0x74, 0x68, 0x5f, 0x61, 0x6e, 0x61, 0x6c, 0x79,
	0x7a, 0x65, 0x72, 0x2e, 0x76, 0x31, 0x2e, 0x50, 0x61, 0x74, 0x68, 0x52, 0x05, 0x70, 0x61, 0x74,
	0x68, 0x73, 0x32, 0xbb, 0x01, 0x0a, 0x0c, 0x50, 0x61, 0x74, 0x68, 0x41, 0x6e, 0x61, 0x6c, 0x79,
	0x7a, 0x65, 0x72, 0x12, 0x70, 0x0a, 0x07, 0x47, 0x65, 0x74, 0x50, 0x61, 0x74, 0x68, 0x12, 0x31,
	0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x68, 0x6f, 0x70, 0x70, 0x69, 0x70, 0x6f, 0x6c, 0x6c,
	0x61, 0x2e, 0x70, 0x61, 0x74, 0x68, 0x5f, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2e,
	0x76, 0x31, 0x2e, 0x47, 0x65, 0x74, 0x50, 0x61, 0x74, 0x68, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73,
	0x74, 0x1a, 0x32, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x68, 0x6f, 0x70, 0x70, 0x69, 0x70,
	0x6f, 0x6c, 0x6c, 0x61, 0x2e, 0x70, 0x61, 0x74, 0x68, 0x5f, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a,
	0x65, 0x72, 0x2e, 0x76, 0x31, 0x2e, 0x47, 0x65, 0x74, 0x50, 0x61, 0x74, 0x68, 0x52, 0x65, 0x73,
	0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x39, 0x0a, 0x07, 0x52, 0x65, 0x66, 0x72, 0x65, 0x73, 0x68,
	0x12, 0x16, 0x2e, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62,
	0x75, 0x66, 0x2e, 0x45, 0x6d, 0x70, 0x74, 0x79, 0x1a, 0x16, 0x2e, 0x67, 0x6f, 0x6f, 0x67, 0x6c,
	0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e, 0x45, 0x6d, 0x70, 0x74, 0x79,
	0x42, 0x3c, 0x5a, 0x3a, 0x67, 0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x6d,
	0x61, 0x72, 0x69, 0x6e, 0x6f, 0x61, 0x6e, 0x64, 0x72, 0x65, 0x61, 0x2f, 0x68, 0x6f, 0x70, 0x70,
	0x69, 0x70, 0x6f, 0x6c, 0x6c, 0x61, 0x2f, 0x70, 0x6b, 0x67, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x2f, 0x70, 0x61, 0x74, 0x68, 0x5f, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x62, 0x06,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
})

var (
	file_path_analyzer_v1_service_proto_rawDescOnce sync.Once
	file_path_analyzer_v1_service_proto_rawDescData []byte
)

func file_path_analyzer_v1_service_proto_rawDescGZIP() []byte {
	file_path_analyzer_v1_service_proto_rawDescOnce.Do(func() {
		file_path_analyzer_v1_service_proto_rawDescData = protoimpl.X.CompressGZIP(unsafe.Slice(unsafe.StringData(file_path_analyzer_v1_service_proto_rawDesc), len(file_path_analyzer_v1_service_proto_rawDesc)))
	})
	return file_path_analyzer_v1_service_proto_rawDescData
}

var file_path_analyzer_v1_service_proto_msgTypes = make([]protoimpl.MessageInfo, 4)
var file_path_analyzer_v1_service_proto_goTypes = []any{
	(*Path)(nil),            // 0: proto.hoppipolla.path_analyzer.v1.Path
	(*Hop)(nil),             // 1: proto.hoppipolla.path_analyzer.v1.Hop
	(*GetPathRequest)(nil),  // 2: proto.hoppipolla.path_analyzer.v1.GetPathRequest
	(*GetPathResponse)(nil), // 3: proto.hoppipolla.path_analyzer.v1.GetPathResponse
	(*empty.Empty)(nil),     // 4: google.protobuf.Empty
}
var file_path_analyzer_v1_service_proto_depIdxs = []int32{
	1, // 0: proto.hoppipolla.path_analyzer.v1.Path.hops:type_name -> proto.hoppipolla.path_analyzer.v1.Hop
	0, // 1: proto.hoppipolla.path_analyzer.v1.GetPathResponse.paths:type_name -> proto.hoppipolla.path_analyzer.v1.Path
	2, // 2: proto.hoppipolla.path_analyzer.v1.PathAnalyzer.GetPath:input_type -> proto.hoppipolla.path_analyzer.v1.GetPathRequest
	4, // 3: proto.hoppipolla.path_analyzer.v1.PathAnalyzer.Refresh:input_type -> google.protobuf.Empty
	3, // 4: proto.hoppipolla.path_analyzer.v1.PathAnalyzer.GetPath:output_type -> proto.hoppipolla.path_analyzer.v1.GetPathResponse
	4, // 5: proto.hoppipolla.path_analyzer.v1.PathAnalyzer.Refresh:output_type -> google.protobuf.Empty
	4, // [4:6] is the sub-list for method output_type
	2, // [2:4] is the sub-list for method input_type
	2, // [2:2] is the sub-list for extension type_name
	2, // [2:2] is the sub-list for extension extendee
	0, // [0:2] is the sub-list for field type_name
}

func init() { file_path_analyzer_v1_service_proto_init() }
func file_path_analyzer_v1_service_proto_init() {
	if File_path_analyzer_v1_service_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: unsafe.Slice(unsafe.StringData(file_path_analyzer_v1_service_proto_rawDesc), len(file_path_analyzer_v1_service_proto_rawDesc)),
			NumEnums:      0,
			NumMessages:   4,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_path_analyzer_v1_service_proto_goTypes,
		DependencyIndexes: file_path_analyzer_v1_service_proto_depIdxs,
		MessageInfos:      file_path_analyzer_v1_service_proto_msgTypes,
	}.Build()
	File_path_analyzer_v1_service_proto = out.File
	file_path_analyzer_v1_service_proto_goTypes = nil
	file_path_analyzer_v1_service_proto_depIdxs = nil
}
