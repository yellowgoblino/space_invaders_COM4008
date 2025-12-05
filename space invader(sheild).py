import pygame

# -------------------------------------------------------
# SHIELD CLASS
# Used as protection between the player and the invaders.
# Has 3 health levels and changes image when damaged.
# -------------------------------------------------------

class Shield:
    def __init__(self, x, y):
        # Load shield images (3 health states)
        self.img_full = pygame.image.load("shield_full.png")   # 3 HP
        self.img_dmg1 = pygame.image.load("shield_dmg1.png")   # 2 HP
        self.img_dmg2 = pygame.image.load("shield_dmg2.png")   # 1 HP

        # Shield size (adjust to match visual style)
        self.w = 120
        self.h = 60

        # Starting health
        self.health = 3

        # Current image (scaled)
        self.img = pygame.transform.scale(self.img_full, (self.w, self.h))

        # For drawing + collision detection
        self.rect = pygame.Rect(x, y, self.w, self.h)

    # ---------------------------
    # Update appearance by health
    # ---------------------------
    def update_image(self):
        if self.health == 3:
            self.img = pygame.transform.scale(self.img_full, (self.w, self.h))
        elif self.health == 2:
            self.img = pygame.transform.scale(self.img_dmg1, (self.w, self.h))
        elif self.health == 1:
            self.img = pygame.transform.scale(self.img_dmg2, (self.w, self.h))

    # ---------------------------
    # Apply damage to shield
    # ---------------------------
    def take_damage(self):
        self.health -= 1

        # Prevent negative health
        if self.health < 0:
            self.health = 0

        # Update texture
        self.update_image()

        # Return True if shield should be removed
        return self.health == 0


# -------------------------------------------------------
# CREATE SHIELDS
# Places 3 shields between player and invaders.
# You can adjust spacing or quantity.
# -------------------------------------------------------

def create_shields():
    shields = []

    # Shield placement (Works with your 1000×1000 window)
    positions = [
        (200, 780),   # left shield
        (450, 780),   # middle
        (700, 780)    # right shield
    ]

    for (x, y) in positions:
        shields.append(Shield(x, y))

    return shields


# -------------------------------------------------------
# DRAW SHIELDS EACH FRAME
# Add this inside your main draw section.
# -------------------------------------------------------

def draw_shields(screen, shields):
    for shield in shields:
        screen.blit(shield.img, shield.rect)


# -------------------------------------------------------
# HANDLE COLLISIONS (PLAYER BULLETS & ENEMY BULLETS)
#
# Call this BEFORE checking bullets vs invaders.
# -------------------------------------------------------

def handle_shield_collision(shields, bullets):
    for b in bullets[:]:           # iterate over copy to allow removal
        for shield in shields[:]:
            if b.rect.colliderect(shield.rect):

                # Remove bullet on impact
                bullets.remove(b)

                # Damage shield
                destroyed = shield.take_damage()

                # Remove shield completely if health is 0
                if destroyed:
                    shields.remove(shield)

                break
