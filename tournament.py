#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Could not connect to database 'tournament'")



def deleteMatches():
    """Remove all the match records from the database."""

    db, cursor = connect()
    cursor.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""

    db, cursor = connect()
    cursor.execute("delete from matches; delete from players;")
                   #  Remove all matches first, as they are dependent on
                   #  table players for primary key.
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""

    db, cursor = connect()
    cursor.execute("select count(*) from players;")
    results = cursor.fetchone()[0]
    db.close()
    return results



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db, cursor = connect()
    cmd = ("insert into players values (%s)")
    cursor.execute(cmd, (name,))
    db.commit()
    db.close()


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

    db, cursor = connect()
    cursor.execute("insert into matches (player_id)"
                   "select player_id from players;")
                   #  First make sure that the correct player_ids are 
                   #  inserted in table matches.
    db.commit()
    cursor.execute("select player_id, player_name, wins, matches from "
                   "standings;")
                   #  Pull data from view standings, composite of 
                   #  table players and table matches.
    results = cursor.fetchall()
    db.close()
    return results



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cursor = connect()
    cmd = """insert into matches (player_id, winner, matched_pairs) values 
    (%s, 1, (select * from matched_pairs)), (%s, 0, (select * from 
    matched_pairs));"""
    #  Wins inserted as boolean 1 or 0, match_id pulls same number from
    #  view match_ids to identify that these two players have played each
    #  other.
    cursor.execute(cmd, (winner,loser))
    db.commit()
    db.close()
 
 
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
    db, cursor = connect()
    cursor.execute("select * from pairs;")
    results = cursor.fetchall()
    db.close()    
    return results


