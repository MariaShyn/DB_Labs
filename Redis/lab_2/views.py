from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.shortcuts import render
from django.http import JsonResponse

import json
import redis
import time
import ast
import random
import pickle

import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps
r = redis.Redis(host='localhost', port=6379, db=0)

client = MongoClient('localhost', 27017)

db = client.driving_school_graduation
schools = db.schools
exams = db.exams
people = db.people
categories = db.categories



def fill_people():
    exams.remove()
    people.remove()
    all_students = [{
        "name" : "Maria Shyn",
        "dateofbirth": "02/03/1997",
        "dateofstart": datetime.datetime.utcnow(),
        'sex': "female",
        'city': 'Lviv'
    }, {
        "name" : "Peter Qwerty",
        "dateofbirth": "19/10/1986",
        "dateofstart": datetime.datetime.utcnow(),
        'sex': "male",
        'city': "Donetchk"
    }, {
        "name" : "Sonya Grethem",
        "dateofbirth": "22/01/1998",
        "dateofstart": datetime.datetime.utcnow(),
        'sex': "female",
        "city" : 'Kiev'
    }, {
        "name" : "Vasya Prewc",
        "dateofbirth": "22/01/1993",
        "dateofstart": datetime.datetime.utcnow(),
        'sex': "male",
        "city" : 'Kiev'
    }, {
        "name" : "Sergey Petrenko",
        "dateofbirth": "22/01/1992",
        "dateofstart": datetime.datetime.utcnow(),
        'sex': "male",
        "city" : 'Kiev'
    }, {
        "name" : "Anna Sirenko",
        "dateofbirth": "22/01/1989",
        "dateofstart": datetime.datetime.utcnow(),
        'sex': "female",
        "city" : 'Lviv'
    }]
    for student in all_students:
        people.insert_one(student)
    return len(all_students)


def fill_school():
    schools.remove()
    all_schools = [{
        "name": "PedalVPol",
        "location" : "Troeshchina"
    }, {
        "name": "Forsaj",
        "location" : "Solomynka"
    }, {
        "name": "Bibi",
        "location" : "Pechersk"
    }, {
        "name": "Shumaher",
        "location": "Darnitca"
    }]
    for school in all_schools:
        schools.insert_one(school)
    return len(all_schools)


def fill_categ():
    categories.remove()
    all_categories = [{
        "name": "A"
    }, {
        "name": "B"
    }, {
        "name": "C"
    }, {
        "name": "D"
    }, {
        "name": "E"
    }, {
        "name": "F"
    }]
    for categ in all_categories:
        categories.insert_one(categ)
    return len(all_categories)


def fill_database(request):
    pass_options = ['true', 'false']
    people_count = fill_people()
    school_count = fill_school()
    categories_count = fill_categ()
    for i in range(0, 50000):
        rand_person = random.randint(0, people_count-1)
        rand_school = random.randint(0, school_count-1)
        rand_category = random.randint(0, categories_count-1)
        rand_passed = random.randint(0, 1)
        one_person = people.find().skip(rand_person).next()
        one_school = schools.find().skip(rand_school).next()
        one_category = categories.find().skip(rand_category).next()
        one_person['_id'] = str(one_person['_id'])
        del one_category['_id']
        one_school['_id'] = str(one_school['_id'])
        exam = {
            'date': datetime.datetime.utcnow(),
            'category': one_category,
            'person': one_person,
            'school': one_school,
            'passed': pass_options[rand_passed]
        }
        exams.insert_one(exam)
    return JsonResponse("success", safe=False)


def renderIndex( request ):
    return render(request, 'index.html')


def get_school():
    rows = []
    for one_school in schools.find():
        rows.append({"id": str(one_school['_id']), "name": one_school['name'], "location": one_school['location']})
    return rows


def get_student():
    rows = []
    for person in people.aggregate(
            [
                {
                    "$sort": {
                        "name": 1,
                        "sex": 1
                    }
                }
            ]
    ):
        rows.append(
            {
                "name": person['name'],
                "dateofbirth": person['dateofbirth'],
                "dateofstart": person['dateofstart'],
                "city": person['city'],
                'sex': person['sex']
             })
    return rows


def get_category():
    rows = []
    for category in categories.find():
        rows.append({"name": category['name']})
    return rows


def get_exam():
    rows = []
    for exam in exams.find():
        rows.append({
            "_id": str(exam['_id']),
            "date": exam['date'],
            "category": exam['category'],
            "person": exam['person'],
            "school": exam['school'],
            "passed": exam['passed']
        })
    return rows


def category( request ):
    if request.method == 'GET':
        return JsonResponse(get_category(), safe=False)
    return HttpResponse("unknown command")


def school( request ):
    if request.method == 'GET':
        return JsonResponse(get_school(), safe=False)
    return HttpResponse("unknown command")


def search( request ):
    if request.method == 'GET':
        all_exams = []
        search_name = request.GET.__getitem__('name')
        start_time = time.time()
        if (r.exists(search_name)):
            cash = True
            all_exams = pickle.loads(r.get(search_name))
        else:
            query = {}
            cash = False
            if search_name != '0':
                query["school.name"] = search_name
                all_exams = list(exams.find(query))
            r.set(search_name, pickle.dumps(all_exams))
        time_res = time.time() - start_time
        print(time_res)
        return JsonResponse({"exams": dumps(all_exams), "cash": cash}, safe=False)
    return HttpResponse("unknown command")


def student(request):
    if request.method == 'GET':
        cities = []
        for item in people.aggregate(
            [
                {"$group":
                    {
                        "_id": "$city",
                        "students": {
                            "$push": "$name"
                        }
                    }
                }
            ]
        ):
            cities.append(item)
        return JsonResponse({'students': get_student(), 'cities': cities}, safe=False)
    return HttpResponse("unknown command")


def exam( request ):
    if request.method == 'GET':
        all_exams = get_exam()
        all_people = get_student()
        all_categories = get_category()
        all_drs = get_school()

        return JsonResponse({"exams": all_exams, "people": all_people,
                             "drivingSchools": all_drs, "categories": all_categories}, safe=False)
    if request.method == 'DELETE':
        id = request.GET.__getitem__('id')
        one_exam = exams.find_one({'_id': ObjectId(id)})
        print(one_exam)
        exams.delete_one({'_id': ObjectId(id)})
        r.delete(one_exam["school"]["name"])
        return JsonResponse({}, safe=False)
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        exams.insert_one({"date": body["date"],
                          "category": json.loads(body["category"]),
                          "person": json.loads(body["person"]),
                          "school": json.loads(body['school']),
                          'passed': body['passed']
        })
        return JsonResponse({}, safe=False)
    return HttpResponse("unknown command")




