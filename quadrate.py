import os

import pygame

pygame.init()
off_white = (230, 230, 230)
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
dark_red = (200, 0, 0)
red = (255, 0, 0)
dark_orange = (200, 110, 0)
orange = (255, 165, 0)
dark_yellow = (200, 200, 0)
yellow = (255, 255, 0)

input_box = pygame.Rect(500, 100, 140, 32)

display_width = 701
display_height = 701
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Quadrant To-do List')
icon = pygame.image.load('files/box.png')
pygame.display.set_icon(icon)


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


def intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    os.system('python setup.py py2exe')
                except:
                    pass
                quit()

        files = ["files/U-I.txt", "files/NU-I.txt", "files/U-NI.txt", "files/NU-NI.txt"]

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, blue, (0, 100, 100, 300))
        pygame.draw.rect(gameDisplay, blue, (0, 400, 100, 300))
        pygame.draw.rect(gameDisplay, blue, (100, 0, 300, 100))
        pygame.draw.rect(gameDisplay, blue, (400, 0, 300, 100))
        pygame.draw.rect(gameDisplay, black, (0, 0, 100, 100))

        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 400 > cur[0] > 100 and 400 > cur[1] > 100:
            pygame.draw.rect(gameDisplay, red, (100, 100, 300, 300))
            if click[0] == 1:
                # print("Red Button")
                gameLoop(files[0])
        else:
            pygame.draw.rect(gameDisplay, dark_red, (100, 100, 300, 300))

        if cur[0] > 700 and 400 > cur[1] > 100:
            pygame.draw.rect(gameDisplay, dark_orange, (400, 100, 300, 300))
        if 700 > cur[0] > 400 > cur[1] > 100:
            pygame.draw.rect(gameDisplay, orange, (400, 100, 300, 300))
            if click[0] == 1:
                # print("Orange Button")
                gameLoop(files[1])
        else:
            pygame.draw.rect(gameDisplay, dark_orange, (400, 100, 300, 300))

        if cur[1] > 700 and 100 < cur[0] < 400:
            pygame.draw.rect(gameDisplay, dark_yellow, (100, 400, 300, 300))
        elif 100 < cur[0] < 400 < cur[1] < 700:
            pygame.draw.rect(gameDisplay, yellow, (100, 400, 300, 300))
            if click[0] == 1:
                # print("Yellow Button")
                gameLoop(files[2])
        else:
            pygame.draw.rect(gameDisplay, dark_yellow, (100, 400, 300, 300))

        if cur[0] > 700 > cur[1] > 400 or cur[1] > 700 > cur[0] > 400:
            pygame.draw.rect(gameDisplay, off_white, (400, 400, 300, 300))
        elif 700 > cur[0] > 400 < cur[1] < 700:
            pygame.draw.rect(gameDisplay, white, (400, 400, 300, 300))
            if click[0] == 1:
                # print("White Button")
                gameLoop(files[3])
        else:
            pygame.draw.rect(gameDisplay, off_white, (400, 400, 300, 300))

        pygame.draw.line(gameDisplay, black, (0, 99), (700, 99), 3)
        pygame.draw.line(gameDisplay, black, (0, 399), (700, 399), 3)
        pygame.draw.line(gameDisplay, black, (0, 699), (700, 699), 3)

        pygame.draw.line(gameDisplay, black, (99, 0), (99, 700), 3)
        pygame.draw.line(gameDisplay, black, (399, 0), (399, 700), 3)
        pygame.draw.line(gameDisplay, black, (699, 0), (699, 700), 3)

        message_to_screen("Urgent", white, 200, 40)
        message_to_screen("Not Urgent", white, 500, 40)
        message_to_screen("Important", white, 40, 200, 90)
        message_to_screen("Not Important", white, 40, 500, 90)

        for i in range(len(files)):
            # print(i)
            text_to_rect(files[i], black, i)

        pygame.display.update()


font = pygame.font.SysFont("timesnewroman", 25)


def message_to_screen(msg, color, x, y, angle=0):
    screen_text = font.render(msg, True, color)
    screen_text = pygame.transform.rotate(screen_text, angle)
    gameDisplay.blit(screen_text, [x, y])


def text_to_rect(file, color, fileNum):
    if fileNum == 0:
        x = 105
        y = 102
    elif fileNum == 1:
        x = 405
        y = 102
    elif fileNum == 2:
        x = 105
        y = 402
    else:
        x = 405
        y = 402

    f = open(file, "a+")
    f.seek(0)

    lines = []
    for line in f:
        lines.append(line.rstrip('\n'))

    for j in range(len(lines)):
        if j<=9:
            s = lines[j].split('##')
            t = s[0]

            button_text = font.render(t, True, color)
            gameDisplay.blit(button_text, [x, y + j * 30])
    f.close()


def gameLoop(name):
    print("into game loop with", name)
    text = ''
    color = red
    active = False
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False

                color = dark_red if active else red

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        f = open(name, "a+")
                        text = "\n" + text + " ##not-done"
                        f.write(text)
                        print(text)
                        text = ''

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                else:
                    if event.key == pygame.K_BACKSPACE:
                        return
        gameDisplay.fill(white)
        f = open(name, "a+")
        f.seek(0)
        lines = []
        for line in f:
            lines.append(line.rstrip('\n'))

        for j in range(len(lines)):
            s = lines[j].split('##')
            t = s[0]

            message_to_screen(t,black,30, 30 + j * 30)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        gameDisplay.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(gameDisplay, color, input_box, 2)
        pygame.display.update()

    pygame.quit()
    os.system('python setup.py py2exe')
    quit()


intro()
