from db import db
from sqlalchemy.sql import text
import users

def post_review(data):
    print(data)
    university = data["university"]
    course = data["course"]

    result = get_university(university)
    if not result:
        add_university(university)
    result = get_university(university)
    university_id, university = result[0], result[1]
    
    result = get_course(course)
    if not result:
        add_course(university, course, data["course-code"])
    result = get_course(course)
    course_id, course_name, course_code = result[0], result[1], result[2]
    
    user_id = users.user_id()
    
    sql = "INSERT INTO reviews (user_id, course_id, published_at, title, content, " \
            "difficulty, time_consumingness, material, credits, practicality, " \
            "interestingness) VALUES (:user_id, :course_id, NOW(), :title, " \
            ":content, :difficulty, :time_consumingness, :material, :credits, " \
            ":practicality, :interestingness)"
    db.session.execute(text(sql), {"user_id":user_id, "course_id":course_id, 
                                    "title":data["title"], "content":data["content"], 
                                    "difficulty":data["difficulty"], 
                                    "time_consumingness":data["time"], 
                                    "material":data["material"], "credits":data["credits"], 
                                    "practicality":data["practicality"], 
                                    "interestingness":data["interestingness"]})
    db.session.commit()
    
def get_university(university):
    sql = "SELECT id, name from universities where LOWER(name) " \
            "LIKE LOWER(:university) "
    return db.session.execute(text(sql), {"university":"%"+university+"%"}).fetchone()

def add_university(university):
    sql = "INSERT INTO universities (name) VALUES (:university)"
    db.session.execute(text(sql), {"university":university})
    db.session.commit()

def get_course(course):
    sql = "SELECT id, course_name, course_code from " \
            "courses where LOWER(course_name) LIKE LOWER(:course)"    
    return db.session.execute(text(sql), {"course":"%"+course+"%"}).fetchone()

def add_course(university, course, course_code):
    sql = "SELECT id FROM universities where LOWER(name) " \
            "LIKE LOWER(:university) "
    result = db.session.execute(text(sql), {"university":"%"+university+"%"}).fetchone()
    university_id = result[0]
    sql = "INSERT INTO courses (course_name, course_code, university_id) " \
            "VALUES (:course, :course_code, :university_id)"
    db.session.execute(text(sql), {"course":course, "course_code":course_code, 
                                    "university_id":university_id})
    db.session.commit()

def get_reviews():
    sql = "SELECT r.id, users.username, universities.name, courses.course_name, " \
            "r.published_at, r.title, r.content, r.difficulty, r.time_consumingness, " \
            "r.material, r.credits, r.practicality, r.interestingness FROM reviews r, " \
            "courses, universities, users WHERE users.id = r.user_id AND " \
            "courses.id = r.course_id AND universities.id = courses.university_id"
    return db.session.execute(text(sql)).fetchall()

def get_course(course_name):
    sql = "SELECT * from courses where course_name=:course_name"
    return db.session.execute(text(sql), {"course_name":course_name}).fetchone()
