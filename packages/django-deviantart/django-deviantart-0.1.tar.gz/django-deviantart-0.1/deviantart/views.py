from django.http.response import HttpResponseServerError
from django.shortcuts import redirect, render_to_response, reverse

from .oauth import Deviantart


def callback(request):
    try:
        deviantart = Deviantart(request.session['redirect_uri'])
    except KeyError:
        return auth(request)
    code = request.GET['code']
    state = request.GET['state']
    deviantart.code = code
    deviantart.fetch_token()
    return redirect('/')


def auth(request):
    request.session['redirect_uri'] = request.build_absolute_uri(
        reverse('deviantart-cb')
    )
    deviantart = Deviantart(request.session['redirect_uri'])
    return redirect(deviantart.auth_url)


def endpoint(request, dapath):

    params = request.GET

    deviantart = Deviantart()
    json = deviantart.get(dapath + ('?' + params.urlencode() if params else ''))
    status_code = json.get('error_code', 200)

    if json.get('error_code', 200) >= 400:
        return HttpResponseServerError(status=status_code)

    return render_to_response('deviantart/endpoint.html', json)
