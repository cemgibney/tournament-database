-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players 
	(
		player_name TEXT, 
		player_id serial PRIMARY KEY
	);

CREATE TABLE matches 
	(
		player_id INTEGER PRIMARY KEY REFERENCES players, 
		winner INTEGER, 
		match_id INTEGER
	);

CREATE VIEW standings 
AS 
	SELECT 	players.player_id, 
			players.player_name, 
			CASE 
				WHEN SUM(matches.winner) IS NULL THEN 0 
				ELSE SUM(matches.winner) 
				END			AS wins, 
				Count(matches.winner) 	AS matches 
	FROM 	players, 
		matches 
	WHERE 	players.player_id = matches.player_id 
	GROUP BY players.player_id 
	ORDER BY wins desc;

CREATE VIEW match_ids 
AS 
	SELECT CASE 
			WHEN Max(match_id) IS NULL THEN 0 
			ELSE Max(match_id) + 1 
		END AS match_id 
	FROM matches;

CREATE VIEW s1
AS 
	SELECT 	Row_number()
			OVER(
				ORDER BY wins DESC) AS 	position, 
		*
	FROM standings;

CREATE VIEW even
AS
	(SELECT Row_number()
			OVER(
				ORDER BY s1.wins DESC) AS i,
			s1.player_id,
			s1.player_name,
			s1.wins
	FROM s1
	WHERE Mod(position, 2) = 0);

CREATE VIEW odd
AS 
	(SELECT Row_number()
			OVER(
				ORDER BY s1.wins DESC) AS i,
			s1.player_id,
			s1.player_name,
			s1.wins
	FROM s1
	WHERE Mod(position, 2) != 0);

CREATE VIEW pairs
AS 
	(SELECT	odd.player_id		AS player_1_id, 
		odd.player_name		AS player_1_name, 
		even.player_id 		AS player_2_id, 
		even.player_name 	AS player_2_name
	FROM	odd,
		even
	WHERE 	odd.i = even.i);
