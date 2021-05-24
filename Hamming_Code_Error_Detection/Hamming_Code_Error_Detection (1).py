import pygame
import os
import random
import math

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.font.init()

font_title = pygame.font.SysFont("timesnewroman", 40)
font_button = pygame.font.SysFont("timesnewroman", 20)
font_text = pygame.font.SysFont("timesnewroman", 20)

CLOCK = pygame.time.Clock()
FPS = 60
WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Hamming Code Error Detection")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 96, 255)
RED = (255, 0, 0)
HOVER_YELLOW = (200, 200, 0)
HOVER_BLUE = (0, 41, 200)
HOVER_RED = (200, 0, 0)
RECT_YELLOW = (230, 450, 160, 60)
RECT_BLUE = (50, 450, 160, 60)
RECT_RED = (140, 530, 160, 60)

ROWS, COLS = 8, 8
GAP = 40

rects = []
numbers = []


class Buttons:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        if RECT_YELLOW[0] < self.mouse[0] < RECT_YELLOW[0] + RECT_YELLOW[2] and \
                RECT_YELLOW[1] < self.mouse[1] < RECT_YELLOW[1] + RECT_YELLOW[3]:
            pygame.draw.rect(WINDOW, HOVER_YELLOW, RECT_YELLOW)
            if self.click[0] == 1:
                pass
        else:
            pygame.draw.rect(WINDOW, YELLOW, RECT_YELLOW)

        if RECT_BLUE[0] < self.mouse[0] < RECT_BLUE[0] + RECT_BLUE[2] and \
                RECT_BLUE[1] < self.mouse[1] < RECT_BLUE[1] + RECT_BLUE[3]:
            pygame.draw.rect(WINDOW, HOVER_BLUE, RECT_BLUE)
            if self.click[0] == 1:
                make_numbers()

        else:
            pygame.draw.rect(WINDOW, BLUE, RECT_BLUE)

        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(WINDOW, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pass
        else:
            pygame.draw.rect(WINDOW, RED, RECT_RED)

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
    if len(numbers) == 0:
        for i in range(0, ROWS * COLS + 1):
            if i == 0:
                pass
            elif not math.log2(i).is_integer() or i == 32:
                numbers.append([i, random.randint(0, 1)])
    print(numbers)
    for i in numbers:
        text_number = font_text.render(str(i[1]), 1, WHITE)
        x, y, w, h = rects[i[0]]
        WINDOW.blit(text_number, (x, y))
        pygame.display.update()

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
    buttons.button_text(RECT_YELLOW, "Error Detection")
    buttons.button_text(RECT_BLUE, "Generate Numbers")
    buttons.button_text(RECT_RED, "Generate Error")
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

        draw(create_buttons())


main()
