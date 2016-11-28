from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.shortcuts import render
from django.http import JsonResponse
import json
import os
import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient

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


def fill_database(request):
    fill_people()
    fill_school()
    fill_categ()
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


def search(request):
    """qw = request.GET.__getitem__('name')
    if qw:
        sw = ("SELECT id, name FROM person WHERE MATCH (name) AGAINST ('\"" + qw + "\"' IN BOOLEAN MODE)")
        db.query(sw)
        r = db.use_result()
        line1 = r.fetch_row()
        results = []
        while line1:
            results.append({"id": line1[0][0], "name": line1[0][1]})
            line1 = r.fetch_row()
    return JsonResponse(results, safe=False)
"""


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


def iter_group(queue):
    buf = []
    prev_key = None

    for val in queue:
        cur_key, cur_val = val
        # print cur_key, cur_val
        if cur_key == prev_key or prev_key is None:
            buf.append(cur_val)
        else:
            yield prev_key, buf
            buf = []
            buf.append(cur_val)
        prev_key = cur_key

    if buf:
        yield cur_key, buf


class MapReduce:
    def __init__(self):
        self.queue = []

    def send(self, a, b):
        self.queue.append((a, b))

    def count(self):
        return len(self.queue)

    def __iter__(self):
        return iter_group(sorted(self.queue))


def rating(request):
    if request.method == 'GET':
        schools = []
        x = MapReduce()
        for item in get_exam():
            x.send(item['school']['name'], 1)
        for word, ones in x:
            schools.append({"name": word, "studentAmount": sum(ones)})
        students = list(exams.aggregate([
            {'$unwind':'$person'},
            { '$group': {'_id': '$person.name', 'amount': {'$sum': 1}}}
        ]))
        return JsonResponse({'schools': schools, 'students': students}, safe=False)
    return HttpResponse("unknown command")


