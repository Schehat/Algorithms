import pygame
import os
import random
import math
import operator
from functools import reduce

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.font.init()

font_title = pygame.font.SysFont("timesnewroman", 40)
font_button = pygame.font.SysFont("timesnewroman", 18)
font_text = pygame.font.SysFont("timesnewroman", 20)
font_binary = pygame.font.SysFont("timesnewroman", 12)

CLOCK = pygame.time.Clock()
FPS = 60
WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Hamming Code Error Detection")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 96, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
HOVER_BLUE = (0, 41, 200)
HOVER_YELLOW = (200, 200, 0)
HOVER_RED = (200, 0, 0)
HOVER_GREEN = (0, 200, 0)
RECT_BLUE = (50, 450, 160, 60)
RECT_YELLOW = (230, 450, 160, 60)
RECT_RED = (50, 530, 160, 60)
RECT_GREEN = (230, 530, 160, 60)

ROWS, COLS = 8, 8
GAP = 40
n_power = int(math.log2(ROWS * COLS))

rects = []
numbers = []
ones = []

ran = None
seconds_reset = 0

# check to avoid multiple checks and to assure correct order of actions
do_parity = True
do_error = True
do_detection = False


class Buttons:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        global numbers, seconds_reset, do_error, ran, ones, do_parity, do_error, do_detection

        if RECT_BLUE[0] < self.mouse[0] < RECT_BLUE[0] + RECT_BLUE[2] and \
                RECT_BLUE[1] < self.mouse[1] < RECT_BLUE[1] + RECT_BLUE[3]:
            pygame.draw.rect(WINDOW, HOVER_BLUE, RECT_BLUE)
            if self.click[0] == 1:
                # avoid spamming clicks
                seconds = pygame.time.get_ticks() // 1000
                if seconds > seconds_reset + 0.2:
                    seconds_reset = seconds
                    if len(numbers) == 0:
                        make_numbers()
                    elif len(numbers) > 0:
                        numbers = []
        else:
            pygame.draw.rect(WINDOW, BLUE, RECT_BLUE)

        if RECT_YELLOW[0] < self.mouse[0] < RECT_YELLOW[0] + RECT_YELLOW[2] and \
                RECT_YELLOW[1] < self.mouse[1] < RECT_YELLOW[1] + RECT_YELLOW[3]:
            pygame.draw.rect(WINDOW, HOVER_YELLOW, RECT_YELLOW)
            if self.click[0] == 1:
                seconds = pygame.time.get_ticks() // 1000
                if seconds > seconds_reset + 0.2:
                    seconds_reset = seconds
                    do_parity_check()
        else:
            pygame.draw.rect(WINDOW, YELLOW, RECT_YELLOW)

        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(WINDOW, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                seconds = pygame.time.get_ticks() // 1000
                if seconds > seconds_reset + 0.2:
                    seconds_reset = seconds
                    ran = random.randint(3, 63)  # no need to take 0, 1, 2
                    while math.log2(ran).is_integer():
                        ran = random.randint(3, 63)
                    if do_error and not do_parity and len(numbers) > 0:
                        do_error = False
                        if numbers[ran][1] == 1:
                            numbers[ran][1] = 0
                            text_number = font_text.render(str(numbers[ran][1]), 1, WHITE, RED)
                            x, y, w, h = rects[ran]
                            WINDOW.blit(text_number, (x, y))
                        else:
                            numbers[ran][1] = 1
                            text_number = font_text.render(str(numbers[ran][1]), 1, WHITE, RED)
                            x, y, w, h = rects[ran]
                            WINDOW.blit(text_number, (x, y))
                            pygame.display.update()
        else:
            pygame.draw.rect(WINDOW, RED, RECT_RED)

        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(WINDOW, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                seconds = pygame.time.get_ticks() // 1000
                if seconds > seconds_reset + 0.2:
                    seconds_reset = seconds
                    count = 0
                    if do_detection and not do_parity and not do_error:
                        do_detection = False
                        for i in numbers:
                            if i[1] == 1:
                                ones.append(i[0])
                                count += 1
                                text_number = font_binary.render(str(bin(i[0])[2:]), 1, WHITE)
                                WINDOW.blit(text_number, (WINDOW_SIZE[0] - 120, 90 + 12 * count))
                                pygame.display.update()

                        text_number = font_binary.render("----------------", 1, RED)
                        WINDOW.blit(text_number, (WINDOW_SIZE[0] - 130, 90 + 12 * (count + 1)))
                        text_number = font_binary.render(
                            f"XOR: {str(bin(reduce(operator.xor, [i for i in ones]))[2:])}", 1, RED)
                        WINDOW.blit(text_number, (WINDOW_SIZE[0] - 130, 90 + 12 * (count + 2)))
                        ones = []
        else:
            pygame.draw.rect(WINDOW, GREEN, RECT_GREEN)

    @staticmethod
    def button_text(rect, text):
        text_output = font_button.render(text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        WINDOW.blit(text_output, text_rect)


def make_grid():
    for i in range(ROWS):
        for j in range(COLS):
            rects.append([j * GAP + 55, i * GAP + 105, GAP, GAP])


def make_numbers():
    global do_parity, do_error, do_detection
    do_parity = True
    do_error = True
    do_detection = True
    for i in range(0, ROWS * COLS):
        if i == 0:
            numbers.append([i, ""])
        elif not math.log2(i).is_integer():
            numbers.append([i, random.randint(0, 1)])
        else:
            numbers.append([i, ""])
    WINDOW.fill(BLACK)
    for i in numbers:
        text_number = font_text.render(str(i[1]), 1, WHITE)
        text_binary = font_binary.render(str(bin(i[0])[2:]), 1, WHITE)
        x, y, w, h = rects[i[0]]
        WINDOW.blit(text_number, (x, y))
        WINDOW.blit(text_binary, (x, y + 27))
        pygame.display.update()


def do_parity_check():
    global numbers, do_parity
    j = 0
    if do_parity and len(numbers) > 0:
        do_parity = False
        # to avoid errors will change parity after this
        numbers[0][1] = 0
        # fill the parity digits (2^n) correctly
        for x in range(n_power):
            j = 0
            for i in numbers:
                try:
                    if str(bin(i[0])[2:][-(x + 1)]) == str(1):
                        if i[1] == 1:
                            j += 1
                except IndexError:
                    pass
            if j % 2 == 0:
                numbers[2 ** x][1] = 0
            else:
                numbers[2 ** x][1] = 1

        # check if we have even 1 digits for the first parity figure
        for i in numbers:
            if str(i[1]) == str(1):
                j += 1
        if j % 2 == 0:
            numbers[0][1] = 0
        else:
            numbers[0][1] = 1

        for i in numbers:
            if i[0] == 0:
                text_number = font_text.render(str(i[1]), 1, BLACK, YELLOW)
                x, y, w, h = rects[i[0]]
                WINDOW.blit(text_number, (x, y))
                pygame.display.update()
            if i[1] != "":
                try:
                    if math.log2(i[0]).is_integer():
                        text_number = font_text.render(str(i[1]), 1, BLACK, YELLOW)
                        x, y, w, h = rects[i[0]]
                        WINDOW.blit(text_number, (x, y))
                        pygame.display.update()
                except ValueError:
                    pass


def draw_text():
    text_title = font_title.render("Binary Search", 1, YELLOW)
    WINDOW.blit(text_title, (int(WINDOW_SIZE[0] / 2 - text_title.get_width() / 2), int(text_title.get_height())))


def create_buttons():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    buttons = Buttons(mouse, click)
    return buttons


def draw(buttons):
    for i in rects:
        x, y, w, h = i
        pygame.draw.rect(WINDOW, WHITE, (x, y, w, h), 1)

    buttons.button_draw()
    buttons.button_text(RECT_BLUE, "1. Generate Numbers")
    buttons.button_text(RECT_YELLOW, "2. Parity Check")
    buttons.button_text(RECT_RED, "3. Generate Error")
    buttons.button_text(RECT_GREEN, "4. Error Detection")
    draw_text()

    pygame.display.update()


def main():
    make_grid()
    run = True
    while run:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        buttons = create_buttons()
        draw(buttons)


main()
