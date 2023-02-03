CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    course_name TEXT,
    course_code TEXT UNIQUE,
    university TEXT UNIQUE,
    department TEXT,
    credits INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses,
    published_at TIMESTAMP,
    title TEXT,
    content TEXT,
    difficulty TEXT,
    time_consumingness TEXT,
    course_material TEXT,
    practical_credit_amount TEXT,
    usefulness TEXT,
    interestingness TEXT
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    age INTEGER,
    university TEXT,
    degree_title TEXT,
    university_credits INTEGER,
    review_amount INTEGER,
    reliability_percentage TEXT
);

CREATE TABLE review_stats (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    agreements INTEGER,
    disagreements INTEGER
);


CREATE TABLE course_stats (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    likes INTEGER,
    difficulty TEXT,
    time_consumingness TEXT,
    course_material TEXT,
    practical_credit_amount TEXT,
    usefulness TEXT,
    interestingness TEXT
)