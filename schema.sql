CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE universities (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    course_name TEXT,
    course_code TEXT,
    university_id INTEGER REFERENCES universities,
    official_credits INTEGER
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
    material TEXT,
    credits TEXT,
    practicality TEXT,
    interestingness TEXT
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    age INTEGER,
    university TEXT,
    degree_title TEXT,
    university_credits INTEGER,
    reviews INTEGER,
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
    material TEXT,
    credits TEXT,
    usefulness TEXT,
    interestingness TEXT
)