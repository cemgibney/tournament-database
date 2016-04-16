-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (player_name text, player_id serial primary key);

create table matches (player_id integer references players, winner integer, match_id integer);

create view standings as select players.player_id, players.player_name, 
case when sum(matches.winner) is null then 0 else sum(matches.winner) end
as wins, count(matches.winner) as matches from players, matches where 
players.player_id = matches.player_id group by players.player_id order by
wins desc;

create view match_ids as select case when max(match_id) is null then 0 
else max(match_id) + 1 end as match_id from matches;
