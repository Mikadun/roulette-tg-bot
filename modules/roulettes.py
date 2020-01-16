import secrets

def randomAB(message):
    try:
        args = message.split()
        return secrets.choice(range(int(args[1]), int(args[2])+1))
    except:
        return "Invalid Command"