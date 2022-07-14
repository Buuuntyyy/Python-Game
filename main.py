from turtle import textinput
import Game
import sys
import pygame

pygame.init()


# charger notre jeu
game = Game.game()
FPS = 100
#définir une clock
clock = pygame.time.Clock()
sys.setrecursionlimit(10000)


# création de la fenêtre
pygame.display.set_caption("Project XXX")
screen = pygame.display.set_mode((1460, 720))

# background
background = pygame.image.load('Forest1.jpg')

#importer la bannière
banner = pygame.image.load('banniere.png')
banner = pygame.transform.scale(banner, (1000, 600))
banner_rect = banner.get_rect()
banner_rect.x = screen.get_width() / 6.5

#importer le bouton de lancement

play_button = pygame.image.load('button.png')
play_button = pygame.transform.scale(play_button, (275, 275))
play_button_rect = play_button.get_rect()
play_button_rect.x = screen.get_width() / 2.65
play_button_rect.y = screen.get_height() / 4

#importer le bouton créer compte
create_new = pygame.image.load('nouveau.png')
create_new = pygame.transform.scale(create_new, (80, 80))
create_new_rect = create_new.get_rect()
create_new_rect.x = screen.get_width() / 6
create_new_rect.y = screen.get_height() / 1.5

#importer le bouton connexion
connexion_button = pygame.image.load('connexion.png')
connexion_button = pygame.transform.scale(connexion_button, (80, 80))
connexion_button_rect = connexion_button.get_rect()
connexion_button_rect.x = screen.get_width() / 1.35
connexion_button_rect.y = screen.get_height() / 1.5

# Importer l'icone magasin
shop = pygame.image.load('boutique_icon.png')
shop_button = pygame.transform.scale(shop, (100, 100))
shop_button_rect = shop_button.get_rect()
shop_button_rect.x = screen.get_width() / 2.3
shop_button_rect.y = screen.get_height() / 1.55

#importer la boutique
shop = pygame.image.load('boutique.png')
shop_surface = pygame.transform.scale(shop, (760, 720))
shop_surface_rect = shop_surface.get_rect()
shop_surface_rect.x = screen.get_width() / 5
shop_surface_rect.y = screen.get_height() / 50

#importer la croix de la boutique
croix = pygame.image.load('croix.png')
croix_surface = pygame.transform.scale(croix, (25, 25))
croix_rect = croix.get_rect()
croix_rect.x = screen.get_width() / 1.60
croix_rect.y = screen.get_height() / 8.25


def afficher_background():
    screen.blit(banner, banner_rect)
    screen.blit(play_button, play_button_rect)
    screen.blit(create_new, create_new_rect)
    screen.blit(connexion_button, connexion_button_rect)
    screen.blit(shop_button, shop_button_rect)
    pygame.display.flip()


running = True

while running is True:

    # fixer le nombre de fps sur la clock
    clock.tick(FPS)

    # appliquer la fenêtre du jeu
    screen.blit(pygame.transform.scale(background, (1460, 720)), (0, 0))

    #vérifier si le jeu a commencé
    if game.is_playing:
        #déclencher la partie
        game.update(screen)
    else:
        #ajouter l'écran de démarrage
        screen.blit(banner, (banner_rect))
        screen.blit(play_button, play_button_rect)
        screen.blit(create_new, create_new_rect)
        screen.blit(connexion_button, connexion_button_rect)
        screen.blit(shop_button, shop_button_rect)
        if game.goto:
            screen.blit(shop_surface, shop_surface_rect)
            screen.blit(croix_surface, croix_rect)
        elif game.close:
            print('okok')
            afficher_background()
        else:
            pass
            

    # mettre à jour l'écran
    pygame.display.flip()

    # si on ferme
    for event in pygame.event.get():
        # event fermeture fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # détcter si la touche est enclenchée pour envoyer le projectile
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()
            elif event.key == pygame.K_m:
                if game.get_nb_meteor() > 0:
                    game.update_nb_meteor()
                    game.player.launch_meteor()
                else:
                    print("Vous n'avez plus de météors !")
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #vérifier si la souris est en collision avec le bouton de lancement
            if play_button_rect.collidepoint(event.pos):
                #lancer le jeu
                game.start()
            elif create_new_rect.collidepoint(event.pos): #sinon si la souris est sur create_button
                print('ok')
                game.create_compte()
            elif connexion_button_rect.collidepoint(event.pos): #sinon si la souris est sur connexion_button
                game.connexion_compte()
            elif shop_button_rect.collidepoint(event.pos):
                game.go_to_shop()
            elif croix_rect.collidepoint(event.pos):
                print('ok')
                game.quit_shop()
