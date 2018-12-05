from graphics import *
from math import *
from gobang_min import *

SIZE = 21
BACKGROUND = "#dacc13"
GRIDCOLOR = "#333"
WIDTH = 400
HEIGH = 400
PADDING=5

def window(size):
	def _draw_line(win,p1,p2):
		l=Line(p1,p2)
		l.setFill(GRIDCOLOR)
		l.setWidth(1)
		l.draw(win)
	#制作21x21的棋盘
	win=GraphWin("阿三哥的傻屌五子棋",WIDTH+2*PADDING,HEIGH+2*PADDING)
	win.setBackground(BACKGROUND)
	# 纵、横 line
	vertical = horizontal = PADDING
	while vertical<=WIDTH+PADDING:
		# point (x,y)
		_draw_line(win,Point(vertical,PADDING),Point(vertical,HEIGH+PADDING))
		vertical += WIDTH/size
	while horizontal<=HEIGH+PADDING:
		_draw_line(win,Point(PADDING,horizontal),Point(WIDTH+PADDING,horizontal))
		horizontal += HEIGH/size
	return win

def point2idx(p):
	y,x = p.getY(),p.getX()
	return int(y//(HEIGH/SIZE)),int(x//(WIDTH/SIZE))
def idx2point(y,x):
	return Point(x*(WIDTH/SIZE)+PADDING,y*(HEIGH/SIZE)+PADDING)
def show(win,gobang):
	def _draw_node(win,point,radius,fillstyle):
		n = Circle(point,radius)
		n.setFill(fillstyle)
		n.draw(win)
	for y in range(SIZE):
		for x in range(SIZE):
			if gobang.map[y][x] is 0:
				continue
			fillstyle = "black" if gobang.map[y][x] is gobang.PLAYER_1 else "white"
			_draw_node(win,idx2point(y,x),8,fillstyle)
		pass
	pass

import time
def main():
	game = GoBang(SIZE)
	win = window(SIZE)
	can_move_flag = 1
	game_flag = 0
	# while flag != game.WIN and flag != game.LOSS:
	while game_flag is 0:
		show(win,game)
		if can_move_flag is 1:
			p = win.getMouse()
			game.move(game.PLAYER_1,point2idx(p))
			can_move_flag = 0
		elif can_move_flag is 0:
			print("robot thinking....")
			game_flag = game.think(game.PLAYER_2)
			can_move_flag = 1
	pass
	show(win,game)
	box = Rectangle(Point(100,100),Point(300,300))
	box.setFill("#fff")
	box.draw(win)
	print(game_flag)
	text = "WELL! YOU WIN!" if game_flag is game.LOSS else "YOU LOSS!"
	message = Text(Point(200,200),text)
	message.draw(win)
	time.sleep(10)
	win.close()
main()