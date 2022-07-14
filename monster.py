import pygame
import random


class Monster(pygame.sprite.Sprite):

    _count=0
    def __init__(self, game, health, max_health, attack, velocity):
        super(Monster, self).__init__()
        self.game = game
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.velocity = velocity
        self.loot_amount = 1

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = self.velocity

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def forward(self):
        # le deplacement ne se fait que si il n'y a pas de collision avec un joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
            #si le monstre est en collision avec le joueur
        else:
            #infliger degats au joueur
            self.game.player.damage(self.attack)

    @staticmethod
    def get_count():
        return Monster._count

    def damage(self, amount):
        #infliger des dégâts
        self.health -= amount

        #vérifier si il est tjrs en vie (0<=)
        if self.health <= 0:
            #supprimer le monstre quand il meurt
            self.game.all_monsters.remove(self)
            #réapparaître comme un nouveau monstre
            #self.rect.x = 1000 + random.randint(0, 500)
            #self.velocity = random.randint(0, 10) / 10
            #self.health = self.max_health
            Monster._count += 1
            #ajouter le nombre de point
            self.game.add_score(self.loot_amount)
            #print(self.get_count())
            if self.get_count() == self.game._nb_tot:
                #print("game start")
                self.game.start()
            else:
                pass

    def update_health_bar(self, surface):

        # dessiner la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x, self.rect.y, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x, self.rect.y, self.health, 5])


class Mob_F(Monster, pygame.sprite.Sprite):

    def __init__(self, game, health=50, max_health=50, attack=2, velocity=1.2+(random.randint(0, 10) / 10)):
        super(Mob_F, self).__init__(game, health, max_health, attack, velocity)
        self.image = pygame.transform.scale(pygame.image.load('monstre(4).png'), (100, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 1000)
        self.rect.y = 450
        self.set_loot_amount(1)


class Mob_M(Monster, pygame.sprite.Sprite):

    def __init__(self, game, health=65, max_health=65, attack=3, velocity=1.5):
        super(Mob_M, self).__init__(game, health, max_health, attack, velocity)
        self.image = pygame.transform.scale(pygame.image.load('monstre(2).png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 1200 + random.randint(0, 1000)
        self.rect.y = 450
        self.set_loot_amount(3)


class Mob_D(Monster, pygame.sprite.Sprite):

    def __init__(self, game, health=65, max_health=65, attack=5, velocity=1):
        super(Mob_D, self).__init__(game, health, max_health, attack, velocity)
        self.image = pygame.transform.scale(pygame.image.load('monstre(1).png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 450
        self.set_loot_amount(5)


class Warrior(Monster, pygame.sprite.Sprite):
    def __init__(self, game, health=400, max_health=400, attack=5, velocity=0.5):
        super(Warrior, self).__init__(game, health, max_health, attack, velocity)
        self.image = pygame.transform.scale(pygame.image.load('ogre.png'), (260, 260))
        self.rect = self.image.get_rect()
        self.rect.x = 1250 + random.randint(0, 300)
        self.rect.y = 350
        self.game = game
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.velocity = velocity
        self.set_loot_amount(10)
