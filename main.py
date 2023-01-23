import pygame
import os
import random
import sys
import sqlite3


SIZE = (1280, 720) # unchangable
FPS = 30
SPAWN_RATE = 2000 # ms
FRUIT_SIDE = 180 # pixels
GRAVITY = 1
SOUNDS_COUNT = 12
HITS = 0

pygame.init()
score_font = pygame.font.Font(None, 72)
score_text = score_font.render(str(HITS), True, "white")


class Background(pygame.sprite.Sprite):
    """Background sprite definiton"""
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def terminate():
    """Kill the game process"""
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Load any image and convert it to alpha-channed if needed"""
    fullname = os.path.join('assets', 'images', name)
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


def load_random_sound():
    return os.path.join('assets', 'sounds', str(random.randrange(1, SOUNDS_COUNT + 1)) + '.mp3')


def get_fruits(db_path):
    """Get fruit names from database"""
    fruits_db_con = sqlite3.connect(db_path)
    cur = fruits_db_con.cursor()
    result = cur.execute("SELECT filename_full, filename_half FROM fruits_table").fetchall()
    return result

FRUIT_NAMES = get_fruits('assets/fruits.db')


def update_score(arg):
    """Update score func"""
    global HITS
    global score_text
    if arg == 'increment':
        HITS += 1
    elif arg == 'zero':
        HITS = 0
    score_text = score_font.render(str(HITS), True, "white")


class Fruit(pygame.sprite.Sprite):
    """Fruit sprite definition"""
    def __init__(self, *group, filename_full, filename_half):
        super().__init__(*group)

        self.image = load_image(filename_full)
        self.image = pygame.transform.scale(self.image, (FRUIT_SIDE, FRUIT_SIDE))
        self.image_half = load_image(filename_half)
        self.image_half = pygame.transform.scale(self.image_half, (FRUIT_SIDE, FRUIT_SIDE))
        self.workaround_group = group
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 800

        self.speed_hor = 17
        self.a_coeff = random.uniform(0.0001, 0.02)
        self.b_coeff = random.randrange(250, 1000)
        self.c_coeff = random.randrange(50, 300)
        self.hitted = False
        self.hit_x_pos = 0

    def parabola(self, x_arg):
        """Generate parabola using mathematical function"""
        return self.a_coeff * (x_arg - self.b_coeff) ** 2 + self.c_coeff

    def create_particles(self, position):
        """Generate particles with random size and speed"""
        particle_count = 20
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers), *self.workaround_group)


    def update(self, *args):
        """Update fruit sprite pos and type (sliced/not sliced)"""
        if self.rect.x > 2 * SIZE[0] // 3 and self.rect.y > 800:
            if not self.hitted:
                update_score('zero')
            self.kill()
        self.rect.x += self.speed_hor
        self.rect.y = self.parabola(self.rect.x)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hitted:
                update_score('increment')
                sound_path = load_random_sound()
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                self.hit_x_pos = self.rect.x
            self.hitted = True
            self.image = self.image_half
            if self.rect.x - self.hit_x_pos < 150:
                self.create_particles((self.rect.x + (FRUIT_SIDE // 2), self.rect.y + (FRUIT_SIDE // 2)))
        return False


screen_rect = (0, 0, SIZE[0], SIZE[1])

class Particle(pygame.sprite.Sprite):
    """Particle sprite definition"""
    def __init__(self, pos, dx, dy, *group):
        super().__init__(*group)
        self.fire = [load_image("particle.png")]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self, event):
        """Update particle speed and pos values"""
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def main():
    """Define main game behavior"""
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)
    wooden_background = Background('background_720.png', [0, 0])

    pygame.mixer.pre_init(frequency=48000, size=-16, channels=1, buffer=512)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)

    all_sprites = pygame.sprite.Group()
    
    FRUITEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(FRUITEVENT, SPAWN_RATE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == FRUITEVENT:
                fruit_tuple = random.choice(FRUIT_NAMES)
                Fruit(all_sprites, filename_full=fruit_tuple[0], filename_half=fruit_tuple[1])

        screen.blit(wooden_background.image, wooden_background.rect)
        screen.blit(score_text, (50, 50))

        all_sprites.update(event)
        clock.tick(FPS)
        all_sprites.draw(screen)
        pygame.display.update()
        

if __name__ == '__main__':
    main()
