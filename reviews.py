from db import db
from sqlalchemy.sql import text
import users

def post_review(data):
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

    posted_review = db.session.execute(text("SELECT * FROM reviews ORDER BY id DESC LIMIT 1")).fetchone()
    set_review_stats(posted_review[0])
    set_user_review_engagement(posted_review[0])
    
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
            "r.material, r.credits, r.practicality, r.interestingness, rs.id, rs.agreements, rs.disagreements FROM reviews r, " \
            "courses, universities, review_stats rs, users WHERE users.id = r.user_id AND " \
            "courses.id = r.course_id AND universities.id = courses.university_id AND rs.review_id = r.id ORDER BY r.published_at DESC"
    return db.session.execute(text(sql)).fetchall()

def get_user_agreements(user_id):
    sql = "SELECT review_id FROM user_review_engagement WHERE user_id = :user_id AND agreed = TRUE"
    result = db.session.execute(text(sql), {"user_id":user_id}).fetchall()
    return result

def get_user_disagreements(user_id):
    sql = "SELECT review_id FROM user_review_engagement WHERE user_id = :user_id AND disagreed = TRUE"
    result = db.session.execute(text(sql), {"user_id":user_id}).fetchall()
    return result

def get_course(course_name):
    sql = "SELECT * from courses where course_name=:course_name"
    return db.session.execute(text(sql), {"course_name":course_name}).fetchone()

def set_review_stats(id):
    sql = "INSERT INTO review_stats (review_id, agreements, disagreements) VALUES (:id, 0, 0)"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def get_review_stats(id):
    sql = "SELECT * from review_stats WHERE review_id = :id"
    result = db.session.execute(text(sql), {"id":id}).fetchone()
    print(result)

def check_if_agreed(review_id, user_id):
    sql = "SELECT agreed FROM user_review_engagement WHERE user_id = :user_id AND review_id = :review_id"
    result = db.session.execute(text(sql), {"user_id":user_id, "review_id":review_id}).fetchone()

def check_if_disagreed(review_id, user_id):
    sql = "SELECT disagreed FROM user_review_engagement WHERE user_id = :user_id AND review_id = :review_id"
    result = db.session.execute(text(sql), {"user_id":user_id, "review_id":review_id}).fetchone()

def agree(review_id, user_id):
    sql = "UPDATE review_stats set agreements = agreements + 1 where review_id = :review_id"
    db.session.execute(text(sql), {"review_id":review_id})
    db.session.commit()

    sql = "UPDATE user_review_engagement SET agreed = TRUE where user_id = :user_id AND review_id = :review_id"
    db.session.execute(text(sql), {"user_id":user_id, "review_id":review_id})
    db.session.commit()

def unagree(review_id, user_id):
    sql = "UPDATE review_stats set agreements = agreements - 1 where review_id = :review_id"
    db.session.execute(text(sql), {"review_id":review_id})
    db.session.commit()

    sql = "UPDATE user_review_engagement SET agreed = FALSE where user_id = :user_id AND review_id = :review_id"
    db.session.execute(text(sql), {"user_id":user_id, "review_id":review_id})
    db.session.commit()

def disagree(review_id, user_id):
    sql = "UPDATE review_stats set disagreements = disagreements + 1 where review_id = :review_id"
    db.session.execute(text(sql), {"review_id":review_id})
    db.session.commit()

    sql = "UPDATE user_review_engagement SET disagreed = TRUE where user_id = :user_id AND review_id = :review_id"
    db.session.execute(text(sql), {"user_id":user_id, "review_id":review_id})
    db.session.commit()

def undisagree(review_id, user_id):
    sql = "UPDATE review_stats set disagreements = disagreements - 1 where review_id = :review_id"
    db.session.execute(text(sql), {"review_id":review_id})
    db.session.commit()

    sql = "UPDATE user_review_engagement SET disagreed = FALSE where user_id = :user_id AND review_id = :review_id"
    db.session.execute(text(sql), {"user_id":user_id, "review_id":review_id})
    db.session.commit()

def set_user_review_engagement(review_id):
    sql = "SELECT id FROM users"
    all_users = db.session.execute(text(sql)).fetchall()

    for user_id in all_users:
        sql = "INSERT INTO user_review_engagement (user_id, review_id, agreed, disagreed) " \
                "VALUES (:user_id, :review_id, FALSE, FALSE)"
        db.session.execute(text(sql), {"user_id":user_id.id, "review_id":review_id})
        db.session.commit()
