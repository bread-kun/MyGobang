#!/usr/bin/env python
# -*- coding:utf-8 -*-

mmap = []
size = 10;
cset = []

def init(maps):
	if type(maps) is list:
		for x in range(0,size-1):
			maps.append([])
			for y in range(0,size-1):
				maps[x].append(0)
				pass
			pass
		pass
	else:
		raise Exception("error maps type")
	pass

def mprint(maps):
	for x in maps:
		for y in x:
			print(" {} ".format(y),end="")
			pass
		pass
		print()
	pass

def minput(maps):
	args = input("input li:")
	args = args.split(",")
	for x in range(0,len(args)-1,2):
		cset.append((int(args[x]),int(args[x+1])))
		maps[int(args[x])][int(args[x+1])] = 1;
		pass
	pass

def isWin(maps):
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
			if maps[j][i] is 1:
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
	pass
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
def mjurge(maps):
	res_score = 0
	# 统计连数，并确定是否单遮挡或双遮挡
	def __jurge__(info_list,style,flags,flagkey,x,y,maps):
		maps_size = len(maps)
		if flags[flagkey] is 1:
			# out of range
			if x >= maps_size or x < 0 or y >= maps_size or y < 0:
				# add half 遮挡 + 1
				# 遮挡设置 -1
				flags[flagkey] = -1
			else:
				if maps[y][x] is 1:
					info_list[style][0] += 1
				elif maps[y][x] is 0:
					flags[flagkey] = 0
				# enemy node
				elif maps[y][x] is -1:
					flagkey[flagkey] = -1
				else:
					raise Exception("error value in mjurge  __jurge__ with y:{}  x:{}".format(y,x))
			pass
		pass
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
		res_score += _t_score
	pass
	return res_score

def main():
	init(mmap)
	mprint(mmap)
	minput(mmap)
	mprint(mmap)
	r = isWin(mmap)
	print(cset)
	print(r)
	s = mjurge(mmap)
	print("score ===> ",s)
	pass

if __name__ == '__main__':
	main()