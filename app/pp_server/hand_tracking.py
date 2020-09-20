from proto.qoin.proto import hand_tracking_pb2_grpc, hand_tracking_pb2


class HandTrackingService(hand_tracking_pb2_grpc.HandTrackingServicer):
    def HandTrackingPullStream(self, request, context):
        for _ in range(100):
            yield hand_tracking_pb2.HandTrackingPullReply()

    def HandTrackingPushStream(self, request, context):
        return hand_tracking_pb2.HandTrackingPushReply()
