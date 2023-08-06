from .base_api import BaseAPI


class Authentication(BaseAPI):

    def login(self, email=None, password=None, **kwargs):
        url = self.client.base_url + "/auth/login"
        payload = {
            'token': self.client.token,
            'username': email,
            'password': password
        }
        payload.update(kwargs)
        return self.client._call('POST', url, payload)

    def password_reset(self, email=None, **kwargs):
        url = self.client.base_url + "/auth/password-reset"
        payload = {
            'email': email,
        }
        payload.update(kwargs)
        return self.client._call('POST', url, payload)
