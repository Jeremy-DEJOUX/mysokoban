from asyncore import loop
import pygame
import pytmx
import pyscroll

from player import Player

class Game:
    
    def __init__(self):
        
        self.map = "world"
        pygame.mixer.music.load('assets/music/fun.mp3')
        pygame.mixer.music.play(loops=-1, start=0.0)

        #creer la fenêtre du jeu
        self.screen = pygame.display.set_mode((1600, 1200)) #Fenêtre de 800pixel Largeur / 600pixels Hauteur
        pygame.display.set_caption("MySokoban") #Permet de changer le nom de la Fenêtre

        #Charger la carte (TMX)
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/carte.tmx')
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
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    #permet de deplacer le joueur
    def handle_input(self):
        pressed = pygame.key.get_pressed() #premet de savoir quelle touche est appuyé
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        self.map = "house"
        pygame.mixer.music.load('assets/music/chasing.mp3')
        pygame.mixer.music.play(loops=-1, start=0.0)
        #Charger la carte (TMX)
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #definir une liste collisison
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
        pygame.mixer.music.load('assets/music/fun.mp3')
        pygame.mixer.music.play(loops=-1, start=0.0)
         #Charger la carte (TMX)
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/carte.tmx')
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

    def update(self):
        self.group.update()

        #verifier l'enter dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.house_rect):
            self.switch_house()
            self.map = 'house'

        if self.map == 'house' and self.player.feet.colliderect(self.house_rect):
            self.switch_world()
            self.map = 'world'

        #verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

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