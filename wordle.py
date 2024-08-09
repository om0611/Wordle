"""
Wordle using Python
"""

from sys import exit
import pygame
import random

pygame.init()

# Constants
FONT = pygame.font.Font('FreeSansBold.otf', 50)

with open('official_wordle.txt') as f:
    ANSWER_WORDS = [str.strip(w) for w in f.readlines()]      # A list containing all the possible answer words.

with open('official_wordle_guesses.txt') as f:
    GUESS_WORDS = [str.strip(w) for w in f.readlines()]       # A list containing all the valid guess words.
    GUESS_WORDS += ANSWER_WORDS

CORRECT = 'Y'
WRONG_POSITION = '?'
INCORRECT = 'N'

RECT_COLOURS = {
    CORRECT: '#6aaa64',         # green
    WRONG_POSITION: '#c9b458',  # orange
    INCORRECT: '#787c7e',       # grey
}

ALPHA_KEYS = {pygame.K_a: 'a', pygame.K_b: 'b', pygame.K_c: 'c', pygame.K_d: 'd', pygame.K_e: 'e', pygame.K_f: 'f',
              pygame.K_g: 'g', pygame.K_h: 'h', pygame.K_i: 'i', pygame.K_j: 'j', pygame.K_k: 'k', pygame.K_l: 'l',
              pygame.K_m: 'm', pygame.K_n: 'n', pygame.K_o: 'o', pygame.K_p: 'p', pygame.K_q: 'q', pygame.K_r: 'r',
              pygame.K_s: 's', pygame.K_t: 't', pygame.K_u: 'u', pygame.K_v: 'v', pygame.K_w: 'w', pygame.K_x: 'x',
              pygame.K_y: 'y', pygame.K_z: 'z'}

LETTER_SIZE = 80
LETTER_SPACING = 10
BOX_SIZE = 100
BOX_SPACING = 10
LOCATIONS_X = [10, 120, 230, 340, 450]
LOCATIONS_Y = [10, 120, 230, 340, 450, 560]


