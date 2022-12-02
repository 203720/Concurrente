import pygame, sys
from settings import *
from components import *
from network import *
from time import sleep 

pygame.init() 
pygame.display.init()
pygame.font.init()

win = pygame.display.set_mode((width, height))
icon = pygame.image.load('Image/icon.png')
pygame.display.set_caption("Snake Multiplayer")
pygame.display.set_icon(icon)

def redrawWindow(win, walls, s1,s2,a, apple_surface):

	win.fill((167,209,61))
	for w in walls:
		w.draw(win)
	s1.draw(win)

	s2.draw(win)
	a.draw(win, apple_surface)
	pygame.display.update()

def redrawMenu(win,front_menu,wait_text, start_text):
	win.blit(front_menu , (0,0,width,height))
	wait_text.draw(win)
	start_text.draw(win)

	pygame.display.update() 	

def main():
	main_run = True
	game_run = True 
	menu_run = True
	clock = pygame.time.Clock()
	enter_pressed = False

	apple_surface = pygame.image.load('Image/apple.png')
	front_menu = pygame.image.load('Image/front.png')

	eat_sound = pygame.mixer.Sound('Sound/eat.wav')
	dead_sound = pygame.mixer.Sound('Sound/dead.wav')
	winner_sound = pygame.mixer.Sound('Sound/win.wav')
	music = pygame.mixer.music.load('Sound/music.wav')
	pygame.mixer.music.set_volume(0.4)
	

	wait_text = Text("Esperando respuesta del rival...", black , 15, 400)
	wait_text.display = False
	start_text = Text("Presiona enter para conectarte" , black , 15, 400)

	while main_run:
		pygame.mixer.music.play(-1 )

		while menu_run:

			clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					menu_run = False
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN :
					if event.key == pygame.K_RETURN:
						try:
							if not enter_pressed:
								print("networking")
								n = Network()
								info = n.connect()
								client_id = int(info['id'])
								print(client_id)
								game = info['game']
								enter_pressed = True
								wait_text.display = True
								start_text.display = False
					

						except Exception as e:
							print(e)
							pygame.quit()
							sys.exit()

			if enter_pressed:
				game = n.send('fetch')

				if game.ready: 	
					menu_run = False
					game_run = True
					s1 = game.snakes[client_id]
					s2 = game.snakes[1 - client_id]
					a = game.a
					G = game.g
					enter_pressed = False
					start_text.display = True
					wait_text.display = False
					break							

			redrawMenu( win , front_menu,  wait_text , start_text)			



		# Making Walls and partitions
		walls = [wall(0,0,width, wall_thickness,wall_color),
		wall(0,0,wall_thickness,height,wall_color),
		wall(0,height-wall_thickness,width,wall_thickness,wall_color),
		wall(width-wall_thickness,0,wall_thickness,height,wall_color)]	

		start_x = wall_thickness
		start_y = wall_thickness

		while start_x < width - wall_thickness-cell_thickness:
			start_x += cell_thickness

			# Vertical wall
			vw = wall(start_x,wall_thickness,partition_thickness,height-(2*wall_thickness),partition_color)
			walls.append(vw)

			start_x += partition_thickness
			

		while start_y < height - wall_thickness-cell_thickness:
			start_y += cell_thickness

			# Horizontal wall
			hw = wall(wall_thickness,start_y,width-(2*wall_thickness),partition_thickness,partition_color)
			walls.append(hw)

			start_y += partition_thickness

		color_info = Text("El color de la snake es: ", s1.color, 15, height/2 -100)
		

		for i in range(3, 0,-1): 
			win.fill(green_2)
			if i ==3:
				timer_info = Text("El juego empieza en "+str(i) , white, 15, height/2 + 50 )
			elif i == 2:
				timer_info = Text("El juego empieza en "+str(i) , orange, 15, height/2 + 50 )
			else:
				timer_info = Text("El juego empieza en "+str(i) , magenta, 15, height/2 + 50 )		
			pygame.draw.rect(win, s1.color, (round(color_info.x+color_info.width/2 -100/2),round(color_info.y +color_info.height),100,100))
			pygame.draw.rect(win,green_2, (round(color_info.x+color_info.width/2 -100/2)+25,round(color_info.y +color_info.height)+20,10,10))
			pygame.draw.rect(win,green_2, (round(color_info.x+color_info.width/2 -100/2)+65,round(color_info.y +color_info.height)+20,10,10))			
			color_info.draw(win)
			timer_info.draw(win)

			pygame.display.update()
			sleep(2)


		while game_run:

			clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_run = False
					pygame.quit()
					sys.exit()

			collision_status = s1.check_collision(a, eat_sound, s2)
			s1.move()


			try:
				game.snakes[client_id] = s1
			except :
				pass

			if collision_status:
				
				game = n.send({'snake' : s1 , 'apple' : a , 'apple_collision_status' : True, 'snake_died' : False})


			else:
				game = n.send({'snake' : s1, 'apple_collision_status' : False , 'snake_died' : False})
				try:
					a = game.a
				except :
					pass

			try:		
				s2 = game.snakes[1 - client_id]	
			except :
				pass	


			redrawWindow(win,walls,s1,s2,a, apple_surface)

			if s1.dead:
				pygame.mixer.music.fadeout(500)
				# You lost
				dead_sound.play()
				print('Has perdido')
				game = n.send('killgame')
				e = EndScreen(False,"Has perdido" , s1, s2)
				e.wait_key_press(win)
				
				game_run = False
				menu_run = True
				break

			elif s2.dead or game ==-1:
				pygame.mixer.music.fadeout(500)
				# You won
				winner_sound.play()
				print('Has ganado')	
				e = EndScreen(True,"Has ganado" , s1, s2)
				e.wait_key_press(win)
				
				game_run = False
				menu_run = True
				break

main()
