import sys
from os import path

import fire
import grpc
import numpy as np
import tensorflow as tf

import config
from proto.qoin.proto import hand_tracking_pb2, hand_tracking_pb2_grpc


def run(host='localhost', port=50051):
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = hand_tracking_pb2_grpc.HandTrackingStub(channel)
    response = stub.HandTrackingPullStream(hand_tracking_pb2.HandTrackingPushRequest())
    model = tf.keras.models.load_model(path.join(config.ProjectRoot, "data", "hand_number_tf"))
    for res in response:
        xyz = np.array([[lm.x, lm.y, lm.z] for lm in res.landmark_list.landmark])
        p = model.predict(np.array([xyz - xyz.mean(axis=0)]))
        hand = p.argmax()
        sys.stdout.write(f"\r {hand}")
        sys.stdout.flush()


if __name__ == '__main__':
    fire.Fire(run)
