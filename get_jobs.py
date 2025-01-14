import requests


class GetJobs:

    def __init__(self, TOKEN):
        self.token = TOKEN
        self.base_url = "https://api.laurentiumarian.ro/"
        self.route = "jobs/get/"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def get_jobs(self, company: str):
        """_summary_

        Args:
            company (str): company name that are present on API to extract jobs

        Raises:
            Exception RequestException: Raise an HTTPError for bad responses
            Exception ValueError:  if response is not valid JSON

        Returns:
            Json: Data with jobs
        """

        page = 1
        all_jobs = []

        while True:
            try:
                response = requests.get(url=f"{self.base_url}{self.route}?company={
                    company}&page={page}", headers=self.headers)

                # Raise an HTTPError for bad responses (4xx and 5xx)
                response.raise_for_status()

                response = response.json()

                # Add jobs to the jobs
                jobs = response['results']
                all_jobs.extend(jobs)

                next_page = response['next']

                if next_page is None:
                    break
                # Incriment page and continue to extract all jobs from API
                page += 1

            except requests.exceptions.RequestException as e:
                # Catch any exceptions raised by the `requests` library
                raise Exception(
                    f"Error while fetching jobs for company {company}: {e}")

        try:
            return all_jobs
        except ValueError:
            # Handle cases where the response is not valid JSON
            raise Exception(
                f"Failed to parse JSON response for company {company}")
