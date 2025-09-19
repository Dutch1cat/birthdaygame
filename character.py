import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {}
        self.load_animations("images/andrej")
        self.direction = "down"
        self.state = "idle"
        self.frame_index = 0
        self.image = self.animations["idle_down"][0]
        self.rect = self.image.get_rect(center=pos)
        self.speed = 4
        self.animation_timer = 0
        self.animation_speed = 0.15

    def load_animations(self, base_path):
        for state in ["idle", "walk"]:
            for direction in ["down", "left", "right", "up"]:
                path = os.path.join(base_path, f"{state}_{direction}")
                frames = [pygame.transform.scale(pygame.image.load(os.path.join(path, f)).convert_alpha(), (24*3, 32*3))
                          for f in sorted(os.listdir(path)) if f.endswith(".png")]
                self.animations[f"{state}_{direction}"] = frames

    def update(self, keys, dt):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
            self.state = "walk"
        elif keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
            self.state = "walk"
        elif keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
            self.state = "walk"
        elif keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
            self.state = "walk"
        else:
            self.state = "idle"
            self.frame_index = 0

        self.rect.x += dx
        self.rect.y += dy

        self.animate(dt)

    def animate(self, dt):
        key = f"{self.state}_{self.direction}"
        frames = self.animations.get(key, [])

        if not frames:
            return  # Evita crash se la lista è vuota

        # Protezione contro indice fuori range
        if self.frame_index >= len(frames):
            self.frame_index = 0

        if self.state == "walk":
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(frames)
        else:
            self.frame_index = 0

        self.image = frames[self.frame_index]

