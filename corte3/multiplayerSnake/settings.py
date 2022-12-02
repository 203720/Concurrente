import socket

width = 800
height = 450
wall_thickness = 13

black = (0,0,0)
white = (255,255,255)
navy = (0,0,128)
purple = (128,0,128)
magenta = (255,0,255)
green = (0,128,0)
maroon = (128,0,0)
lime = (0,255,0)
red = (255,0,0)
orange = (255,140,0)
green_lime = (175,215,70)
blue = (0, 0, 255)
green_2 = (99, 166, 92)

wall_color = green_2
snake_head_width = 30
snake_head_height = 30

wall_info = (wall_thickness,width,height)

partition_color = green_2
partition_thickness = 1

cell_thickness = 40

rows = 24
cols = 31

headings = ['U','L','R','D']

clr_list_1 = [blue]
clr_list_2 = [red]

HEADERSIZE = 10

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
server = IPAddr
port = 5555