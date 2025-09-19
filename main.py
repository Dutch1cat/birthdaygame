import pygame
import random
from character import Player
from battle import Battle

pygame.init()
screen = pygame.display.set_mode((1120, 800))
clock = pygame.time.Clock()

# === Mappa ===
base_tile = pygame.image.load("images/bg/background.png").convert_alpha()
base_tile = pygame.transform.scale(base_tile, (32, 32))
you_won = False
win_timer = 0


def random_green():
    r = random.randint(0, 50)
    g = random.randint(150, 255)
    b = random.randint(0, 50)
    return (r, g, b)

def apply_green_mask(tile):
    mask_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    for _ in range(random.randint(5, 15)):
        x = random.randint(0, 31)
        y = random.randint(0, 31)
        radius = random.randint(2, 6)
        pygame.draw.circle(mask_surface, random_green() + (80,), (x, y), radius)
    tile.blit(mask_surface, (0, 0))
    return tile

map_tiles = []
for row in range(25):
    map_row = []
    for col in range(35):
        tile = base_tile.copy()
        tile = apply_green_mask(tile)
        map_row.append(tile)
    map_tiles.append(map_row)

# === Personaggio ===
player = Player(pos=(400, 300))
all_sprites = pygame.sprite.Group(player)

# === Dischi ===
disk_colors = ["red", "blue", "green", "purple"]
disk_positions = [(32, 32), (1056, 32), (32, 736), (1056, 736)]
disk_sprites = []
collected_disks = []

for color, pos in zip(disk_colors, disk_positions):
    idle_img = pygame.image.load(f"images/{color}_disk/frame_0.png").convert_alpha()
    idle_img = pygame.transform.scale(idle_img, (64, 64))
    rect = idle_img.get_rect(topleft=pos)
    disk_sprites.append({"color": color, "image": idle_img, "rect": rect, "active": True})

# === Battle ===
battle = None
in_battle = False
battle_color = None

# === Font ===
font = pygame.font.SysFont(None, 32)

# === Loop principale ===
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if in_battle:
        battle.update(dt, keys)
        if battle.finished:
            if battle.won and battle_color not in collected_disks:
                collected_disks.append(battle_color)
            else:
                # Riattiva il disco se hai perso
                for disk in disk_sprites:
                    if disk["color"] == battle_color:
                        disk["active"] = True
                        break
                player.rect.center = (400, 300)  # Reset position on loss
            in_battle = False
            battle = None
            battle_color = None
            
    else:
        all_sprites.update(keys, dt)

        # Check collision with disks
        for disk in disk_sprites:
            if disk["active"] and player.rect.colliderect(disk["rect"]):
                disk["active"] = False
                in_battle = True
                battle_color = disk["color"]
                battle = Battle(screen, battle_color)
                break
    
    if len(collected_disks) == 4 and not you_won:
        you_won = True
        win_timer = pygame.time.get_ticks()
    # === Drawing ===
    screen.fill((0, 0, 0))

    # Mappa
    for row_idx, row in enumerate(map_tiles):
        for col_idx, tile in enumerate(row):
            screen.blit(tile, (col_idx * 32, row_idx * 32))

    if in_battle:
        battle.draw()
    else:
        # Dischi
        for disk in disk_sprites:
            if disk["active"]:
                screen.blit(disk["image"], disk["rect"])

        # Personaggio
        all_sprites.draw(screen)

        # Contatore dischi
        text = font.render(f"collected disks: {len(collected_disks)}/4", True, (255, 255, 255))
        screen.blit(text, (20, 20))
    
    if you_won:
        win_text = font.render("YOU WON!", True, (255, 255, 0))
        big_font = pygame.font.SysFont(None, 120)
        win_text = big_font.render("YOU WON!", True, (255, 255, 0))
        text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(win_text, text_rect)

        if pygame.time.get_ticks() - win_timer >= 3000:
            raise SystemExit("you won!")

    pygame.display.flip()
    print(clock.get_fps())

pygame.quit()
