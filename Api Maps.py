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
input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
font = pygame.font.Font(None, 32)
color = color_inactive
active = False
text = ''
screen = pygame.display.set_mode((600, 450))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEUP] and z < 19:
        z += 1
    elif keys[pygame.K_PAGEDOWN] and z > 2:
        z -= 1
    elif keys[pygame.K_RIGHT]:
        if 19 >= z > 15:
            ll[0] += 0.001
        elif 15 >= z > 10:
            ll[0] += 0.01
        elif 10 >= z > 8:
            ll[0] += 0.1
        elif 8 >= z > 4:
            ll[0] += 1
        else:
            ll[0] += 7
    elif keys[pygame.K_LEFT]:
        if 19 >= z > 15:
            ll[0] -= 0.001
        elif 15 >= z > 10:
            ll[0] -= 0.01
        elif 10 >= z > 8:
            ll[0] -= 0.1
        elif 8 >= z > 4:
            ll[0] -= 1
        else:
            ll[0] -= 7
    elif keys[pygame.K_UP]:
        if 19 >= z > 15:
            ll[1] += 0.001
        elif 15 >= z > 10:
            ll[1] += 0.01
        elif 10 >= z > 8:
            ll[1] += 0.1
        elif 8 >= z > 4:
            ll[1] += 1
        else:
            ll[1] += 7
    elif keys[pygame.K_DOWN]:
        if 19 >= z > 15:
            ll[1] -= 0.001
        elif 15 >= z > 10:
            ll[1] -= 0.01
        elif 10 >= z > 8:
            ll[1] -= 0.1
        elif 8 >= z > 4:
            ll[1] -= 1
        else:
            ll[1] -= 7
    elif keys[pygame.K_m]:
        l = "map"
    elif keys[pygame.K_s]:
        l = "sat"
    elif keys[pygame.K_g]:
        l = "sat,skl"
    elif keys[pygame.K_p]:
        l = "map,trf"

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
    screen.fill((30, 30, 30))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.display.flip()
    os.remove(map_file)
pygame.quit()
