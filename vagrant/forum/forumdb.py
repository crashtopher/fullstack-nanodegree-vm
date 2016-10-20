#
# Database access functions for the web forum.
#

import time
import psycopg2

## Get posts from database.
def GetAllPosts():
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute('SELECT time, conent FROM posts ORDER BY time DESC')
    posts = ({'conent': str(row[1]), 'time': str(row[0])}
             for row in c.fetchall())
    DB.close
    return posts

## Add a post to the database.

def AddPost(content):
    DB = DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute('INSERT INTO posts (content) VALUES (%s)' %content)
    DB.commit()
    DB.close