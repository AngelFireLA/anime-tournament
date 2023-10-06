import random, io, pygame, sys, time, threading
import mal_api_handling as mal_api
from urllib.request import urlopen
from button import Button
from gamestate import GameState
from essential_functions import  place_text


pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

anime_cover_surfaces = {}

simulated = False

start_menu = GameState("start_menu", screen)
simulating = GameState("simulating", screen)
winning = GameState("winning", screen)

button = pygame.image.load("button.png").convert_alpha()
start = Button(300, 200, 1, "Start", button, screen)
anime_names = []

delay = 0


def get_image_from_web(link):
    image_str = urlopen(link).read()
    image_file = io.BytesIO(image_str)
    return image_file


def simulate_tournament(bracket):
    # simulate_tournament function takes a bracket as input, and returns the winner of the tournament
    # the function uses a while loop to keep iterating through the bracket until there is only one item left
    # in the bracket, which is the winner
    while len(bracket) > 1:
        event_manager()
        new_bracket = []
        for i in range(0, len(bracket), 2):
            event_manager()
            #randomly chooses a winner from the current bracket
            screen.fill("white")
            pygame.display.flip()
            picked = False
            if not type(bracket[i]) == str:
                if len(bracket[i]) == 1:
                    bracket[i].append(' ')
                if bracket[i][1] in anime_names:
                    image1 = anime_cover_surfaces[bracket[i][0]]
                    image1_rect = image1.get_rect()
                    image1_rect.topleft = (50, 0)
                    image2 = anime_cover_surfaces[bracket[i][1]]
                    image2_rect = image2.get_rect()
                    image2_rect.topleft = (300, 0)
                    screen.blit(image1, image1_rect)
                    place_text(300, 340, bracket[i][0], 20, screen)
                    place_text(300, 365, bracket[i][1], 20, screen)
                    screen.blit(image2, image2_rect)
                    pygame.display.flip()
                    while not picked:
                        event_manager()
                        if pygame.mouse.get_pressed()[0] and image1_rect.collidepoint(pygame.mouse.get_pos()):
                            picked = True
                            winner = bracket[i][0]
                        elif pygame.mouse.get_pressed()[0] and image2_rect.collidepoint(pygame.mouse.get_pos()):
                            picked = True
                            winner = bracket[i][1]

                else:
                    image1 = anime_cover_surfaces[bracket[i][0]]
                    image1_rect = image1.get_rect()
                    image1_rect.topleft = (50, 0)
                    screen.blit(image1, image1_rect)
                    pygame.display.flip()
                    while not picked:
                        event_manager()
                        if pygame.mouse.get_pressed()[0] and image1_rect.collidepoint(pygame.mouse.get_pos()):
                            picked = True
                            winner = bracket[i][0]

            else:
                image1 = anime_cover_surfaces[bracket[i]]
                image1_rect = image1.get_rect()
                image1_rect.topleft = (50, 0)
                screen.blit(image1, image1_rect)
                pygame.display.flip()
                while not picked:
                    event_manager()
                    if pygame.mouse.get_pressed()[0] and image1_rect.collidepoint(pygame.mouse.get_pos()):
                        picked = True
                        winner = bracket[i]

            #if there is another item in the bracket, it will also randomly choose a winner from that item
            if i+1 < len(bracket):
                winner = [winner, random.choice(bracket[i+1])]
            #appends the winner to the new bracket
            new_bracket.append(winner)
            pygame.time.delay(500)
        bracket = new_bracket
    return bracket[0]


def full_tournament(mini=7):
    global anime_cover_surfaces, anime_names
    # Gets a list of name using the getanimes function from the mal_api_handling module
    screen.fill("white")
    anime_list = mal_api.getanimes("shazzo", mini=mini)
    anime_names = anime_list[0]
    anime_covers = anime_list[1]

    for k, v in mal_api.get_images("shazzo", mini=mini, getanime=anime_covers).items():
        event_manager()
        anime_cover_surfaces[k] = pygame.image.load(get_image_from_web(v)).convert_alpha()

    # shuffle the list of names
    random.shuffle(anime_names)
    # divides the list of names into pairs
    bracket = [anime_names[i:i + 2] for i in range(0, len(anime_names), 2)]

    # gets the winner of the tournament
    winner = simulate_tournament(bracket)
    # if the winner is a list, it means there is a tie and the winner is the first item of the list
    while type(winner) is list:
        event_manager()
        winner = winner[0]

    print(winner)
    return True


def event_manager():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()


while True:
    event_manager()
    screen.fill("white")
    if start.draw():
        if not simulated:
            print("started")

            full_tournament()
            simulated = True
    pygame.display.flip()
