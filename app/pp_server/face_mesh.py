from proto.qoin.proto import face_mesh_pb2_grpc, face_mesh_pb2


class FaceMeshService(face_mesh_pb2_grpc.FaceMeshServicer):
    def FaceMeshPullStream(self, request, context):
        for _ in range(100):
            yield face_mesh_pb2.FaceMeshPullReply()

    def FaceMeshPushStream(self, request, context):
        return face_mesh_pb2.FaceMeshPushReply()
