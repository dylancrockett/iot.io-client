from iotio_client import IoTClient
from iotio_client.Endpoint import EndpointInfo, EndpointConstraint, EndpointType
import logging
"""
Example of a iot.io client which uses the EndpointInfo api to tell the server what data it is expecting for each
event endpoint on it's end.

This can be used to auto-generate a Api which will handle requests which can pass data to the client's defined
event endpoints and will auto-parse the data based on the constraints for the endpoint provided by the client.

This is useful if you plan to have clients of the same type which accept different values for the same event, or if 
you want to avoid writing an Api yourself and having the server do that for you. The current Endpoint Api does have
many limitations, such as limited constraints and support for only 4 data types: bool, int, string, and enum. 
"""


# create client
client = IoTClient("test_endpoint_client", "endpoint_echo")


# define the 'boolean' event and give info about the endpoint
@client.on("boolean", EndpointInfo("Bool", EndpointType.BOOLEAN))
def boolean(data):
    print("Got Type:", type(data))
    print("Got Bool from Server API: '", data, "'")
    return "echo_response", data


# define the 'integer' event and give info about the endpoint and what constraints it has
@client.on("integer", EndpointInfo("Int", EndpointType.INTEGER, constraints=EndpointConstraint(min_v=5, max_v=10)))
def echo(data):
    print("Got Type:", type(data))
    print("Got Int from Server API: '", data, "'")
    return "echo_response", data


# define the 'string' event and give info about the endpoint and what constraints it has
@client.on("string", EndpointInfo("String", EndpointType.STRING,
                                  constraints=EndpointConstraint(allow_list="abcdef123456789", length=5)))
def string(data):
    print("Got Type:", type(data))
    print("Got String from Server API: '", data, "'")
    return "echo_response", data


# define the 'enum' event and give info about the endpoint and what constraints it has
@client.on("enum", EndpointInfo("Echo", EndpointType.ENUM,
                                constraints=EndpointConstraint(values={
                                    "apl": "Apple",
                                    "ban": "Banana",
                                    "can": "Cantaloupe"
                                })))
def enum(data):
    print("Got Type:", type(data))
    print("Got Enum from Server API: '", data, "'")
    return "echo_response", data


# connect client
client.run("localhost:5000", use_tls=False)
