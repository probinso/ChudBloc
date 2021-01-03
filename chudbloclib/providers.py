import urllib.parse
import yaml
import json

from starlette.config import Config

from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI

app = FastAPI()

def get_oauth(provider='twitter'):
    with open('config.yml') as fd:
        settings = yaml.load(fd)['provider'][provider]

    config = Config(environ=settings['consumer'])
    oauth = OAuth(config)

    oauth.register(
        name=provider,
        **settings['register']
    )
    return oauth

app.add_middleware(SessionMiddleware, secret_key="!secret")

oauth = get_oauth(provider='twitter')


@app.route('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.twitter.authorize_redirect(request, redirect_uri)


@app.route('/callback')
async def auth(request: Request):
    token = await oauth.twitter.authorize_access_token(request)
    url = 'account/verify_credentials.json'
    resp = await oauth.twitter.get(
        url, params={'skip_status': True}, token=token)
    print(resp)
    user = resp.json()
    print(user)
    request.session['user'] = dict(token)
    return RedirectResponse(url='/')


@app.route('/logout')
async def logout(request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

"""
@app.route('/login')
async def auth(request: Request):
    # Step 1: Get a request token. This is a temporary token that is used for 
    # having the user authorize an access token and to sign the request to obtain 
    # said access token.

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    print("Request Token:")
    print("    - oauth_token        = {}".format(request_token['oauth_token']))
    print("    - oauth_token_secret = {}".format(request_token['oauth_token_secret']))

    # Step 2: Redirect to the provider. Since this is a CLI script we do not 
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print("Go to the following link in your browser:")
    print("{0}?oauth_token={1}".format(authorize_url, request_token['oauth_token']))


@app.route('/callback')
async def callback(request: Request):
    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    oauth_verifier = input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the 
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this 
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'],
                        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    print("Access Token:")
    print("    - oauth_token        = {}".format(access_token['oauth_token']))
    print("    - oauth_token_secret = {}".format(access_token['oauth_token_secret']))

    print("You may now access protected resources using the access tokens above.")
"""


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
