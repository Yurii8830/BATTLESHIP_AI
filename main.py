import pygame
import random
from engine import Player, Game

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
myfont = pygame.font.SysFont("freesans", 100)
small_font = pygame.font.SysFont("freesans", 30)

# Global variables
SQ_SIZE = 35
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDTH = SQ_SIZE * 10 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN
INDENT = 8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HUMAN1 = True
HUMAN2 = False

# Calm and soothing colors
LIGHT_BLUE = (173, 216, 230)  # Light blue for background
DARK_BLUE = (70, 130, 180)  # Slightly darker blue for water
LIGHT_BROWN = (210, 180, 140)  # Wood-like color for ships
SHIP_ACCENT = (255, 222, 173)  # Lighter accent color for ship details
SHADOW_COLOR = (40, 40, 40)  # Darker shade for ship shadow
COLORS = {"U": DARK_BLUE, "M": LIGHT_BLUE, "H": (255, 69, 0), "S": (255, 105, 180)}  # Soothing color palette

# Function to draw the grid with subtle ripple effect
def draw_grid(player, left=0, top=0, search=False):
    for i in range(100):
        x = left + i % 10 * SQ_SIZE
        y = top + i // 10 * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)

        # Add subtle ripple effect (light)
        ripple_effect = random.randint(0, 2)
        if ripple_effect:
            pygame.draw.circle(SCREEN, LIGHT_BLUE, (x + SQ_SIZE // 2, y + SQ_SIZE // 2), random.randint(5, 10), width=2)

        pygame.draw.rect(SCREEN, LIGHT_BLUE, square)  # Calm blue water color
        pygame.draw.rect(SCREEN, DARK_BLUE, square, width=3)  # Light border
        if search:
            x += SQ_SIZE // 2
            y += SQ_SIZE // 2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x, y), radius=SQ_SIZE // 4)

# Function to draw ships without animation for movement
def draw_ships(player, left=0, top=0):
    for ship in player.ships:
        x = left + ship.col * SQ_SIZE + INDENT
        y = top + ship.row * SQ_SIZE + INDENT
        if ship.orientation == "h":
            width = ship.size * SQ_SIZE - 2 * INDENT
            height = SQ_SIZE - 2 * INDENT
        else:
            width = SQ_SIZE - 2 * INDENT
            height = ship.size * SQ_SIZE - 2 * INDENT

        # Shadow for the ship with a smooth effect
        shadow = pygame.Rect(x + 3, y + 3, width, height)
        pygame.draw.rect(SCREEN, SHADOW_COLOR, shadow)  # Soft shadow

        # Draw ship with wood-like texture and curved edges
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, LIGHT_BROWN, rectangle, border_radius=12)  # Rounded ship design

        # Add ship accents for detail (e.g., a light accent line)
        accent_rect = pygame.Rect(x + width // 4, y + height // 4, width // 2, height // 2)
        pygame.draw.rect(SCREEN, SHIP_ACCENT, accent_rect, border_radius=8)

# Function to create a gradient effect in the background (calm waves)
def draw_gradient():
    for i in range(HEIGHT):
        # Ensure the green value is capped at 255
        green_value = min(216 + int(i * 0.15), 255)
        color = (173, green_value, 230)
        pygame.draw.line(SCREEN, color, (0, i), (WIDTH, i))

# Function to draw a message (whose turn it is)
def draw_turn_message(player1_turn):
    turn_message = "Player 1's turn" if player1_turn else "Player 2's turn"
    text = small_font.render(turn_message, True, (255, 255, 255))  # White text for better visibility
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))

game = Game(HUMAN1, HUMAN2)

# Function to set the algorithm choice for the AI
def set_algorithm_choice(choice):
    game.algorithm = choice

# Pygame loop
animating = True
pausing = False
while animating:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False

        # User clicks on mouse
        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
            x, y = pygame.mouse.get_pos()
            if game.player1_turn and x < SQ_SIZE * 10 and y < SQ_SIZE * 10:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)
            elif not game.player1_turn and x > WIDTH - SQ_SIZE * 10 and y > SQ_SIZE * 10 + V_MARGIN:
                row = (y - SQ_SIZE * 10 - V_MARGIN) // SQ_SIZE
                col = (x - SQ_SIZE * 10 - H_MARGIN) // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                animating = False
            if event.key == pygame.K_SPACE:
                pausing = not pausing
            if event.key == pygame.K_RETURN:
                game = Game(HUMAN1, HUMAN2)

        if not pausing:
            SCREEN.fill(DARK_BLUE)  # Set a background color for the main screen
            draw_gradient()  # Apply gradient background

            # Draw grids with subtle ripple effect
            draw_grid(game.player1, search=True)
            draw_grid(game.player2, search=True, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN,
                      top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)

            draw_grid(game.player1, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
            draw_grid(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

            # Draw ships with modern, subtle design (without animation)
            draw_ships(game.player1, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
            draw_ships(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

            # Computer moves
            if not game.over and game.computer_turn:
                if game.player1_turn:
                    game.hunting_targeting_ai()
                else:
                    game.hunting_targeting_ai()

            # Game over message with green text for winner
            if game.over:
                text = "Player " + str(game.result) + " wins!"
                textbox = myfont.render(text, False, (0, 255, 0))  # Green text for winner
                SCREEN.blit(textbox, (WIDTH // 2 - 240, HEIGHT // 2 - 50))

            # Draw whose turn it is
            draw_turn_message(game.player1_turn)

            pygame.time.wait(0)
            pygame.display.flip()
