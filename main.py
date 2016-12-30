import config
import twitter
import time
import random


class colors:
    HEADER = '\033[95m' if config.print_in_color else ""
    OKBLUE = '\033[94m' if config.print_in_color else ""
    OKGREEN = '\033[92m' if config.print_in_color else ""
    WARNING = '\033[93m' if config.print_in_color else ""
    FAIL = '\033[91m' if config.print_in_color else ""
    ENDC = '\033[0m' if config.print_in_color else ""
    BOLD = '\033[1m' if config.print_in_color else ""
    UNDERLINE = '\033[4m' if config.print_in_color else ""

print(colors.HEADER + "Make sure no config variables are in blank!")
# All variables related to the Twitter API
twitter_api = twitter.Api(consumer_key=config.twitter_credentials["consumer_key"],
                          consumer_secret=config.twitter_credentials["consumer_secret"],
                          access_token_key=config.twitter_credentials["access_token"],
                          access_token_secret=config.twitter_credentials["access_secret"])
friends = []

while len(friends) is not twitter_api.GetUser(screen_name="only0dallas").friends_count:
    try:
        f = twitter_api.GetFriends(screen_name="only0dallas")
        friends = [x.screen_name for x in f]
        print(colors.OKGREEN + "Friends retrieved successfully!")
    except Exception as e:
        # Friends couldn't be retrieved
        print(colors.FAIL + colors.BOLD + str(e) + colors.ENDC)
        print(colors.FAIL + colors.BOLD + "Couldn't retrieve friends. The bot won't unfollow someone random when we start"
                                            " following someone else. So your account might reach the limit (following 2000"
                                            " users)" + colors.ENDC)
        if config.wait_retrieve is False:
            break
        time.sleep(600)


def check():
    print(colors.OKGREEN + "Started Analyzing (" + str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) + ":" + str(
        time.gmtime().tm_sec) + ")")
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
                if any(x in tweet.retweeted_status.text.lower().split() for x in config.retweet_tags):
                    tweet = tweet.retweeted_status
                else:
                    continue
            if tweet.user.screen_name.lower() in config.banned_users or any(x in tweet.user.name.lower() for x in config.banned_name_keywords):
                # If it's the original one, we check if the author is banned
                print(colors.WARNING + "Avoided user with ID: " + tweet.user.screen_name + " & Name: " + tweet.user.name + colors.ENDC)
                continue

            try:
                # RETWEET
                # This is ran under a try clause because there's always an error when trying to retweet something
                # already retweeted. So if that's the case, the except is called and we skip this tweet
                # If the tweet wasn't retweeted before, we retweet it and check for other stuff
                twitter_api.PostRetweet(status_id=tweet.id)
                print(colors.OKBLUE + "Retweeted " + str(tweet.id))

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
                    destroyFriends = []
                    if tweet.user.screen_name not in friends:
                        twitter_api.CreateFriendship(screen_name=tweet.user.screen_name)
                        print("Followed: @" + tweet.user.screen_name)
                        destroyFriends.append(tweet.user.screen_name)
                        time.sleep(config.follow_rate - config.retweet_rate if config.follow_rate > config.retweet_rate else 0)
                    for name in tweet.user_mentions:
                        if name.screen_name in friends:
                            continue
                        twitter_api.CreateFriendship(screen_name=name.screen_name)
                        print("Followed: @" + name.screen_name)
                        destroyFriends.append(name.screen_name)
                    friends.extend(destroyFriends)
                    # Twitter sets a limit of not following more than 2k people in total (varies depending on followers)
                    # So every time the bot follows a new user, its deletes another one randomly
                    if len(friends) >= 2000:
                        for friend in destroyFriends:
                            x = friends[random.randint(0, len(friends) - 1)]
                            while x is friend:
                                x = friends[random.randint(0, len(friends) - 1)]
                            print("Unfollowed: @" + x)
                            twitter_api.DestroyFriendship(screen_name=x)
                            friends.remove(x)
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
                if "retweeted" not in str(e):
                    print(colors.FAIL + colors.BOLD + str(e) + colors.ENDC)
                    return
            # And continues with the next item
    print(colors.OKGREEN + "Finished Analyzing (" + str(len(searched_tweets)) + " tweets analyzed)")


while True:
    print("\n")
    try:
        check()
    except Exception as e:
        print(colors.FAIL + colors.BOLD + str(e) + colors.ENDC)
    # This is here in case there were not tweets checked
    time.sleep(2*len(config.search_tags))
