import pygame
import sys
import os
import random


SIZE = (1280, 720)
FPS = 30
G = 1


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"File named '{fullname}' is not found")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Fruit(pygame.sprite.Sprite):
    def __init__(self, *group, image_name):
        super().__init__(*group)
        path = os.path.join("assets", image_name + '.png')
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000)
        self.rect.y = random.randrange(500)
    def update(self, *args):
        self.rect = self.rect.move(random.randrange(3) - 1, 
                                   random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom



def main():
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = SIZE
    screen = pygame.display.set_mode(size)

    BackGround = Background('assets/background.png', [0,0])
    screen.blit(BackGround.image, BackGround.rect)

    all_sprites = pygame.sprite.Group()
    Fruit(all_sprites, image_name='apple_full')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        all_sprites.draw(screen)
        all_sprites.update()

        # screen.blit(BackGround.image, BackGround.rect)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
