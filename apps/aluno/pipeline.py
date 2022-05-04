# -*- coding: utf-8 -*-
# Autor: christian
from sorl.thumbnail import get_thumbnail
from apps.aluno.models import Aluno
from libs.util.oauth import get_facebook_graph_fields


def create_aluno(backend, user, social_user, is_new=False, new_association=False, *args, **kwargs):
    """
        Part of SOCIAL_AUTH_PIPELINE. Works with django-social-auth==0.7.21 or newer
        @backend - social_auth.backends.twitter.TwitterBackend (or other) object
        @user - User (if is_new) or django.utils.functional.SimpleLazyObject (if new_association)
        @social_user - UserSocialAuth object
    """
    if is_new or new_association:
        data = get_facebook_graph_fields(social_user.uid, social_user.extra_data.get('access_token'))
        url_get_img = "http://graph.facebook.com/{0}/picture?type=large".format(social_user.uid)
        img = get_thumbnail(url_get_img, "200x200", crop='center', quality=95).url
        email = data.get('email')
        nome = data.get('name')
        aluno = Aluno(
            usuario=social_user.user, nome=nome, email=email, foto=img.replace('/media/', '')
        )
        aluno.save()


    # if is_new:
    #     send_welcome_email.delay(user.email, user.first_name)
    #
    # if backend.name == 'twitter':
    #     if is_new or new_association:
    #         access_token = social_user.extra_data['access_token']
    #         # parsed_tokens = parse_qs(access_token)
    #         oauth_token = parsed_tokens['oauth_token'][0]
    #         oauth_secret = parsed_tokens['oauth_token_secret'][0]
    #         tweet_on_join.delay(oauth_token, oauth_secret)

    return None    # profile = UserProfile.objects.get_or_create(user = user)[0]
    # profile.photo = img_url
    # profile.save()