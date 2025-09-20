from requests import Session


class HTTPClient:
    def __init__(self, session: Session, endpoint):
        self.session = session
        self.endpoint = endpoint

    def get(self, *args, **kwargs):
        response = self.session.get(*args, **kwargs)
        return response

    def post(self, *args, **kwargs):
        response = self.session.post(*args, **kwargs)
        return response

    def put(self, *args, **kwargs):
        response = self.session.put(*args, **kwargs)
        return response

    def delete(self, *args, **kwargs):
        response = self.session.delete(*args, **kwargs)
        return response
