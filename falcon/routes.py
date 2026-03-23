import falcon
import json

class CommonClass:
    """
    A sink that catches all unmatched routes (defined by r'/+') 
    and returns a standard 404 Not Found response.
    """
    def __call__(self, req: falcon.Request, resp: falcon.Response):
        """This method handles any requests that fall into the sink."""
        
        # Set the status to 404 Not Found
        resp.status = falcon.HTTP_404
        resp.content_type = falcon.MEDIA_JSON
        
        # Provide a helpful error message
        resp.text = json.dumps({
            "error": "Not Found",
            "message": f"The requested resource was not found on this server: {req.path}",
            "available_routes": ["/", "/info", "/health"]
        })
