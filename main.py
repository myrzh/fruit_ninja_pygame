import pygame
import os
import random
import sys


SIZE = (1280, 720) # unchangable
FPS = 30
FRUIT_NAMES = ['apple',
               'avocado',
               'egg',
               'mangosteen',
               'onion',
               'orange',
               'strawberry',
               'watermelon']


class Background(pygame.sprite.Sprite):
    """Background sprite definiton"""
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def terminate():
    """Kill the game process"""
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Load any image and convert it to alpha-channed if needed"""
    fullname = os.path.join('assets', name)
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
    """Fruit sprite definition"""
    def __init__(self, *group, image_name):
        super().__init__(*group)
        # path = os.path.join("assets", image_name + '.png')
        self.image = load_image(image_name + '_full' + '.png')
        self.image_half = load_image(image_name + '_half' + '.png')
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 800
        self.speed_hor = 17
        self.a_coeff = random.uniform(0.00008, 0.02)
        self.b_coeff = random.randrange(250, 1000)
        self.c_coeff = random.randrange(50, 100)
        # self.speed_ver = 5

    def parabola(self, x_arg):
        """Generate parabola using mathematical function"""
        return self.a_coeff * (x_arg - self.b_coeff) ** 2 + self.c_coeff

    def update(self, *args):
        """Update fruit sprite pos and type (sliced/not sliced)"""
        self.rect.x += self.speed_hor
        self.rect.y = self.parabola(self.rect.x)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_half
            self.clicked = True
            return True
        return False


def main():
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = SIZE
    screen = pygame.display.set_mode(size)
    wooden_background = Background('assets/background_720.png', [0, 0])

    hits = 0
    score_font = pygame.font.Font(None, 72)
    score_text = score_font.render(str(hits), True, "white")

    all_sprites = pygame.sprite.Group()
    Fruit(all_sprites, image_name=random.choice(FRUIT_NAMES))
    # for _ in range(50):
    #     Fruit(all_sprites, image_name='apple')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(wooden_background.image, wooden_background.rect)
        screen.blit(score_text, (50, 50))

        hit_on_update = all_sprites.update(event)
        print(hit_on_update)
        if hit_on_update:
            # print('hit!')
            hits += 1
            score_text = score_font.render(str(hits), True, 'white')
        
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()


# TODO:
# -- тыки чтоб расхерачить пололам штука (далее -- разрыв штука) (почти уже)
# -- много штука
# -- траектория падения штука разрыв
# -- счетчик разрыв штука
# -- партиклы от штука когда разрыв
