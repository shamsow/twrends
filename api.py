import tweepy
import json
import os
from datetime import datetime


woeid = {"WW": 1, "US": 2442047, "LA":2442047}

with open("auth.json", "r") as f:
    creds = json.load(f)

def check_time(t1, limit=4):
    trends_valid = True
    time1 = datetime.strptime(t1[:-1], "%Y-%m-%dT%H:%M:%S")
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    time2 = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S")
    delta = (time2 - time1).total_seconds() / 3600
    print("Delta:", delta)
    if delta > limit:
        trends_valid = False 
    return trends_valid

def load_data(directory, filename):
    with open(os.path.join(directory, filename), 'r') as f:
        data = json.load(f)
    return data

class TwitterAPI:
    
    consumer_key = creds["API_KEY"]
    consumer_secret = creds["API_SECRET"]

    def __init__(self):
        self.auth = tweepy.AppAuthHandler(self.consumer_key, self.consumer_secret)
        self.api = tweepy.API(self.auth)
    
    def available_locations(self, save=False):
        locations = self.api.trends_available()
        if save:
            # with open("trends/locations.json", "w") as f:
            with open(os.path.join('locations', 'locations-all.json'), 'w') as f:
                json.dump(locations, f)
            return
        return locations


    def get_trending(self, directory, id=1) -> dict:
        data = {}
        filename = f"{id}.json"
        if not os.path.exists(os.path.join(directory, filename)):
            print("Trend uncached, fetching Trend...")
            self.store_trending(id=id)

        # with open(os.path.join(directory, filename), 'r') as f:
        #     data = json.load(f)
        data = load_data(directory, filename)

        last_time = data["as_of"]
        if not check_time(last_time):
            print("Trend outdated, updating...")
            self.store_trending(id=id)
            data = load_data(directory, filename)

        return data["trends"]

    def store_trending(self, id=1, directory="trends"):
        trends = self.api.trends_place(id)[0]
        filename = f"{id}.json"
        with open(os.path.join(directory, filename), 'w') as f:
            json.dump(trends, f)


def main():
    api = TwitterAPI()
    # api.available_locations(save=True)
    # api.store_trending(id=woeid["WW"])
    # print(api.get_trending("trends", id=woeid["WW"]))
    # auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

# api = tweepy.API(auth)
# for tweet in tweepy.Cursor(api.search, q='anime').items(10):
#     print(tweet.text)

# trends = api.trends_place(1)[0]["trends"]
# trends = api.trends_place(1)[0]

# with open('trends.json', 'w') as f:
#     json.dump(trends, f)

# # print(trends)
# data = {"as_of": }
# for trend in trends:
#     data["trends"][trend["name"]] = trend["tweet_volume"]
    # try:
    #     data[trend["name"]] =  int(trend["tweet_volume"])
    # except:
    #     data[trend["name"]] =  0
    
# print(sorted(data, key=lambda x: data[x]))
if __name__ == "__main__":
    main()