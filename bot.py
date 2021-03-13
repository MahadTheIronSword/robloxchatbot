import requests
import time

url = 'https://chat.roblox.com/v2/send-message'
getUrl = 'https://chat.roblox.com/v2/get-user-conversations?pageNumber=1&pageSize=250'
loginUrl = 'https://auth.roblox.com/v2/logout'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'

cookie = input('.ROBLOSECURITY: ')

body = 'hi'


def token():
    request = requests.post(loginUrl, headers={
        'User-Agent': userAgent
    }, cookies={
        '.ROBLOSECURITY': cookie
    })
    return request.headers.get('x-csrf-token')


xsrf = token()


def getConversations():
    getRequest = requests.get(getUrl, headers={
        'User-Agent': userAgent
    }, cookies={
        '.ROBLOSECURITY': cookie
    })
    print(getRequest.json())
    return getRequest


def send(loop):
    global xsrf
    for conversation in loop:
        if conversation.get('id'):
            pmRequest = requests.post(url, headers={
                'User-Agent': userAgent,
                'X-CSRF-TOKEN': xsrf
            }, cookies={
                '.ROBLOSECURITY': cookie
            }, data={
                'message': body,
                'conversationId': conversation.get('id'),
            })
            print(pmRequest.json())
            if 'TooManyRequests' in str(pmRequest.json()):
                print('TooManyRequests - Waiting 150')
                time.sleep(150)
            elif str(pmRequest) == '<Response [403]>':
                xsrf = token()


conversationJson = getConversations().json()
send(conversationJson)
