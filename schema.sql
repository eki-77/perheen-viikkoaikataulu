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
    calendar_id INTEGER REFERENCES calendars,
    user_id INTEGER REFERENCES users
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    calendar_id INTEGER REFERENCES calendars,
    day INTEGER,
    start_time TIME,
    end_time TIME,
    eventname TEXT,
    items TEXT
);

CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    calendar_id INTEGER REFERENCES calendars,
    name TEXT,
);

CREATE TABLE event_persons (
    event_id INTEGER REFERENCES events,
    person_id INTEGER REFERENCES persons,
);
