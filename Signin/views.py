import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import ResetPassword
import resetpassword
import http.client
import Signin.getlogs as getlogs

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def index(request):
    form = ResetPassword()
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
            "form": form
        },
    )

# @api_view(['POST'])
def dummy(request):
    if request.method == 'POST':
        print('post')
        form = ResetPassword(data=request.POST)
        if form.is_valid():
            print('valid')
            
            # take data
            data = form.cleaned_data
            password = data["password"]
            # reset password with api
            reset_password(password)
            resetpassword.run()

            print(type(request))
            return render(
                request,
                "index.html",
                {
                    "session": request.session.get("user"),
                    "form": form,
                    "data": data["password"],
                    "data1": type(request)
                }
            )
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        print('post')
        form = ResetPassword(data=request.POST)
        if form.is_valid():
            print('valid')
            
            # take data
            data = form.cleaned_data
            password = data["password"]
            # reset password with api
            conn = http.client.HTTPSConnection("dev-onwaezps.jp.auth0.com")

            payload = "{\"password\": \"" + password + "\",\"connection\": \"Username-Password-Authentication\"}"

            headers = {
                'content-type': "application/json",
                'authorization': "Bearer " + settings.AUTH0_ACCESS_TOKEN
                }

            conn.request("PATCH", "/api/v2/users/auth0%7C62fd8c733d70b8389b7e598d", payload, headers)

            res = conn.getresponse()
            data = res.read()

            print(data.decode("utf-8"))
            return render(
                request,
                "reset.html",
                {
                    "session": request.session.get("user"),
                    "form": form,
                    "data": "success"
                }
            )
    return Response(status=status.HTTP_400_BAD_REQUEST)

def get_logs(request):
    user = request.session.get("user")
    print('user')
    print(user)
    print(type(user))
    print(user['userinfo']['email'])
    res = getlogs.get_logs(settings.AUTH0_ACCESS_TOKEN, user['userinfo']['email'])
    print(type(res))
    res = res.decode("UTF-8")
    print('after')
    print(type(res))
    res = json.loads(res)
    print(type(res))
    return render(
        request,
        "logs.html",
        {
            "session": user,
            "data": res
        }
    )