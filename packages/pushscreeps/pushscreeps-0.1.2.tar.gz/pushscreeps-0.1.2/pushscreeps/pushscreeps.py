#!/usr/bin/env python3

__version__ = "0.1.2"

import sys
import os
import requests
import argparse


def parse_args():
    # defaults
    branch = 'default'
    server = 'screeps.com'
    ptr = False
    insecure = False
    get = False
    path = '.'

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str,
                        help="username (if not from config)")
    parser.add_argument("-p", "--password", type=str,
                        help="password (if not from config)")
    parser.add_argument("-b", "--branch", type=str, default=branch,
                        help="choose branch to push towards")
    parser.add_argument("-s", "--server", type=str, default=server,
                        help="choose your server")
    parser.add_argument("-t", "--testrealm", type=bool, default=ptr,
                        help="use public test realm (PTR)")
    parser.add_argument("-i", "--insecure", type=bool, default=insecure,
                        help="is the server using https?")
    parser.add_argument("-g", "--get", type=bool, default=get,
                        help="get code instead of pushing?")
    parser.add_argument("path", type=str, default=path,
                        help="where to find .js-files")
    return parser.parse_args()


def gen_url(args):
    url = '/api/'
    if args.testrealm:
        url = '/ptr' + url
    url = args.server + url
    if args.insecure:
        url = 'http://' + url
    else:
        url = 'https://' + url
    return url


def get_token(url, user, password):
    url = url + 'auth/signin'
#    url = "http://odin.aiur.no:21025/auth/signin"
    data = {'email': user, 'password': password}
    r = requests.post(url, json=data)
    if not r.status_code == 200:
        raise RuntimeError('token failed: ' + r.text)
    return r.json()['token']


def do_req(mode, url, token, **args):
    headers = {'X-Token': token, 'X-Username': token}
    if mode == 'GET':
        return requests.get(url, headers=headers, **args)
    elif mode == 'POST':
        return requests.post(url, headers=headers, **args)
    else:
        raise NotImplemented('mode not GET or POST')


def get_code(url, token):
    url = url + 'user/code'
    r = do_req('GET', url, token)
    print(r.json())


def push_code(url, token, data):
    url = url + 'user/code'
    r = do_req('POST', url, token, json=data)
    print(r.json())


def get_data(path, branch):
    data = {'branch': branch}
    files = {}
    for file in os.listdir(path):
        if file.endswith('.js'):
            fileshort = file.replace(".js", "")
            files[fileshort] = open(os.path.join(path, file), 'r').read()
    data['modules'] = files
    return data


def main():
    token = None
    args = parse_args()

    # FIXME: read config here sometime
    if not args.user:
        raise ValueError('missing username')
    if not args.password:
        raise ValueError('missing password')
    user = args.user
    password = args.password

    url = gen_url(args)

    if not token:
        token = get_token(url, user, password)
    if not token:
        raise RuntimeError('no token')

    if args.get:
        get_code(url, token)
        sys.exit()

    data = get_data(args.path, args.branch)
    push_code(url, token, data)

    sys.exit()


if __name__ == '__main__':
    main()
