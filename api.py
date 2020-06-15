import tweepy
import json
import os
from datetime import datetime

# Some ids saved for testing purposes
woeid = {"WW": 1, "US": 2442047, "LA":2442047}

# Get Twitter API credentials
with open("auth.json", "r") as f:
    creds = json.load(f)

def check_time(t1, limit=4):
    """
    Compare the Trends time with the current time to see if the Trend needs to be updated.
    Returns True if the Trend is still valid, False otherwise.
    """
    trends_valid = True
    # Convert all times to datetime objects
    time1 = datetime.strptime(t1[:-1], "%Y-%m-%dT%H:%M:%S")
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    time2 = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S")
    # Calculate change in time in hours
    delta = (time2 - time1).total_seconds() / 3600
    print("Delta:", delta)
    # Update result
    if delta > limit:
        trends_valid = False 
    return trends_valid

def load_data(directory, filename):
    """
    Load a JSON file into a dictionary
    """
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
        """
        Get all the available locations from Twitter.
        Can be saved as a JSON file if save=True.
        """
        locations = self.api.trends_available()
        if save:
            # with open("trends/locations.json", "w") as f:
            with open(os.path.join('locations', 'locations-all.json'), 'w') as f:
                json.dump(locations, f)
            return
        return locations


    def get_trending(self, directory, id=1) -> dict:
        """
        Get the Trends for a certain id.
        If the Trend doesn't exist, request it from Twitter and save in a JSON file.
        If the Trend has been saved in the last 4 hours then return it from that file,
        otherwise, update it from Twitter.
        """
        data = {}
        filename = f"{id}.json"
        # If the Trend isn't already saved, get it and save it
        if not os.path.exists(os.path.join(directory, filename)):
            print("Trend uncached, fetching Trend...")
            self.store_trending(id=id)

        # Get the trending data from the file
        data = load_data(directory, filename)
        
        last_time = data["as_of"]
        # If the saved Trend is older than 4 hour, then update it
        if not check_time(last_time):
            print("Trend outdated, updating...")
            self.store_trending(id=id)
            data = load_data(directory, filename)

        return data["trends"]


    def store_trending(self, id=1, directory="trends"):
        """
        Get the Trend from Twitter according to id and save it in a JSON file
        """
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


if __name__ == "__main__":
    main()