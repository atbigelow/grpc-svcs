# grpc-svcs: A gRPC integration for SVCS

Very in-development

## Installation
```shell
pip install grpc-svcs
```

## Usage
```python
import grpc_svcs
import svcs

registry = svcs.Registry()
# Register services
registry.register_value(MyType, MyType())

# Attach a `SVCSInterceptor` when creating server.
server = grpc.server(intercepters=[grpc_svcs.SVCSInterceptor(registry)])

# Attach a `SVCSAsyncIntercept` when creating an async server.
server = grpc.aio.server(intercepters=[grpc_svcs.SVCSAsyncInterceptor(registry)])

# Retrieve container inside a servicer
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # call svcs_from
        container = grpc_svcs.svcs_from()
        # get items from svcs
        my_type = container.get(MyType)

        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)