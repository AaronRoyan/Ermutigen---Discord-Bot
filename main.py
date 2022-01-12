import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ['sad', 'depressed','sucks', ':(','miserable', 'unhappy','depressing']

startup_encouragment = [
  'hey, cheer up', 'Hang in there', "My Mother didn't pack SMILIES",'Listen to some music',''
]

if "responding" not in db.keys():
  db["responding"] = True

my_secret = os.environ['TOKEN']
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def updateEncouragement(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len (encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

#how you register
@client.event
async def on_ready():
  print("We Have Logged in as {0.user}  ".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Greetings')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$joke'):
    pass

  if message.content.startswith('thanks'):
    await message.channel.send("You're Welcome")

  options = startup_encouragment

  if "encouragements" in db.keys():
    options += db["encouragements"]

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    updateEncouragement(encouraging_message)
    await message.channel.send("Word added to my Dictionary")
  if db["responding"]: 
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)  

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]    
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("Can't get enough of me, can you? ;)")
    if value.lower() == "off":
      db["responding"] = False
      await message.channel.send("Thank you for shutting me OFF >:(")

keep_alive()
client.run(my_secret)  # or client.run(*token) on replit.com