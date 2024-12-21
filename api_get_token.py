import requests

class GetToken:
    
    """
    - Method to get token
    """
    
    def __init__(self):
        
        self.EMAIL = 'chigaiiura@yahoo.com'
        self.DOMAIN = 'https://api.peviitor.ro/v5/'
        self.TOKEN_ROUTE = 'get_token/'
        
        self.header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            }
        
    
    def get_token(self):
        
        url = f"{self.DOMAIN}{self.TOKEN_ROUTE}"

        response = requests.post(url, json={"email": self.EMAIL}, headers=self.header)
        if response.status_code != 200:
            raise Exception("Get token conection code", response.status_code)
        else:
            return response.json()["access"]
