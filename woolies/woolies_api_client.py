import requests

class ApiClient():
    base_url = None
    token = None

    def __init__(self, url, user_token):
        self.base_url = url
        self.token = user_token

    def get_headers(self):
        return {'Accept': 'application/json'}

    def get_products(self):
        r = requests.get('{}/api/resource/products?token={}'.format(self.base_url, self.token), headers=self.get_headers()) 
        return r.json()

    def get_shopper_history(self):
        r = requests.get('{}/api/resource/shopperHistory?token={}'.format(self.base_url, self.token), headers=self.get_headers()) 
        return r.json()
