import zmq
import time
from tqdm import tqdm




context = zmq.Context()

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:12345")

latencies_ms = []

try:

    for _ in tqdm(range(100000), desc="Sending requests"):
        start_time = time.perf_counter()

        request_message = "Request"
        socket.send_string(request_message)

        message_rx = socket.recv()
        # print(message_rx)
        print(f"Received message: {message_rx.decode('utf-8')}")

        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000
        latencies_ms.append(latency_ms)

except KeyboardInterrupt:
    print("\nClient has been stopped prematurely.")

finally:
    socket.close()
    context.term()

    if latencies_ms:
        latencies_ms.sort()
        mid = len(latencies_ms) // 2
        if len(latencies_ms) % 2 == 0:
            median_latency_ms = (latencies_ms[mid - 1] + latencies_ms[mid]) / 2
        else:
            median_latency_ms = latencies_ms[mid]
        
        print(f"Median latency: {median_latency_ms} milliseconds")
    else:
        print("No latencies were recorded.")
