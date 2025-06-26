class Response:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        return self._json_data

def get(*args, **kwargs):
    raise NotImplementedError("requests.get is not implemented. Use mocks in tests.")
