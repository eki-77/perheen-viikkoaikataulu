CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT, 
    admin BOOLEAN
);

CREATE TABLE calendars (
    id SERIAL PRIMARY KEY,
    calendarname TEXT
);

CREATE TABLE calendar_owners (
    calendar_id INTEGER REFERENCES calendars ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    calendar_id INTEGER REFERENCES calendars ON DELETE CASCADE,
    day INTEGER,
    start_time TIME,
    end_time TIME,
    eventname TEXT,
    items TEXT
);

CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    calendar_id INTEGER REFERENCES calendars ON DELETE CASCADE,
    name TEXT
);

CREATE TABLE event_persons (
    event_id INTEGER REFERENCES events ON DELETE CASCADE,
    person_id INTEGER REFERENCES persons ON DELETE CASCADE
);

