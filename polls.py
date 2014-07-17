import os, sys
from django.conf import settings

ROOT_DIR = os.getcwd()
if not settings.configured:
    settings.configure(DEBUG=True,
                       TEMPLATE_DEBUG=True,
                       DATABASES={},
                       ROOT_URLCONF='polls',
                       INSTALLED_APPS=[],
                       MIDDLEWARE_CLASSES=[],
                       TEMPLATE_DIRS=[os.path.join(ROOT_DIR, 'templates')])

from jsonstore import JSONStore
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


# ========================================
# Custom code
# ========================================

CHOICES = {'krk': 'Cracow',
           'rad': 'Radom',
           'waw': 'Warsaw',
           'wro': 'Wroclove'}


def index(request):
    return render_to_response('index.html', {
        'title': 'Please complete this simple poll!',
        'choices': CHOICES
    })

def cast(request):
    vote = request.POST.get('vote')
    if vote is None:
        return HttpResponseRedirect('/')
    with JSONStore(os.path.join(ROOT_DIR, 'votes.json')) as votes:
        votes[vote] = votes.get(vote, 0) + 1
    return render_to_response('cast.html', {
        'title': 'Thanks for casting your vote!',
        'choices': CHOICES,
        'text': CHOICES[vote]
    })

def results(request):
    votes = JSONStore(os.path.join(ROOT_DIR, 'votes.json'))
    results = {text: 0 for text in CHOICES.values()}
    for id, count in votes.items():
        results[CHOICES[id]] = count
    overall_count = sum(votes.values())
    return render_to_response('results.html', {
        'title': 'Poll results',
        'results': results,
        'overall_count': overall_count
    })


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^cast/$', cast, name='cast'),
    url(r'^results/$', results, name='results'))


# ========================================
# Django application - don't touch
# ========================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
