-- ======================================================
--  Tennis Project Database Schema
-- ======================================================

-- Drop old tables if they exist (order matters for FKs)
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS competitions;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS venues;

-- ======================================================
-- Competitions Table
-- ======================================================
CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255)
);

-- ======================================================
-- Players Table
-- ======================================================
CREATE TABLE players (
    player_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    nationality VARCHAR(100),
    ranking INT
);

-- ======================================================
-- Venues Table
-- ======================================================
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100)
);

-- ======================================================
-- Matches Table
-- ======================================================
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

