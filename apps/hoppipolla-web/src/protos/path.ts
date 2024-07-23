// @ts-nocheck
/**
 * Generated by the protoc-gen-ts.  DO NOT EDIT!
 * compiler version: 3.19.1
 * source: path.proto
 * git: https://github.com/thesayyn/protoc-gen-ts */
import * as pb_1 from "google-protobuf";
import * as grpc_1 from "@grpc/grpc-js";
export namespace hoppipolla.path {
    export class Hop extends pb_1.Message {
        #one_of_decls: number[][] = [];
        constructor(data?: any[] | {
            isd_as?: string;
            inbound_interface?: number;
            outbound_interface?: number;
        }) {
            super();
            pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
            if (!Array.isArray(data) && typeof data == "object") {
                if ("isd_as" in data && data.isd_as != undefined) {
                    this.isd_as = data.isd_as;
                }
                if ("inbound_interface" in data && data.inbound_interface != undefined) {
                    this.inbound_interface = data.inbound_interface;
                }
                if ("outbound_interface" in data && data.outbound_interface != undefined) {
                    this.outbound_interface = data.outbound_interface;
                }
            }
        }
        get isd_as() {
            return pb_1.Message.getFieldWithDefault(this, 1, "") as string;
        }
        set isd_as(value: string) {
            pb_1.Message.setField(this, 1, value);
        }
        get inbound_interface() {
            return pb_1.Message.getFieldWithDefault(this, 2, 0) as number;
        }
        set inbound_interface(value: number) {
            pb_1.Message.setField(this, 2, value);
        }
        get outbound_interface() {
            return pb_1.Message.getFieldWithDefault(this, 3, 0) as number;
        }
        set outbound_interface(value: number) {
            pb_1.Message.setField(this, 3, value);
        }
        static fromObject(data: {
            isd_as?: string;
            inbound_interface?: number;
            outbound_interface?: number;
        }): Hop {
            const message = new Hop({});
            if (data.isd_as != null) {
                message.isd_as = data.isd_as;
            }
            if (data.inbound_interface != null) {
                message.inbound_interface = data.inbound_interface;
            }
            if (data.outbound_interface != null) {
                message.outbound_interface = data.outbound_interface;
            }
            return message;
        }
        toObject() {
            const data: {
                isd_as?: string;
                inbound_interface?: number;
                outbound_interface?: number;
            } = {};
            if (this.isd_as != null) {
                data.isd_as = this.isd_as;
            }
            if (this.inbound_interface != null) {
                data.inbound_interface = this.inbound_interface;
            }
            if (this.outbound_interface != null) {
                data.outbound_interface = this.outbound_interface;
            }
            return data;
        }
        serialize(): Uint8Array;
        serialize(w: pb_1.BinaryWriter): void;
        serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
            const writer = w || new pb_1.BinaryWriter();
            if (this.isd_as.length)
                writer.writeString(1, this.isd_as);
            if (this.inbound_interface != 0)
                writer.writeUint32(2, this.inbound_interface);
            if (this.outbound_interface != 0)
                writer.writeUint32(3, this.outbound_interface);
            if (!w)
                return writer.getResultBuffer();
        }
        static deserialize(bytes: Uint8Array | pb_1.BinaryReader): Hop {
            const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new Hop();
            while (reader.nextField()) {
                if (reader.isEndGroup())
                    break;
                switch (reader.getFieldNumber()) {
                    case 1:
                        message.isd_as = reader.readString();
                        break;
                    case 2:
                        message.inbound_interface = reader.readUint32();
                        break;
                    case 3:
                        message.outbound_interface = reader.readUint32();
                        break;
                    default: reader.skipField();
                }
            }
            return message;
        }
        serializeBinary(): Uint8Array {
            return this.serialize();
        }
        static deserializeBinary(bytes: Uint8Array): Hop {
            return Hop.deserialize(bytes);
        }
    }
    export class Path extends pb_1.Message {
        #one_of_decls: number[][] = [];
        constructor(data?: any[] | {
            fingerprint?: string;
            src_isd_as?: string;
            dst_isd_as?: string;
            sequence?: string;
            expiration?: string;
            mtu?: number;
            hops?: Hop[];
        }) {
            super();
            pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [7], this.#one_of_decls);
            if (!Array.isArray(data) && typeof data == "object") {
                if ("fingerprint" in data && data.fingerprint != undefined) {
                    this.fingerprint = data.fingerprint;
                }
                if ("src_isd_as" in data && data.src_isd_as != undefined) {
                    this.src_isd_as = data.src_isd_as;
                }
                if ("dst_isd_as" in data && data.dst_isd_as != undefined) {
                    this.dst_isd_as = data.dst_isd_as;
                }
                if ("sequence" in data && data.sequence != undefined) {
                    this.sequence = data.sequence;
                }
                if ("expiration" in data && data.expiration != undefined) {
                    this.expiration = data.expiration;
                }
                if ("mtu" in data && data.mtu != undefined) {
                    this.mtu = data.mtu;
                }
                if ("hops" in data && data.hops != undefined) {
                    this.hops = data.hops;
                }
            }
        }
        get fingerprint() {
            return pb_1.Message.getFieldWithDefault(this, 1, "") as string;
        }
        set fingerprint(value: string) {
            pb_1.Message.setField(this, 1, value);
        }
        get src_isd_as() {
            return pb_1.Message.getFieldWithDefault(this, 2, "") as string;
        }
        set src_isd_as(value: string) {
            pb_1.Message.setField(this, 2, value);
        }
        get dst_isd_as() {
            return pb_1.Message.getFieldWithDefault(this, 3, "") as string;
        }
        set dst_isd_as(value: string) {
            pb_1.Message.setField(this, 3, value);
        }
        get sequence() {
            return pb_1.Message.getFieldWithDefault(this, 4, "") as string;
        }
        set sequence(value: string) {
            pb_1.Message.setField(this, 4, value);
        }
        get expiration() {
            return pb_1.Message.getFieldWithDefault(this, 5, "") as string;
        }
        set expiration(value: string) {
            pb_1.Message.setField(this, 5, value);
        }
        get mtu() {
            return pb_1.Message.getFieldWithDefault(this, 6, 0) as number;
        }
        set mtu(value: number) {
            pb_1.Message.setField(this, 6, value);
        }
        get hops() {
            return pb_1.Message.getRepeatedWrapperField(this, Hop, 7) as Hop[];
        }
        set hops(value: Hop[]) {
            pb_1.Message.setRepeatedWrapperField(this, 7, value);
        }
        static fromObject(data: {
            fingerprint?: string;
            src_isd_as?: string;
            dst_isd_as?: string;
            sequence?: string;
            expiration?: string;
            mtu?: number;
            hops?: ReturnType<typeof Hop.prototype.toObject>[];
        }): Path {
            const message = new Path({});
            if (data.fingerprint != null) {
                message.fingerprint = data.fingerprint;
            }
            if (data.src_isd_as != null) {
                message.src_isd_as = data.src_isd_as;
            }
            if (data.dst_isd_as != null) {
                message.dst_isd_as = data.dst_isd_as;
            }
            if (data.sequence != null) {
                message.sequence = data.sequence;
            }
            if (data.expiration != null) {
                message.expiration = data.expiration;
            }
            if (data.mtu != null) {
                message.mtu = data.mtu;
            }
            if (data.hops != null) {
                message.hops = data.hops.map(item => Hop.fromObject(item));
            }
            return message;
        }
        toObject() {
            const data: {
                fingerprint?: string;
                src_isd_as?: string;
                dst_isd_as?: string;
                sequence?: string;
                expiration?: string;
                mtu?: number;
                hops?: ReturnType<typeof Hop.prototype.toObject>[];
            } = {};
            if (this.fingerprint != null) {
                data.fingerprint = this.fingerprint;
            }
            if (this.src_isd_as != null) {
                data.src_isd_as = this.src_isd_as;
            }
            if (this.dst_isd_as != null) {
                data.dst_isd_as = this.dst_isd_as;
            }
            if (this.sequence != null) {
                data.sequence = this.sequence;
            }
            if (this.expiration != null) {
                data.expiration = this.expiration;
            }
            if (this.mtu != null) {
                data.mtu = this.mtu;
            }
            if (this.hops != null) {
                data.hops = this.hops.map((item: Hop) => item.toObject());
            }
            return data;
        }
        serialize(): Uint8Array;
        serialize(w: pb_1.BinaryWriter): void;
        serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
            const writer = w || new pb_1.BinaryWriter();
            if (this.fingerprint.length)
                writer.writeString(1, this.fingerprint);
            if (this.src_isd_as.length)
                writer.writeString(2, this.src_isd_as);
            if (this.dst_isd_as.length)
                writer.writeString(3, this.dst_isd_as);
            if (this.sequence.length)
                writer.writeString(4, this.sequence);
            if (this.expiration.length)
                writer.writeString(5, this.expiration);
            if (this.mtu != 0)
                writer.writeUint64(6, this.mtu);
            if (this.hops.length)
                writer.writeRepeatedMessage(7, this.hops, (item: Hop) => item.serialize(writer));
            if (!w)
                return writer.getResultBuffer();
        }
        static deserialize(bytes: Uint8Array | pb_1.BinaryReader): Path {
            const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new Path();
            while (reader.nextField()) {
                if (reader.isEndGroup())
                    break;
                switch (reader.getFieldNumber()) {
                    case 1:
                        message.fingerprint = reader.readString();
                        break;
                    case 2:
                        message.src_isd_as = reader.readString();
                        break;
                    case 3:
                        message.dst_isd_as = reader.readString();
                        break;
                    case 4:
                        message.sequence = reader.readString();
                        break;
                    case 5:
                        message.expiration = reader.readString();
                        break;
                    case 6:
                        message.mtu = reader.readUint64();
                        break;
                    case 7:
                        reader.readMessage(message.hops, () => pb_1.Message.addToRepeatedWrapperField(message, 7, Hop.deserialize(reader), Hop));
                        break;
                    default: reader.skipField();
                }
            }
            return message;
        }
        serializeBinary(): Uint8Array {
            return this.serialize();
        }
        static deserializeBinary(bytes: Uint8Array): Path {
            return Path.deserialize(bytes);
        }
    }
    export class GetPathForAddrRequest extends pb_1.Message {
        #one_of_decls: number[][] = [];
        constructor(data?: any[] | {
            destination?: string;
        }) {
            super();
            pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
            if (!Array.isArray(data) && typeof data == "object") {
                if ("destination" in data && data.destination != undefined) {
                    this.destination = data.destination;
                }
            }
        }
        get destination() {
            return pb_1.Message.getFieldWithDefault(this, 1, "") as string;
        }
        set destination(value: string) {
            pb_1.Message.setField(this, 1, value);
        }
        static fromObject(data: {
            destination?: string;
        }): GetPathForAddrRequest {
            const message = new GetPathForAddrRequest({});
            if (data.destination != null) {
                message.destination = data.destination;
            }
            return message;
        }
        toObject() {
            const data: {
                destination?: string;
            } = {};
            if (this.destination != null) {
                data.destination = this.destination;
            }
            return data;
        }
        serialize(): Uint8Array;
        serialize(w: pb_1.BinaryWriter): void;
        serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
            const writer = w || new pb_1.BinaryWriter();
            if (this.destination.length)
                writer.writeString(1, this.destination);
            if (!w)
                return writer.getResultBuffer();
        }
        static deserialize(bytes: Uint8Array | pb_1.BinaryReader): GetPathForAddrRequest {
            const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new GetPathForAddrRequest();
            while (reader.nextField()) {
                if (reader.isEndGroup())
                    break;
                switch (reader.getFieldNumber()) {
                    case 1:
                        message.destination = reader.readString();
                        break;
                    default: reader.skipField();
                }
            }
            return message;
        }
        serializeBinary(): Uint8Array {
            return this.serialize();
        }
        static deserializeBinary(bytes: Uint8Array): GetPathForAddrRequest {
            return GetPathForAddrRequest.deserialize(bytes);
        }
    }
    export class GetPathForAddrResponse extends pb_1.Message {
        #one_of_decls: number[][] = [[1]];
        constructor(data?: any[] | ({} & (({
            path?: Path;
        })))) {
            super();
            pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
            if (!Array.isArray(data) && typeof data == "object") {
                if ("path" in data && data.path != undefined) {
                    this.path = data.path;
                }
            }
        }
        get path() {
            return pb_1.Message.getWrapperField(this, Path, 1) as Path;
        }
        set path(value: Path) {
            pb_1.Message.setOneofWrapperField(this, 1, this.#one_of_decls[0], value);
        }
        get has_path() {
            return pb_1.Message.getField(this, 1) != null;
        }
        get _path() {
            const cases: {
                [index: number]: "none" | "path";
            } = {
                0: "none",
                1: "path"
            };
            return cases[pb_1.Message.computeOneofCase(this, [1])];
        }
        static fromObject(data: {
            path?: ReturnType<typeof Path.prototype.toObject>;
        }): GetPathForAddrResponse {
            const message = new GetPathForAddrResponse({});
            if (data.path != null) {
                message.path = Path.fromObject(data.path);
            }
            return message;
        }
        toObject() {
            const data: {
                path?: ReturnType<typeof Path.prototype.toObject>;
            } = {};
            if (this.path != null) {
                data.path = this.path.toObject();
            }
            return data;
        }
        serialize(): Uint8Array;
        serialize(w: pb_1.BinaryWriter): void;
        serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
            const writer = w || new pb_1.BinaryWriter();
            if (this.has_path)
                writer.writeMessage(1, this.path, () => this.path.serialize(writer));
            if (!w)
                return writer.getResultBuffer();
        }
        static deserialize(bytes: Uint8Array | pb_1.BinaryReader): GetPathForAddrResponse {
            const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new GetPathForAddrResponse();
            while (reader.nextField()) {
                if (reader.isEndGroup())
                    break;
                switch (reader.getFieldNumber()) {
                    case 1:
                        reader.readMessage(message.path, () => message.path = Path.deserialize(reader));
                        break;
                    default: reader.skipField();
                }
            }
            return message;
        }
        serializeBinary(): Uint8Array {
            return this.serialize();
        }
        static deserializeBinary(bytes: Uint8Array): GetPathForAddrResponse {
            return GetPathForAddrResponse.deserialize(bytes);
        }
    }
    interface GrpcUnaryServiceInterface<P, R> {
        (message: P, metadata: grpc_1.Metadata, options: grpc_1.CallOptions, callback: grpc_1.requestCallback<R>): grpc_1.ClientUnaryCall;
        (message: P, metadata: grpc_1.Metadata, callback: grpc_1.requestCallback<R>): grpc_1.ClientUnaryCall;
        (message: P, options: grpc_1.CallOptions, callback: grpc_1.requestCallback<R>): grpc_1.ClientUnaryCall;
        (message: P, callback: grpc_1.requestCallback<R>): grpc_1.ClientUnaryCall;
    }
    interface GrpcStreamServiceInterface<P, R> {
        (message: P, metadata: grpc_1.Metadata, options?: grpc_1.CallOptions): grpc_1.ClientReadableStream<R>;
        (message: P, options?: grpc_1.CallOptions): grpc_1.ClientReadableStream<R>;
    }
    interface GrpWritableServiceInterface<P, R> {
        (metadata: grpc_1.Metadata, options: grpc_1.CallOptions, callback: grpc_1.requestCallback<R>): grpc_1.ClientWritableStream<P>;
        (metadata: grpc_1.Metadata, callback: grpc_1.requestCallback<R>): grpc_1.ClientWritableStream<P>;
        (options: grpc_1.CallOptions, callback: grpc_1.requestCallback<R>): grpc_1.ClientWritableStream<P>;
        (callback: grpc_1.requestCallback<R>): grpc_1.ClientWritableStream<P>;
    }
    interface GrpcChunkServiceInterface<P, R> {
        (metadata: grpc_1.Metadata, options?: grpc_1.CallOptions): grpc_1.ClientDuplexStream<P, R>;
        (options?: grpc_1.CallOptions): grpc_1.ClientDuplexStream<P, R>;
    }
    interface GrpcPromiseServiceInterface<P, R> {
        (message: P, metadata: grpc_1.Metadata, options?: grpc_1.CallOptions): Promise<R>;
        (message: P, options?: grpc_1.CallOptions): Promise<R>;
    }
    export abstract class UnimplementedPathAnalyzerService {
        static definition = {
            GetPathForAddr: {
                path: "/hoppipolla.path.PathAnalyzer/GetPathForAddr",
                requestStream: false,
                responseStream: false,
                requestSerialize: (message: GetPathForAddrRequest) => Buffer.from(message.serialize()),
                requestDeserialize: (bytes: Buffer) => GetPathForAddrRequest.deserialize(new Uint8Array(bytes)),
                responseSerialize: (message: GetPathForAddrResponse) => Buffer.from(message.serialize()),
                responseDeserialize: (bytes: Buffer) => GetPathForAddrResponse.deserialize(new Uint8Array(bytes))
            }
        };
        [method: string]: grpc_1.UntypedHandleCall;
        abstract GetPathForAddr(call: grpc_1.ServerUnaryCall<GetPathForAddrRequest, GetPathForAddrResponse>, callback: grpc_1.sendUnaryData<GetPathForAddrResponse>): void;
    }
    export class PathAnalyzerClient extends grpc_1.makeGenericClientConstructor(UnimplementedPathAnalyzerService.definition, "PathAnalyzer", {}) {
        constructor(address: string, credentials: grpc_1.ChannelCredentials, options?: Partial<grpc_1.ChannelOptions>) {
            super(address, credentials, options);
        }
        GetPathForAddr: GrpcUnaryServiceInterface<GetPathForAddrRequest, GetPathForAddrResponse> = (message: GetPathForAddrRequest, metadata: grpc_1.Metadata | grpc_1.CallOptions | grpc_1.requestCallback<GetPathForAddrResponse>, options?: grpc_1.CallOptions | grpc_1.requestCallback<GetPathForAddrResponse>, callback?: grpc_1.requestCallback<GetPathForAddrResponse>): grpc_1.ClientUnaryCall => {
            return super.GetPathForAddr(message, metadata, options, callback);
        };
    }
}