import requests
import pickle

game_number = 4987803371569152
game_API_key = "xBTVIL"
round_tick_length = 1

root = "https://np.ironhelmet.com/api"
params = {"game_number" : game_number,
                 "code" : game_API_key,
          "api_version" : "0.1"}
payload = requests.post(root, params).json()


# Tick = Hour in game time

filename = 'pickled_tick'

def pickle_last_tick(current_tick):
    outfile = open(filename, 'wb')
    pickle.dump(current_tick, outfile)
    outfile.close()


def unpickle_last_tick():
    infile = open(filename, 'rb')
    unpickled_tick = pickle.load(infile)
    infile.close()
    return unpickled_tick

def check_pickle_file_is_not_empty():
    try:
        return unpickle_last_tick()
    except EOFError:
        return 0



last_tick = check_pickle_file_is_not_empty()
# print("Last Tick: ", last_tick)
current_tick = payload['scanning_data']['tick']
# print("Current Tick: ", current_tick)

if current_tick > last_tick:
    pickle_last_tick(current_tick)
    print('New turn!')
    print('We are on tick ' + str(last_tick))
else:
    print('Still waiting...')
