import json
import base64


def create(response, username):
    session_info = json.dumps({'username': username}).encode('utf-8')
    safe_for_cookie = base64.b64encode(session_info).decode('utf-8')
    response.set_cookie('vulpy_session', safe_for_cookie)
    return response


def load(request):
    session = {}
    cookie = request.cookies.get('vulpy_session')

    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(decoded.decode('utf-8'))
    except Exception as e:
        print(f"Failed to load session: {str(e)}")
        pass
    return session



def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response

