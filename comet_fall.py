import pygame
import random


class Comet(pygame.sprite.Sprite):
    
    def __init__(self, comet_event):
        super(Comet, self).__init__()
        #image de la comete
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('comete_fall.png'), (85, 85)), 45)
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(-50, 50)
        self.rect.x = random.randint(-10, 1500)
        self.velocity = random.randint(1, 3)
        self.comet_event = comet_event

    def remove(self):
        self.comet_event.all_cometes_fall.remove(self)

    def fall(self):
        self.rect.y += self.velocity

        if self.rect.y >= 500:
            self.remove()

        elif self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            self.remove()
            #subir des dégats
            self.comet_event.game.player.damage(20)