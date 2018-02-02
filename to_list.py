import tweepy
import os, json


with open(os.path.join(os.getcwd(),"data/credentials_rw.json")) as data_file:    
    key = json.load(data_file)

with open(os.path.join(os.getcwd(),"data/names_plus.json")) as data_file:    
    records = json.load(data_file)


def twitter_setup():
    #authentication
    auth = tweepy.OAuthHandler(key["API_KEY"], key["API_SECRET"])
    auth.set_access_token(key["ACCESS_TOKEN"], key["ACCESS_TOKEN_SECRET"])    
    return tweepy.API(auth)

api = twitter_setup()

# Add people from a json file to existing list (might hit API throttler ~= 1000)
# https://twittercommunity.com/t/cant-add-members-to-a-list-code-104/25824/8

x_list = api.get_list(owner_screen_name='cdvel', slug='this-is-a-list')

print x_list.id

for record in records:
	for slug in record['match']:
		print 'add %s'%(slug.encode('utf-8'));		
		api.add_list_member(screen_name='@'+slug.encode('utf-8'), list_id=x_list.id)

print 'end *'
