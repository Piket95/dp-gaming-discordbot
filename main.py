from dotenv import load_dotenv
from random import randrange
import os
import discord
import pymysql
import datetime

load_dotenv()


class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.ganyulist = [
            "https://img.pr0gramm.com/2021/02/17/f9d0364a8ae8f40d.png",
            "https://img.pr0gramm.com/2021/02/14/088a63c397562f07.jpg",
            "https://img.pr0gramm.com/2021/02/11/3399b272d5d80159.png",
            "https://img.pr0gramm.com/2021/02/09/706302fc327ad217.jpg",
            "https://img.pr0gramm.com/2021/01/26/2b31c4a38c1f1ff8.jpg",
            "https://img.pr0gramm.com/2021/02/10/d2cc18cdd77d312e.jpg",
            "https://img.pr0gramm.com/2021/02/15/1bbbc2e3eaa8ca26.jpg",
            "https://img.pr0gramm.com/2021/02/02/9120ee9297589bc2.jpg",
            "https://img.pr0gramm.com/2021/02/03/1425b11f74013fe8.jpg",
            "https://img.pr0gramm.com/2021/02/08/3df03ead57d82ff8.jpg"
        ]

        self.db = pymysql.connect(host=os.getenv("DBHOST"),
                                  user=os.getenv("DBUSER"),
                                  database=os.getenv("DB"))
        self.cursor = self.db.cursor()
        self.cursor.execute("SHOW TABLES LIKE 'games'")

        if not self.cursor.fetchone():
            sql = """CREATE TABLE games (
                               id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                               name  CHAR(20) NOT NULL )"""
            self.cursor.execute(sql)

    # Einloggen
    async def on_ready(self):
        print("Ich habe mich eingeloggt!")

    # Wenn Nachricht geschrieben wird
    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("!ganyu"):
            await message.channel.send(self.ganyulist[randrange(len(self.ganyulist))])

        if message.content.startswith("!game list"):
            self.cursor.execute("SELECT * FROM games")
            results = self.cursor.fetchall()

            if not results:
                await message.channel.send("Keine Einträge gefunden!")
            else:
                msg = ""

                for row in results:
                    msg = msg + "- " + row[1] + "\n"

                await message.channel.send(msg)

        if message.content.startswith("!game add "):
            game = message.content.replace('!game add ', '')

            try:
                self.cursor.execute(f"INSERT INTO games (name) VALUES ('{game}')")
                self.db.commit()
            except:
                self.db.rollback()

            await message.channel.send("\"" + game + "\" wurde erfolgreich in die Liste aufgenommen")

        # if message.content.startswith("!game remove "):

        if message.content.startswith("!game next"):
            msg = ""

            # today = datetime.date.today() + datetime.timedelta(6) # Heute +6 Tage simuliert
            today = datetime.date.today()
            wednesday = today + datetime.timedelta((1 - today.weekday()) % 7 + 1)
            msg = msg + "Nächster Spielabend ist am: " + wednesday.strftime("%d.%m.%Y") + "\n"

            games = self.get_games()

            if not games:
                await message.channel.send("Keine Liste mit Spielen in der Datenbank vorhanden!")

            rngGame = games[randrange(len(games))]
            msg = msg + "Folgendes Spiel wird gespielt: " + rngGame

            await message.channel.send(msg)

        # HELP Befehl mit Auflistung aller Befehle

    # !game next automatisch jeden Mittwoch abend?

    def get_games(self):
        self.cursor.execute("SELECT * FROM games")
        results = self.cursor.fetchall()

        if not results:
            return

        games = []

        for row in results:
            games.append(row[1])

        return games


client = MyClient()
client.run("NjE4ODI5ODUxNTYyMDgyMzc1.XW_YNQ.JfMU8QMmaE5z_02t28-YDeamz4Y")
