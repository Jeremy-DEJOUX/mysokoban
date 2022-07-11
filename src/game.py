from asyncore import loop
from gc import get_objects
import pygame
import pytmx
import pyscroll
from caisse import Caisse

from player import Player

class Game:
    
    def __init__(self):
        
        self.map = "world"
        # pygame.mixer.music.load('assets/music/fun.mp3')
        # pygame.mixer.music.play(loops=-1, start=0.0)

        #creer la fenêtre du jeu
        self.screen = pygame.display.set_mode((1600, 1200)) #Fenêtre de 800pixel Largeur / 600pixels Hauteur
        pygame.display.set_caption("MySokoban") #Permet de changer le nom de la Fenêtre

        #Charger la carte (TMX)
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/world.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        #generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        #definir une liste collisison
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    

        #dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        self.group.add(self.player)

        #definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def switch_house(self):
        self.map = "dungeon_Lvl_1"
        # pygame.mixer.music.load('assets/music/chasing.mp3')
        # pygame.mixer.music.play(loops=-1, start=1.0)

        
        #Charger la carte (TMX)
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/dungeon_Lvl_1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2


        caisse_position = tmx_data.get_object_by_name("Caisse_3")
        self.caisse = Caisse(caisse_position.x, caisse_position.y)


        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                

        #dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #definir le rectangle de collision pour entrer dans la maison
        exit_house = tmx_data.get_object_by_name("exit_house")
        self.house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        #Récuperer le point de spawn
        spawn_house_point = tmx_data.get_object_by_name("spawn_enter_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 30

    
    def switch_world(self):
        self.map = "world"

        # pygame.mixer.music.load('assets/music/fun.mp3')
        # pygame.mixer.music.play(loops=-1, start=0.0)

         #Charger la carte (TMX)
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/world.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        #definir une liste collisison
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        #dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #definir le rectangle de collision pour sortir de la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #Récuperer le point de spawn
        spawn_house_point = tmx_data.get_object_by_name("spawn_exit_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y

    #permet de deplacer le joueur
    def handle_input(self):
        pressed = pygame.key.get_pressed() #premet de savoir quelle touche est appuyé
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')

            if self.map == 'dungeon_Lvl_1':
                self.caisse.move_up()


        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def update(self):
        self.group.update()

        #verifier l'enter dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.house_rect):
            self.switch_house()
            self.map = 'dungeon_Lvl_1'

        if self.map == 'dungeon_Lvl_1' and self.player.feet.colliderect(self.house_rect):
            self.switch_world()
            self.map = 'world'


        # if self.map == "dungeon_Lvl_1":
        #     if self.player.feet.colliderect(self.caisse_rect):
        #         print('bonjour')

        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

    def run(self):

        clock = pygame.time.Clock()

        #Boucle de jeu permettant de laisser la fenêtre ouverte
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen) #dessine les calques sur le screen
            pygame.display.flip() #permet d'actualiser

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()