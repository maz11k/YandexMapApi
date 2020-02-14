import os
import sys
import pygame
import requests

response = None
z = 9
l = "map"
ll = [37.622498, 55.753227]
link = "https://static-maps.yandex.ru/1.x/"

pygame.init()
screen = pygame.display.set_mode((600, 450))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEUP] and z < 19:
        z += 1
    elif keys[pygame.K_PAGEDOWN] and z > 2:
        z -= 1

    params = {
        "ll": str(ll[0]) + "," + str(ll[1]),
        "z": str(z),
        "l": l
    }

    response = requests.get(link, params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)
pygame.quit()
