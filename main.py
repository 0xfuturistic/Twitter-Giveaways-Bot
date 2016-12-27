import config
import twitter
import time
import random


print("\033[95mMake sure no config variables are in blank!\033[0m")
# All variables related to the Twitter API
twitter_api = twitter.Api(consumer_key=config.twitter_credentials["consumer_key"],
                          consumer_secret=config.twitter_credentials["consumer_secret"],
                          access_token_key=config.twitter_credentials["access_token"],
                          access_token_secret=config.twitter_credentials["access_secret"])


def check():
    print("\033[92mStarted Analyzing (" + str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) + ":" + str(
        time.gmtime().tm_sec) + ") \033[0m")
    # Retrieving the last 1000 tweets for each tag and appends them into a list
    searched_tweets = []
    for x in config.search_tags:
        searched_tweets += twitter_api.GetSearch(term=x, count='1000')

    for tweet in searched_tweets:
        if any(x in tweet.text.lower().split() for x in config.retweet_tags):
            # The script only cares about contests that require retweeting. It would be very weird to not have to
            # retweet anything; that usually means that there's a link  you gotta open and then fill up a form.
            # This clause checks if the text contains any retweet_tags
            if tweet.retweeted_status is not None:
                # In case it is a retweet, we switch to the original one
                if any(x in tweet.retweeted_status.text.lower() for x in config.retweet_tags) and tweet.retweeted_status.user.screen_name.lower() not in config.banned_users and not any(x in tweet.user.name.lower() for x in config.banned_name_keywords):
                    tweet = tweet.retweeted_status
                else:
                    continue
            elif tweet.user.screen_name.lower() in config.banned_users or any(x in tweet.user.name.lower() for x in config.banned_name_keywords):
                # If it's the original one, we check if the author is banned
                print("\033[93mAvoided user with ID: " + tweet.user.screen_name + " & Name: " + tweet.user.name + "\033[0m")
                continue

            try:
                # RETWEET
                # This is ran under a try clause because there's always an error when trying to retweet something
                # already retweeted. So if that's the case, the except is called and we skip this tweet
                # If the tweet wasn't retweeted before, we retweet it and check for other stuff
                twitter_api.PostRetweet(status_id=tweet.id)
                print("\033[94mRetweeted " + str(tweet.id))

                # MESSAGE
                if any(x in tweet.text.lower() for x in config.message_tags):
                    # If the tweet contains any of the message_tags, we send a DM to the author with a random sentence
                    # from the message_text list
                    twitter_api.PostDirectMessage(
                        text=config.message_text[random.randint(0, len(config.message_text) - 1)],
                        screen_name=tweet.user.screen_name)
                    print("DM sent to: " + tweet.user.screen_name)
                    # 1 every 86.4s guarantees we won't pass the 1000 DM per day limit
                    time.sleep(config.msg_rate)

                # FOLLOW
                if any(x in tweet.text.lower() for x in config.follow_tags):
                    # If the tweet contains any follow_tags, it automatically follows all the users mentioned in the
                    # tweet (if there's any) + the author
                    twitter_api.CreateFriendship(screen_name=tweet.user.screen_name)
                    print("Followed: @" + tweet.user.screen_name)
                    time.sleep(config.follow_rate - config.retweet_rate if config.follow_rate > config.retweet_rate else 0)
                    for name in tweet.user_mentions:
                        twitter_api.CreateFriendship(screen_name=name.screen_name)
                        print("Followed: @" + name.screen_name)
                        # 1 follow every 86.4s. 86.4 - 36 = 50.4. The first follow adds 50.4, and the next ones 86.4s
                        time.sleep(config.follow_rate)

                # LIKE
                if any(x in tweet.text.lower() for x in config.like_tags):
                    # If the tweets contains any like_tags, it automatically likes the tweet
                    twitter_api.CreateFavorite(status_id=tweet.id)
                    print("Liked: " + str(tweet.id))
                # Max is 2400 tweets per day in windows of half an hour. Thus, 36s as interval guarantees as we won't
                # pass that amount
                time.sleep(config.retweet_rate)
            except Exception as e:
                # In case the error contains sentences that mean the app is probably banned or the user over daily
                # status update limit, we cancel the function
                if "Application cannot perform write actions" in str(e) or "User is over daily status update limit" in str(e):
                    print('\033[91m' + '\033[1m' + str(e) + '\033[0m')
                    return
            # And continues with the next item
    print("\033[92mFinished Analyzing (" + str(len(searched_tweets)) + " tweets analyzed)")


while True:
    print("\n")
    try:
        check()
    except Exception as e:
        print('\033[91m' + '\033[1m' + str(e) + '\033[0m')
    # This is here in case there were not tweets checked
    time.sleep(2*len(config.search_tags))
