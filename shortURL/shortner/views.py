from django.http import HttpResponse, HttpResponseRedirect
from shortner.models import *
from django.shortcuts import get_object_or_404
from django.utils import simplejson

def index(request):
    past_shorts = ShortURL.objects.filter(owner=request.session.session_key)
    html = '<ul>'
    for s in past_shorts:
        html = html + '<li>' + s.get_shortURL() + ' - ' + ((s.url[:50] + '...')  if len(s.url) > 50 else s.url) + ' - <a href="/delete_code/' + s.code + '">Delete</a></li>'
    html = html + '</ul>'
    return HttpResponse("Max Jaderberg's URL shortner.</br></br>" + html)
    
def code_redirect(request, code):
    s = get_object_or_404(ShortURL, code=code)
    return HttpResponseRedirect(s.url)
    
def get_code(request, url):
    # NOTE: need to use $.URLEnode(url) to encode ?s and &s in url
    # See if a preffered code was given
    try:
        desired_code = request.GET.get('code')
        if desired_code == 'get_code':
            # cheeky fuckers...dont let them have it
            desired_code = ''
    except:
        desired_code = ''
    # Use sessions
    request.session.set_expiry(60*60*24*365)
    # Link owner to session
    owner = request.session.session_key
    # Generate
    s = ShortURL.create(url, desired_code, owner)
    s.save()
    resp = {'url': s.url, 'short_url': s.get_shortURL()}
    return __jsonResponse(request, resp)
    
def delete_code(request, code):
    s = get_object_or_404(ShortURL, code=code)
    s.delete()
    return __jsonResponse(request, {'result': 'success'})
    
def check_code(request, code):
    taken = ShortURL.code_taken(code)
    return __jsonResponse(request, {'taken': taken})
    

def __jsonResponse(request, response_data):
    try:
        func = request.GET.get('callback')
        return HttpResponse(func + '(' + simplejson.dumps(response_data) + ')', mimetype="application/javascript")
    except:
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/javascript")
