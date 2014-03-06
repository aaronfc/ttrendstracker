import tweepy
import shelve
# Twitter Authentication import
from config.TwitterAuth import twitter_api_key, twitter_api_secret_key
# Terms under tracking
from config.Terms import terms

# Twitter API instantiation
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
api = tweepy.API(auth)

#Storage initialization
storage = shelve.open('twitter_data.db')

try:
    last_lw_ids = storage['last_tw_ids'];
except Exception:
    last_lw_ids = {}

for term in terms:
    print "Searching for \"{}\"".format(term)
    if term in last_lw_ids.keys():
        last_id = last_lw_ids[term]
    else:
        last_id = None
    tweets = tweepy.Cursor(api.search,
            q=term,
            count=100,
            result_type="recent",
            include_entities=True,
            lang="es",
            locale="es",
            since_id=last_id).items()
    #print len(tweets)
    try:
        tweet = tweets.next()
        print tweet.text.encode('utf-8')
        print tweet.id
        last_lw_ids[term] = tweet.id
    except StopIteration:
        print "No new twits"

storage['last_tw_ids'] = last_lw_ids
storage.close()


