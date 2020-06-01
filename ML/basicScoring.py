print("Enter Views")
views = input()
print("Enter Favorites")
favs=input()
print("Enter Comments")
comm=input()
score = (((int(views) * 0.00005)+(int(favs) *0.00003)+(int(comm) *0.00002))/5)+1
print(score)
	
	
	