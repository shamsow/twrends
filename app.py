import os
import json
from flask import Flask, render_template, request, url_for, redirect, jsonify
from helper import create_embed, get_tweets
from api import TwitterAPI

app = Flask(__name__)
# Initialise the API class to get trending data
twitter = TwitterAPI()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_locations(directory="locations", filename="locations-small.json") -> dict:
    """Read a location JSON file and return the location data"""
    with open(os.path.join(directory, filename), 'r') as f:
        data = json.load(f)
    woeid = {}
    for country in data:
        woeid[country["countryCode"]] = {"id": country["woeid"], "name": country["name"]}

    return woeid


def in_thousands(n) -> str:
    """Convert a large number in to thousands"""
    try:
        n = int(n) / 1000
        return f"{n:.2f}K"
    except:
        return '-'



@app.route('/')
def index():
    shortlist_locations = get_locations()
    all_locations = get_locations(filename="locations.json")

    return render_template("home.html", locations=shortlist_locations, all_locations=all_locations)


@app.route('/ajax/trends')
def trends():
    woeid = request.args.get('woeid', None)
    # print(woeid)
    if woeid is not None:
        trends = twitter.get_trending("trends", id=woeid)
        titles = [(trend["name"], in_thousands(trend["tweet_volume"]), trend["url"]) for trend in trends]
        # print(titles)
        return jsonify(result=titles)
    else:
        return "Unknown location"


@app.route('/ajax/tweets')
def tweets():
    
    q = request.args.get('q', None)
    if q is not None:
        print("Searching twitter")
        tweets = get_tweets(q)
        print(len(tweets))
        urls = [tw.link for tw in tweets[:8]]
        print("Creating embed links")
        links = [create_embed(url) for url in urls]
    
        # print(q, links[-1])
        return jsonify(result=links)
    else:
        return "NO RESULTS"

if __name__ == '__main__':
    app.run(debug=True)