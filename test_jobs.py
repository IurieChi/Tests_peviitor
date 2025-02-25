"""_summary_

Raises:
    Exception: _description_

Returns:
    _type_: False or True for jobs if job pass all validation
"""

import requests
from job_location import validate_city


class ValidateJob:
    """
    Logic to validate all jobs
    """

    default_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    def __init__(self, job, header=None):
        self.job = job
        self.header = header if header is not None else ValidateJob.default_header

    def get_content(self):
        """
        Extract job content fetched from the  job URL.

        """

        try:
            response = requests.get(
                url=self.job["job_link"],
                headers=self.header,
                allow_redirects=True,
                timeout=50,
            )
            if response.status_code == 200:
                return response.text.lower()

        except requests.RequestException as e:
            # Handle exceptions (e.g., network errors, invalid responses)
            print(f"An error occurred: {e}")

    def validate_job_link(self):
        """Check if the link is accessible.
        Raises:
            AssertionError: If 'link' is not accesible.

        """

        try:
            response = requests.get(
                url=self.job["job_link"],
                headers=self.header,
                allow_redirects=True,
                timeout=20,
            )

            # Assert the status code is 200
            assert (
                response.status_code == 200
            ), f"Company: {self.job["company_name"]}: {
                self.job["job_link"]} Link is not accessible"

        except requests.RequestException as e:
            # Handle exceptions (e.g., network errors, invalid responses)
            print(f"An error occurred: {e}")

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
        title = self.job["job_title"]
        try:
            assert (
                title.lower() in content
            ), f"Job title:'{self.job["job_title"]}' NOT FOUND on the page:{
                self.job["job_link"]}"
            return self.job

        except AssertionError as e:
            print(f"AssertionError: {e}")
            self.job["job_title"] = False
            return self.job

    def validate_job_city(self):
        """
        Validate that the 'city' field is not an empty string or an empty list.

        Raises:
            AssertionError: If 'city' is an empty string or an empty list.
        """
        try:

            assert self.job["city"] not in (
                "",
                [],
            ), f"City fild is empty for Company: {
                self.job["company_name"]} and job title: {self.job["job_title"]}"

            validated_cities = validate_city(self.job["city"])

            if isinstance(validated_cities, list):
                assert all(validated_cities), (
                    f"One or more cities in the list are not valid for Company: "
                    f"{
                    self.job['company_name'].upper()}: and job title: {self.job['job_title']}"
                )
                self.job["city"] = validated_cities
                # print(self.job["city"])
            else:
                assert validated_cities, (
                    f"{self.job['city']} is not a valid city in Romania for Company: "
                    f"{
                                          self.job['company_name']} and job title: {self.job['job_title']}"
                )
                # self.job["city"] = validated_cities

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
        expected_job_type_formats = ["hybrid", "remote", "on-site"]
        try:
            assert self.job["remote"] not in (
                "",
                [],
            ), f"Job type fild is empty for Company: {
                self.job["company_name"]} and job title: {self.job["job_title"]}"
            if isinstance(self.job["remote"], list):
                for job in self.job["remote"]:
                    assert (
                        job in expected_job_type_formats
                    ), f"Job type {self.job["remote"]
                        } is not like expected format for job title: {self.job["job_title"]}"

        except AssertionError as e:

            print(f"AssertionError: {e}")
            self.job["remote"] = False
            return self.job

    def update_job_type_from_content(self, content):
        """check expected job type on the job description page"""
        expected_job_type_formats = ["hybrid", "remote", "on-site"]

        content_job_type = []
        for job_type in expected_job_type_formats:
            if job_type in content:
                content_job_type.append(job_type)

        if len(content_job_type) > 1 and self.job["remote"] != content_job_type:
            self.job["remote"] = content_job_type
