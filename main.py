from threading import Thread
import time
import json

from api_get_token import GetToken
from get_jobs import GetJobs
from companies import companies
from filter_jobs import FilterJobs
from test_jobs import ValidateJob
from job_failed import Item
from job_publish import job_publish_to_prod


TOKEN = GetToken().get_token()
job = GetJobs(TOKEN)

header = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}
# Company name and jobs number that failed validation
faild_validation_jobs = []
# List to store companies with 401 Unauthorized errors
unauthorized_companies = []
# company that fail to publish
fail_to_publish_validator = []

# Define the variable globally
JOB_COUNT_PASS_VALIDATION = 0
JOB_COUNT_FAIL_VALIDATION = 0


def validayte_job(company_name):
    """_summary_

    Args:
        company (str): this function is extracting jobs from DB for each company
        validate them if  all parameters are
        present and add  it  to a  jobs_to_publish = []
    """
    global JOB_COUNT_PASS_VALIDATION  # [global-statement]
    global JOB_COUNT_FAIL_VALIDATION

    jobs = job.get_jobs(company_name)

    # Check if the error is 401 Unauthorized
    if len(jobs) == 0:
        unauthorized_companies.append(f"{company_name}")

    filtered_jobs = FilterJobs(jobs).filter_jobs()

    print(
        f"\nNumber of total jobs {len(jobs)} for {company_name}\nNumeber of jobs to be validated {len(filtered_jobs)}"
    )

    jobs_to_publish = []
    fail_job_count = 0

    if filtered_jobs:

        for job_to_validate in filtered_jobs:
            job_instance = ValidateJob(job_to_validate)
            job_instance.validate_job_link()
            # check if link is not accesible  move to another job
            if job_to_validate["job_link"] is False:
                fail_job_count += 1
                continue
            content = job_instance.get_content()
            if content is None:
                print(f"**- Can't get content for {job_to_validate["job_link"]}")
                fail_job_count += 1
                continue
            job_instance.update_job_type_from_content(content=content)
            job_instance.validate_job_title(content=content)
            job_instance.validate_job_city()
            job_instance.validate_job_type()

            if (
                job_to_validate["job_link"]
                and job_to_validate["job_title"]
                and job_to_validate["city"]
                and job_to_validate["remote"]
            ):
                job_to_validate["published"] = True
                jobs_to_publish.append(job_to_validate)

            else:
                # increments job number that failed validation
                fail_job_count += 1
        if fail_job_count >= 1:
            faild_validation_jobs.append(
                Item(company=company_name, failed_jobs=fail_job_count).to_dict()
            )
            JOB_COUNT_FAIL_VALIDATION += fail_job_count

    if jobs_to_publish:
        job_publish_to_prod(
            jobs_to_publish, filtered_jobs, fail_to_publish_validator, headers=header
        )
        # increments number of jobs
        JOB_COUNT_PASS_VALIDATION += len(jobs_to_publish)
    elif company_name not in unauthorized_companies:
        print(f"{company_name.upper()} don't have jobs to publish")


if __name__ == "__main__":
    start_time = time.time()
    try:

        for company in companies:
            thread = Thread(target=validayte_job, args=[company])
            thread.run()

    except Exception as e:
        print("\nSomething went wrong", e)
    finally:
        end_time = time.time()
        # Execution time
        print(f"\nExecution time: {(end_time - start_time) / 60:.2f} min\n")

        print(f"Jobs pass validation to be published: {JOB_COUNT_PASS_VALIDATION} \n")

        print(f"Jobs didn't pass validation: {JOB_COUNT_FAIL_VALIDATION} \n")
        for item in faild_validation_jobs:
            print(f"Company:{item["company"]}, Failed jobs:{item["failed_jobs"]}")

        print("fail post request to publish", fail_to_publish_validator)
        print("401 Unauthorized\n")
        for compan in unauthorized_companies:
            print(f"Company:{compan}")