def run_wordle() -> None:
    """
    Runs Wordle using Pygame.
    """
    pygame.init()
    screen = _initialize_pygame_window()
    draw_layout(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
    answer = random.choice(ANSWER_WORDS)        # choose a random answer word
    guesses_remaning = 6
    guess = ''
    x, y = 0, 0
    running = True

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(guess) == 5:
                    if guess in GUESS_WORDS:
                        status = get_guess_status(answer, guess)
                        draw_status(screen, status, guess, LOCATIONS_Y[y])
                        pygame.display.flip()
                        guesses_remaning -= 1
                        if answer == guess:
                            print("Congratulations! You have correctly guessed the word!")
                            running = False
                            break
                        elif guesses_remaning == 0:
                            print("Good try! The correct word was \'", answer, "\'.", sep="")
                            running = False
                            break
                        else:
                            y += 1
                            x = 0
                            guess = ''
                            continue
                    else:
                        print("Not a valid word.")

                elif event.key == pygame.K_BACKSPACE and len(guess) > 0:
                    x -= 1
                    guess = guess[:-1]      # remove the last char from guess
                    remove_char(screen, LOCATIONS_X[x], LOCATIONS_Y[y])
                    pygame.display.flip()

                elif event.key in ALPHA_KEYS and len(guess) < 5:
                    letter = ALPHA_KEYS[event.key]      # stores the char corresponding to the key pressed
                    draw_letter(screen, letter, LOCATIONS_X[x], LOCATIONS_Y[y], (0, 0, 0),
                                (0, 0, 0), 1)
                    pygame.display.flip()
                    guess += letter
                    x += 1

        clock.tick(60)      # while loop should not repeat more than 60 times per second

    pygame.time.delay(5000)
    pygame.quit()
    exit()


def _initialize_pygame_window() -> pygame.Surface:
    """
    Initialize and return a new Pygame window.
    """
    pygame.init()

    screen_width = 560
    screen_height = 670
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((255, 255, 255))    # white
    pygame.display.set_caption("Wordle, Python Edition!")

    return screen


def draw_layout(screen: pygame.Surface) -> None:
    """
    Draws the boxes for the letters on the pygame screen.
    """
    colour = (128, 128, 128)   # grey
    for y in range(6):
        for x in range(5):
            draw_box(screen, colour, pygame.Rect(LOCATIONS_X[x], LOCATIONS_Y[y], BOX_SIZE, BOX_SIZE), 1)


def draw_status(screen: pygame.Surface, status: list[str], guess: str, y: float) -> None:
    """
    Draw the status of each character in the guess word.
    """
    for x in range(5):
        bg_colour = RECT_COLOURS[status[x]]
        text_colour = (255, 255, 255)
        draw_letter(screen, guess[x], LOCATIONS_X[x], y, text_colour, bg_colour, 0)


def draw_box(screen: pygame.Surface, colour: tuple[int, int, int], rect: pygame.Rect, width: int) -> None:
    """
    Draws a letter box on the screen in the given colour, using the rect object, and with the given border width.
    """
    pygame.draw.rect(screen, colour, rect, width)


def draw_letter(screen: pygame.Surface, letter: str, x: float, y: float, text_colour: tuple[int, int, int],
                bg_colour: tuple[int, int, int], width: int) -> None:
    """
    Draw a letter on the screen at the given position. Letters are automatically converted to uppercase.
    """
    text_position = (x + BOX_SIZE // 2, y + BOX_SIZE // 2)
    text_screen = FONT.render(str.upper(letter), True, text_colour)
    text_rect = text_screen.get_rect(center=text_position)
    draw_box(screen, bg_colour, pygame.Rect(x, y, BOX_SIZE, BOX_SIZE), width)
    screen.blit(text_screen, text_rect)


def remove_char(screen: pygame.Surface, x: float, y: float) -> None:
    """
    Removes the char at the given position.
    """
    # Erase the char by putting a white box on top
    draw_box(screen, (255, 255, 255), pygame.Rect(x, y, BOX_SIZE, BOX_SIZE), 0)

    # Add a grey border to the box
    draw_box(screen, (128, 128, 128), pygame.Rect(x, y, BOX_SIZE, BOX_SIZE), 1)


def is_correct_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is CORRECT.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_correct_char('teach', 'adieu', 3)
    False
    >>> is_correct_char('teaching', 'reacting', 1)
    True
    """
    return guess[i] == answer[i]


def is_wrong_position_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is WRONG_POSITION.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_wrong_position_char('teach', 'adieu', 3)
    True
    >>> is_wrong_position_char('teaching', 'reacting', 1)
    False
    >>> # Cases with duplicate characters!
    >>> is_wrong_position_char('hello', 'hoops', 1)
    True
    >>> is_wrong_position_char('hello', 'hoops', 2)
    True
    >>> # Case that counts as 'incorrect' rather than 'wrong position' due to guess already being correct at the
    >>> # right position index
    >>> is_wrong_position_char('hello', 'keeps', 2)
    False
    """
    not_correct = not is_correct_char(answer, guess, i)
    at_diff_index = any([guess[i] == answer[j] for j in range(len(guess)) if j != i and guess[j] != answer[j]])
    return not_correct and at_diff_index


def is_incorrect_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is INCORRECT.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_incorrect_char('teach', 'adieu', 1)
    True
    >>> is_incorrect_char('teaching', 'reacting', 1)
    False
    >>> is_incorrect_char('hello', 'keeps', 2)
    True

    HINT: you can use the previous two status functions to implement this one.
    """
    not_correct = not is_correct_char(answer, guess, i)
    not_wrong_pos = not is_wrong_position_char(answer, guess, i)
    return not_correct and not_wrong_pos


def get_character_status(answer: str, guess: str, i: int) -> str:
    """Return the character status of guess[i] with respect to answer.

    The return value is one of the three values {INCORRECT, WRONG_POSITION, CORRECT}.
    (These values are imported from the a2_helpers.py module for you already.)

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> get_character_status('teach', 'adieu', 1) == INCORRECT
    True
    >>> get_character_status('teaching', 'reacting', 1) == CORRECT
    True
    """
    if is_correct_char(answer, guess, i):
        return CORRECT
    elif is_wrong_position_char(answer, guess, i):
        return WRONG_POSITION
    else:
        return INCORRECT


def get_guess_status(answer: str, guess: str) -> list[str]:
    """Return the guess status of the given guess with respect to answer.

    The return value is a list with the same length as guess, whose
    elements are all in the set {INCORRECT, WRONG_POSITION, CORRECT}.

    Preconditions:
    - answer != ''
    - len(answer) == len(guess)

    >>> example_status = get_guess_status('teach', 'adieu')
    >>> example_status == [WRONG_POSITION, INCORRECT, INCORRECT, WRONG_POSITION, INCORRECT]
    True
    """
    return [get_character_status(answer, guess, i) for i in range(len(guess))]


if __name__ == "__main__":
    run_wordle()
