import pygame
import projectiles


class Player(pygame.sprite.Sprite):
    def __init__(self, game, health=100, max_health=100, attack=10, velocity=2):
        super(Player, self).__init__()
        self.image = pygame.image.load('mage.png')
        self.image = pygame.transform.scale(pygame.image.load('guerrier.png'), (200, 160))
        self.rect = self.image.get_rect()
        self.rect.y = 300
        self.game = game
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.velocity = velocity
        self.all_projectiles = pygame.sprite.Group()

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            #si le joueur n'a plus de points de vie
            self.game.game_over()

    def update_health_bar(self, surface):

        # dessiner la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 20, self.rect.y, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 20, self.rect.y, self.health, 5])

    def move_right(self):
        # le déplacement ne se fait que si le joueur n'est pas en collision avec un monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def launch_projectile(self):
        self.all_projectiles.add(projectiles.Projectile(self))

    def launch_meteor(self):
        self.all_projectiles.add(projectiles.meteor(self))


class Sorcier(Player):

    def __init__(self, game, health=150, max_health=150, attack=13, velocity=6):
        super(Sorcier, self).__init__(game)
        self.image = pygame.image.load('mage.png')
        self.image = pygame.transform.scale(pygame.image.load('mage.png'), (200, 160))
        self.rect = self.image.get_rect()
        self.rect.y = 375
        self.game = game
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.attack_spe = 1.5
        self.velocity = velocity
