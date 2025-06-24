class BaseAuthHandler:
    def register(self, data):
        raise NotImplementedError()

    def login(self, data):
        raise NotImplementedError()

    def validate_token(self, token):
        raise NotImplementedError()

    def get_user(self, token):
        raise NotImplementedError()
