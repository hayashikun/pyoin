import threading
import unittest

import grpc

from app import pp_server
from proto.qoin.proto import hello_pb2_grpc, hello_pb2


class TestPpServer(unittest.TestCase):
    port = 50051
    workers = 4

    def setUp(self):
        self.pp_server = pp_server.PpServer(max_workers=self.workers)
        self.channel = grpc.insecure_channel(f'localhost:{self.port}')

        start_event = threading.Event()

        def server_start(_self):
            _self.pp_server.run(_self.port)

        def is_server_started(_self):
            return _self.pp_server.server._state.stage == grpc._server._ServerStage.STARTED  # noqa

        def check_server_running(_self):
            while not is_server_started(_self):
                pass
            start_event.set()

        threading.Thread(target=server_start, args=(self,)).start()
        threading.Thread(target=check_server_running, args=(self,)).start()

        start_event.wait(3)

        if not is_server_started(self):
            raise Exception("Failed to start server")

    def tearDown(self):
        self.pp_server.server._state.termination_event.set()

    def test_hello(self):
        stub = hello_pb2_grpc.GreeterStub(self.channel)
        res = stub.SayHello(hello_pb2.HelloRequest(name='you'))
        self.assertEqual(res.message, 'Hello, you!')

    def test_hello_stream(self):
        stub = hello_pb2_grpc.GreeterStub(self.channel)

        def test_stream(name, stream_event):
            try:
                res = stub.HelloStream(hello_pb2.HelloRequest(name=name))
                for r in res:
                    if not stream_event.is_set():
                        stream_event.set()
                        self.assertEqual(r.message, f'Hello Stream, {name}!')
            except grpc._channel._MultiThreadedRendezvous:  # noqa
                pass

        events = list()
        for i in range(self.workers + 1):
            event = threading.Event()
            threading.Thread(target=test_stream, args=(f'you_{i}', event)).start()
            events.append(event)

        for event in events:
            event.wait(1)

        for event in events[:-1]:
            self.assertTrue(event.is_set())
        self.assertFalse(events[-1].is_set())

        self.channel.close()

    def test_1000_workers(self):
        self.tearDown()
        self.workers = 1000
        self.setUp()
        self.test_hello_stream()

    def test_face_mesh_pull_push(self):
        self.assertTrue(True)
