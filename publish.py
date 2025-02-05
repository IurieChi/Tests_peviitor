"""publish jobs to production"""

import requests
from job_failed import Item


def job_publish_to_prod(jobs_to_publish, filtered_jobs ,fail_to_publish_validator, headers):
    """
    Function to publish jobs in ptoduction
    """
    url = "https://api.laurentiumarian.ro/jobs/publish/"
    try:

        responce = requests.post(url=url, headers=headers, json=jobs_to_publish, timeout=100)

        if responce.status_code == 200:
            print(f"For {jobs_to_publish[0]["company"].upper()} has been published: {
                len(jobs_to_publish)}, {len(filtered_jobs) - len(jobs_to_publish)
                }:jobs failed to publish, request status {responce.status_code}")

    except requests.RequestException as e:
        print(e)
        print(f"Error post request {responce.status_code}: to publish jobs {
            len(jobs_to_publish)} for {jobs_to_publish[0]["company"]}")

        fail_to_publish_validator.append(Item(company=jobs_to_publish[0]["company"], failed_jobs=len(jobs_to_publish)).to_dict())
