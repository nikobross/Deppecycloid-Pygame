import random
import pygame

people = []

def choose_bracket(people):
    # choose 8 random people from the list and make them into a bracket
    bracket = {}
    for i in range(1, 9):
        person = people.pop(random.randint(0, len(people) - 1))
        bracket[i] = person
    return bracket


def display_bracket(bracket):
    # set of matchups with 1 with 8 2 2ith 7 3 with 6 4 with 5
    matchups = {}
    matchups[bracket[1]] = bracket[8]
    matchups[bracket[2]] = bracket[7]
    matchups[bracket[3]] = bracket[6]
    matchups[bracket[4]] = bracket[5]
    return matchups

def draw_bracket(matchups):
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Bracket")

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    screen.fill(white)

    # Define bracket positions
    x = 100
    y = 100
    spacing = 50


    pygame.draw.line(screen, black, (x + spacing * 3, y + spacing - 20), (x + spacing * 3, y + spacing + 20), 2)
    pygame.draw.line(screen, black, (x + spacing * 3, y + spacing * 3 - 20), (x + spacing * 3, y + spacing * 3 + 20), 2)

    pygame.draw.line(screen, black, (x + spacing * 3 - 40, y + spacing - 20), (x + spacing * 3, y + spacing - 20), 2)
    pygame.draw.line(screen, black, (x + spacing * 3 - 40, y + spacing * 3 + 20), (x + spacing * 3, y + spacing * 3 + 20), 2)
    
    pygame.draw.line(screen, black, (x + spacing * 3 - 40, y + spacing + 20), (x + spacing * 3, y + spacing + 20), 2)
    pygame.draw.line(screen, black, (x + spacing * 3 - 40, y + spacing * 3 - 20), (x + spacing * 3, y + spacing * 3 - 20), 2)


    pygame.draw.line(screen, black, (x + spacing * 3, y + spacing - 20), (x + spacing * 3, y + spacing + 20), 2)
    pygame.draw.line(screen, black, (x + spacing * 3, y + spacing * 3 - 20), (x + spacing * 3, y + spacing * 3 + 20), 2)

    pygame.draw.line(screen, black, (x + spacing * 4, y + spacing), (x + spacing * 4, y + spacing * 3), 2)
    pygame.draw.line(screen, black, (x + spacing * 3, y + spacing), (x + spacing * 4, y + spacing), 2)
    pygame.draw.line(screen, black, (x + spacing * 3, y + spacing * 3), (x + spacing * 4, y + spacing * 3), 2)

    pygame.draw.line(screen, black, (x + spacing * 4, y + spacing * 2), (x + spacing * 5, y + spacing * 2), 2)

    # Draw matchup text
    font = pygame.font.Font(None, 30)
    text_y = y + spacing // 2 - 10
    for i, (player1, player2) in enumerate(matchups.items()):
        text_x = x + spacing * 5
        text = font.render(f"{player1} vs {player2}", True, black)
        screen.blit(text, (text_x, text_y))
        text_y += spacing

    pygame.display.flip()
    # Wait for user to close the window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

people.append("Bob")
people.append("Charlie")
people.append("David")
people.append("Eve")
people.append("Frank")
people.append("Grace")
people.append("Heidi")
people.append("Ivan")
people.append("Judy")
people.append("Kevin")

bracket = choose_bracket(people)
matchups = display_bracket(bracket)
draw_bracket(matchups)