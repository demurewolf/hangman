#!/usr/bin/env python3.8

from asyncio import IncompleteReadError
from random import choice
import sys

class HangManGame():
    _tries = 10
    _word = ""
    _player_guesses = []
    _incorrect_guesses = []
    _STARTER_WORDS = ["bumble", "humble", "tumble", "dawdle", "bauble", "throttle"]
    _game_over = False

    def __init__(self, starting_words=None) -> None:
        if starting_words:
            with open(starting_words, 'r') as wf:
                print(f"Opening provided wordfile {starting_words}")
                words = wf.readlines()
                words = [word.rstrip('\n\r') for word in words]
                self._word = choice(words)
        else:
            self._word = choice(self._STARTER_WORDS)

        print(f"Using {self._word} as game-word!")

    def show_blanks(self):
        b = ""
        for i in range(len(self._word)):
            if self._word[i] in self._player_guesses:
                b += " " + self._word[i] + " "
            else:
                b += " _ "
        print(b)

    def show_letters(self) -> None:
        player_s = ''
        incorrect_s = ''
        avail_s = ''
        avail_s_total = 'abcdefghijklmnopqrstuvwxyz'

        for l in avail_s_total:
            if l in self._incorrect_guesses:
                incorrect_s += l + ','
            elif l in self._player_guesses:
                player_s += l + ','
            else:
                avail_s += l + ','

        avail_s = avail_s.rstrip(',')
        incorrect_s = incorrect_s.rstrip(',')
        player_s = player_s.rstrip(',')

        print(f"Available letters: {avail_s}")
        print(f"You\'ve guessed: {player_s}")
        print(f"You were wrong: {incorrect_s}")

    def check_guess(self, player_guess) -> None:
        for l in player_guess:
            if l not in self._word:
                self._tries -= 1
                self._incorrect_guesses.append(l)
                if self._tries == 0:
                    self._game_over = True
                    return
            else:
                self._player_guesses.append(l)
        
        #print(f"{self._player_guesses}")
        found = True
        for l in self._word:
            if l not in self._player_guesses:
                found = False
        
        self._game_over = found

    def run(self) -> None:
        print("##### Welcome to HANGMAN! #####")

        while(self._tries > 0 and not self._game_over):
            
            self.show_blanks()
            print(f"You have {self._tries} tries remaining.")
            self.show_letters()

            player_input = input("What's your guess?: ")
            self.check_guess(player_input)

        if self._tries == 0:
            print("@@@@@@  YOU LOST HANGMAN!  @@@@@@")
            print("@@@@@ BETTER LUCK NEXT TIME @@@@@")

        else:
            print("##### YOU FOUND THE WORD!! #####")
            print(f"Game word was: {self._word}")
        


if __name__ == "__main__":
    # Driver
    if len(sys.argv) > 1:
        wordfile = sys.argv[len(sys.argv)-1]
        print(f"Using {wordfile} as game words.")

        game = HangManGame(wordfile)
    else:
        game = HangManGame()

    game.run()