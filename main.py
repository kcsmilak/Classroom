import pygame
import helpers

pygame.init()


WIDTH = 600
HEIGHT = 480

class Player():
    def __init__(self):
        self.color = (0,0,255)
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.airborn = False

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)



debugui = helpers.DebugUI()
keyboard = helpers.Keyboard()
player = Player()

NORMAL_SPEED = 3
JUMP_BOOST = 30
TERMINAL_VELOCITY = 30
GRAVITY = 1.5

screen = pygame.display.set_mode((WIDTH, HEIGHT))

run = True
while run:

    pygame.time.Clock().tick(60)  

    
    # Handle Input
    # - needs keyboard
    for event in pygame.event.get():       
        if event.type == pygame.QUIT:
            run = False
        elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
            keyboard.handleEvent(event)


    # Update World
    # - needs keyboard, player, world objects
    dx = 0
    if (keyboard.d and not keyboard.a):
        dx += NORMAL_SPEED
        if (keyboard.s): dx = dx // 3
    elif (keyboard.a and not keyboard.d):
        dx -= NORMAL_SPEED
        if (keyboard.s): dx = dx // 3
     
    dy = player.y_vel
    if (keyboard.w and not keyboard.s and not player.airborn):
        dy -= JUMP_BOOST
        player.airborn = True


    # Add Gravity
    dy += GRAVITY
    if dy > TERMINAL_VELOCITY: dy = TERMINAL_VELOCITY

    # Test Collision
    crash = False
    if (player.rect.bottom + dy > HEIGHT):
        player.airborn = False
        player.rect.bottom = HEIGHT
        dy = 0
    debugui.data['crash'] = crash


    player.rect.x += dx
    player.rect.y += dy

    player.y_vel = dy

    debugui.data['x'] = player.rect.x
    debugui.data['y'] = player.rect.y
    debugui.data['bottom'] = player.rect.bottom
    debugui.data['dx'] = dx
    debugui.data['dy'] = dy
    debugui.data['x_vel'] = player.x_vel
    debugui.data['y_vel'] = player.y_vel
    debugui.data['fps'] = pygame.time.Clock().get_fps()

    debugui.data['up'] = keyboard.up
    debugui.data['down'] = keyboard.down
    
    
    debugui.update()

    # Render

    screen.fill((100,100,100))
    player.draw(screen)
    debugui.draw(screen)

    pygame.display.update()
