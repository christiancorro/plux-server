import json
import math
import random
import zmq


class ServerClass:
    def __init__(self, attribute1, attribute2):
        self.valueA = attribute1
        self.valueB = attribute2

    def to_dict(self):
        return {"attribute1": self.valueA, "attribute2": self.valueB}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:12345")

t = 0

instance = ServerClass("server_value1", 3)

while True:
    #  wait request from client
    message_rx = socket.recv()
    print(f"Received request: {message_rx}")

    #  do something
    # time.sleep(1) `t` appropriately in your code

    instance.valueA = math.sin(t)
    instance.valueB = math.sin(t + math.pi / 2)

    #  reply to client
    serialized_instance = json.dumps(instance.to_dict())
    socket.send_string(serialized_instance)
    t += 0.1