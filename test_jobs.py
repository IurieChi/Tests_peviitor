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
        """Check if the link is accessible."""

        response = requests.head(self.job["job_link"], timeout=10)
        try:
            assert response.status_code == 200
            # print(f"{self.job["job_link"]} OK")
            return self.job
        except:
            print(f"Company {self.job["company_name"]}: {self.job["job_link"]} Link is not accessible")
            return False

    def validate_job_title(self, content):
        """Check if the job title is present in the content"""
        try:
            assert self.job["job_title"] in content, f"Job title not found in the Page {self.job["job_link"]}"
            return self.job

        except AssertionError as e:
            print(f"AssertionError: {e}")
            return False

    