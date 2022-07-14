import pygame
from comet_fall import Comet

class CometFallEvent(pygame.sprite.Sprite):

    def __init__(self, game):
        super(CometFallEvent, self).__init__()
        self.percent = 0
        self.percent_speed = 100
        self.game = game
        #définir un groupe pour nos comètes
        self.all_cometes_fall = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed / 100

    def is_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0

    def comete_fall(self):
        self.all_cometes_fall.add(Comet(self))

    def attempt_fall(self):
        if self.is_loaded():
            self.comete_fall()
            self.reset_percent()
            #self.comete_fall()

    def update_event(self, surface):
        #ajouter du pourcentage à la barre
        self.add_percent()

        #appel de la méthode pour déclencher la pluie
        self.attempt_fall()

        pygame.draw.rect(surface, (0, 0, 0), [0, surface.get_height() - 40, surface.get_width(), 25])
        pygame.draw.rect(surface, (255, 0, 0), [0, surface.get_height() - 40, (surface.get_width() / 100) * self.percent, 25])
