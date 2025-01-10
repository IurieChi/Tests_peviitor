
class FilterJobs:
    
    def __init__(self, jobs):
        self.jobs = jobs
    
    def filter_jobs(self):
        """This function  is filtering jobs from DB,  add to list only jobs that need to be tested and validated
            to be published in production

        Returns:
            _type_: list  of jobs that are not published
        """
        jobs_not_pub = [job for job in self.jobs  if not job["published"]]
        return jobs_not_pub
    
    
