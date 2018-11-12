#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
mmap = []
size = 10;

PYALER_1 = 1
PYALER_2 = 2
BLOCK = -88
GUESS_RANGE = 2
cset_1 = []
cset_2 = []


def init():
	global size,mmap
	if type(mmap) is list:
		mmap = [[0]*size for i in range(size)]
	else:
		raise Exception("error mmap type")
	pass
# recall player step
def recall(maps,player,recall_step = 1):
	global cset_1,cset_2
	###############################
	cset = (cset_1 if player is PYALER_1 else cset_2)
	###############################
	if len(cset)<1:
		raise Exception("no more history on cset")
	y,x = cset.pop()
	maps[y][x] = 0
	if recall_step > 1:
		recall(maps, (PYALER_2 if player is PYALER_1 else PYALER_1),recall_step-1)
		pass
	pass
# play chess
# node need tulpe or list
def mmove(maps, player, node):
	try:
		n = [node[0],node[1]]
	except IndexError as e:
		print(node)
		raise e
	maps[n[0]][n[1]] = player
	cset = cset_1 if player is PYALER_1 else cset_2
	cset.append(n)
	pass

def mprint(maps):
	for x in maps:
		for y in x:
			print(" {} ".format(y),end="")
		print()

def minput(maps, player,cset):
	args = input("player {} input li:".format(player))
	if args is "#":
		recall(maps, player, 2)
		return minput(maps, player, cset)
	args = args.split(",")
	for x in range(0,len(args)-1,2):
		cset.append((int(args[x]),int(args[x+1])))
		maps[int(args[x])][int(args[x+1])] = player;
		pass
	pass

# AI guess
def guess(maps,player,cset):
	global size
	# min: cset.x/y - 2
	# max: cset.x/y + 2
	_range = GUESS_RANGE
	guess_set = set()
	enemy_cset = cset_1 if player is PYALER_2 else cset_2
	enemy = PYALER_1 if player is PYALER_2 else PYALER_2
	for y,x in enemy_cset:
		for i in range(-_range, _range+1):
			for j in range(-_range, _range+1):
				# current node
				if i is 0 and j is 0:
					continue
				# out of range
				if y+i<0 or x+j<0 or y+i>=size or x+j>=size:
					continue
				# not null
				if maps[y+i][x+j] is not 0:
					continue
				guess_set.add((y+i,x+j))
		pass
	# 贪心
	max_node = []
	max_val = 0
	# if no max val then less loss
	less_node = []
	less_loss = 999999
	for y,x in guess_set:
		mmove(maps, player, (y,x))
		player_score = mjurge(maps,player,cset)
		enemy_score = mjurge(maps,enemy,enemy_cset)
		print(y,x)
		print(player_score,enemy_score)
		if max_val <= (player_score-enemy_score):
			max_val = player_score-enemy_score
			max_node = [y,x]
		if less_loss > (enemy_score-player_score):
			less_loss = enemy_score-player_score
			less_node = [y,x]
		# recall
		recall(maps, player)
		pass
	pass
	# print(guess_set)
	if len(max_node) > 1:
		return mmove(maps, player, max_node)
	mmove(maps, player, less_node)

def isWin(maps,player,cset):
	# \/-|
	def __win__(linkcountlist):
		for k,v in linkcountlist.items():
			if v>=5:
				return True
		return False
	# 判断是否5连
	def __jurge__(linkcountlist,countkey,flags,flagkey,i,j,maps):
		mrange = range(0, len(maps)-1)
		if flags[flagkey] and (i in mrange and j in mrange):
			if maps[j][i] is player:
				linkcountlist[countkey] += 1
			else:
				flags[flagkey] = False
		pass
	for _py,_px in cset:
		linkcounts = {"x1":1,"x2":1,"h":1,"s":1}
		flags = {"x1_up":True,"x1_down":True,"x2_up":True,"x2_down":True,"left":True,"right":True,"up":True,"down":True}
		for i in range(1,5):
			# \
			_x,_y = _px-i,_py-i
			__jurge__(linkcounts,"x1",flags,"x1_up",_x,_y,maps)
			_x,_y = _px+i,_py+i
			__jurge__(linkcounts,"x1",flags,"x1_down",_x,_y,maps)

			# /
			_x,_y = _px+i,_py-i
			__jurge__(linkcounts,"x2",flags,"x2_up",_x,_y,maps)
			_x,_y = _px-i,_py+i
			__jurge__(linkcounts,"x2",flags,"x2_down",_x,_y,maps)

			# -
			_x = _px-i
			__jurge__(linkcounts,"h",flags,"left",_x,_py,maps)
			_x = _px+i
			__jurge__(linkcounts,"h",flags,"right",_x,_py,maps)

			# |
			_y = _py-i
			__jurge__(linkcounts,"s",flags,"up",_px,_y,maps)
			_y = _py+i
			__jurge__(linkcounts,"s",flags,"down",_px,_y,maps)
			if __win__(linkcounts):
				return True
	return False

