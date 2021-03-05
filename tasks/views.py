from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .tasks import c_get_tweets, celery_task


@require_http_methods(["POST"])
@login_required(login_url='/login', redirect_field_name='')
def scrape_tweets(request):
    tweet_ids_to_scrape = request.POST.get('tweet_ids')

    result = c_get_tweets.delay(uid=request.user.id, tweet_ids=tweet_ids_to_scrape)

    messages.add_message(request, messages.INFO, "Importing tweets by tweet IDs")

    return redirect('home')


def celery_view(request):
    for counter in range(2):
        celery_task.delay(counter)
    return HttpResponse("FINISH PAGE LOAD")
