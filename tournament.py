#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from matches; delete from players;")
                   #  Remove all matches first, as they are dependent on
                   #  table players for primary key.
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from players;")
    results = cursor.fetchall()[0][0]
    conn.close()
    return results



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    cursor = conn.cursor()
    cmd = ("insert into players values (%s)")
    cursor.execute(cmd, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches (player_id)"
                   "select player_id from players;")
                   #  First make sure that the correct player_ids are 
                   #  inserted in table matches.
    conn.commit()
    cursor.execute("select players.player_id, players.player_name, "
                    #  Pull player names
                    "case when sum(matches.winner) is null then 0 else "
                    "sum(matches.winner) end as wins, count(matches.winner) "
                    #  Sum the winners column (set to 0 if null)
                    "as matches from players, matches where players.player_id"
                    " = matches.player_id group by players.player_id order by"
                    " wins desc;")
    results = cursor.fetchall()
    conn.close()
    return results



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    cursor = conn.cursor()
    cmd = "insert into matches (player_id, winner, match_id) values (%s, 1, (select * from match_ids)), (%s, 0, (select * from match_ids));"
    cursor.execute(cmd, (winner,loser))
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select distinct a.player_id, a.player_name, b.player_id, "
                   "b.player_name from standings as a, standings as b where "
                   "a.player_id != b.player_id and a.wins = b.wins limit 4;")
                   #  Join standings to self, pull player 1 and player 2 based
                   #  on their win records, make sure they are distinct, and
                   #  limit to 4 pairs.
    results = cursor.fetchall()
    conn.close()    
    return results
