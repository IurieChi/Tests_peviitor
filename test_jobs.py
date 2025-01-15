import requests
import subprocess


class ValidateJob():

    def __init__(self, job):
        self.job = job

    def get_content(self):
        """
        Extract job content fetched from the  job URL.

        """
        # content = requests.get(self.job["job_link"], timeout=10)
        # return content
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        }

        try:
            # Construct the curl command
            command = [
                'curl', '-s', '-A', headers['User-Agent'], self.job["job_link"]
            ]
            # Execute the curl command and capture the output
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
            # Check if there was an error
            if result.returncode != 0:
                raise Exception(result.stderr.decode('utf-8'))
            # Decode the output using utf-8
            return result.stdout.decode('utf-8')
        except Exception as e:
            # Handle exceptions (e.g., network errors, invalid responses)
            print(f"An error occurred: {e}")
            return None

    def validate_job_link(self):
        """Check if the link is accessible.
        Raises:
            AssertionError: If 'link' is not accesible.

        """

        response = requests.get(self.job["job_link"], timeout=10)
        try:
            assert response.status_code == 200, f"Company: {self.job["company_name"]}: {
                self.job["job_link"]} Link is not accessible"

            return self.job

        except AssertionError as e:
            print(f"AssertionError: {e}")
            self.job["job_link"] = False

            return self.job

    def validate_job_title(self, content):
        """
        Check if the job title is present in the content

        Raises:
            AssertionError: If 'tittle' is not present on the page.

        """
        try:
            assert self.job["job_title"] in content, f"Job title not found in the Page {
                self.job["job_link"]}"
            return self.job

        except AssertionError as e:
            print(f"AssertionError: {e}")
            self.job["job_title"] = False
            return self.job

    def validate_job_location(self):
        """
        Validate that the 'city' field is not an empty string or an empty list.

        Raises:
            AssertionError: If 'city' is an empty string or an empty list.
        """
        try:
            assert self.job["city"] not in ("", []), f"City fild is empty for Company: {
                self.job["company_name"]} and job title: {self.job["job_title"]}"

        except AssertionError as e:

            print(f"AssertionError: {e}")
            self.job["city"] = False
            return self.job

    def validate_job_type(self):
        """
        Validate that the 'remote' field is not an empty string or an empty list.

        Raises:
            AssertionError: If 'remote' is an empty string or an empty list.
        """
        try:
            assert self.job["remote"] not in ("", []), f"Job type fild is empty for Company: {
                self.job["company_name"]} and job title: {self.job["job_title"]}"

        except AssertionError as e:

            print(f"AssertionError: {e}")
            self.job["remote"] = False
            return self.job
