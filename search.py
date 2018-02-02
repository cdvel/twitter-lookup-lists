import tweepy
import os, json


with open(os.path.join(os.getcwd(),"data/credentials.json")) as data_file:    
    key = json.load(data_file)

with open(os.path.join(os.getcwd(),"data/names.json")) as data_file:    
    records = json.load(data_file)


def twitter_setup():
    #authentication
    auth = tweepy.OAuthHandler(key["API_KEY"], key["API_SECRET"])
    auth.set_access_token(key["ACCESS_TOKEN"], key["ACCESS_TOKEN_SECRET"])    
    return tweepy.API(auth)

extractor = twitter_setup()
idx = 1;
keywords = ['crypto', 'blockchain', 'bitcoin']

# from list of names find a match on twitter and filter by keywords
# augment file with match and non_match twitter screen_names

for record in records:
	users = extractor.search_users(record['name'])
	match = []
	non_match = []
	print ("%i %s " % (idx, record['name']))
	for user in users:
		if any (x in user.description.lower() for x in keywords):
			match.append(user.screen_name)
		else:
			non_match.append(user.screen_name)
	
	idx += 1
	print "match(%d) %s" % (len(match), ' '.join(match))
	print "non_match(%d) %s" % (len(non_match), ' '.join(non_match))
	record["match"] = match
	record["non_match"] = non_match

	print ("-"*10)


with open(os.path.join(os.getcwd(),"data/names_plus.json"), 'w') as out_file:    
    json.dump(records, out_file)


print 'END *'