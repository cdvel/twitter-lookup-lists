import tweepy
import os, json


with open(os.path.join(os.getcwd(),"data/credentials_rw.json")) as data_file:    
    key = json.load(data_file)

with open(os.path.join(os.getcwd(),"data/names_plus.json")) as data_file:    
    records = json.load(data_file)

def get_list_members(api, owner, slug):
	members = []
	# need a cursor, otherwise just 20
	for page in tweepy.Cursor(api.list_members, owner, slug).items():
		members.append(page)
	return [ m.screen_name.encode('utf-8') for m in members ]

def twitter_setup():
    auth = tweepy.OAuthHandler(key["API_KEY"], key["API_SECRET"])
    auth.set_access_token(key["ACCESS_TOKEN"], key["ACCESS_TOKEN_SECRET"])    
    return tweepy.API(auth)

api = twitter_setup()
owner = ''
list_slug = ''

# Add people from a json file to existing list (might hit API throttler ~= 1000)
# https://twittercommunity.com/t/cant-add-members-to-a-list-code-104/25824/8

print "rate limit %s"%(api.rate_limit_status()['resources']['lists']['/lists/members'])

prev_list = get_list_members(api, owner, list_slug)
x_list = api.get_list(owner_screen_name=owner, slug=list_slug)

print "rate limit %s"%(api.rate_limit_status()['resources']['lists']['/lists/members'])

for record in records:
	for slug in record['match']:
		handle = slug.encode('utf-8')
		# usr = api.get_user(screen_name='@'+handle)
		if handle not in prev_list:
			try:
				api.add_list_member(screen_name='@'+handle, list_id=x_list.id)
				print '[ADD]\t %s'%(handle)
			except Exception as e:
				print '[FORBID]\t %s'%(handle)
				raise
		else:
			print '[SKIP]\t %s'%(handle)
print '\nend *'
