import requests


class GetJobs:
    """_summary_
    """

    def __init__(self, TOKEN):
        self.token = TOKEN
        self.base_url = "https://api.laurentiumarian.ro/"
        self.route = "jobs/get/"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def get_jobs(self, company: str):
        """
        Fetch jobs for a specific company from the API.

        Args:
            company (str): company name that are present on API to extract jobs

        Raises:
            Exception RequestException: Raise an HTTPError for bad responses
            Exception ValueError:  if response is not valid JSON

        Returns:
            list: A list of all job entries for the given company.
        """

        pages = 1
        all_jobs = []
        url = f"{self.base_url}{self.route}?company={company}&page={pages}"

        while True:
            try:
                response = requests.get(url=url, headers=self.headers, timeout=10)

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
                pages += 1

            except requests.exceptions.RequestException as e:
                # Catch any exceptions raised by the `requests` library
                print(f"Error while fetching jobs for company '{
                      company.upper()}': {e}")
                break  # Exit the loop and move to the next company

        try:
            return all_jobs
        except ValueError  as exc:
            # Handle cases where the response is not valid JSON
            raise ValueError( f"Failed to parse JSON response for company {company}") from exc
