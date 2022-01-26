from threading import Thread
from collections import deque, Counter
from pandas import read_json
from reddit import analyze_subreddit
import asyncio
import json
import multiprocessing as mp
import asyncio
import datetime
import random
import websockets

manager = mp.Manager()

queue = mp.Queue(maxsize=100)

stock_data = manager.dict()
stock_sentiment = manager.dict()

most_freq_stocks = Counter()

subreddits = read_json('subreddits.json')['subreddits'].to_list()

processes = [mp.Process(target=analyze_subreddit, args=(subreddit, queue, stock_sentiment, stock_data)) for subreddit in subreddits]

for p in processes:
    p.start()

# Reference: https://websockets.readthedocs.io/en/stable/intro.html
async def time(websocket, path):
    while True:
        if not queue.empty():
            stock_info = queue.get()
            stock_name = stock_info.ticker
            most_freq_stocks.update({stock_name : 1})
            most_freq = most_freq_stocks.most_common(5)
            res = [stock_data[stock[0]].__dict__ for stock in most_freq if stock[0] in stock_data]
            now = json.dumps(res)
            try:
                await websocket.send(now)
                await asyncio.sleep(random.random() * 3)
            except ConnectionError: 
                # This is an anti-pattern, though unfortunately the server has a chance of stopping
                # when the client becomes unavailable
                print(f'ERROR :: {ConnectionError}')
                

print(':::: Server up!')
# Source: https://stackoverflow.com/a/58993145
start_server = websockets.serve(time, '0.0.0.0', 80, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
