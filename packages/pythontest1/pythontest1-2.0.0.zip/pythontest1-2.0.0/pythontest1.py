def print2(list1):
	for name in list1 :
	    if isinstance(name,list):
			    print2(name)
	    else :
		    print(name)