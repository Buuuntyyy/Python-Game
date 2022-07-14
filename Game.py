import random
import pygame
import Player
import monster
import sqlite3
from comet_event import CometFallEvent

#importer l'image de la bdf spéciale :
bdf = pygame.image.load('bdf.png')
bdf = pygame.transform.scale(pygame.transform.rotate(bdf, 90), (60, 60))
bdf_rect = bdf.get_rect()
bdf_rect.x = 150
bdf_rect.y = 0

# classe du jeu
class game:
    _nb_tot = 0
    _nb_tospawn_mob = 20
    _bonus_wave = 10
    _nb_mob_next = 0
    _last_wave = 0
    _compte_location = 0
    _pseudo = ''
    _classement = 0
    _text = []
    _classement = []
    _nb_meteor = 25
    goto = False
    to_connect = False
    close = False


    def __init__(self):
        #définir si le jeu a commencé
        self.is_playing = False
        # générer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player.Sorcier(self)
        self.all_players.add(self.player)
        #generer la pluie de comete
        self.comet_event = CometFallEvent(self)
        # groupe de mob
        self.all_monsters = pygame.sprite.Group()
        #mettre le score à 0
        self.font = pygame.font.Font("policy/Mohave-Bold.ttf", 25)
        self.score = 0
        self.pressed = {}
        self.bonus_attack = 0
        # importer bannière (bouton de connexion/création compte)
        self.banner = pygame.image.load('banniere.png')
        self.banner = pygame.transform.scale(self.banner, (1000, 600))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = 1080 / 6.5
        # Importer magasin
        self.shop = pygame.image.load('boutique_icon.png')
        self.shop = pygame.transform.scale(self.shop, (200, 200))
        self.shop_rect = self.shop.get_rect()
        self.shop_rect.x = 1080 / 2

    def create_classement(self):
        connect = sqlite3.connect('comptes.db')
        cursor2 = connect.cursor()
        cursor2.execute('Select * FROM comptes ORDER by score DESC')
        all = cursor2.fetchall()
        i = 0
        while i < len(all) and i < 10:
            self._classement.append(all[i])
            i += 1

    def get_nb_meteor(self):
        return self._nb_meteor

    def update_nb_meteor(self):
        self._nb_meteor -= 1

    def start(self):
        self.is_playing = True
        self._nb_tospawn_mob = 20
        self._nb_tospawn_mob -= self._bonus_wave
        #print("nb_next" + str(self._nb_mob_next))
        #print("to spawn" + str(self._nb_tospawn_mob))
        #print("nbtot" + str(self._nb_tot))
        #print("inf" + str(self._nb_mob_next - self._last_wave))
        #print("wave" + str(self._bonus_wave))
        self.create_classement()
        if monster.Monster.get_count() < 10:
            for i in range(0, self._nb_tospawn_mob):
                self.spawn_monster1()
                self._nb_tot += 1
            self._bonus_wave = 12
            self._nb_mob_next = self._nb_tot + (20 - self._bonus_wave)
        elif monster.Monster.get_count() == self._nb_tot and monster.Monster.get_count() < self._nb_mob_next - self._last_wave:
            for i in range(0, self._nb_tospawn_mob):
                self._nb_tot += 1
                self.spawn_monster2()
            self._last_wave = 20 - self._bonus_wave
            self._bonus_wave = 14
            self._nb_mob_next = self._nb_tot + (20 - self._bonus_wave)
        elif monster.Monster.get_count() == self._nb_tot and monster.Monster.get_count() < self._nb_mob_next - (self._last_wave -3):
            for i in range(0, self._nb_tospawn_mob):
                self._nb_tot += 1
                self.spawn_monster3()
            self._last_wave = 20 - self._bonus_wave
            self._bonus_wave = 19
            self._nb_mob_next = self._nb_tot + (20 - self._bonus_wave)
        elif monster.Monster.get_count() == self._nb_tot and monster.Monster.get_count() < self._nb_mob_next:
            for i in range(0, self._nb_tospawn_mob):
                self._nb_tot += 1
                self.spawn_Warrior()
        else:
            if self._nb_tot < 10000:
                if self.comet_event.percent_speed < 250:
                    self.comet_event.percent_speed += 5
                else:
                    pass
                self._nb_meteor += 5
                mob_f = random.randint(4, 10)
                mob_m = random.randint(2, 7)
                mob_d = random.randint(1, 4)
                warriors = random.randint(0, 1)
                for i in range(0, mob_f):
                    self.spawn_monster1()
                    self._nb_tot += 1
                for i in range(0, mob_m):
                    self.spawn_monster2()
                    self._nb_tot += 1
                for i in range(0, mob_d):
                    self.spawn_monster3()
                    self._nb_tot += 1
                for i in range(0, warriors):
                    self.spawn_Warrior()
                    self._nb_tot += 1

    def create_compte(self):
        created = False
        pseudo = input("Entrez votre pseudo : ")
        self._pseudo = pseudo
        pseudo = str(pseudo)
        verif = sqlite3.connect('comptes.db')
        curs = verif.cursor()
        curs.execute("Select * FROM comptes where pseudo LIKE ?", ('' + pseudo + '', ))
        if len(curs.fetchall()) == 0:
            print('Compte créé avec succés, bon jeu {} !'.format(self._pseudo))
            created = True
        else:
            print('Pseudo déjà existant : tentez à nouveau de créer un compte avec un autre pseudo !\n')
            if len(curs.fetchall()) == 0:
                print('Compte créé avec succès, bon jeu {}'.format(self._pseudo))
                created = True
            else:
                print('Nombre de mauvaises tentatives trop élevé, le jeu se ferme . . .')
                return 0

        if created:
            connection = sqlite3.connect('comptes.db')
            cursor = connection.cursor()
            cursor.execute("insert into comptes(pseudo, score, rank) values (?, 0, 0)", ('' + pseudo + '', ))
            connection.commit()
            connection.close()

        else:
            pass

    def connexion_compte(self):
        pseudo = input("Entrez votre pseudo de jeu : ")
        print(pseudo)
        print("Vérification de l'existence de votre pseudo . . .")
        connexion = sqlite3.connect('comptes.db')
        cursor = connexion.cursor()
        cursor.execute('Select * FROM comptes where pseudo LIKE ?', ('' + pseudo + '', ))
        if len(cursor.fetchall()) != 0:
            self._pseudo = pseudo
            print('compte trouvé')
        else:
            print("Désole votre pseudo n'a pas été trouvé, réessayez en vérifiant son orthographe !")
            connexion.commit()
            connexion.close()
            pseudo2 = input('Entre votre pseudo de jeu : ')
            print("Vérification de l'existence de votre pseudo . . .")
            connexion2 = sqlite3.connect('comptes.db')
            cursor2 = connexion2.cursor()
            cursor2.execute('Select * FROM comptes where pseudo LIKE ?', ('' + pseudo2 + '',))
            if len(cursor2.fetchall()) != 0:
                self._pseudo = pseudo2
                print('Votre compte a finalement été trouvé, bon jeu {} !'.format(pseudo2))
            else:
                print('Tentative de connexion trop nombreuse, le jeu se ferme . . .')
                return 0
        return True

    def quit_shop(self):
        self.close = True
        pygame.display.flip()
        print(self.close)
        print('ok ok')

    def add_score(self, points=1):
        self.score += points

    def classement_aff(self, screen1, banner, banner_rect):
        screen1.blit(banner, (banner_rect))
        j1 = self.font.render(f"Score : {self._classement[0][1:3]}", False, (155, 0, 255))
        screen1.blit(j1, (510, 250))
        j2 = self.font.render(f"Score : {self._classement[1][1:3]}", False, (0, 19, 255))
        screen1.blit(j2, (510, 275))
        j3 = self.font.render(f"Score : {self._classement[2][1:3]}", False, (25, 148, 25))
        screen1.blit(j3, (510, 300))
        j4 = self.font.render(f"Score : {self._classement[3][1:3]}", False, (245, 146, 10))
        screen1.blit(j4, (510, 325))
        j5 = self.font.render(f"Score : {self._classement[4][1:3]}", False, (37, 136, 103))
        screen1.blit(j5, (510, 350))
        j6 = self.font.render(f"Score : {self._classement[5][1:3]}", False, (196, 32, 121))
        screen1.blit(j6, (510, 375))
        j7 = self.font.render(f"Score : {self._classement[6][1:3]}", False, (247, 0, 255))
        screen1.blit(j7, (510, 400))
        j8 = self.font.render(f"Score : {self._classement[7][1:3]}", False, (194, 162, 238))
        screen1.blit(j8, (510, 425))
        j9 = self.font.render(f"Score : {self._classement[8][1:3]}", False, (187, 248, 35))
        screen1.blit(j9, (510, 450))
        j10 = self.font.render(f"Score : {self._classement[9][1:3]}", False, (255, 0, 0))
        screen1.blit(j10, (510, 475))

    def game_over(self):
        #remettre le jeu à 0 : retirer monstres, remettre le joueur au max, remettre isplaying a False
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        score = self.score
        score = str(score)
        print("score = " + score)
        connexion = sqlite3.connect('comptes.db')
        cursor = connexion.cursor()
        print(f'pseudo = {self._pseudo}')
        cursor.execute('SELECT score FROM comptes WHERE pseudo = ?', ['' + self._pseudo + '']) #on récupere le score du joueur
        verif = cursor.fetchall()
        if int(verif[0][0]) < self.score: #on compare le score que vient de faire le joueur avec son meilleur score
            connexion.commit()
            connexion.close()
            connexion2 = sqlite3.connect('comptes.db')
            cursor2 = connexion2.cursor()
            cursor2.execute('UPDATE comptes SET score = ? WHERE pseudo = ?', ('' + score + '', '' + self._pseudo + '',))
            connexion2.commit()
            connexion2.close()
        else:
            pass

        self.score = 0
        self.is_playing = False

    def go_to_shop(self):
        self.goto = True
        pygame.display.flip()

    def update(self, screen):

        #afficher le score sur l'écran
        score_text = self.font.render(f"Score : {self.score}", False, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        #afficher la quantité disponible des compétences
        screen.blit(bdf, bdf_rect)
        number_meteor = self.font.render(f"{self._nb_meteor}", False, (255, 255, 255))
        screen.blit(number_meteor, (180, 50))

        # appliquer l'image de mon joueur
        screen.blit(self.player.image, self.player.rect)
        # afficher barre de vie du joueur
        self.player.update_health_bar(screen)

        # récupérer les projectiles
        for projectiles in self.player.all_projectiles:
            projectiles.move()

        # récupérer les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)

        #récupérer les cometes du jeu
        for comet in self.comet_event.all_cometes_fall:
            comet.fall()

        # appliquer l'ensemble des projectiles
        self.player.all_projectiles.draw(screen)

        # afficher l'ensemble des monstres
        self.all_monsters.draw(screen)

        #afficher l'ensemble des cometes
        self.comet_event.update_event(screen)
        self.comet_event.all_cometes_fall.draw(screen)

        # tant que la touche est enclenchée faire :
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x + self.player.rect.width > 200:
            self.player.move_left()
        elif self.pressed.get(pygame.K_c):
            self.classement_aff(screen, self.banner, self.banner_rect)

    def spawn_monster1(self):
        Monster1 = monster.Mob_F(self)
        self.all_monsters.add(Monster1)

    def spawn_monster2(self):
        Monster2 = monster.Mob_M(self)
        self.all_monsters.add(Monster2)

    def spawn_monster3(self):
        Monster3 = monster.Mob_D(self)
        self.all_monsters.add(Monster3)

    def spawn_Warrior(self):
        Warrior = monster.Warrior(self)
        self.all_monsters.add(Warrior)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
