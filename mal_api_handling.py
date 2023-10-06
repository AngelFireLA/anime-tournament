import requests, pygame, sys
pygame.init()


def event_manager():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()


def get_score(anime: list):
    return int(anime["list_status"]["score"])


def get_name(anime: list):
    return anime["node"]["title"]


def mal_request(pseudo):
    CLIENT_ID = '5a433618d10417e64a676117051f6c86'

    url = f'https://api.myanimelist.net/v2/users/{pseudo}/animelist?fields=list_status&limit=999&status=completed'

    response = requests.get(url, headers={
        'X-MAL-CLIENT-ID': CLIENT_ID
    })

    response.raise_for_status()
    anime_list = response.json()
    response.close()
    return anime_list


def getanimes(pseudo, score=False, mini=1):
    anime_list = mal_request(pseudo)
    actual_anime_list = []
    named_anime_list = []
    for anime in anime_list['data']:
        event_manager()
        if score:
            if get_score(anime) >= mini:
                named_anime_list.append({"name": get_name(anime), "score": get_score(anime)})
                actual_anime_list.append(anime)
        else:
            if get_score(anime) >= mini:
                named_anime_list.append(get_name(anime))
                actual_anime_list.append(anime)
    return named_anime_list, actual_anime_list


def get_images(pseudo, mini=8, getanime=None):
    if not getanime:
        actual_anime_list = getanimes(pseudo, mini=mini)[1]
    else:
        actual_anime_list = getanime
    anime_covers = {}
    for anime in actual_anime_list:
        event_manager()
        anime_covers[get_name(anime)] = anime["node"]["main_picture"]["medium"]

    return anime_covers

