import os

import fire
import grpc
import numpy as np

import config
from proto.qoin.proto import hand_tracking_pb2, hand_tracking_pb2_grpc


def run(name, host='localhost', port=50051):
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = hand_tracking_pb2_grpc.HandTrackingStub(channel)
    response = stub.HandTrackingPullStream(hand_tracking_pb2.HandTrackingPullRequest())
    landmarks = list()
    try:
        for res in response:
            xyz = np.array([[lm.x, lm.y, lm.z] for lm in res.landmark_list.landmark])
            landmarks.append(xyz)
    except KeyboardInterrupt:
        file = os.path.join(config.ProjectRoot, "data", f"{name}.npy")
        if not os.path.exists(dirname := os.path.dirname(file)):
            os.makedirs(dirname)
        np.save(file, np.array(landmarks))
        print(f"{len(landmarks)} data has been saved.")


if __name__ == '__main__':
    fire.Fire(run)
