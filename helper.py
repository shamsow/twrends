import os
import twint
import requests

# c = twint.Config()
# c.Search = "men"
# c.Min_likes = 30000
# c.Limit = 20
# c.Output = "men.json"
# c.Year = '2020'
# c.Store_json = True
# twint.run.Search(c)

def main():
    print(get_tweets("anime"))


def get_tweets(query):
    print("Fetching Tweets")
    c = twint.Config()
    c.Search = query
    # Increments of 20
    c.Limit = 20
    c.Store_object = True
    # c.Min_likes = 100
    c.Popular_tweets = True
    # c.Year = '2020'
    c.Lang = "en"
    c.Hide_output = True

    twint.run.Search(c)
    print("Found Tweets")
    return twint.output.tweets_list[::-1]


def create_embed(url):
    payload = {'url': url}
    page = requests.get("https://publish.twitter.com/oembed", payload)
    return page.json()["html"]


if __name__ == "__main__":
    main()