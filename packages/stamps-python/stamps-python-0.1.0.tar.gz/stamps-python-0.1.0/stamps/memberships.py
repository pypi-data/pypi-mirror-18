from .base_api import BaseAPI


class Memberships(BaseAPI):

    def status(self, user=None, **kwargs):
        url = self.client.base_url + "/memberships/status"

        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'user': user
        }
        payload.update(kwargs)
        return self.client._call('GET', url, payload)

    def register(self, name=None, email=None, birthday=None, gender=None,
                 member_id=None, phone=None, address=None, password=None,
                 **kwargs):

        url = self.client.base_url + "/memberships/register"
        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'name': name,
            'email': email,
            'gender': gender,
            'birthday': birthday,
            'member_id': member_id,
            'phone': phone,
            'address': address,
            'password': password
        }
        payload.update(kwargs)
        return self.client._call('POST', url, payload)

    def add_stamps(self, user=None, stamps=None, note=None, **kwargs):
        url = self.client.base_url + "/memberships/add-stamps"
        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'user': user,
            'note': note,
            'stamps': stamps
        }
        payload.update(kwargs)
        return self.client._call('POST', url, payload)

    def change(self, user_id=None, email=None, name=None, birthday=None, gender=None,
               phone=None, address=None, **kwargs):
        url = self.client.base_url + "/memberships/change"

        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'id': user_id,
            'email': email,
            'name': name,
            'gender': gender,
            'birthday': birthday,
            'phone': phone,
            'address': address
        }
        payload.update(kwargs)
        return self.client._call('POST', url, payload)
