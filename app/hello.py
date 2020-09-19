import grpc

from proto.qoin.proto import hello_pb2_grpc, hello_pb2


def hello():
    channel = grpc.insecure_channel('localhost:50051')
    stub = hello_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(name='you'))
    print("Greeter client received: ", response.message)
    response = stub.SayHelloAgain(hello_pb2.HelloRequest(name='you'))
    print("Greeter client received: ", response.message)

    response = stub.HelloStream(hello_pb2.HelloRequest(name='hayashi'))
    for res in response:
        print(res)


if __name__ == "__main__":
    hello()
