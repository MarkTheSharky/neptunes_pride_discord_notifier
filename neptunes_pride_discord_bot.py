import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests
import pickle
from datetime import datetime
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

game_number = 4987803371569152
game_API_key = "xBTVIL"
filename = 'pickled_tick'

def call_neptunes_api():
    root = "https://np.ironhelmet.com/api"
    params = {"game_number" : game_number,
                     "code" : game_API_key,
              "api_version" : "0.1"}
    payload = requests.post(root, params).json()
    return payload

def pickle_last_tick(current_tick):
    print("pickle_last_tick called")
    outfile = open(filename, 'wb')
    pickle.dump(current_tick, outfile)
    outfile.close()


def unpickle_last_tick():
    print('unpickle_last_tick called')
    infile = open(filename, 'rb')
    unpickled_tick = pickle.load(infile)
    infile.close()
    return unpickled_tick

def check_pickle_file_is_not_empty():
    print('check_pickle_file_is_not_empty called')
    try:
        return unpickle_last_tick()
    except EOFError:
        return 0



payload = {}
last_tick = 0
current_tick = 0

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} is connected to the server.')
    post_when_new_turn.start()


@tasks.loop(minutes=5)
async def post_when_new_turn():
    global payload, last_tick, current_tick
    payload = call_neptunes_api()
    last_tick = check_pickle_file_is_not_empty()
    time.sleep(5)
    # print("Payload tick: " + str(payload['scanning_data']['tick']))
    current_tick = payload['scanning_data']['tick']
    print("post_when_new_turn has ran at " + str(datetime.now()))
    print('Last tick: ', last_tick)
    print('Current tick: ', current_tick)
    if current_tick > last_tick:
        pickle_last_tick(current_tick)
        channel = client.get_channel(840646529328349184)
        await channel.send('New turn! We are now on tick ' + str(current_tick))
    else:
        pass


client.run(TOKEN)