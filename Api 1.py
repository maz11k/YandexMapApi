import os
import sys
import pygame
import requests

response = None
params = {
    "ll": "37.622498,55.753227",
    "z": "9",
    "l": "map"
}
link = "https://static-maps.yandex.ru/1.x/"
response = requests.get(link, params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)


map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)
