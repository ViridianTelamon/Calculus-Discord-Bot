"""    
    Copyright (C) 2022 ViridianTelamon (Viridian)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from discord.ext import commands
from discord import Member
from time import time
import json
import discord
import os
import random

#Calculus Discord Bot.
#By:  ViridianTelamon.

client = commands.Bot(command_prefix = "!")

token = "Put Discord Bot Token Here."

#On Ready Event.
@client.listen()
async def on_ready():
  print("Bot Ready.")
  #time.sleep(1)
  print("Logged In As:  {0.user}".format(client))

#Function For Getting A Users Information And Level Them Up.
@client.listen()
async def on_member_join(member):
  with open("users.json", "r") as f:
    users = json.load(f)

  await update_data(users, member)

  with open("users.json", "w") as f:
    json.dump(users, f)

#Member's Messages.
member_messages = {}

#Function For The System That Creates And Uses The Leveling System.
@client.listen()
async def on_message(message):
  global member_messages

  if message.author.id not in member_messages:
    member_messages[message.author.id] = 0

  current_time = time()
  last_message_requirement = current_time - 2
  
  if member_messages[message.author.id] <= last_message_requirement:
    with open("users.json", "r") as f:
      users = json.load(f)
  
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)
  
    with open("users.json", "w") as f:
      json.dump(users, f)

      member_messages[message.author.id] = current_time

#The Function For Updating The Leveling Data.
async def update_data(users, user):
  if not str(user.id) in users:
    users[str(user.id)] = {}
    users[str(user.id)]["experience"] = 0
    users[str(user.id)]["level"] = 1

#The Function For Adding Experience To Someone's Level.
async def add_experience(users, user, exprience):
  users[str(user.id)]["experience"] += exprience

#The Function For Leveling People Up.
async def level_up(users, user, channel):
  experience = users[str(user.id)]["experience"]
  level_start = users[str(user.id)]["level"]
  level_end = int(experience ** (1/4))

  if level_start < level_end:
    await channel.send(f"{user.mention} Has Leveled Up!  They Have Leveled Up To Level {level_end}!")
    users[str(user.id)]["level"] = level_end

#The Function For Checking Your Current Level.
@client.command(name="level")
async def get_level(ctx, user: Member):
  with open("users.json") as f:   
    json_information = json.load(f)
    level_information = json_information.get(str(user.id))
    if not level_information:
      await ctx.send(f"{user.mention} Is Level 0.")
    else:
      await ctx.send(f"{user.mention} Is Level {level_information.get('level')}.")

client.run(token)
