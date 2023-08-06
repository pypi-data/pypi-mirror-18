def smart(haha):
	for x in haha:
		if isinstance(x,list):
			smart(x)
		else:
			print(x)
