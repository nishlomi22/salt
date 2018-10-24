from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

UNSCORED = -1

students = {}
courses = {}

@app.route('/students/<string:name>', methods=['POST'])
def add_new_student(self, name):
    if name not in students:
        students[name] = {}
    
    return jsonify(name)

@app.route('/courses/<string:name>', methods=['POST'])
def add_new_course(self, name):
    points = request.json['points']

    if name not in courses:
        courses[name] = {"points": points, "students": []}
        
    return name, 201

    return jsonify(name)

    
@app.route('/students/<string:name>', methods=['DELETE'])
def remove_student(name):
    if name not in students:
        abort(404)

    del students[name]        

    #delete student from all courses
    for course_details in courses.values():
        if name in course_details["students"]:
            course_details["students"].remove(name)
    
    return jsonify({'status': 'success'})

            
@app.route('/students/<string:name>', methods=['DELETE'])
def remove_course(name):
    if name not in courses:
        abort(404)

    del courses[name]        

    #delete course from all students
    for student_courses in students.values():
        if course_name in student_courses:
            del student_courses[course_name]
    
    return jsonify({'status': 'success'})

@app.route('/courses/<string:course_name>', methods=['PUT'])
def assign_course_to_student(self, course_name):
    student_name = request.json['student_name']
    
    if student_name not in students or \
       course_name not in courses or \
       course_name in students[student_name]:
        abort(404)
    
    students[student_name][course_name] = UNSCORED
    courses[course_name]["students"].append(student_name)
    
    return jsonify({'status': 'success'})

@app.route('/students/<string:student_name>', methods=['PUT'])
def set_score_to_course_for_student(score):
    course_name = request.json['course_name']
    score = request.json['score']
    
    if student_name not in students or \
       course_name not in courses:
        abort(404)
    
    students[student_name][course_name] = score
    
    return jsonify({'status': 'success'})

@app.route('/student_list/<string:course_name>', methods=['GET'])        
def get_all_students_assign_to_course(course_name):
    if course_name not in courses:
        abort(404)
    
    return jsonify(courses[course_name]["students"])

@app.route('/courses_list/<string:student_name>', methods=['GET'])        
def get_all_courses_assign_to_student(student_name):
    if student_name not in students:
        abort(404)
    
    return jsonify(students[student_name].keys())

@app.route('/student_average/<string:student_name>', methods=['GET'])        
def get_weighted_average(student_name):
    if student_name not in students or \
       len(students[student_name].values())==0:
        abort(404)
        
    points_sum = 0
    total_sum = 0
    for course_name, score in students[student_name]:
        if score == UNSCORED:
            continue
        points_sum += courses[course_name]["points"]
        total_sum += courses[course_name]["points"] * score
    
    if points_sum == 0:
        return UNSCORED
        
    return total_sum / points_sum

@app.route('/excellent_students', methods=['GET'])    
def get_all_students_with_average_above_90():
    result = []
    for student_name in students.keys():
        if get_weighted_average(student_name) > 90:
            result.append(student_name)
            
    return jsonify(result)

@app.errorhandler(404)
def not_found(e):
    return '', 404