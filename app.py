#!/usr/bin/python

import requests
from flask import Flask, request
import json
import csv
import io

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def result():
    # 1. Define inputs for the POST/GET request
    base_url = 'https://youraccount.instructure.com/api/v1/accounts/self/' 
    header = {'Authorization' : 'Bearer YOUR_ACCESS_TOKEN_HERE'}
    my_data = request.get_json()
    enrollment_properties = []
    course_titles = [] #list of course titles. You can also use course ID's.
    for item in my_data['line_items']:
		#check that you're only processing course enrollments from your shopify store
        if item["title"] in course_titles:
            enrollment_properties.append(item['properties'])
    if not enrollment_properties:
        return "No courses were ordered."

    test_enrollment = open('test_enrollment.csv', 'w', newline='')
    enrollment_data = io.StringIO()
    csv_header = []
    csvwriter = csv.writer(enrollment_data)
    for record in enrollment_properties:
        csv_values = [] #Data rows go here. Have to clear it at the beginning of each iteration.
        if(enrollment_properties.index(record) == 0):
            for pair in record:
                csv_header.append(pair['name'])
            csvwriter.writerow(csv_header)
        for pair in record:
            if pair['name'] == 'course_id':
                print(pair['value'])
            csv_values.append(pair['value'])
        csvwriter.writerow(csv_values)
    
    
    payload = {'import_type' : 'instructure_csv', 'extension' : 'csv'}
    data = enrollment_data.getvalue()
    enrollment_data.close()

    #For submitting an import leave at None.
    import_id = None
   
    # Create a response object from the POST/GET request
    if not import_id:
        r = requests.post(base_url + "/sis_imports/", headers=header, params=payload, data=data)
    else:
        r = requests.get(base_url +  "/sis_imports/" + import_id, headers=header)
    
    return 'no errors to date'

#Create a response object from the POST request
def myrequest(base_url, header, payload, data):
    if not import_id:
        r = requests.post(base_url + "/sis_imports/", headers=header, params=payload, data=data)
    else:
        r = requests.get(base_url +  "/sis_imports/" + import_id, headers=header)
    return r

def parsejson(r):
    rjson = json.loads(r.text)
    return rjson
