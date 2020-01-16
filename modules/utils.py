import json

def getToken():
    file_path = 'telegram-token.json'
    try:
        return json.load(open(file_path))['token']
    except:
        print('Miss token file. Write your telegram bot token here')
        token = input()
        for c in [' ', '\n', '"', "'"]:
            token = token.strip(c)
        json.dump({'token': token}, open(file_path, 'w'))
        return getToken()

if __name__ == '__main__':
    print(getToken())