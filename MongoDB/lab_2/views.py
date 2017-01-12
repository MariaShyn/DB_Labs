from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.shortcuts import render
from django.http import JsonResponse
from bson.code import Code
import json
import random
import os
import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.driving_school_graduation_lab2
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
        "location" : "Solomyznka"
    }, {
        "name": "Bibi",
        "location" : "Pechersk"
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
    for i in range(0, 100):
        rand_person = random.randint(0, people_count - 1)
        rand_school = random.randint(0, school_count - 1)
        rand_category = random.randint(0, categories_count - 1)
        rand_passed = random.randint(0, 1)
        one_person = people.find().skip(rand_person).next()
        one_school = schools.find().skip(rand_school).next()
        one_category = categories.find().skip(rand_category).next()
        one_person['_id'] = str(one_person['_id'])
        one_category['_id'] = str(one_category['_id'])
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
        rows.append({"name": one_school['name'], "location": one_school['location']})
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
            "id": str(exam['_id']),
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
        date = request.GET.__getitem__('date')
        name = request.GET.__getitem__('name')
        exams.delete_one({'date': date, 'person.name': name})
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
    if request.method == 'PUT':
        body = json.loads(request.body.decode('utf-8'))
        x = ObjectId(body['id'])
        exams.update({
           '_id': x
        }, {
            "date": body["date"],
            "category": body["category"],
            "person": body["person"],
            "school": body['school'],
            'passed': body['passed']
        })
        JsonResponse("success", safe=False)
    return HttpResponse("unknown command")


def rating(request):
    map1 = Code("function () {"
                "    emit(this.category.name, 1);"
                "}")
    reduce1 = Code("function (key, values) {"
                    "var total = 0;"
                    "for (var i = 0; i < values.length; i++) {"
                    "    total += values[i];"
                    "  }"
                    "  return total;"
                    "}")
    result1 = exams.map_reduce(map1, reduce1, "myresults1")

    map2 = Code("function () {"
                "   if(this.passed) {"
                "       emit(this.school.name, 1);"
                "   }"
                "}")
    reduce2 = Code("function (key, values) {"
                   "var total = 0;"
                   "for (var i = 0; i < values.length; i++) {"
                   "    total += values[i];"
                   "  }"
                   "  return total;"
                   "}")
    result2 = exams.map_reduce(map2, reduce2, "myresults2")
    if request.method == 'GET':
        all_categories = []
        all_schools = []
        for doc in result1.find():
            all_categories.append(doc)
        for doc in result2.find():
            all_schools.append(doc)
        print(all_schools)
        print(all_categories)
        return JsonResponse({'schools': all_schools, 'categories': all_categories}, safe=False)
    return HttpResponse("unknown command")


