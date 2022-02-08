import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Wordle")

screen = pygame.display.set_mode([560, 670])
FONT = pygame.font.SysFont('arial', 50,  bold=pygame.font.Font.bold)

class Letter():
    def __init__(self, letter, position, row):
        self.letter = letter
        self.position = position + 1
        self.row = row
        self.coordinate_X = ((position * 100) - 100) + (position * 10)
        self.coordinate_Y = (row * 100) + (10 * (row + 1))
        self.colour = (120,124,126)
        self.YELLOW = (201,180,88)
        self.GREEN = (106,170,100)

    def draw(self):
        pygame.draw.rect(screen, self.colour ,(self.coordinate_X,self.coordinate_Y,100,100))
        text = FONT.render(self.letter, True, (255,255,255))
        text_x = (self.coordinate_X + 50) - (text.get_width() / 2)
        text_y = (self.coordinate_Y + 20)
        screen.blit(text, (text_x, text_y))

    def status(self, word_list):
        if any(self.letter in word for word in word_list):
            self.colour = self.YELLOW
            if self.letter == word_list[self.position - 2]:
                self.colour = self.GREEN
                return True


COLOR_INACTIVE = (120,124,126)
COLOR_ACTIVE = (50,50,50)
            
def random_word():
    with open('words.txt') as f:
        lines = f.readlines()
        words = lines[0].split()
        return list(words[random.randint(0,len(words))])
        
def guess(row, attempts):
    row = []
    position = 0
    # open file and pick a random word
    with open('words.txt') as f:
        lines = f.readlines()
        words = lines[0].split()
        max_length = len(words) - 1
        random_guess = list(words[random.randint(0,max_length)])
    
    for i in range(5):
        position += 1
        row.append(Letter(random_guess[i], position, attempts))
    position = 0
    return row

run = True

games = 0
wins = 0

while run:
    letters = []
    attempts = 0
    screen.fill((255, 255, 255))
    events = pygame.event.get()

    guessing = True

    while guessing:
        random_word_to_guess = random_word()
        for i in range(6):
            correct_letters = 0
            random_guess = guess(letters, attempts)
            attempts += 1

            for each_letter in random_guess:
                if each_letter.status(random_word_to_guess):
                    correct_letters += 1
                each_letter.draw()
                if correct_letters == 5:
                    wins += 1
                    guessing = False
            correct_letters = 0
                    
        games += 1
        guessing = False

    for event in events:
        if event.type == pygame.QUIT:
            run = False

    # print(f'{(wins / games) * 100} % of games have been won')
    print(f'{wins} / {games} have been won')

    pygame.display.flip()

# pygame.quit

