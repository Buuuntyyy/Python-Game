import pygame


# classe qui gère le projectile du joueur
class Projectile(pygame.sprite.Sprite):

    # definir constructeur de la classe
    def __init__(self, player):
        super().__init__()
        self.velocity = 12
        self.player = player
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('bdf.png'), (50, 50)), 90)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        #vérifier si le projectile entre en collision avec un monstre

        for monster in  self.player.game.check_collision(self, self.player.game.all_monsters):
            #supprimer le projectile
            self.remove()
            #infliger dégâts aux monstres
            monster.damage(self.player.attack)

        # vérifier si le projectile est sorti de l'écran
        if self.rect.x > 1460:
            # supprimer le projectile
            self.remove()


class meteor(Projectile, pygame.sprite.Sprite):
    def __init__(self, player):
        super(meteor, self).__init__(player)
        self.velocity = 12
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('meteorite.png'), (70, 70)), 45)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80

    def move(self):
        self.rect.x += self.velocity
        # vérifier si le projectile entre en collision avec un monstre

        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            # infliger dégâts aux monstres
            monster.damage(self.player.attack_spe)

        # vérifier si le projectile est sorti de l'écran
        if self.rect.x > 1460:
            # supprimer le projectile
            self.remove()


    def remove(self):
        self.player.all_projectiles.remove(self)