from dotenv import load_dotenv
import os
import discord
import pymysql

import spieleabend
import verwaltung

load_dotenv()


class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)

        self.db = pymysql.connect(host=os.getenv("DBHOST"),
                                  user=os.getenv("DBUSER"),
                                  password=os.getenv("DBPASS"),
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
        elif not message.content.startswith("!"):
            return

        # TODO: Switch Statement benutzen um zu checken, welcher Befehl geschrieben wurde

        if message.content.startswith("!help"):
            embed = discord.Embed(title="Befehlsübersicht",
                                  description="Folgende Befehle sind mir bisher bekannt:",
                                  color=0x3f51b5)
            embed.set_author(name="DPGamingBot")
            embed.add_field(name="Spielabend",
                            value="`!game next` Gibt das Datum des nächsten Spielabend an und das "
                                  "Spiel das gespielt werden soll\n"
                                  "`!game add <Spielname>` Fügt ein Spiel der Liste hinzu\n"
                                  "`!game list` Gibt eine Liste der hinterlegten Spiele zurück\n",
                            inline=False)
            await message.channel.send(embed=embed)

        if not isinstance(message.channel, discord.channel.DMChannel):

            if message.content.startswith("!game list"):
                await spieleabend.gamelist(self.cursor, message)
            elif message.content.startswith("!game add "):
                await spieleabend.add_games(message, self.cursor, self.db)
            elif message.content.startswith("!game next"):
                await spieleabend.next_game(message, self.cursor)
            else:
                if not message.content.startswith("!help"):
                    await message.channel.send("Diesen Befehl kenne ich leider nicht!")

            await message.delete()
        else:
            if not message.content.startswith("!help"):
                await message.channel.send("Diesen Befehl kenne ich entweder nicht oder ich kann ihn nicht in "
                                           "privaten Chats ausführen!")

        # TODO: !clear Befehle


client = MyClient()
client.run(os.getenv("DISCORDTOKEN"))
