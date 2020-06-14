import os
import json
from flask import Flask, render_template, request, url_for, redirect, jsonify
from helper import create_embed, get_tweets
from api import TwitterAPI

app = Flask(__name__)

twitter = TwitterAPI()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_locations(directory="locations", filename="locations-small.json"):
    with open(os.path.join(directory, filename), 'r') as f:
        data = json.load(f)
    woeid = {}
    for country in data:
        woeid[country["countryCode"]] = {"id": country["woeid"], "name": country["name"]}

    return woeid

def in_thousands(n):
    try:
        n = int(n) / 1000
        return f"{n:.2f}K"
    except:
        return '-'



@app.route('/')
def index():
    shortlist_locations = get_locations()
    all_locations = get_locations(filename="locations.json")


    # print(get_tweets("day")[0].link)
    # url = 'https://twitter.com/jack/status/20'
    # url = get_tweets("day")[0].link
    # link = create_embed(url)
    return render_template("home.html", locations=shortlist_locations, all_locations=all_locations)


@app.route('/ajax/trends')
def trends():
    woeid = request.args.get('woeid', None)
    # print(woeid)
    trends = twitter.get_trending("trends", id=woeid)
    titles = [(trend["name"], in_thousands(trend["tweet_volume"]), trend["url"]) for trend in trends]
    # print(titles)
    return jsonify(result=titles)


@app.route('/ajax/tweets')
def tweets():
    
    q = request.args.get('q', None)
    if q is not None:
    # trends = twitter.get_trending("trends", "trends.json", id=2352824)
    # titles = [trend["name"] for trend in trends]
        print("searching twitter")
        tweets = get_tweets(q)
        print(len(tweets))
        urls = [tw.link for tw in tweets[:8]]
        # links = [create_embed(url)[:-147] for url in urls]
        print("creating embed links")
        links = [create_embed(url) for url in urls]
    
        print(q, links[-1])
        return jsonify(result=links, trend=q)
    else:
        return "NO RESULTS"

if __name__ == '__main__':
    app.run(debug=True)