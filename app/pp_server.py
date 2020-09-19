from concurrent import futures

import grpc

from proto.qoin.proto import hello_pb2_grpc, hello_pb2, \
    face_mesh_pb2_grpc, face_mesh_pb2, \
    hand_tracking_pb2_grpc, hand_tracking_pb2


class HelloService(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return hello_pb2.HelloReply(message='Hello Again, %s!' % request.name)

    def HelloStream(self, request, context):
        for _ in range(10):
            yield hello_pb2.HelloReply(message='Hello Stream, %s!' % request.name)


class HandTrackingService(hand_tracking_pb2_grpc.HandTrackingServicer):
    def HandTrackingPullStream(self, request, context):
        for _ in range(100):
            yield hand_tracking_pb2.HandTrackingPullReply()

    def HandTrackingPushStream(self, request, context):
        return hand_tracking_pb2.HandTrackingPushReply()


class FaceMeshService(face_mesh_pb2_grpc.FaceMeshServicer):
    def FaceMeshPullStream(self, request, context):
        for _ in range(100):
            yield face_mesh_pb2.FaceMeshPullReply()

    def FaceMeshPushStream(self, request, context):
        return face_mesh_pb2.FaceMeshPushReply()


def run(port=50051):
    hello_service = HelloService()
    hand_tracking_service = HandTrackingService()
    face_mesh_service = FaceMeshService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))

    hello_pb2_grpc.add_GreeterServicer_to_server(hello_service, server)
    hand_tracking_pb2_grpc.add_HandTrackingServicer_to_server(hand_tracking_service, server)
    face_mesh_pb2_grpc.add_FaceMeshServicer_to_server(face_mesh_service, server)
    server.add_insecure_port(f'localhost:{port}')
    server.start()
    print(f"Server running http://localhost:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    run()
