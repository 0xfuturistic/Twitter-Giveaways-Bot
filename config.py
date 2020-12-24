"""
   ___                 __  _
  / __\  ___   _ __   / _|(_)  __ _
 / /    / _ \ | '_ \ | |_ | | / _` |
/ /___ | (_) || | | ||  _|| || (_| |
\____/  \___/ |_| |_||_|  |_| \__, |
                              |___/
"""

# Twitter API credentials. If you need any help have a look at README.md
twitter_credentials = {
    "consumer_key": '',
    "consumer_secret": '',
    "access_token": '',
    "access_secret": '',
}
# DON'T WRITE ANYTHING IN CAPS, AS THE BOT AUTOMATICALLY FLATTERS ALL INPUT TEXTS. THUS ANY WORD WITH CAPS WON'T BE RECOGNIZED
# Tags that Twitter will use to look up our tweets. Really important as all the script will be based on them
search_tags = ["giveaway", "contest", "sorteo", "to win"]
# Don't start the bot if friends weren't correctly retrieved
wait_retrieve = False
# Enable this if you want the bot to send a DM in case it detects any message_tags
use_msgs = False

#Ignore tweets that contain any of these words
BadList = ["throat","bone","naked","selfie","photo","onlyfans","nude","+18","femdom","fendom","whatsapp","sex","xxx","daddy","mommy","sugar","vid","#imgxnct","pic","tits" ,"booty" ,"boob", "freenude","cum", "dick" ,"gay" ,"onlyfans.com","hot", "ass", "fuck", "suck", "cock", "lick","pussy" ]

# What words will the bot check in order to retweet a tweet. It's important because if the bot doesnt
# recognize any, it will skip the whole tweet and it wont check if it has to like, msg, or follow
retweet_tags = ["retweet", "retweetea", "retwitea", "rt"]
# What words will trigger to send the author a DM with a random message_text
message_tags = ["message", "dm"]
# What words will the bot check in order to follow the author of the tweet plus all the users mentioned in the text
# (we assume that a retweet tag was recognized)
follow_tags = ["follow", "fl", "sigue", "seguir", "siguenos"]
# What words will the bot look for in order to like a tweet (it also needs to contain a retweet tag)
like_tags = ["like", "fav", "favorite"]
# These are supposed to be random msgs the bot would send if DMing is required
message_text = ["I want to enter to the giveaway!", "Hope to win :D"]
# Add to this list all the users whose contests (actually tweets that contain retweet_tags keywords) the script will
# always skip (this is for the user's username, not name!) (username is the @ one)
# Variables related to avoiding users don't need to have a value
banned_users = []
# Same but but in this case applied to the author's name
banned_name_keywords = ["bot", "spotting", "spot", "spotter"]
# Search_rate means how long it'll have to wait to loop again after checking all tweets
search_rate = 2
# How long to wait to pass to next tweet + follow_rate or dm_rate if it has to follow or dm someone
retweet_rate = 36
# How long to wait after messaging someone. Just the diff between its value and retweet_rate's is added
msg_rate = 30
# How long to wait after following someone. 1st time the diff is added, afterwards the entire rate is added to the sleep
follow_rate = 30
# Enable printing in colors
print_in_color = False

# I still want to add more features! So please have patience :D
