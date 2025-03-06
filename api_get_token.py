"""Get tocket from API

Raises:
    Exception: _description_
    Exception: _description_

Returns:
    _type_: Token
"""

import requests


class GetToken:
    """
    - Method to get token
    """

    def __init__(self):

        self.EMAIL = "chigaiiura@yahoo.com"
        self.DOMAIN = "https://api.peviitor.ro/v5/"
        self.TOKEN_ROUTE = "get_token/"
        self.header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

    def get_token(self):
        """
        Raises:
            Exception: Raise HTTPError for bad responses (4xx and 5xx)
            Exception: Error while attempting to get token:

        Returns:
            _type_: Token Key
        """
        url = f"{self.DOMAIN}{self.TOKEN_ROUTE}"

        try:
            response = requests.post(
                url, json={"email": self.EMAIL}, headers=self.header, timeout=10
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        except requests.exceptions.ReadTimeout as e:
            print("Timed out: api is not reachable", e)
        except requests.exceptions.RequestException as e:
            # Catch any requests-related exceptions and raise a new exception with details
            print(
                "Something went wrong: get_token endpoint did not respond",
                response.status_code,
            )

        try:
            return response.json()["access"]
        except KeyError as e:
            # Handle case where "access" key is not in the response
            print("'access'key not found in the response", e)
