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


pygame.init()
size = width, height = SIZE
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
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
    # image = load_image("assets/apple_full.png")
    image = load_image("apple_full.png")
    # image_boom = load_image("apple_half.png")
    image_boom = load_image("apple_half.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. 
        # Это очень важно !!!
        super().__init__(group)
        self.image = Fruit.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SIZE[0])
        self.rect.y = random.randrange(SIZE[1])

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
    for _ in range(50):
        Fruit(all_sprites)
    all_sprites.draw(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
         

        all_sprites.update(event)

        # screen.blit(BackGround.image, BackGround.rect)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
