from db import db
from sqlalchemy.sql import text
import users

def post_review(data):
    university = data["university"]
    course = data["course"]

    result = get_university(university)
    if not result:
        university_id = add_university(university)
        add_course(university_id, course, data["course-code"])
    result = get_university(university)
    university_id, university = result[0], result[1]
    
    result = get_course(course, university_id)
    if not result:
        add_course(university_id, course, data["course-code"])
    result = get_course(course, university_id)
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
    sql = "SELECT id, name from universities where LOWER(name) = " \
            "LOWER(:university) "
    return db.session.execute(text(sql), {"university":university}).fetchone()

def add_university(university):
    sql = "INSERT INTO universities (name) VALUES (:university) RETURNING id"
    result = db.session.execute(text(sql), {"university":university}).fetchone()[0]
    db.session.commit()
    return result

def get_course(course, university_id):
    sql = "SELECT id, course_name, course_code from " \
            "courses where university_id = :university_id AND LOWER(course_name) = LOWER(:course)"    
    result = db.session.execute(text(sql), {"course":course, "university_id":university_id}).fetchone()
    return result

def add_course(university_id, course, course_code):
    sql = "INSERT INTO courses (course_name, course_code, university_id) " \
            "VALUES (:course, :course_code, :university_id)"
    db.session.execute(text(sql), {"course":course, "course_code":course_code, 
                                    "university_id":university_id})
    
    db.session.commit()

def get_reviews():
    sql = "SELECT r.id, users.username, universities.name, courses.course_name, " \
            "r.published_at, r.title, r.content, r.difficulty, r.time_consumingness, " \
            "r.material, r.credits, r.practicality, r.interestingness, rs.id, rs.agreements, rs.disagreements, r.course_id, r.user_id FROM reviews r, " \
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

def set_review_stats(id):
    sql = "INSERT INTO review_stats (review_id, agreements, disagreements) VALUES (:id, 0, 0)"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

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

def get_course_stats(course_id):
    sql = "SELECT ROUND(AVG(cast(difficulty AS INTEGER)), 1), ROUND(AVG(cast(time_consumingness AS INTEGER)), 1), " \
            "ROUND(AVG(cast(material AS INTEGER)), 1), ROUND(AVG(cast(credits AS INTEGER)), 1), " \
            "ROUND(AVG(cast(practicality AS INTEGER)), 1), ROUND(AVG(cast(interestingness AS INTEGER)), 1) FROM " \
            "reviews WHERE course_id = :course_id"
    
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchone()
    return result

def get_course_info(course_id):
    sql = "SELECT courses.course_name, courses.course_code, universities.name FROM courses LEFT JOIN universities " \
            "ON courses.university_id = universities.id WHERE courses.id = :course_id"
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchone()
    return result

def get_user_reviews(user_id):
    sql = "SELECT * FROM reviews WHERE user_id = :user_id"
    result = db.session.execute(text(sql), {"user_id":user_id}).fetchall()
    return result

def get_username(user_id):
    sql = "SELECT username FROM users WHERE id = :user_id"
    result = db.session.execute(text(sql), {"user_id":user_id}).fetchone()
    return result