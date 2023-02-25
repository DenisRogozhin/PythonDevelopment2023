import random
import argparse
from urllib import parse, request
import sys
from cowsay import cowsay

def bullscows(guess: str, secret:str) -> (int, int):
    cows = 0
    bulls = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in secret:
            cows += 1        
    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    print('secret', secret)
    guessed = False
    attemts = 0
    while not guessed:
        guess = ask("Введите слово: ", words)
        while len(guess) != len(secret):
            print('Words must have the same len!')
            guess = ask("Введите слово: ", words)
        print("guess", guess)
        attemts += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}",  bulls, cows)
        guessed = guess == secret
    return attemts

def ask(prompt: str, valid: list[str] = None) -> str:
    print(cowsay(prompt))
    word = str(input())
    if not valid:
        return word
    else:
        while word not in valid:
            print(cowsay('word is not valid'))
            #print(prompt, end=' ')
            word = str(input())
        return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay(format_string.format(bulls, cows)))
    return    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'bullscows',
                    description = 'Playing bullscows')
    parser.add_argument('dictionary')
    parser.add_argument('words_len', nargs='?')
    args = parser.parse_args()
    print(args.dictionary)
    print(args.words_len)
    words = []
    if parse.urlparse(args.dictionary).scheme:
        for line in request.urlopen(args.dictionary):
            words.append(line.decode("utf-8")[:-1])
    else:
        try:
            with open(args.dictionary, 'r') as f:
                words = f.read().split()
        except FileNotFoundError:
            print("Dictionary must be URL or filename")
            sys.exit(1)
                
    
    if args.words_len:
        length = args.words_len
    else:
        length = 5
    words = [word for word in words if len(word) == length]
    print(len(words))
    print(gameplay(ask, inform, words = words))
    