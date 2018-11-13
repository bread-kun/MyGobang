#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
	main game
"""
class GoBang():
	"""docstring for GoBang"""
	# main variable
	PLAYER_1 = 1
	PLAYER_2 = 2
	GUESS_RANGE = 2
	history_1 = []
	history_2 = []
	def __init__(self, size):
		self.map = [[0]*size for i in range(size)]

	# move a chess on main map
	# @param	node should be a tulpe or list with two element
	def move(self, player, node):
		try:
			y,x = node[0],node[1]
		except Exception as e:
			print("An Error happend on move function because node:",node)
			raise e
		self.map[y][x] = player
		history = history_1 if player is PLAYER_1 else history_2
		history.append(n)

	# recall current player abode step
	def recall(self, plaler, recall_step = 1):
		history = self.get_history(player)
		if len(history) < 1:
			raise Exception("no more history on player:",player)
		y,x = history.pop()
		if recall_step > 1:
			enemy = PLAYER_2 if player is PLAYER_1 else PLAYER_1
			self.recall(enemy, recall_step-1)

	# get history by player
	def get_history(self, player):
		return history_1 if player is PLAYER_1 else history_2

	# 
	def guess(self):
		pass

	# return score that enemy player +1 max step score minus current player max score
	def analyze(self):
		res_score = 0
		# ls : Left slash 	: \
		# rs : right slash : /
		# ver : vertical 	: |
		# hor : Horizontal : -
		link_count_info = {"ls":[1,0],"rs":[1,0],"ver":[1,0],"hor":[1,0]}
		# deraction flags, for judge deraction is have more link node or not
		flags = {"ls_up":1,"ls_down":1,"rs_up":1,"rs_down":1,"left":1,"right":1,"up":1,"down":1}
		# linkcountlist content link info with style \/-|
		def __isWin__(linkcountlist):
			for k,v in linkcountlist.items():
				if v>=5:
					return True
			return False
		# count link info and set block(half block or full)
		def __link_analy__(linkcountlist,style, flags, flagkey, x,y):
			if flags[flagkey] is 1:
				
				pass
			pass