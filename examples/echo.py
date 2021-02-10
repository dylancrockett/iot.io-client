from iotio_client import IoTClient
import threading
import time

# create client
client = IoTClient("echo_test_client", "echo")


# define a handler for "echo_response" events
@client.on("echo_response")
def echo(data):
    print("'echo_response' from Server: '" + str(data) + "'\n")


def send():
    client.ensure_open()

    # loop while client is connected
    while client.connected:
        message = input("Enter a value to send to the server: ")

        # send message over the echo channel
        client.send("echo", message)
        print("")
        time.sleep(1)


# start background send task
send_thread = threading.Thread(None, send)
send_thread.start()

# connect client
client.run("localhost:5000", use_tls=False)
send_thread.join()
