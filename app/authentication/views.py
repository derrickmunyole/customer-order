from django.shortcuts import render
from django.urls import reverse
from users.models import User
from .oauth import oauth


def login_view(request):
    redirect_uri = request.build_absolute_uri(reverse('auth_callback'))
    return oauth.google.authorize_redirect(request, redirect_uri)


def validate_user(userinfo):
    email = userinfo.get('email')
    if not email:
        raise ValueError('Email is required')
    return email


def retrieve_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def create_user(email, userinfo):
    """
    Create user entry in the database
    """
    return User.objects.create(
        email=email,
        oidc_id=userinfo.get('sub', '')
    )


def login_create_user_wrapper(userinfo):
    """
    Authenticate existing user or create new user based on OIDC userinfo object
    """
    email = validate_user(userinfo)
    user = retrieve_user_by_email(email)

    if not user:
        user = create_user(email, userinfo)
    return user


def auth_callback(request):
    token = oauth.google.authorize_access_token(request)
    userinfo = oauth.google.parse_id_token(request, token)

    user = login_create_user_wrapper(userinfo)
    request.session['user_id'] = str(user.id)
    request.session['email'] = user.email
    return render(request, 'home.html')
