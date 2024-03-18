import json
import math
from threading import Thread, Lock
import zmq

import subprocess
from serverClass import ServerClass
from threading import Lock
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from bokeh.layouts import column
from serverClass import ServerClass
import json
import math
from threading import Thread
import zmq
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler

lock = Lock()
instance = ServerClass(0, 0)

def update_values():
    global t
    while True:
        with lock:
            instance.valueA = math.sin(t)
            instance.valueB = math.cos(t)
        t += 0.1

def server_task():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:12345")
    while True:
        # serialized_instance = json.dumps(instance.to_dict())
        message_rx = socket.recv()
        print(f"Received request: {message_rx}")
        socket.send_string("serialized_instance")



def make_document(doc):
    # Initialize plots for valueA and valueB
    plot_valueA = figure(width=800, height=400, title="Value A")
    plot_valueB = figure(width=800, height=400, title="Value B")

    # Add line renderer to each plot
    line_valueA = plot_valueA.line([], [], color="firebrick", line_width=2)
    line_valueB = plot_valueB.line([], [], color="navy", line_width=2)

    # Reference to each plot's data source for easy updating
    ds_valueA = line_valueA.data_source
    ds_valueB = line_valueB.data_source

    @linear()
    def update(step):
        # Simulate update of values (this logic will depend on your actual data update mechanism)
        instance.valueA = math.sin(step * 0.1)
        instance.valueB = math.cos(step * 0.1)

        # Append new data points to the lines
        ds_valueA.data['x'].append(step)
        ds_valueA.data['y'].append(instance.valueA)
        ds_valueB.data['x'].append(step)
        ds_valueB.data['y'].append(instance.valueB)

        # Trigger update to both data sources to refresh the plots
        ds_valueA.trigger('data', ds_valueA.data, ds_valueA.data)
        ds_valueB.trigger('data', ds_valueB.data, ds_valueB.data)

    # Add both plots to the document using a column layout
    doc.add_root(column(plot_valueA, plot_valueB))
    doc.add_periodic_callback(update, 100)  # Adjust the update frequency as needed

def start_bokeh_server():
    bokeh_app = Application(FunctionHandler(make_document))
    server = Server({'/': bokeh_app}, num_procs=1)
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

if __name__ == "__main__":
    start_bokeh_server()
    Thread(target=update_values, daemon=True).start()
    zmq_thread = Thread(target=server_task, daemon=True)
    zmq_thread.start()
    # zmq_thread.join()
