import random

def coin(*args):
    if args == None:
        return random.choice(('heads', 'tails'))
    else:
        return random.choice(args)

if __name__ == '__main__':
    print()