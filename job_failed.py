class Job:
    
    def __init__(self, company, failed_jobs):
        self.company = company
        self.failed_jobs = failed_jobs

    def to_dict(self):
        return { 'company': self.company, 'failed_jobs': self.failed_jobs }
    