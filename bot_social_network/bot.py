import requests
import random
import string
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

NUMBER_OF_USERS = int(config['Settings']['NUMBER_OF_USERS'])
MAX_POSTS_PER_USER = int(config['Settings']['MAX_POSTS_PER_USER'])
MAX_LIKES_PER_USER = int(config['Settings']['MAX_LIKES_PER_USER'])
ALPHABET = tuple(string.ascii_lowercase)
DIGITS = tuple(string.digits)

SIGN_UP_URL = 'http://127.0.0.1:8000/sign_up/'
POSTS_URL = 'http://127.0.0.1:8000/posts/'
POST_LIKE_URL = 'http://127.0.0.1:8000/posts/{}/like/'


users_list = []
for i in range(NUMBER_OF_USERS):
    user_params = {
        'posts_created': [],
    }

    username = ''.join(random.choices(ALPHABET, k=5))
    password = ''.join(random.choices(DIGITS, k=5))

    request = requests.post(
        SIGN_UP_URL,
        data={
            'username': username,
            'password': password,
        },
    )

    data = request.json()
    user_params['user_id'] = data.get('id')
    user_params['username'] = data.get('username')
    token = data.get('token')
    if token is not None:
        token = token.get('access')
        user_params['headers'] = {
            'Authorization': f'Bearer {token}',
        }

    users_list.append(user_params)

for user_params in users_list:
    count = 0
    while count < MAX_POSTS_PER_USER:
        text = ''.join(random.choices(ALPHABET + DIGITS, k=50))
        request = requests.post(
            POSTS_URL,
            data={
                'text': text,
                'owner': user_params.get('user_id'),
            },
            headers=user_params.get('headers'),
        )
        data = request.json()
        user_params['posts_created'].append(data.get('id'))
        count += 1

for user_params in users_list:
    request = requests.get(
        POSTS_URL,
        headers=user_params.get('headers'),
    )
    posts_ids = [post.get('id') for post in request.json()]
    for post_id in random.choices(posts_ids, k=MAX_LIKES_PER_USER):
        request = requests.get(
            POST_LIKE_URL.format(post_id),
            headers=user_params.get('headers'),
        )
