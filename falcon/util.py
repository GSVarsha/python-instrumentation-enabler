import falcon
import logging

# # Set up logging for better visibility
# logging.basicConfig(level=logging.DEBUG)

class AuthMiddleware:
    """
    A placeholder middleware for demonstration purposes. 
    In a real app, this would handle authentication, authorization, or request logging.
    """
    def process_request(self, req: falcon.Request, resp: falcon.Response):
        """Called before the request is routed to a resource."""
        logging.info(f"Incoming request: {req.method} {req.path}")

    def process_response(self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded: bool):
        """Called after the response is sent back to the client."""
        logging.info(f"Outgoing response: {req.method} {req.path} -> Status {resp.status}")
