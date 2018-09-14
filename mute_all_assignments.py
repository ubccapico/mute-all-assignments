# -*- coding: utf-8 -*-
"""
Mute all assingments in courses listed in a csv file.

@author: Adam Dixon
"""
try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])
    import requests

try:
    import pandas as pd
except:
    import pip
    pip.main(['install', 'pandas'])
    import pandas as pd

try:
    import json
except:
    import pip
    pip.main(['install', 'json'])
    import json

url = "https://canvas.ubc.ca/api/v1/"
with open('Canvas API Token.txt') as f:
    token = f.read() 

# ===============================================================================================================
# @param : csv_file_name is a string that is not empty and has ".csv" at the end of it
# @effects : mutes and prints all assignments in the course 
# ===============================================================================================================
def mute_all_csv(csv_file_name):
    ss = pd.read_csv(csv_file_name)
    
    for idx, row in ss.iterrows():
        a_list = get_assignment_list(row['courses'])
        mute_all_assignments(a_list, row['courses'])
        print(get_all_assignment_names(a_list))

# ===============================================================================================================
# @param : course_id is a valid Canvas course that you have access to
# @returns : a list of all assignment objects from that course
# ===============================================================================================================
def get_assignment_list(course_id):
    
    r = requests.get(url + "courses/" + str(course_id) + "/assignments?per_page=100",
                     headers =  {'Authorization': 'Bearer ' + str(token)})
        
    assignment_list = json.loads(r.text)
    
    return assignment_list

# ===============================================================================================================
# @param : assignment_list, a list of assignment objects from a course
# @returns : a string with all assignment names separated by new lines
# ===============================================================================================================
def get_all_assignment_names(assignment_list):
    
    s = ""
    
    for idx, val in enumerate(assignment_list):
        s = s + str(assignment_list[idx]['name']) + "\n"

    return s

# ===============================================================================================================
# @param : a_list is a list of assignments in a course
# @effects: utes all assignments in a_list
# ===============================================================================================================
def mute_all_assignments(a_list, course_id):
    
    for idx, val in enumerate(a_list):
        requests.put(url + "courses/" + str(course_id) + "/assignments/" + str(a_list[idx]['id']),
                     headers =  {'Authorization': 'Bearer ' + str(token)},
                     params = {"assignment[muted]" : True})        
    return None

print()
print("Make sure you have copy and pasted your token into the file 'Canvas API token.txt'")
mute_all_csv("courses.csv")
print("Complete!")
