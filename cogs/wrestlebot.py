import time
import config
import os, sys, discord, platform, subprocess
import sqlite3
from discord.ext import commands

dbFile = "./wrestlebot.db"
# Main Piece for the Cog
class Wrestlebot(commands.Cog, name="wrestlebot"):
    def __init__(self, bot):
        # Needed for cogs
        self.bot = bot

        # Check if database exists
        if not os.path.exists(dbFile):
            conn = sqlite3.connect(dbFile)
            c = conn.cursor()
            c.execute("CREATE TABLE wrestlers (id INTEGER PRIMARY KEY, username TEXT, discord_id TEXT)")
            conn.commit()
            c.execute("CREATE TABLE matches (id INTEGER PRIMARY KEY, wrestler1 TEXT, wrestler2 TEXT, winner TEXT, loser TEXT, date TEXT)")
            conn.close()  
        
        # Check if matches table exists and create it if it doesn't
        conn = sqlite3.connect(dbFile)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matches'")
        result = c.fetchone()
        conn.close()
        if result is None:
            conn = sqlite3.connect(dbFile)
            c = conn.cursor()
            c.execute("CREATE TABLE matches (id INTEGER PRIMARY KEY, wrestler1 TEXT, wrestler2 TEXT, winner TEXT, loser TEXT, date TEXT, wrestler1_health INTEGER, wrestler2_health INTEGER)")
            conn.commit()
            conn.close()
    
    def get_wrestler_id(self, username):
        conn = sqlite3.connect(dbFile)
        c = conn.cursor()
        c.execute("SELECT id FROM wrestlers WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        if result is None:
            return None
        else:
            return result[0]

    def get_wrestler_username(self, discord_id):
        conn = sqlite3.connect(dbFile)
        c = conn.cursor()
        c.execute("SELECT username FROM wrestlers WHERE discord_id = ?", (discord_id,))
        result = c.fetchone()
        conn.close()
        if result is None:
            return None
        else:
            return result[0]
    
    def add_wrestler(self, username, discord_id):
        conn = sqlite3.connect(dbFile)
        c = conn.cursor()
        c.execute("INSERT INTO wrestlers(username, discord_id) VALUES (?, ?)", (username, discord_id))
        conn.commit()
        conn.close()
        return True

    # Match Command
    @commands.command(name="match")
    async def match(self, context, *args):
        """
        Main wrestling command
        .match <wrestler1> <wrestler2>
        """
        # If no arguements, return the match status in an embed
        if len(args) == 0:
            conn = sqlite3.connect(dbFile)
            c = conn.cursor()
            c.execute("SELECT * FROM matches")
            result = c.fetchall()
            conn.close()
            if result is None:
                await context.send("No matches have been recorded yet.")
            else:
                embed = discord.Embed(title="Wrestling Matches", description="", color=0x00ff00)
                for match in result:
                    embed.add_field(name=f"{match[1]} vs {match[2]}", value=f"Winner: {match[3]}\nLoser: {match[4]}\nDate: {match[5]}", inline=False)
                await context.send(embed=embed)
            return
        # Set an object for the match to be stored in 
        match = {}
        # Get the wrestlers
        wrestler1 = args[0]
        wrestler2 = args[1]
        # Get the ids
        wrestler1_id = self.get_wrestler_id(wrestler1)
        wrestler2_id = self.get_wrestler_id(wrestler2)
        # Check if wrestlers exist
        if wrestler1_id is None:
            await context.send(f"{wrestler1} does not exist in the database")
            return
        if wrestler2_id is None:
            await context.send(f"{wrestler2} does not exist in the database")
            return
        # Set the wrestlers
        match["wrestler1"] = wrestler1
        match["wrestler2"] = wrestler2
        # Set the ids
        match["wrestler1_id"] = wrestler1_id
        match["wrestler2_id"] = wrestler2_id
        # Set the health for both wrestlers
        match["wrestler1_health"] = 100
        match["wrestler2_health"] = 100
        # Add the match to the database
        conn = sqlite3.connect(dbFile)
        c = conn.cursor()
        c.execute("INSERT INTO matches(wrestler1, wrestler2, wrestler1_health, wrestler2_health) VALUES (?, ?, ?, ?)", (match["wrestler1"], match["wrestler2"], match["wrestler1_health"], match["wrestler2_health"]))
        conn.commit()
        conn.close()
        # Get the match id from the database and set it to the match object
        match["id"] = c.lastrowid
        # Embed the match stats to be sent to the channel
        embed = discord.Embed(title=f"{match['wrestler1']} vs {match['wrestler2']}", description=f"{match['wrestler1']} has {match['wrestler1_health']}% health and {match['wrestler2']} has {match['wrestler2_health']}% health", color=0x00ff00)
        # Set thumbnail
        embed.set_thumbnail(url="https://thumbs.dreamstime.com/z/classic-vintage-boxing-ring-old-surrounded-ropes-spotlit-middle-isolated-dark-background-49089696.jpg")
        embed.set_footer(text=f"Match ID: {match['id']}")
        # Send the embed to the channel
        await context.send(embed=embed)  

    

    
    # Roster Command
    @commands.command(name="roster")
    async def roster(self, context):
        """
        Show the current roster of wrestlers
        """
        conn = sqlite3.connect(dbFile)
        c = conn.cursor()
        c.execute("SELECT * FROM wrestlers")
        result = c.fetchall()
        conn.close()

        # Save the total rows returned to a variable
        total_rows = len(result)
        if result is None:
            await context.send("No wrestlers in the roster")
            return
        else:  
            # Create a string to hold the list of wrestlers
            list_of_wrestlers = ""
            # Loop through the list of wrestlers
            for i in range(0, total_rows):
                # Add the wrestler to the list
                list_of_wrestlers += f"{result[i][1]}\n"
            # Send the list of wrestlers
            await context.send(list_of_wrestlers)
            return

    # Wrestler Command
    @commands.command(name="wrestle")
    async def wrestle(self, context, *args):
        """
        Make a wrestling account
        """
        # Check if the user is already registered
        if self.get_wrestler_id(context.author.name) is not None:
            await context.send("You are already registered as a wrestler")
            return
        else:
            # Register the user
            self.add_wrestler(context.author.name, context.author.id)
            await context.send("You are now registered as a wrestler")
            return


def setup(bot):
    bot.add_cog(Wrestlebot(bot))

    


