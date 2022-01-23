from __future__ import print_function

import boto3
import json

def lambda_handler(event, context):
    # TODO implement
    
    try:
        applicant_info = event["values"]
        year_graduate = applicant_info["Year of Graduation"]
        gpa = applicant_info["GPA"]
        majors = applicant_info["Major(s)"]
        classes = applicant_info["Classes Taken Already & Currently Enrolled (or equivalent if similar) ex. cs 589 = stats 697ml"]
        
        return {"status": "success", "message": applicant_info}
    except Exception as e:
        raise e