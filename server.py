from flask import Flask, abort, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

UNSCORED = -1

students = {}
courses = {}

class StudentResource(Resource):
    def delete(self, student_name):
        if name not in students:
            abort(404)

        del students[name]        

        #delete student from all courses
        for course_details in courses.values():
            if name in course_details["students"]:
                course_details["students"].remove(name)
    
    #assign_course_to_student
    def put(self, student_name):
        data = request.json
        course_name = data['course_name']
        
        if student_name not in students:
            abort(404)
        if course_name not in courses:
            abort(404)
        if course_name in students[student_name]:
            abort(404)
        
        students[student_name][course_name] = UNSCORED
        courses[course_name]["students"].append(student_name)


class StudentListResource(Resource):
    def get(self):
        return students

    def post(self):
        data = request.json
        name = data['name']
        
        if name not in students:
            students[name] = {}
        
        return name, 201

class CourseResource(Resource):
    def delete(self, course_name):
        if name not in courses:
            abort(404)

        del courses[name]        

        #delete course from all students
        for student_courses in students.values():
            if course_name in student_courses:
                del student_courses[course_name]


class CourseListResource(Resource):
    def get(self):
        return courses

    def post(self):
        data = request.json
        name = data['name']
        points = data['points']
        
        if name not in courses:
            courses[name] = { "points": points, "students": []}
            
        return name, 201


api.add_resource(StudentListResource, '/student')
api.add_resource(StudentResource, '/student/<string:student_name>')
api.add_resource(CourseListResource, '/course')
api.add_resource(CourseResource, '/course/<string:course_name>')


@app.errorhandler(404)
def not_found(e):
    return '', 404