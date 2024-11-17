import sys
import pygame

# Initialize Pygame
pygame.init()

# Mobile-like screen dimensions and settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dodo Bird Game')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load images
background_image = pygame.image.load('background.png')  # Load background for start screen
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen size

bird_image = pygame.image.load('bird.png')  # Load the bird image
bird_image = pygame.transform.scale(bird_image, (50, 50))  # Scale bird image to fit (adjust size as needed)

start_button_image = pygame.image.load('start.png')  # Load start button image
start_button_image = pygame.transform.scale(start_button_image, (200, 100))  # Scale the start button (adjust size as needed)

game_over_image = pygame.image.load('game_over.png')  # Load the game over image
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fill the screen

exit_button_image = pygame.image.load('exit.png')  # Load exit button image
exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))  # Scale the exit button (adjust size as needed)

# Player settings
player_x = SCREEN_WIDTH // 2
player_y = 100
player_velocity_y = 0
gravity = 0.5
jump_force = -10

# Ground settings
ground_height = 50
ground_y = SCREEN_HEIGHT - ground_height

# Points system
points = 0
font = pygame.font.SysFont('Arial', 30)

# Game state
is_alive = False  # Start screen active by default
is_playing = False  # Game not started yet

# Ground object
ground = pygame.Rect(0, ground_y, SCREEN_WIDTH, ground_height)

# Game clock
clock = pygame.time.Clock()

def draw_score():
    """Display the current score on the screen"""
    score_text = font.render(f'Points: {points}', True, WHITE)
    screen.blit(score_text, (10, 10))

def reset_player():
    """Reset player position, velocity, and score"""
    global player_y, player_velocity_y, points
    player_y = 100
    player_velocity_y = 0
    points = 0

def game_over():
    """Handle the game over screen and show points"""
    global is_alive
    # Display "Game Over!" image
    screen.blit(game_over_image, (0, 0))  # Draw the game over image on top of the screen

    # Display "Press R to Restart" text
    restart_text = font.render('Press R to Restart', True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    # Display the points at the end of the game
    points_text = font.render(f'Final Score: {points}', True, WHITE)
    screen.blit(points_text, (SCREEN_WIDTH // 2 - points_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    # Display the exit button
    exit_button_rect = screen.blit(exit_button_image, (SCREEN_WIDTH // 2 - exit_button_image.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    pygame.display.update()  # Make sure the screen is updated

    return exit_button_rect

def die():
    """Handle player death - this will trigger when the player hits the ground"""
    global is_alive
    is_alive = False  # Stop the game loop
    return game_over()  # Show the game over image and text, return exit button for detection

def update_player():
    """Update player position with gravity and check for death"""
    global player_y, player_velocity_y, is_alive, points

    # Apply gravity
    player_velocity_y += gravity

    # Update player position
    player_y += player_velocity_y

    # Check if the player hits the ground (death condition)
    if player_y + 50 >= ground_y:  # 50 is the height of the bird image
        player_y = ground_y - 50
        die()  # Call die function when player hits the ground

def jump():
    """Make the player jump"""
    global player_velocity_y
    if player_y == ground_y - 50:  # Only jump if on the ground (50 is the bird's height)
        player_velocity_y = jump_force

def show_start_screen():
    """Display the start screen and handle button click"""
    # Fill screen with black for the start screen
    screen.fill(BLACK)

    # Render "Press Enter to Start" text
    start_text = font.render('Press Enter to Start', True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    # Display background image for the start menu
    screen.blit(background_image, (0, 0))

    # Display the start button
    start_button_rect = screen.blit(start_button_image, (SCREEN_WIDTH // 2 - start_button_image.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()  # Update the screen with the button

    # Check for mouse click on the start button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                if start_button_rect.collidepoint(event.pos):  # Check if click is inside the button
                    return True  # Return True to indicate the game should start

    return False  # No click or wrong click, so stay in start screen

def main_game_loop():
    """The main game loop"""
    global is_alive, is_playing, points
    while is_playing:
        screen.fill(BLACK)  # Fill screen with black for gameplay

        # Draw background
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Jump when space is pressed
                    if is_alive:
                        jump()
                if event.key == pygame.K_r:  # Restart game when 'R' is pressed
                    if not is_alive:
                        reset_player()
                        is_alive = True
                        points = 0

        if is_alive:
            # Update player position and check collisions
            update_player()

            # Draw the player (bird)
            screen.blit(bird_image, (player_x, player_y))  # Draw the bird at the player's position

            # Draw ground
            pygame.draw.rect(screen, WHITE, ground)

            # Draw points
            draw_score()

            # Increment points over time
            points += 1

        else:
            # Game Over state, show exit button
            exit_button_rect = game_over()

            # Check for mouse click on the exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        if exit_button_rect.collidepoint(event.pos):  # Check if click is inside the exit button
                            return False  # Return False to go back to start screen

        # Update the display after everything is drawn
        pygame.display.update()

        # Frame rate control
        clock.tick(FPS)

# Main loop: Show start screen
while True:
    # Show start screen and wait for the start button to be clicked
    if show_start_screen():
        is_playing = True
        is_alive = True
        reset_player()  # Reset the player state
        main_game_loop()

    # Frame rate control for the start screen (you can make it slower)
    clock.tick(30)