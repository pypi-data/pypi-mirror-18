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

    def change_password(self, email=None, old_password=None, new_password=None, **kwargs):
        url = self.client.base_url + "/auth/change-password"

        payload = {
            'token': self.client.token,
            'email': email,
            'old_password': old_password,
            'new_password': new_password
        }

        payload.update(kwargs)
        return self.client._call('POST', url, payload)
