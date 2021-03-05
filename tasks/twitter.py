import json

from django_rabbitmq_celery import settings
from .models import *
from celery.utils.log import get_task_logger
import tweepy

logger = get_task_logger(__name__)


def twitter_api():
    """Authenticate Twitter API and return the object.

    :rtype: tweepy.api
    :return: Authenticated Tweepy API object
    """
    auth = tweepy.OAuthHandler(settings['Twitter_API_key'], settings['Twitter_API_secret_key'])
    auth.set_access_token(settings['Twitter_access_token'], settings['Twitter_access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

    return api


def get_tweets(api, tweet_id, tweet):
    """Use the Twittter API to get Tweet objects.

    :param api: The authenticated Tweepy Twitter API wrapper
    :type api: tweepy.api
    :param tweet_id: Twitter Tweet ID to be scraped
    :type tweet_id: int
    :param tweet: Tweet database object
    :type tweet: django.db.models.Model
    """
    try:
        api_tweet = api.get_status(tweet_id, tweet_mode='extended')

        tweet.active = True
        tweet.tweet_id = api_tweet.id
        tweet.text = api_tweet.full_text
        tweet.save()

    except Exception as e:
        error = json.dumps(e.args[0][0])
        tweet.active = False
        tweet.exception = error
        tweet.save()
