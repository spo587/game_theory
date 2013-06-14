from titfortat import *

teamlist = []
numteams = 9



for i in range(numteams):
    Team(i,random.choice(strat_list))
print len(teamlist)

teamorder = range(numteams)
print teamorder

for i in range(numteams):
    teamorder[i] = teamlist[teamorder[i]]
    

def all_matches():
    list_tups = []
    # print numteams  
    for j in range(numteams):
        for i in range(j+1,numteams):
            list_tups.append((i,j))
            
    random.shuffle(list_tups)
    return list_tups

    

def play_oneround_randomorder(toPrint = False):
    l = all_matches()
    for tup in l:
        play(teamlist[tup[0]],teamlist[tup[1]],toPrint2 = True)
    if toPrint:
        print '!!!!!!!!!!!!!!!!!!!ROUND COMPLETED!!!!!!!!!!!!!!'
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        
def play_multiple_rounds(numrounds):
    for t in range(numrounds):
        play_oneround_randomorder()
    
    
def play_each_other(numtimes):
    for t in range(numtimes):
        random.shuffle(teamorder)
       
        
        for j in range(numteams):
            for i in range(j+1,numteams):
                play(teamorder[i],teamorder[j])
            
    
play_multiple_rounds(2)
for i in range(len(teamlist)):
    print str(teamlist[i].__str__()) + '\'s'+'points=' + str(teamlist[i].points) + '   ',str(teamlist[i].strat)
    


