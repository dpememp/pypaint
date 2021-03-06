#!/usr/bin/python3

import math

width,height = 990,540

def flood_field(wmatrix,ms,icolor):
	subs = None
	pels = []
	aux  = []
	dic  = {}

	j = 0
	subs = wmatrix[ms[0]][ms[1]]
	if icolor != subs:
		aux.append(ms)
		pels.append(ms)
		wmatrix[ms[0]][ms[1]] = icolor
	for i in aux:
		j += 1
		x  = i[0]
		y  = i[1]
		x1 = i[0] - 1
		x2 = i[0] + 1
		y1 = i[1] - 1
		y2 = i[1] + 1
		try:
			if wmatrix[x][y1] == subs:
				wmatrix[x][y1] = icolor
				aux.append((x,y1))
				pels.append((x,y1))
		except:
			continue

		try:
			if wmatrix[x][y2] == subs:
				wmatrix[x][y2] = icolor
				aux.append((x,y2))
				pels.append((x,y2))
		except:
			continue

		try:
			if wmatrix[x1][y] == subs:
				wmatrix[x1][y] = icolor
				aux.append((x1,y))
				pels.append((x1,y))
		except:
			continue

		try:
			if wmatrix[x2][y] == subs:
				wmatrix[x2][y] = icolor
				aux.append((x2,y))
				pels.append((x2,y))
		except:
			continue

#		aux.remove(i)

	return pels

def rectangle(p1,p2):
	pels = []

	p3 = (p1[0],p2[1])
	p4 = (p2[0],p1[1])

	pels  = bresenham(p1,p3)
	pels += bresenham(p2,p4)
	pels += bresenham(p1,p4)
	pels += bresenham(p2,p3)

	return pels

def bezier(p1,p2,p3,p4):
	pels = []
	for t in range(0,100,1):
		t = t/100
		omt  = 1 - t
		omt2 = omt*omt
		omt3 = omt2*omt
		t2   = t*t
		t3   = t2*t

		x = omt3*p1[0] + ((3*omt2)*t*p1[0]) + (3*omt*t2*p3[0]) + t3*p4[0]
		y = omt3*p1[1] + ((3*omt2)*t*p1[1]) + (3*omt*t2*p3[1]) + t3*p4[1]

		x = int(round(x,0))
		y = int(round(y,0))

		pels.append((x,y))

	return pels

def mid_point_circle(p1,p2):
	raio = round(math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1])))
	aux  = []
	pels = []

	x = 0
	y = raio
	d = 1 - raio

	aux.append((x,y))
#	print(raio)
#	print(str(p1) + " " + str(p2))

	while y > x:
		if d < 0:
			d += (2 * x) + 3
		else:
			d += (2 * (x - y)) + 5
			y -= 1
		x += 1
		aux.append((x,y))

	for i in aux:
		x = i[0]
		y = i[1]

		pels.append((x,y))
		pels.append((y,x))
		pels.append(((-1)*x,y))
		pels.append(((-1)*y,x))
		pels.append((x,(-1)*y))
		pels.append((y,(-1)*x))
		pels.append(((-1)*x,(-1)*y))
		pels.append(((-1)*y,(-1)*x))

	aux = pels
	pels = []

	for i in aux:
		x = i[0] + p1[0]
		y = i[1] + p1[1]

		pels.append((x,y))
#		if x < width and x >= 0 and y < height and y >= 0:
#			pels.append((x,y))

	return pels


#Pratically done, still need to confirm if p1 and p2 are in the line #################################

def bresenham(p1,p2):
	pels = []
	inv = False
	neg = False

	if p1 == p2:
		return pels

#	print(p1)
#	print(p2)
#	print((p2[1] - p1[1])/(p2[0] - p1[0]))
#	print("-----------------------------------------------------------")

#m == 0 -----------------------------------------------------------------------------------------------
	if p1[0] == p2[0]: #Check if p1 and p2 are in pels
			if(p1[1] < p2[1]):
				for i in range(p1[1],p2[1]):
					pels.append((p1[0],i))
				return pels
			else:
				for i in range(p2[1],p1[1]):
					pels.append((p1[0],i))
				return pels
	elif p1[1] == p2[1]: #Check if p1 and p2 are in pels
			if(p1[0] < p2[0]):
				for i in range(p1[0],p2[0]):
					pels.append((i,p1[1]))
				return pels
			else:
				for i in range(p2[0],p1[0]):
					pels.append((i,p1[1]))
				return pels
#Solve mirror problem x-axys --------------------------------------------------------------------------
	if p1[0] > p2[0]:
		aux = p1
		p1  = p2
		p2  = aux
#Solve mirror problem y-axys --------------------------------------------------------------------------
	if p1[1] > p2[1]:
#		print("Neg")
		neg = True
		base = p1
		p1 = (0,0)
		p2 = (p2[0] - base[0],(p2[1] - base[1])*(-1))
#------------------------------------------------------------------------------------------------------

	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	m  = dy/dx
	x = p1[0]
	y = p1[1]

	if m > 1: 
#		print("Inv")
		inv = True
		dx = p2[1] - p1[1]
		dy = p2[0] - p1[0]
		x = p1[1]
		y = p1[0]

	dy2 = 2*dy
	pant = dy2 - dx
	dydx2 = dy2 - 2*dx
	
	pels.append((x,y))

	for i in range(dx):
		if pant < 0:
			pels.append((x + 1,y))
			pant = pant + dy2
		else:
			pels.append((x + 1,y + 1))
			pant = pant + dydx2
			y += 1
		x += 1

	if inv:
		aux = []
		for i in pels:
			aux.append((i[1],i[0]))
		pels = aux
	if neg:
		aux = []
		for i in pels:
			aux.append((i[0] + base[0],(i[1] * (-1)) + base[1]))
		pels = aux

#	if p1 not in pels:
#		print("No p1")
#	if p2 not in pels:
#		print("No p2")

	return pels
