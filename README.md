# Twitter Giveaways Bot

A bot that will constantly look for new *giveaways* and *contests* on **Twitter**; and enter to *all* of them!
It will do whatever it's needed, either retweeting or liking something, or even following and DMing someone :D

Limits are pretty high; the bot can enter to more than **1000 giveaways per day**, so it's likely that you'll win several giveaways :)

## What's new? 😃
* Added ban keyword list (ignore tweets that contain certain keywords)
* Don't retweet tweets that have a few numbers of retweets (to avoid retweeting fake giveaways)
* Don't retweet old tweets (you can set the bot to ignore tweets that're older than 30 days for example)


## Getting Started

These instructions will get your bot started in minutes.

### Prerequisites

Things you need to have installed in order to be able to run the script.

```
Python 3.5
python-twitter
```

### Installing

First of all, if you don't already have Python in your system, [download](https://www.python.org/downloads/) and install it now. Once that's done, for the 
script to be able to work with Twitter you'll need to install its API

```
pip install python-twitter
```
You should also download both scripts: ``main.py`` and ``config.py``. Preferably, put them in the same folder.

Once there, open the ``config.py`` file with a text editor; don't run it!
This file has all the variables the main script will use. Give each one of them the values you want, or just leave them by default.

However, you do need to change the first variable: ``twitter_credentials``. As it contains all the credentials related to the Twitter API; 
they can't stay blank (what's by default) if you want the bot to connect to Twitter.

#### Twitter App
This is meant to be a short guide on how to get the twitter credentials your bot will need. Here I assume you already have Twitter account, if you don't please make one now. 
##### Steps: 
* Enter to [Twitter Apps](https://apps.twitter.com/) and click the `Create New App` button
* Fill out all details and create the app
* Enter to the ``Keys and Access Token`` section and create a new access token. 
* Now copy ``Consumer Key``, ``Consumer Secret``, ``Access Token``, ``Access Token Secret`` and paste them into their right place inside
the ``config.py``'s ``twitter_credentials`` variable.

If you've followed the steps correctly, now to start the bot you just need to run the ``main.py`` script. **Experiment with the variables at your own risk.**

## How it works
As soon as the script starts, the bot authenticates to Twitter and searches for tweets with the tags given in the ``search_tags`` variable. It stores them in a list so then in can 
iterate through each one of them, and checks if they contain any ``retweet_tags``; it would be very weird not having to retweet anything, that usually means you have to open a link
to enter, thus it isn't a Twitter giveaway anymore and we skip the whole tweet.


If it does contain a ``retweet_tag``, the bot retweets it and proceeds to check if it has any
* ``message_tag``
* ``follow_tag``
* ``like_tag``

 
If the bot finds them in the tweet's text, it'll do its right action. You can find more info in ``config.py``. 

Once the bot is done with analyzing tweet and entering to the giveaway, it will sleep for the seconds defined in the ``retweet_rate`` variable; this is 
what will avoid the bot getting banned, or what will get the bot banned. 
After the bot has checked all tweets in the list, the script sleeps for the value defined in ``search_rate`` and the loop stars again. 

To check the limits Twitter sets please refer to [Twitter's Rate Limits](https://dev.twitter.com/rest/public/rate-limits) and [Twitter’s Account Limits](https://support.twitter.com/articles/344781).

*The bot prints everything into the console with colors and all, so it's easy to see what's going on. And all files are well commented*

## Disclaimer

This is entirely for educational purpose. Use at your own risk and responsibility, there's a possibility that your Twitter account gets banned. I hold no liability for what you use the bot for or the consequences.

## Authors

* **Diego Estevez** - Please check out my [blog](https://www.diegoestevez.me), you'll love my other projects!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Troubleshooting

Rate limit exceeded => All info [here](https://github.com/imdiegoestevez/Twitter-Giveaways-Bot/issues/1)

## Acknowledgments

* Thank you [Hunter Scott](http://www.hscott.net/twitter-contest-winning-as-a-service/) for your inspiration!

