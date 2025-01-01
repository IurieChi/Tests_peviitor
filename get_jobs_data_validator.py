import requests
from api_get_token import GetToken


class GetJobs:

    def __init__(self):
        self.token = GetToken().get_token()
        self.route = "jobs/get/"
        self.base_url = "https://api.laurentiumarian.ro/"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def get_jobs(self, company: str):
        """_summary_

        Args:
            company (str): _description_

        Raises:
            Exception: _description_
            Exception: _description_

        Returns:
            Json: Data with jobs
        """
        url = f"{self.base_url}{self.route}?company={company}"

        try:
            response = requests.request("GET", url, headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.RequestException as e:
            # Catch any exceptions raised by the `requests` library
            raise Exception(
                f"Error while fetching jobs for company {company}: {e}")

        try:
            return response.json()
        except ValueError:
            # Handle cases where the response is not valid JSON
            raise Exception(
                f"Failed to parse JSON response for company {company}")



