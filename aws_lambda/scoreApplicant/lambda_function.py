from __future__ import print_function

import boto3
import json
import datetime

'''
from urllib import request
def write_to_mongo(data, dbName, collecName, headers={'Content-Type':'application/json'}):
    url = 'https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/amp-vjzhz/service/addRecord/incoming_webhook/addRecord'
    data = json.dumps({'db': dbName, 'collecName': collecName, 'doc': data})
    # if data is not in bytes, convert to it to utf-8 bytes
    bindata = data if type(data) == bytes else data.encode('utf-8')
    req = request.Request(url, bindata, headers)
    resp = request.urlopen(req)
    return resp.read(), resp.getheaders()
'''
def lambda_handler(event, context):
    # TODO implement
    try:
        applicant_info = event["values"]
        year_graduate = applicant_info["Year of Graduation"]
        gpa = applicant_info["GPA"]
        majors = applicant_info["Major(s)"]
        classes = applicant_info["Classes Taken Already & Currently Enrolled (or equivalent if similar) ex. cs 589 = stats 697ml"]
        skills_map = applicant_info["skills_adjusted_score"]
        commit_time = applicant_info["How many hours per week can you commit to BUILD?"]
        first_regularly_meeting = applicant_info["Will you be able to regularly attend weekly Monday @ 5:30pm general body meetings?"]
        second_regularly_meeting = applicant_info["If we moved our regularly attending weekly meeting to Monday @ 7:00 pm, could you attend? (We realized courses go from 5:30-6:45 this sem)"]
        if not isinstance(first_regularly_meeting, bool): first_regularly_meeting = False
        if not isinstance(second_regularly_meeting, bool): second_regularly_meeting = False
        
        # Now, let's evaluate our candidates
        
        
        # GPA_WEIGHT = GPA * 4
        GPA_WEIGHT = gpa
        # Classes taken
            # If 600+ taken (+10 points)
            # If 500+ taken (+7 points each)
            # If CS 187, CS 311, CS 320/326, CS 325, CS 345, CS 497S, CS 490U, CS 445 (+5 points each)
            # IF CS 370, CS 490A, CS 377, CS 453, CS 446, CS 389 (+4 points)
            # CS 121, CS 220, CS 230, CS 240, CS 383, CS 410/610, CS 420 (+3 points)
            # Math 233, Math 235, Math 545, Stats 516, Stats 525 (+2 points)
            # Else (+1 point)
            # Additionally 
                # (100 level courses) - multiply by 1 point
                # (200 level courses) - multiply by 1.25 point
                # (300 level courses) - multiply by 1.5 point
                # (400 level courses) - multiply by 1.65 point
                # (500 level courses) - multiply by 1.8 point
                # (600 level courses) - multiply by 2.0 point
            # if not a cs major tho, we multiply their score by 3
            # if multiple majors, we multiply their score by 1.33 to optimize their score since they may take another major
        
        five_point_class_set = {"CS 187", "CS 311", "CS 320/326", "CS 325", "CS 345", "CS 497S", "CS 490U", "CS 445"}
        four_point_class_set = {"CS 490A", "CS 377", "CS 453", "CS 446", "CS 389"}
        three_point_class_set = {"CS 121", "CS 220", "CS 230", "CS 240", "CS 383", "CS 410/610", "CS 420"}
        two_point_class_set = {"Math 233", "Math 235", "Math 545", "Stats 516", "Stats 525"}
        
        ans_map = {}
        classes_score = 0
        for i in range(len(classes)):
            if classes[i].startswith("CS 6"):
                classes_score += 10
            elif classes[i].startswith("CS 5"):
                classes_score += 7
            elif classes[i] in five_point_class_set:
                classes_score += 5
            elif classes[i] in four_point_class_set:
                classes_score += 4
            elif classes[i] in three_point_class_set:
                classes_score += 3
            elif classes[i] in two_point_class_set:
                classes_score += 2
            else:
                classes_score += 1
        
        if "Computer Science" not in majors:
            classes_score *= 2
        elif len(majors) >= 2:
            classes_score *= 1.33
        
        # Total academic score = gpa weight + classes_score
        # final academic score = total academic score / (year of graduation * 5)
        total_academic_score = (GPA_WEIGHT * classes_score) / (1 / (year_graduate + 0.5 - (datetime.datetime.today().year)) * 6) 
        
        # Commitment time (based on hours given) 
        commit_time_weight = commit_time * 4       
        
        # Can meet at those times
            # Yes -> +5 points, No -> 0 point
        meet_times = 10 if first_regularly_meeting or second_regularly_meeting else 0
        
        # Skills ranking (based on projects done for BUILD)
        skill_score = 0
        for skill, conf_score in skills_map.items():
            skill_score += conf_score
        
        final_score = total_academic_score + commit_time_weight + meet_times + skill_score
        
        final_evaluate = {
            "email": applicant_info["School Email"],
            "first_name": applicant_info["First Name"],
            "last_name": applicant_info["Last Name"],
            "graduation": year_graduate,
            "final_score": final_score,
            "commit_time_weight": commit_time_weight,
            "classes_score": classes_score,
            "total_academic_score": total_academic_score,
            "gpa": gpa,
            "skill_score": skill_score,
            "meet_times": meet_times
        }
        
        # dbName = "applicant"
        # collecName = "score"
        # write_to_mongo(final_evaluate, db)
        
        return {"status": 200, "message": final_evaluate}
    except Exception as e:
        return {"status": 403, "message": e}