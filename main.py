from random import random
import pygame
import random

pygame.init()
pygame.display.set_caption("Wordle")

SCREEN = pygame.display.set_mode([560, 800])
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
        pygame.draw.rect(SCREEN, self.colour ,(self.coordinate_X,self.coordinate_Y,100,100))
        text = FONT.render(self.letter, True, (255,255,255))
        text_x = (self.coordinate_X + 50) - (text.get_width() / 2)
        text_y = (self.coordinate_Y + 20)
        SCREEN.blit(text, (text_x, text_y))

    def status(self, word_list):
        if any(self.letter in word for word in word_list):
            self.colour = self.YELLOW
            if self.letter == word_list[self.position - 2]:
                self.colour = self.GREEN

COLOR_INACTIVE = (120,124,126)
COLOR_ACTIVE = (50,50,50)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 1)
            

with open('words.txt') as f:
    lines = f.readlines()
    words = lines[0].split()
    word_list = list(words[random.randint(0,len(words))])
    print(word_list)

letters = []

def add_letter(letters):
    row = 5
    position = 0
    guess = "cones"
    guess = guess.upper()
    guess_list = list(guess)
    for i in range(5):
        position += 1
        letters.append(Letter(guess_list[i], position, row))
    row += 1
    position = 0

RUN = True

input_box1 = InputBox(180, 700, 120, 60)
input_boxes = [input_box1]

while RUN:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            for box in input_boxes:
                box.handle_event(event)

    SCREEN.fill((255, 255, 255))

    add_letter(letters)

    for box in letters:
        box.status(word_list)
        box.draw()
                
    for box in input_boxes:
        box.update()

    for box in input_boxes:
        box.draw(SCREEN)

    pygame.display.update()

pygame.quit

