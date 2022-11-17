import random
import sys
import pygame
import time
from pygame.locals import *

screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
ground_y = screen_height * 0.9
game_images = {}
game_sounds = {}
fps = 32
pipe = 'images/pipe.png'
background = 'images/background.png'
player = 'images/yellowbird-midflap.png'
player2 = 'images/bluebird-midflap.png'
gameover = 'images/gameover.png'

if __name__ == '__main__':
    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    # Game Images
    game_images['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['message'] = pygame.image.load('images/message.png').convert_alpha()
    game_images['base'] = pygame.image.load('images/base.png').convert()
    game_images['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert(), 180),
        pygame.image.load(pipe).convert_alpha()
    )
    game_images['background'] = pygame.image.load(background).convert()
    game_images['player'] = pygame.image.load(player).convert_alpha()
    game_images['player2'] = pygame.image.load(player2).convert_alpha()
    game_images['gameover'] = pygame.image.load(gameover).convert_alpha()

    #Game Sounds
    game_sounds['die'] = pygame.mixer.Sound('audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('audio/wing.wav')

def welcomeScreen():
    player_x = int(screen_width / 8)
    player_y = int((screen_height - game_images['player'].get_height()) / 1.9)
    player2_x = int(screen_width / 7)
    player2_y = int((screen_height - game_images['player'].get_height()) / 1.5)
    message_x = int((screen_width - game_images['message'].get_width()) / 2)
    message_y = int(screen_height * 0.2)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_images['background'],(0,0))    
                screen.blit(game_images['message'],(message_x,message_y))
                screen.blit(game_images['player'],(player_x,player_y))
                screen.blit(game_images['player2'],(player2_x,player2_y))
                screen.blit(game_images['base'],(base_x,ground_y))
                pygame.display.update()
                fps_clock.tick(fps)
    

def mainGame():
    score = 0
    player_x = int(screen_width/8)
    player_y = int(screen_height/1.9)
    player2_x = int(screen_width/7)
    player2_y = int(screen_height/1.5)
    base_x = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
 
    upperPipes = [
        {'x': screen_width+200, 'y': newPipe1[0]['y']},
        {'x': screen_width+200+(screen_width/2), 'y': newPipe2[0]['y']}
    ]
 
    lowerPipes = [
        {'x': screen_width+200, 'y': newPipe1[1]['y']},
        {'x': screen_width+200+(screen_width/2), 'y': newPipe2[1]['y']}
    ]
 
    pipeVelX = -4
 
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
 
    playerFlapVel = -8
    playerFlapped = False
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    playerVelY = playerFlapVel 
                    playerFlapped = True
                    game_sounds['wing'].play()
 
        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)
        if crashTest:
            return
 
        playerMidPos = player_x + game_images['player'].get_width() / 2  
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your Score is {score}")
                game_sounds['point'].play()
 
        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
 
        if playerFlapped:
            playerFlapped = False
        playerHeight = game_images['player'].get_height()
        player_y = player_y + min(playerVelY, ground_y - player_y - playerHeight)   
 
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x']  += pipeVelX
 
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])   
 
        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)   
 
        screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        
    
        screen.blit(game_images['player'], (player_x, player_y))
        base_x -= 1
        screen.blit(game_images['base'], (base_x, ground_y))
        screen.blit(game_images['base'], (base_x + screen_width, ground_y))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (screen_width - width) / 2 
 
        for digit in myDigits:
            screen.blit(game_images['numbers'][digit], (Xoffset, screen_height * 0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        fps_clock.tick(fps)



def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y > ground_y - 25 or player_y < 0:
        game_sounds['hit'].play()
        showGameOver()
        return True
 
    for pipe in upperPipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if (player_y < pipeHeight + pipe['y']) and (abs(player_x - pipe['x']) < game_images['pipe'][0].get_width() - 15):
            game_sounds['hit'].play()
            showGameOver()
            return True
 
    for pipe in lowerPipes:
        if (player_y + game_images['player'].get_height() > pipe['y']) and (abs(player_x - pipe['x']) < game_images['pipe'][0].get_width() - 15):
            game_sounds['hit'].play()
            showGameOver()
            return True
 
    return False
 
 
def getRandomPipe():
    pipeHeight = game_images['pipe'][0].get_height()    
    offset = screen_height / 3
    y2 = offset + random.randrange(0, int(screen_height - game_images['base'].get_height() - 1.2 * offset))
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

def showGameOver():
    gameover_x = int((screen_width - game_images['gameover'].get_width()) / 2)
    gameover_y = int((screen_height - game_images['gameover'].get_width()) / 2)
    time.sleep(0.5)
    screen.blit(game_images['gameover'], (gameover_x, gameover_y))
    pygame.display.update()


while True:
    welcomeScreen()
    mainGame()


