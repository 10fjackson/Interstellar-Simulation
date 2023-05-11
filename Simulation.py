import pygame
import pygame.math as math

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define the font for the instructions
instructions_font = pygame.font.Font(None, 24)
instructions_text = instructions_font.render("Move the ship using the arrow keys, don't get too close to the black hole!", True, (255, 255, 255))

# Load the images
background_image = pygame.image.load('background.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

ship_image = pygame.image.load('spaceship.png').convert_alpha()
ship_image = pygame.transform.scale(ship_image, (100, 100))

# Create the black hole and ship
black_hole_pos = math.Vector2(screen_width / 2, screen_height / 2)
ship_pos = math.Vector2(50, 50)

# Gravity constant
G = 4

# Ship speed
ship_speed = 0.25

# Font for displaying text
font = pygame.font.Font(None, 36)

# Button dimensions
button_width = 200
button_height = 50

# Main game loop
running = True
game_over = False
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                # Reset the game if the button is clicked
                if (screen_width / 2 - button_width / 2 < event.pos[0] < screen_width / 2 + button_width / 2 and
                    screen_height / 2 < event.pos[1] < screen_height / 2 + button_height):
                    ship_pos = math.Vector2(50, 50)
                    game_over = False
    # Check for pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_pos.x -= ship_speed
    if keys[pygame.K_RIGHT]:
        ship_pos.x += ship_speed
    if keys[pygame.K_UP]:
        ship_pos.y -= ship_speed
    if keys[pygame.K_DOWN]:
        ship_pos.y += ship_speed

    # Calculate the force of gravity and update the ship's position
    distance = ship_pos.distance_to(black_hole_pos)
    if distance < 75:  # The ship gets eaten if it gets too close to the black hole
        game_over = True
    elif distance < 300 and not game_over:  # Only apply gravity if the ship is close to the black hole and not eaten
        gravity = G * (black_hole_pos - ship_pos).normalize() / (distance / 10)
        ship_pos += gravity

    # Draw the background
    screen.blit(background_image, (0, 0))
    # Draw the instructions
    screen.blit(instructions_text, (125, 550))  # 10 pixels from the left and top edge


    # Draw the black hole and the ship
    if not game_over:
        screen.blit(ship_image, (ship_pos.x - 50, ship_pos.y - 50))

    if game_over:
        # Draw the game over message
        message = font.render("You got eaten!", True, (255, 255, 255))
        screen.blit(message, (screen_width / 2 - message.get_width() / 2, screen_height / 2 - message.get_height() / 2 - 30))

        # Draw the reset button
        pygame.draw.rect(screen, (255, 0, 0), ((screen_width - button_width) / 2, screen_height / 2, button_width, button_height))
        reset_text = font.render("Reset", True, (255, 255, 255))
        screen.blit(reset_text, ((screen_width - reset_text.get_width()) / 2, screen_height / 2 + (button_height - reset_text.get_height()) / 2))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()