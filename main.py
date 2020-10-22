import pygame
import math
import random

"""Setup Display"""
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

"""Button Variables"""
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = start_y + (i // 13) * (GAP + RADIUS * 2)
    letters.append([x, y, chr(A + i), True])

"""Fonts"""
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

"""Load Images"""
images = [pygame.image.load("images/hangman" + str(i) + ".png") for i in range(7)]

"""Games variables"""
hangman_status = 0
with open('words_alpha.txt', 'r') as f:
    words_list = f.readlines()
    word = words_list[random.randint(0, len(words_list))].strip().upper()
guessed = []

"""Colors"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw():
    win.fill(WHITE)

    """Draw Title"""
    title_text = TITLE_FONT.render("HANGMAN GAME", 1, BLACK)
    win.blit(title_text, (int(WIDTH / 2) - int(title_text.get_width() / 2), 20))

    """Draw Word"""
    display_word = ""
    for character in word:
        if character in guessed:
            display_word += character + " "
        else:
            display_word += "_ "
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(word_text, (320, 200))

    """Draw Buttons"""
    for ltr_item in letters:
        pos1, pos2, ltr, visible = ltr_item
        if visible:
            pygame.draw.circle(win, BLACK, (pos1, pos2), RADIUS, 3)
            ltr_text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(ltr_text, (pos1 - int(ltr_text.get_width() / 2), pos2 - int(ltr_text.get_height() / 2)))

    win.blit(images[hangman_status], (70, 100))
    pygame.display.update()


def display_message(msg):
    pygame.time.delay(1000)
    win.fill(WHITE)
    msg_text = WORD_FONT.render(msg, 1, BLACK)
    win.blit(msg_text, (int(WIDTH / 2) - int(msg_text.get_width() / 2), int(HEIGHT / 2) - int(msg_text.get_height() / 2)))
    pygame.display.update()
    pygame.time.delay(3000)


if __name__ == '__main__':
    """Setup Game Loop"""
    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for item in letters:
                    x, y, alphabet, visibility = item
                    if visibility:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            item[3] = False
                            guessed.append(alphabet)
                            if alphabet not in word:
                                hangman_status += 1
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("YOU WON!")
            break

        if hangman_status == 6:
            display_message("YOU LOST!")
            break

    pygame.quit()
