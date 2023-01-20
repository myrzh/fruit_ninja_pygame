import os
import random
import sys

import pygame

SIZE = (1280, 720)
FPS = 30
G = 1


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def terminate():
    pygame.quit()
    sys.exit()


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
    def __init__(self, *group, image_name):
        super().__init__(*group)
        # path = os.path.join("assets", image_name + '.png')
        self.image = pygame.image.load(os.path.join("assets", image_name + '_full' + '.png'))
        self.image_half = pygame.image.load(os.path.join("assets", image_name + '_half' + '.png'))
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 800
        self.speed_hor = 17
        self.a_coeff = random.uniform(0.00008, 0.02)
        self.b_coeff = random.randrange(250, 1000)
        self.c_coeff = random.randrange(50, 100)
        # self.speed_ver = 5

    def parabola(self, x):
        return self.a_coeff * (x - self.b_coeff) ** 2 + self.c_coeff


    def update(self, *args):
        self.rect.x += self.speed_hor
        self.rect.y = self.parabola(self.rect.x)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_half
            self.clicked = True


def main():
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = SIZE
    screen = pygame.display.set_mode(size)

    BackGround = Background('assets/background_720.png', [0, 0])

    all_sprites = pygame.sprite.Group()
    Fruit(all_sprites, image_name='apple')
    # for _ in range(50):
    #     Fruit(all_sprites, image_name='apple')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        all_sprites.update(event)

        screen.blit(BackGround.image, BackGround.rect)
        all_sprites.draw(screen)

        # screen.blit(BackGround.image, BackGround.rect)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()


# TODO:
# -- тыки чтоб расхерачить пололам штука (далее -- разрыв штука)
# -- много штука
# -- разные штука (картинка есть)
# -- траектория падения штука разрыв
# -- счетчик разрыв штука
