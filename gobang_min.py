#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
class GoBang():
	PLAYER_1,PLAYER_2 = 1,2
	history_1 = []
	history_2 = []
	WIN,LOSS = 500000000,-500000000
	GUESS_RANGE = 2
	def __init__(self, size):
		self.map = [[0]*size for i in range(size)]
	def move(self, player, node):
		assert len(node) is 2 , ("An Error happend on move function because node:",node)
		y,x = node
		self.map[y][x] = player
		self.get_history(player).append((y,x))

	# recall current player abode step, if recall_step is bigger than 1, that will recall enemy step
	def recall(self, player, recall_step = 1):
		history = self.get_history(player)
		assert len(history) > 1, "no more history on current player: {}".format(player)
		y,x = history.pop()
		self.map[y][x] = 0
		if recall_step > 1:
			self.recall(self.get_enemy(player), recall_step-1)
	def get_history(self, player):
		return self.history_1 if player is self.PLAYER_1 else self.history_2
	def get_enemy(self,player):
		return self.PLAYER_2 if player is self.PLAYER_1 else self.PLAYER_1
	# robot win return LOSS; user win return WIN; none win return 0
	def think(self,player):
		enemy = self.get_enemy(player)
		# check enemy win
		if self.isWin(enemy):
			print("player win!!")
			return self.LOSS;
		size = len(self.map)
		history = self.get_history(enemy)
		# 1.as first player
		if len(history)<1:
			self.move(player,(random.randrange(size//3,size//3*2-1),random.randrange(size//3,size//3*2-1)))
			return 0
		# 2.as second player;choose a node near center
		elif len(history)+len(self.get_history(player)) == 1:
			y,x = history[0]
			_maybe = ((y-1,x-1),(y+1,x-1),(y+1,x+1),(y-1,x+1))
			center = size//2
			# min idx and v
			minn = [0,999999]
			i = 0
			for y,x in _maybe:
				v = (center-y)**2+(center-x)**2
				if v < minn[1]:
					minn = [i,v]
				i += 1
			print("robot none guess: ",(_maybe[minn[0]][0],_maybe[minn[0]][1]))
			self.move(player,(_maybe[minn[0]][0],_maybe[minn[0]][1]))
			return 0
		else:
			node = self.guess(player)
			print("robot guess: ",node)
			self.move(player,node)
		if self.isWin(player):
			print("robot win!!")
			return self.WIN
		return 0

	def isWin(self,player):
		return True if self.analyze(player) == self.WIN else False

	# return a node can move
	def guess(self,player,deep = 2):
		# return a set content node witch around by enemy node depend by _range
		def __guess_set__(maps,player,_range=2):
			guess_set = set()
			for y,x in self.get_history(player):
				for i in range(-_range, _range+1):
					for j in range(-_range, _range+1):
						if y+i<0 or x+j<0 or y+i>=len(maps) or x+j>=len(maps):
							continue
						if maps[y+i][x+j] is not 0:
							continue
						guess_set.add((y+i,x+j))
			return guess_set
		# 模拟行为,return moveable node
		def __simulate__(maps,player,guess_set,tree = []):
			enemy = self.get_enemy(player)
			for n in guess_set:
				self.move(player,n)
				if self.analyze(player) == self.WIN:
					return n
				###############################
				# key: node position; child: after guess_set;  score: score
				tree.append({"key":n, "child":[],"child_score":0 ,"score":(self.analyze(player)-self.analyze(enemy))})
				_idx = len(tree)-1
				# enemy want to get max score, then ignore other score
				_enemy_max_scores = -9999
				_max_node = []
				for enemy_n in __guess_set__(maps,enemy):
					self.move(enemy,enemy_n)
					##########
					_c_score = self.analyze(enemy)-self.analyze(player)
					if _c_score > _enemy_max_scores:
						_enemy_max_scores = _c_score
						_max_node = [enemy_n]
					elif _c_score == _enemy_max_scores:
						_max_node.append(enemy_n)
					##########
					self.recall(enemy)
				tree[_idx]["child"] = _max_node
				tree[_idx]["child_score"] = _enemy_max_scores
				###############################
				self.recall(player)
			# stop the enemy win key
			max_enemy_score = [0,-999]
			# find min enemy max score and max robot , minus eachother compare
			# 1 的所有最大可行域中最小值，2 最大值，对比二者中最终 1 的最大值是否“差异过大”
			# 0: node_index, 1 child score
			defender_mod = [[0],self.WIN]
			i = 0
			for n in tree:
				# take enemy min score 暂时未考虑多个最小
				if n["child_score"] < defender_mod[1]:
					defender_mod = [[i],n["child_score"]]
				elif n["child_score"] == defender_mod[1]:
					defender_mod = [[i],n["child_score"]]
				if n["child_score"] > max_enemy_score[1]:
					max_enemy_score = [i,n["child_score"]]
					pass
				i += 1
			if max_enemy_score[1]/self.WIN>0.75:
				return tree[max_enemy_score[0]]["child"][0]
			res_idx_list = defender_mod[0]
			rand_idx = random.randrange(0,len(res_idx_list))
			return tree[res_idx_list[rand_idx]]["key"]

		return __simulate__(self.map, player,__guess_set__(self.map,player))
	def analyze(self, player):
		def __isWin__(linkcountlist):
			for k,v in linkcountlist.items():
				if v[0]>=5:
					return True
			return False
		def __link_analy__(linkcountlist,style, flags, flagkey, x,y):
			size = len(self.map)
			if flags[flagkey] is 1:
				if x >= size-1 or x < 0 or y >= size-1 or y < 0:
					flags[flagkey] = -1
				else:
					if self.map[y][x] is player:
						linkcountlist[style][0] += 1
					elif self.map[y][x] is 0:
						flags[flagkey] = 0
					else:
						flags[flagkey] = -1
		history = self.get_history(player)
		if len(history)<1:
			return 0
		res_score = 0
		for y,x in history:
			link_count_info = {"ls":[1,0],"rs":[1,0],"ver":[1,0],"hor":[1,0]}
			flags = {"ls_up":1,"ls_down":1,"rs_up":1,"rs_down":1,"left":1,"right":1,"up":1,"down":1}
			for i in range(1,5):
				__link_analy__(link_count_info,"ls",flags,"ls_up",x-i,y-i)
				__link_analy__(link_count_info,"ls",flags,"ls_down",x+i,y+i)
				__link_analy__(link_count_info,"rs",flags,"rs_up",x+i,y-i)
				__link_analy__(link_count_info,"rs",flags,"rs_down",x-i,y+i)
				__link_analy__(link_count_info,"ver",flags,"left",x-i,y)
				__link_analy__(link_count_info,"ver",flags,"right",x+i,y)
				__link_analy__(link_count_info,"hor",flags,"up",x,y-i)
				__link_analy__(link_count_info,"hor",flags,"down",x,y+i)
			if __isWin__(link_count_info):
				return self.WIN
			# 遮挡值 0 + 1 | 1 + 1 | 0 + 0
			link_count_info["ls"][1] = -flags["ls_up"] + (-flags["ls_down"])
			link_count_info["rs"][1] = -flags["rs_up"] + (-flags["rs_down"])
			link_count_info["ver"][1] = -flags["left"] + (-flags["right"])
			link_count_info["hor"][1] = -flags["up"] + (-flags["down"])
			_t_score = 0
			for v in link_count_info.values():
				link,block = v[0],v[1]
				if link > 4:
					_t_score += 999999999
					break
				assert block  in [0,1,2], "an Error in value count with value link:{}  block:{}".format(link,block)
				if block is 2:
					_t_score += 1
				elif block is 1:
					_t_score += 10**link/2
				else:
					_t_score += 10**link
			res_score += _t_score
		return res_score