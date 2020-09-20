from proto.qoin.proto import hello_pb2_grpc, hello_pb2


class HelloService(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return hello_pb2.HelloReply(message='Hello Again, %s!' % request.name)

    def HelloStream(self, request, context):
        while True:
            yield hello_pb2.HelloReply(message='Hello Stream, %s!' % request.name)