# 局势评估
# 局势估值：本方赢未正值
# win : 9999999
# lost : -9999999
# 1 : 10
# *1 : 10/2
# 2 : 10*10
# *2 : 10*10/2
# 3 : 10*10*10
# *3 : 10*10*10/2
# *n* ： 1
# @return  win值(正) + lost值(负)
def mjurge(maps,player,cset):
	res_score = 0
	# 统计连数，并确定是否单遮挡或双遮挡
	def __jurge__(info_list,style,flags,flagkey,x,y,maps):
		if flags[flagkey] is 1:
			# out of range
			if x >= size-1 or x < 0 or y >= size-1 or y < 0:
				# 遮挡设置
				flags[flagkey] = -1
			else:
				if maps[y][x] is player:
					info_list[style][0] += 1
				elif maps[y][x] is 0:
					flags[flagkey] = 0
				# enemy node
				else:
					flags[flagkey] = -1
			pass
		pass
	if len(cset) < 1:
		return res_score
	for _py,_px in cset:
		_t_score = 0
		# ls : Left slash 	: \
		# rs : right slash : /
		# ver : vertical 	: |
		# hor : Horizontal : -
		link_infos = {"ls":[1,0],"rs":[1,0],"ver":[1,0],"hor":[1,0]}
		flags = {"ls_up":1,"ls_down":1,"rs_up":1,"rs_down":1,"left":1,"right":1,"up":1,"down":1}
		for i in range(1,5):
			# \
			_x,_y = _px-i,_py-i
			__jurge__(link_infos,"ls",flags,"ls_up",_x,_y,maps)
			_x,_y = _px+i,_py+i
			__jurge__(link_infos,"ls",flags,"ls_down",_x,_y,maps)

			# /
			_x,_y = _px+i,_py-i
			__jurge__(link_infos,"rs",flags,"rs_up",_x,_y,maps)
			_x,_y = _px-i,_py+i
			__jurge__(link_infos,"rs",flags,"rs_down",_x,_y,maps)

			# -
			_x = _px-i
			__jurge__(link_infos,"ver",flags,"left",_x,_py,maps)
			_x = _px+i
			__jurge__(link_infos,"ver",flags,"right",_x,_py,maps)

			# |
			_y = _py-i
			__jurge__(link_infos,"hor",flags,"up",_px,_y,maps)
			_y = _py+i
			__jurge__(link_infos,"hor",flags,"down",_px,_y,maps)

		# 遮挡值 0 + 1 | 1 + 1 | 0 + 0
		link_infos["ls"][1] = -flags["ls_up"] + (-flags["ls_down"])
		link_infos["rs"][1] = -flags["rs_up"] + (-flags["rs_down"])
		link_infos["ver"][1] = -flags["left"] + (-flags["right"])
		link_infos["hor"][1] = -flags["up"] + (-flags["down"])
	
		# 叠加点集合值统计
		for v in link_infos.values():
			link,block = v[0],v[1]
			if block is 2:
				_t_score += 1
			elif block is 1:
				_t_score += 10**link/2
			elif block is 0:
				_t_score += 10**link
			else:
				raise Exception("an Error in value count with value link:{}  block:{}".format(link,block))
			if link > 4:
				_t_score += 999999999
		res_score += _t_score
	return res_score

def main():
	init()
	mprint(mmap)
	player = PYALER_1
	# input
	while 1:
		#######################################
		cset = (cset_1 if player is PYALER_1 else cset_2)
		#######################################
		if player is PYALER_1:
			minput(mmap,PYALER_1,cset)
		elif player is PYALER_2:
			# minput(mmap,PYALER_2,cset)
			guess(mmap, PYALER_2, cset)
		else:
			raise Exception("None player with value : ",player)
		# os.system("cls")
		mprint(mmap)
		r = isWin(mmap,player,cset)
		print(cset)
		print(r)
		s = mjurge(mmap,player,cset)
		print("score ===> ",s)
		#######################################
		player = (PYALER_1 if player is PYALER_2 else PYALER_2)
		#######################################
		pass

if __name__ == '__main__':
	main()