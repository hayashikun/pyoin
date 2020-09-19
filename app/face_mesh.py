import os

import fire
import grpc
import numpy as np

import config
from proto.qoin.proto import face_mesh_pb2, face_mesh_pb2_grpc


def run(name, host='localhost', port=50051):
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = face_mesh_pb2_grpc.FaceMeshStub(channel)
    response = stub.FaceMeshPullStream(face_mesh_pb2.FaceMeshPullRequest())
    landmarks = list()
    try:
        for res in response:
            xyz = np.array([
                [[lm.x, lm.y, lm.z] for lm in lml.landmark]
                for lml in res.landmark_list])
            landmarks.append(xyz)
    except KeyboardInterrupt:
        file = os.path.join(config.ProjectRoot, "data", f"{name}.npy")
        if not os.path.exists(dirname := os.path.dirname(file)):
            os.makedirs(dirname)
        np.save(file, np.array(landmarks))
        print(f"{len(landmarks)} data has been saved.")


if __name__ == '__main__':
    fire.Fire(run)
