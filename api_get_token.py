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
        
        try:
            response = requests.post(url, json={"email": self.EMAIL}, headers=self.header)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.RequestException as e:
            # Catch any requests-related exceptions and raise a new exception with details
            raise Exception(f"Error while attempting to get token: {e}")
        
        try:
            return response.json()["access"]
        except KeyError:
            # Handle case where "access" key is not in the response
            raise Exception("Token not found in the response")
