import sqlite3
import os


os.remove("games.db")
con = sqlite3.connect("games.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS first(
   server_id INT,
   channel_id INT,
   white_player_id INT,
   black_player_id INT);
""")
con.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS stats(
   player_id INT,
   number_of_games INT,
   wins INT,
   loses INT);
""")
con.commit()
con.close()
