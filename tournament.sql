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
		player_name text, 
		player_id serial primary key
	);

CREATE TABLE matches 
	(
		player_id integer primary key references players, 
		winner integer, 
		match_id integer
	);

CREATE VIEW standings 
AS 
	SELECT 	players.player_id, 
			players.player_name, 
			CASE 
				WHEN SUM(matches.winner) IS NULL THEN 0 
				ELSE SUM(matches.winner) 
				END					  AS wins, 
				Count(matches.winner) AS matches 
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
