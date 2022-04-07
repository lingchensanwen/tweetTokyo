import tweepy
#assign the values accordingly 
API_KEY = "9rS27sic1cLETydC7TgmNmci4"
API_SECRET_KEY = "1dUr02sHsEqLdH269PJz1hrk4RxxP32PptkKYB4bvdCJNDDdnT"
ACCESS_TOKEN = "1495507437352333323-YDCrJ0JSe8kDgked3hWmh4tATKiZBm"
ACCESS_TOKEN_SECRET = "J4WBlVmGYjeRg08LaTP1XbB6aPUfWYpAz6LK49pBTegbd"

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)

# set access to user's access key and access secret  
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# calling the api
api = tweepy.API(auth, wait_on_rate_limit=True)

import csv
# Reading IDs from  file
with open('tweet-ids-tokyo.csv', 'r') as tweets_id_train:
    tweets = csv.DictReader(tweets_id_train)


    # preparing writing results on a CSV file
    with open('tweets_message_tokyo.csv', 'w', newline='') as savefile:
        fieldnames = ['id', 'time', 'text', 'city_name', 'coordinates', 'place']
        writer = csv.DictWriter(savefile, fieldnames)
        # writer.writerow(["id", "text", "place"])
        writer.writeheader()
        count = 0
        i = 0
        tweets_id_list = []
        tweets_message_list = []
        
        # looping each tweet id
        for tweet in tweets:
            count = count + 1
            # convert string id to int
            tweets_id_list.append(int(tweet['tweet_id']))
            # grouping 100 ids each time
            if count == 100:
                # calling twitter for getting results for 100 given ids
                twt = api.lookup_statuses(tweets_id_list)
                tweets_message_list.insert(i, twt)
                count = 0
                tweets_id_list.clear()
                i = i + 1
                print(i)

             # looping result list by response objectes
        for ii in range(i):
            for j in range(len(tweets_message_list[ii])):
                # checking if index existe
                if tweets_message_list[ii][j]:
                    tweet_id = tweets_message_list[ii][j].id
                    time = tweets_message_list[ii][j].created_at
                    tweet_text = tweets_message_list[ii][j].text.encode("utf-8")
                    tweet_place = tweets_message_list[ii][j].place
                    if tweet_place is None or tweet_place.country_code != 'US':
                        continue
                    if tweet_place.bounding_box is None or tweet_place.full_name is None:
                        continue
                    city_name = tweet_place.full_name
                    coordinates = tweet_place.bounding_box.coordinates
                    # getting text of tweets from each object and write on the CSV file
                    writer.writerow({'id': str(tweet_id), 'time': time,'text': str(tweet_text), 'city_name': city_name, 'coordinates': coordinates, 'place': tweet_place})
