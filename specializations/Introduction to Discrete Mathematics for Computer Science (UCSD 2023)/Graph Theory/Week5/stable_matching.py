'''
Project Description
We'll implement the Stable Matching algorithm from the previous lesson. 

Recall the pseudocode of the algorithm:

While there exists an unmarried man:

1. Pick an arbitrary unmarried man M

2. Choose the top woman W from his list to whom he hasn't proposed yet

3. If W is free or prefers M over her current husband, then marry M and W

We'll write a Python function stableMatching(n, menPreferences, womenPreferences) that gets the number n of women and men, preferences of all women and men, and outputs a stable matching.

For simplicity we'll be assuming that the names of n men and n women are 0, 1, ..., n-1.

Then the menPreferences is a two-dimensional array (a list of lists in Python) of dimensions n by n, where menPreferences[i] contains the list of all women sorted according to their rankings by the man number i. As an example, the man number i likes the best the woman number menPreferences[i][0], and likes the least the woman number menPreferences[i][n-1]. Similarly, the array womenPreferences contains rankings of men by women. For example, womenPreferences[i][0] is the number of man who is the top choice for woman i.

Our function will return a list of length n, where ith element is the number of woman chosen for the man number i.

For convenience we can store

1. unmarriedMen -- the list of currently unmarried men;

2. manSpouse -- the list of current spouses of all man;

3. womanSpouse -- the list of current spouses of all woman;

4. nextManChoice -- contains the number of proposals each man has made.
'''

def stableMatching1(n, menPreferences, womenPreferences):
	
	unmarriedMen, manSpouse, womanSpouse, nextManChoice = list(range(n)), [None]*n, [None]*n, [0]*n
	for man in range(n):
		married = False
		while not married:
			woman = nextManChoice[man]
			curHusband = womanSpouse[menPreferences[woman]]
			if not curHusband or womanSpouse.index(man) < womanSpouse.index(curHusband):
				married = True
				manSpouse[man], womanSpouse[woman] = woman, man
				print('man {} married with woman {}'.format(man, woman))
				break
			nextManChoice[man] += 1

def stableMatching(n, menPreferences, womenPreferences):
# Do not change the function definition line.

    # Initially, all n men are unmarried
    unmarriedMen = list(range(n))
    # None of the men has a spouse yet, we denote this by the value None
    manSpouse = [None] * n                      
    # None of the women has a spouse yet, we denote this by the value None
    womanSpouse = [None] * n                      
    # Each man made 0 proposals, which means that 
    # his next proposal will be to the woman number 0 in his list
    nextManChoice = [0] * n                       
    
    # While there exists at least one unmarried man:
    while unmarriedMen:
        # Pick an arbitrary unmarried man
        he = unmarriedMen[0]                      
        # Store his ranking in this variable for convenience
        hisPreferences = menPreferences[he]       
        # Find a woman to propose to
        she = hisPreferences[nextManChoice[he]] 
        # Store her ranking in this variable for convenience
        herPreferences = womenPreferences[she]
        # Find the present husband of the selected woman (it might be None)
        currentHusband = womanSpouse[she]         
        
        # Write your code here
        
        # Now "he" proposes to "she". 
        # Decide whether "she" accepts, and update the following fields
        # 1. manSpouse
        # 2. womanSpouse
        # 3. unmarriedMen
        # 4. nextManChoice
        if currentHusband is None or herPreferences.index(he) < herPreferences.index(currentHusband):
            if not currentHusband is None:
                manSpouse[currentHusband] = None
                unmarriedMen.append(currentHusband)
                ###########nextManChoice[currentHusband] += 1
                #print('man {} divorced with woman {}'.format(currentHusband, she))
            manSpouse[he], womanSpouse[she] = she, he
            unmarriedMen.remove(he)
            #print('man {} married with woman {}'.format(he, she))
        nextManChoice[he] += 1
        #print(unmarriedMen, manSpouse, womanSpouse, nextManChoice)
            
    # Note that if you don't update the unmarriedMen list, 
    # then this algorithm will run forever. 
    # Thus, if you submit this default implementation,
    # you may receive "SUBMIT ERROR".
    return manSpouse
    
# You might want to test your implementation on the following two tests:
#assert(stableMatching(1, [ [0] ], [ [0] ]) == [0])
#assert(stableMatching(2, [ [0,1], [1,0] ], [ [0,1], [1,0] ]) == [0, 1])

#n = 4
#menPreferences = [[0, 1, 3, 2], [0, 2, 3, 1], [1, 0, 2, 3], [0, 3, 1, 2]]
#womenPreferences = [[3, 1, 2, 0], [3, 1, 0, 2], [0, 3, 1, 2], [1, 0, 3, 2]]
#stableMatching(n, menPreferences, womenPreferences)

#n=1
#menPreferences = [ [0] ]
#womenPreferences = [ [0] ]
#print(stableMatching(n, menPreferences, womenPreferences))

n=2
menPreferences = [ [0,1], [1,0] ]
womenPreferences = [ [0,1], [1,0] ]
print(stableMatching(n, menPreferences, womenPreferences))
