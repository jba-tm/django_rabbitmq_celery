from django.db import models


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    tweet_id = models.BigIntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)
    exception = models.CharField(max_length=600, blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return "[{0}] Twitter ID: {1}".format(self.id, self.tweet_id)
