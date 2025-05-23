import pygame, pytmx, sys
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Jungle Run ") 
clock = pygame.time.Clock()

# Load sound and music
pygame.mixer.music.load('assets/sounds/bg_music.mp3')
pygame.mixer.music.play(-1)
jump_sfx = pygame.mixer.Sound('assets/sounds/jump.wav')
walk_sfx = pygame.mixer.Sound('assets/sounds/walk.wav')

# Load map
tmx_data = pytmx.load_pygame('assets/mymap.tmx')
tile_width, tile_height = tmx_data.tilewidth, tmx_data.tileheight

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle = pygame.image.load('assets/player/idle.png')
        self.run = [pygame.image.load(f'assets/player/run{i}.png') for i in (1, 2)]
        self.jump = pygame.image.load('assets/player/jump.png')
        self.image = self.idle
        self.rect = self.image.get_rect(topleft=(50, 500))
        self.vel_y = 0
        self.on_ground = True
        self.frame = 0
        self.score = 0

    def update(self, keys):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
            self.animate()
            walk_sfx.play()
        elif keys[pygame.K_RIGHT]:
            dx = 5
            self.animate()
            walk_sfx.play()
        else:
            self.image = self.idle

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            jump_sfx.play()
            self.on_ground = False
            self.image = self.jump

        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= 550:
            self.rect.bottom = 550
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx

    def animate(self):
        self.frame = (self.frame + 1) % len(self.run)
        self.image = self.run[self.frame]

def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_width, y * tile_height))

def show_text(text, y):
    font = pygame.font.SysFont(None, 60)
    surf = font.render(text, True, (255, 255, 255))
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)

# Scenes
def start_screen():
    while True:
        screen.fill((0, 100, 0))
        show_text("🌴 Jungle Run 🌴", 200)
        show_text("Press SPACE to Start", 300)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def end_screen(score):
    while True:
        screen.fill((0, 50, 0))
        show_text("🎉 You Win! 🎉", 200)
        show_text(f"Score: {score}", 300)
        show_text("Press ESC to Exit", 400)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

# Run Game
start_screen()
player = Player()
group = pygame.sprite.Group(player)

while True:
    screen.fill((0, 0, 0))
    draw_map()
    keys = pygame.key.get_pressed()
    group.update(keys)
    group.draw(screen)

    player.score += 1
    if player.rect.x >= 700:
        end_screen(player.score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
