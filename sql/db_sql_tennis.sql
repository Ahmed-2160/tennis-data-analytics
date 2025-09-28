CREATE DATABASE tennis_db;
SHOW TABLES;
USE tennis_db;
SHOW TABLES;
ALTER TABLE competitions DROP FOREIGN KEY competitions_ibfk_1;
DROP TABLE categories;
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
SELECT * FROM categories LIMIT 5;
SELECT * FROM competitions LIMIT 5;
-- Players table
CREATE TABLE IF NOT EXISTS players (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    date_of_birth DATE,
    ranking INT
);

CREATE TABLE IF NOT EXISTS venues (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT
);

DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS competitions;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS venues;

CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255)
);
CREATE TABLE players (
    player_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    nationality VARCHAR(100),
    ranking INT
);
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100)
);
CREATE TABLE matches (
    match_id VARCHAR(50) PRIMARY KEY,
    competition_id VARCHAR(50),
    venue_id VARCHAR(50),
    player1_id VARCHAR(50),
    player2_id VARCHAR(50),
    scheduled DATETIME,
    status VARCHAR(50),
    winner_id VARCHAR(50),
    FOREIGN KEY (competition_id) REFERENCES competitions(competition_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (player1_id) REFERENCES players(player_id),
    FOREIGN KEY (player2_id) REFERENCES players(player_id),
    FOREIGN KEY (winner_id) REFERENCES players(player_id)
);
ALTER TABLE competitions DROP COLUMN category;
ALTER TABLE competitions
  ADD COLUMN parent_id VARCHAR(50),
  ADD COLUMN type VARCHAR(50),
  ADD COLUMN gender VARCHAR(50),
  ADD COLUMN category_id VARCHAR(50);
  CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
SHOW TABLES;
DESCRIBE players;
SELECT COUNT(*) FROM players;

SELECT * FROM matches;
SELECT name, nationality FROM players WHERE ranking IS NOT NULL;

----- List all competitions with their category name


SELECT c.competition_id, c.name AS competition, c.category_id, cat.category_name AS category
FROM competitions c
LEFT JOIN categories cat ON c.category_id = cat.category_id
LIMIT 1000;

----- Count the number of competitions in each categor

SELECT cat.category_name AS category, COUNT(c.competition_id) AS total_competitions
FROM categories cat
JOIN competitions c ON cat.category_id = c.category_id
GROUP BY cat.category_name;

----- Find all competitions of type

SELECT name, type
FROM competitions
WHERE type = 'doubles';

----- get competitions that belong to a specific category

SELECT c.name AS competition
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

----- Identify parent competitions and their sub-competitions

SELECT parent.name AS parent_competition, child.name AS sub_competition
FROM competitions child
JOIN competitions parent ON child.parent_id = parent.competition_id;

----- Analyze the distribution of competition types by category

SELECT cat.category_name AS category, c.type AS competition_type, COUNT(*) AS total
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type;

----- List all competitions with no parent (top-level competitions)

SELECT name AS top_level_competition
FROM competitions
WHERE parent_id IS NULL;

----- List all venues along with their associated complex name

SELECT v.name AS venue, c.name AS complex
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id;


----- Get details of venues in a specific country

	SELECT *
	FROM venues
	WHERE country = 'Chile';

INSERT INTO venues (venue_id, name, city, country)
VALUES ('venue_001', 'Estadio Nacional', 'Santiago', 'Chile');

SELECT *
FROM venues
WHERE country = 'Chile';

----- List venues grouped by country

SELECT country, COUNT(*) AS venue_count
FROM venues
GROUP BY country;

CREATE TABLE complexes (
  complex_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100),
  city VARCHAR(100),
  country VARCHAR(100)
);

ALTER TABLE venues ADD COLUMN complex_id VARCHAR(50);

REPLACE INTO complexes (complex_id, name, city, country)
VALUES 
  ('cx_001', 'Nacional', 'Santiago', 'Chile'),
  ('cx_002', 'Grand Arena', 'Madrid', 'Spain');

UPDATE venues
SET complex_id = 'cx_001'
WHERE city = 'Santiago' AND venue_id = 'venue_001';

UPDATE venues
SET complex_id = 'cx_002'
WHERE city = 'Madrid' AND venue_id = 'venue_002';

----- List all venues with their complex name

SELECT v.name AS venue, c.name AS complex
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id;

 ----- Count venues in each complex
 
 SELECT c.name AS complex, COUNT(v.venue_id) AS venue_count
FROM complexes c
LEFT JOIN venues v ON c.complex_id = v.complex_id
GROUP BY c.name;

----- Complexes with more than one venue

SELECT c.name AS complex
FROM complexes c
JOIN venues v ON c.complex_id = v.complex_id
GROUP BY c.name
HAVING COUNT(v.venue_id) > 1;

----- Venues for a specific complex

SELECT v.name AS venue
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
WHERE c.name = 'Nacional';



