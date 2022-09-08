from states import *

'''
    Polish ideas:
        - animate the cauldron
        - animate the lights
        - make the skull blink
        - animate some flies over the poo
    
    TODO:
        - make it so you have to click a little circle on the base to make a new glass jar appear
        - implement customer behavior
'''

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    WIDTH, HEIGHT = screen.get_size()
    stateManager.run(screen, events)

    pygame.display.flip()
    fpsClock.tick()