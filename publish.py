"""publish jobs to production"""

import requests
from api_get_token import GetToken
from get_jobs import GetJobs
from job_failed import Item

TOKEN = GetToken().get_token()
job = GetJobs(TOKEN)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def job_publish_to_prod(jobs_to_publish, filtered_jobs ,fail_to_publish_validator):
    """
    Function to publish jobs in ptoduction
    """
    url = "https://api.laurentiumarian.ro/jobs/publish/"
    try:

        responce = requests.post(url=url, headers=headers, json=jobs_to_publish, timeout=50)

        if responce.status_code == 200:
            print(f"For {jobs_to_publish[0]["company"].upper()} has been published: {
                len(jobs_to_publish)}, {len(filtered_jobs) - len(jobs_to_publish)
                }:jobs failed to publish, request status {responce.status_code}")

    except requests.RequestException as e:
        print(e)
        print(f"Error post request {responce.status_code}: to publish jobs {
            len(jobs_to_publish)} for {jobs_to_publish[0]["company"]}")

        fail_to_publish_validator.append(Item(company=jobs_to_publish[0]["company"], failed_jobs=len(jobs_to_publish)).to_dict())
