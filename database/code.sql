--- Tables ---

-- capital cities
CREATE TABLE capital_cities (
    cc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL
);

-- weather for next day
CREATE TABLE weather_tomorrow (
    wt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    cc_id INTEGER NOT NULL,
    temperature INTEGER NOT NULL,
    pressure ,
    humidity,
    visibility,
    FOREIGN KEY (cc_id) REFERENCES capital_cities (cc_id) ON DELETE SET NULL
);


-- weather
CREATE TABLE weather (
    w_id
    date 
    cc_id
);