import zmq
import json

def server_task():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:12345")
    print("Server started, waiting for connections...")

    try:
        while True:
            # Wait for the next request from a client
            message = socket.recv_string()
            print(f"Received request: {message}")

            # Do some work here (simulate with sleep, process data, etc.)

            # Send reply back to client
            response = json.dumps({"response": "OK"})
            socket.send_string(response)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    server_task()