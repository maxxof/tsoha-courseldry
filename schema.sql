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

CREATE TABLE review_stats (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    agreements INTEGER,
    disagreements INTEGER
);

CREATE TABLE user_review_engagement(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    review_id INTEGER REFERENCES reviews,
    agreed BOOLEAN DEFAULT FALSE,
    disagreed BOOLEAN DEFAULT FALSE
);