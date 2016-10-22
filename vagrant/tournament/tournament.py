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
    c = conn.cursor()
    c.execute("UPDATE t_results Set wins = 0, matches = 0;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM t_results;")
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as num FROM players;")
    val = c.fetchone()[0]
    return val
    conn.close()

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) Values (%s)",(name,))
    conn.commit()
    c.execute("SELECT id FROM players WHERE name = %s", (name,))
    player_id = c.fetchone()
    c.execute("INSERT INTO t_results (id, wins, matches) VALUES (%s, 0 ,0)", (player_id,))
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
    c = conn.cursor()
    c.execute("SELECT players.id, name, wins, matches FROM t_results LEFT JOIN players ON players.id=t_results.id ORDER BY wins DESC;")
    val = c.fetchall()
    return val
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE t_results set wins = wins+1, matches = matches+1  where t_results.id=%s;", (winner,))
    conn.commit()
    c.execute("UPDATE t_results set matches = matches+1  where t_results.id=%s;", (loser,))
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
    c = conn.cursor()
    c.execute("CREATE VIEW standings AS SELECT players.id, name, wins, matches FROM t_results LEFT JOIN players ON players.id=t_results.id ORDER BY wins DESC;")
    c.execute("SELECT id, name FROM standings;")
    info = c.fetchall()
    pairings = []
    v1 = info[0] + info[1]
    v2 = info[2] + info[3]
    v3 = info[4] + info[5]
    v4 = info[6] + info[7]
    pairings.append(v1)
    pairings.append(v2)
    pairings.append(v3)
    pairings.append(v4)
    return pairings
    c.execute("DROP VIEW standings")
    conn.close()