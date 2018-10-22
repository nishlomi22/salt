UNSCORED = -1

students = {}
courses = {}

def add_new_student(name):
    if name not in students:
        students[name] = {}

def add_new_course(name, points):
    if name not in courses:
        courses[name] = { "points": points, "students": []}

def remove_student(name):
    if name in students:
        del students[name]        

def remove_course(name):
    if name in courses:
        del courses[name]

def assign_course_to_student(student_name, course_name):
    if student_name not in students:
        #ERROR
        return
    
    if course_name not in courses:
        #ERROR
        return
    
    if course_name in students[student_name]:
        return
    
    students[student_name][course_name] = UNSCORED
    courses[course_name]["students"].append(student_name)

def set_score_to_course_for_student(student_name, course_name, score):
    if student_name not in students:
        #ERROR
        return
    
    if course_name not in courses:
        #ERROR
        return
    
    students[student_name][course_name] = score

def get_all_students_assign_to_course(course_name):
    if course_name not in courses:
        #ERROR
        return
    
    for student_name in students.keys():
        assign_course_to_student(student_name,course_name)

def get_all_courses_assign_to_student(course_name):
    if student_name not in students:
        #ERROR
        return
    
    for course_name in courses.keys():
        assign_course_to_student(student_name,course_name)

def get_weighted_average(student_name):
    if student_name not in students:
        #ERROR
        return
    if len(students[student_name].values())==0:
        #ERROR
        return 0
        
    points_sum = 0
    total_sum = 0
    for course_name, score in students[student_name]:
        points_sum += courses[course_name]["points"]
        total_sum += courses[course_name]["points"] * score
    
    if points_sum == 0:
        #ERROR
        return
        
    return total_sum / points_sum

def get_all_students_with_average_above_90():
    result = []
    for student_name in students.keys():
        if get_weighted_average(student_name) > 90:
            result.append(student_name)
            
    return result
        
if __name__=="__main__":
    print "Hello"