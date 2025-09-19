import pygame
import random
import sys
import os
def resource_path(relative_path):
    """Restituisce il path assoluto al file, compatibile con PyInstaller."""
    try:
        # Se l'app è impacchettata con PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Se stai eseguendo da sorgente
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Battle:
    def __init__(self, screen, disk_color):
        self.screen = screen
        self.disk_color = disk_color

        self.heart_img = pygame.transform.scale(pygame.image.load(resource_path("images/andrej/heart/heart.png")).convert_alpha(), (32, 32))
        self.note_img = pygame.transform.scale(pygame.image.load(resource_path("images/disk_attack/note.png")).convert_alpha(), (32, 32))
        self.disk_img = pygame.transform.scale(pygame.image.load(resource_path(f"images/{disk_color}_disk/frame_1.png")).convert_alpha(), (64, 64))

        self.heart_rect = pygame.Rect(100, 300, 32, 32)
        self.heart_speed = 4
        self.heart_health = 3
        self.heart_alive = True

        self.arena_rect = pygame.Rect(80, 200, 200, 200)

        self.notes = []
        self.note_spawn_timer = 0
        self.note_spawn_interval = 0.5

        self.phase = "attack"
        self.phase_timer = 0
        self.attack_duration = 15

        self.bar_active = False
        self.bar_rect = pygame.Rect(80, 420, 200, 20)
        self.bar_moving = pygame.Rect(80, 420, 20, 20)
        self.bar_target = pygame.Rect(150, 420, 30, 20)
        self.bar_direction = 1

        self.disc_health = 100
        self.font = pygame.font.SysFont(None, 24)

        self.finished = False
        self.won = False

    def update(self, dt, keys):
        if not self.heart_alive:
            self.finished = True
            self.won = False
            return

        if self.disc_health <= 0:
            self.finished = True
            self.won = True
            return

        if self.phase == "attack":
            self.phase_timer += dt
            self.move_heart(keys)
            self.spawn_notes(dt)
            self.move_notes()
            self.check_collisions()

            if self.phase_timer >= self.attack_duration:
                self.phase = "strike"
                self.bar_active = True
                self.phase_timer = 0

        elif self.phase == "strike":
            self.move_bar()
            if keys[pygame.K_SPACE]:
                if self.bar_moving.colliderect(self.bar_target):
                    self.disc_health -= 25
                self.notes.clear()
                self.bar_active = False
                self.phase = "attack"
                self.phase_timer = 0
                self.bar_moving.x = self.bar_rect.x
                self.bar_direction = 1

    def move_heart(self, keys):
        if keys[pygame.K_w] and self.heart_rect.top > self.arena_rect.top:
            self.heart_rect.y -= self.heart_speed
        if keys[pygame.K_s] and self.heart_rect.bottom < self.arena_rect.bottom:
            self.heart_rect.y += self.heart_speed
        if keys[pygame.K_a] and self.heart_rect.left > self.arena_rect.left:
            self.heart_rect.x -= self.heart_speed
        if keys[pygame.K_d] and self.heart_rect.right < self.arena_rect.right:
            self.heart_rect.x += self.heart_speed

    def spawn_notes(self, dt):
        self.note_spawn_timer += dt
        if self.note_spawn_timer >= self.note_spawn_interval:
            self.note_spawn_timer = 0
            y = random.randint(self.arena_rect.top, self.arena_rect.bottom - 32)
            note_rect = pygame.Rect(700, y, 32, 32)
            self.notes.append(note_rect)

    def move_notes(self):
        for note in self.notes:
            note.x -= 5
        self.notes = [note for note in self.notes if note.right > 0]

    def check_collisions(self):
        for note in self.notes:
            if self.heart_rect.colliderect(note):
                self.heart_health -= 1
                self.notes.remove(note)
                if self.heart_health <= 0:
                    self.heart_alive = False

    def move_bar(self):
        self.bar_moving.x += self.bar_direction * 5
        if self.bar_moving.right >= self.bar_rect.right or self.bar_moving.left <= self.bar_rect.left:
            self.bar_direction *= -1

    def draw(self):
        # Arena
        pygame.draw.rect(self.screen, (0, 0, 0), self.arena_rect, 2)

        # Heart
        if self.heart_alive:
            self.screen.blit(self.heart_img, self.heart_rect)

        # Heart health
        health_text = self.font.render(f"Player life: {self.heart_health}", True, (255, 100, 100))
        self.screen.blit(health_text, (80, 180))

        # Notes
        for note in self.notes:
            self.screen.blit(self.note_img, note)

        # Disc image
        self.screen.blit(self.disk_img, (700 - 32, 300 - 32))

        # Disc health bar
        pygame.draw.rect(self.screen, (255, 0, 0), (660, 250, 80, 10))
        pygame.draw.rect(self.screen, (0, 255, 0), (660, 250, int(80 * (self.disc_health / 100)), 10))

        # Strike bar
        if self.bar_active:
            pygame.draw.rect(self.screen, (100, 100, 100), self.bar_rect)
            pygame.draw.rect(self.screen, (255, 255, 0), self.bar_target)
            pygame.draw.rect(self.screen, (255, 0, 0), self.bar_moving)
