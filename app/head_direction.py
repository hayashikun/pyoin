import sys

import fire
import grpc
import numpy as np

from app.face_mesh_landmark_parts_index import parts_index
from proto.qoin.proto import face_mesh_pb2, face_mesh_pb2_grpc


def run(host='localhost', port=50051):
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = face_mesh_pb2_grpc.FaceMeshStub(channel)
    response = stub.FaceMeshPullStream(face_mesh_pb2.FaceMeshPullRequest())

    xy_threshold = 0.5  # tilt head
    yz_threshold = 0.2  # turn up/down
    xz_threshold = 0.5  # turn right/left

    def calc_slope(landmark):
        left_eye = landmark[parts_index["left_eye"], :].mean(axis=0)
        right_eye = landmark[parts_index["right_eye"], :].mean(axis=0)
        eye_center = (left_eye + right_eye) / 2
        upper_lip = landmark[parts_index["upper_lip"], :].mean(axis=0)
        lower_lip = landmark[parts_index["lower_lip"], :].mean(axis=0)
        lip_center = (upper_lip + lower_lip) / 2
        xy_eye_slope = (right_eye[1] - left_eye[1]) / (right_eye[0] - left_eye[0])
        xz_eye_slope = (right_eye[2] - left_eye[2]) / (right_eye[0] - left_eye[0])
        yz_eye_lip_slope = (eye_center[2] - lip_center[2]) / (eye_center[1] - lip_center[1])
        return xy_eye_slope, yz_eye_lip_slope, xz_eye_slope,

    sampling_count = 10
    samples = list()
    init_slope = None

    for res in response:
        xyz = np.array([[lm.x, lm.y, lm.z] for lm in res.landmark_list[0].landmark])
        if 0 < sampling_count:
            samples.append(xyz)
            sampling_count -= 1
            continue
        if init_slope is None:
            init_slope = calc_slope(np.mean(samples, axis=0))
            print(f"Sampling done, xy: {init_slope[0]:.2f}, yz: {init_slope[1]:.2f}, zx: {init_slope[2]:.2f}")

        xy, yz, xz = calc_slope(xyz)
        xy -= init_slope[0]
        yz -= init_slope[1]
        xz -= init_slope[2]

        head_direction = f"\rxy: {xy:+.2f}, yz: {yz:+.2f}, zx: {xz:+.2f}"
        if np.abs(xy) > xy_threshold:
            head_direction += ", tilt " + ("left" if xy < 0 else "right")
        if np.abs(yz) > yz_threshold:
            head_direction += ", turn " + ("up" if yz < 0 else "down")
        if np.abs(xz) > xz_threshold:
            head_direction += ", turn " + ("right" if yz < 0 else "left")

        sys.stdout.write(head_direction)
        sys.stdout.flush()


if __name__ == '__main__':
    fire.Fire(run)
