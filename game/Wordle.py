import random
#Bonus: Implement hardmode option: +20%

class Wordle:
    def __init__(self):
        """Set up the wordle game by initializing the word list, getting the word to guess, and initializing the game's state"""
        self.setWord(self.getWord())
        self.gameWon = False
        self.gameLost = False
        self.errorCount = 0
       

    def initWordlist(self):
        """Initializes the word list by reading them out of knuth_wordle_list."""
        file = open("knuth_wordle_list.txt", "r") #this opens the file and reads it and sets it to the variable file
        return file 
        

    def getWord(self):
        """Returns a word to be guessed, chosen from the list of words."""
        file = self.initWordlist()
        line = next(file) #gets the next line from the file
        for num, aline in enumerate(file, 2): #for loop over num and aline, numbers the lines in the file and loops over them
            if random.randrange(num): #random number in the range 0-num
                continue #if randrange is not 0, go to the top of the loop, 0 is false in binary, everything else is true
            line = aline #else the randomly chosen line becomes the current line, then the loop goes back to the top
            return line.rstrip() #returns the wordle word to be guessed
    def setWord(self, word):
        """Sets the given word as the word to guess, updating the working word and the list of already guessed letters as well."""
        self.wordToGuess = word.lower()
#         self.workingWord = ["-"]*len(self.wordToGuess)
        self.guessedAlready = {}
        self.guessList = 0
        self.GUESS_LIMIT = 6
    
    def allowableGuess(self, guess):
        """Returns true if guess is a five-letter string that does not appear in guessedAlready. Assumes guess is a string."""
        
        if len(guess) == 5:     
            if guess.lower() in self.guessedAlready.keys():
                return False
            else:
                return True
        else:
            return False
    def guessFeedback(self, guess):
        """Returns a string with the guess feedback. Letters that are in the proper place are in caps, letters that are in the wrong place are lower case, and letters that don't appear are replaced by -."""
#         print(guess)
#         guess = guess.upper()
        
        self.workingWord = []
        self.workingWord[:0] = guess
#         print(self.workingWord)
        for i in range(len(guess)):
            if guess[i] == self.wordToGuess[i]:
                self.workingWord[i] = guess[i].upper()
            elif guess[i] in self.wordToGuess:
                self.workingWord[i] = guess[i].lower()
            else:
                self.workingWord[i] = '-'
        self.workingWord = ''.join(self.workingWord)
        return self.workingWord
##        self.workingWord = self.workingWord[:i] + list(guess) + self.workingWord[i + 1:]

        
    def updateGame(self, guess):
        """Updates the game's state in response to the provided guess. Updates guessedAlready and whether the game is won or lost. Assumes guess is a string and is allowable."""
#         print(self.guessFeedback(guess))
        self.guessList += 1
        self.gameWon = False
        self.gameLost = False
        if guess.lower() == self.wordToGuess:
            self.gameWon = True
            self.gameLost = False
        elif self.guessList == 6:
            self.gameLost = True
            self.gameWon = False
        else:
            self.gameWon = False
            self.gameLost = False
        self.guessedAlready[guess] = self.guessFeedback(guess)

###Functions below this point assume that the game is being played on the terminal, and can use print and input.
    def showInTerminal(self):
        """Prints the current state of the game to the terminal (in the format guess:feedback for all guesses to date)."""
        print(self.guessedAlready)
          
    def getGuessFromTerminal(self):
        """Gets the next guess from the user. Returns the user's guess if and only if the guess is allowable (i.e., it repeats until an allowable guess is given)."""
        while True:
            guess = input('What Word would you like to try?\n')
            guess = guess.lower()
            if self.allowableGuess(guess):
                return guess
                
            
       
    def playGame(self):
        """Instructs the game to play itself with the user in the terminal."""
        self.gameEnded = False
        while (not self.gameEnded) and (len(self.guessedAlready) != 6):
            word = self.getGuessFromTerminal()
            print(word)
            self.updateGame(word)
            self.showInTerminal()
            if self.gameWon:
                self.gameEnded = True
                print("Nice Job! You got the word")
            elif self.gameLost:
                print("Try again next time, you did not get the word")
                self.gameEnded = True
            else:
                self.gameEnded = False
                

if __name__ == "__main__":
    game = Wordle()
    game.playGame()
