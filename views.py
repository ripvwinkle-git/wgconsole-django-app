'''
Wgconsole views
'''
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib import auth
from django.urls import reverse
from .models import Peer

def index(request):
    '''
    Wgconsole index page view
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('wgconsole:login'))
    user = request.user
    peers = Peer.objects.filter(user=user)
    context = {'user':user, 'peers':peers}
    template = loader.get_template('wgconsole/index.html')
    return HttpResponse(template.render(context, request))

def login(request):
    '''
    Wgconsole login page view
    '''
    context = {'auth_failure':False}
    template = loader.get_template('wgconsole/login.html')
    if ('username' and 'password') in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('wgconsole:index'))
        context = {'auth_failure':True}
        return HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))

def logout(request):
    '''
    Wgconsole logout view
    '''
    auth.logout(request)
    return HttpResponseRedirect(reverse('wgconsole:login'))

def ajax(request):
    '''
    Ajax view
    '''
    if 'keygen' in request.headers:
        key = Peer.genkey()
        return JsonResponse({'genkey': key})
    if 'pubkey' in request.headers:
        key = Peer.pubkey(request.headers['pubkey'])
        return JsonResponse({'pubkey': key})
    return None
