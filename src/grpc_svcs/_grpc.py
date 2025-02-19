import contextvars

from grpc_interceptor import AsyncServerInterceptor, ServerInterceptor
from svcs import Container, Registry

_containers: contextvars.ContextVar[Container] = contextvars.ContextVar("svcs_containers")


def svcs_from() -> Container:
    """
    Get the container for the current gRPC request Context.
    """
    return _containers.get()


# TODO: Use the built-in grpc.ServerInterceptor instead of adding the grpc-interceptor dependency
class SVCSInterceptor(ServerInterceptor):
    """A sync gRPC server interceptor for svcs."""

    def __init__(self, registry: Registry | None = None):
        """Create an interceptor to handle svcs Container creation."""
        if registry is None:
            registry = Registry()

        self._registry = registry

    def intercept(self, method, request_or_iterator, context, method_name):
        _containers.set(Container(self._registry))

        # Ensure Container is closed
        try:
            return method(request_or_iterator, context)
        except:
            raise
        finally:
            container = _containers.get()
            container.close()


# TODO: Use the built-in grpc.aio.ServerInterceptor instead of adding the grpc-interceptor dependency
class SVCSAsyncInterceptor(AsyncServerInterceptor):
    """An async gRPC interceptor for svcs."""

    def __init__(self, registry: Registry | None = None):
        """Create an async interceptor to handle svcs Container creation."""
        if registry is None:
            registry = Registry()

        self._registry = registry

    async def intercept(self, method, request_or_iterator, context, method_name):
        _containers.set(Container(self._registry))

        # Ensure Container is closed
        try:
            return await method(request_or_iterator, context)
        except:
            raise
        finally:
            container = _containers.get()
            container.close()
