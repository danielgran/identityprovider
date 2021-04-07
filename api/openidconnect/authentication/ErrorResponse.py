import json


# TODO Redis Cache Store (MySQL)
class ErrorResponse:
    def __init__(self, message):
        self.message = message

    message = ""


    def __repr__(self):
        return json.dumps({
            "message": self.message
        })
