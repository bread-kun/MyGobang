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
# @return  win值(正) + lost值(负)
def mjurge(maps):

	pass

def main():
	init(mmap)
	mprint(mmap)
	minput(mmap)
	mprint(mmap)
	r = isWin(mmap)
	print(cset)
	print(r)
	pass

if __name__ == '__main__':
	main()