import sqlite3

# Connect to the database
conn = sqlite3.connect('game.db')
c = conn.cursor()