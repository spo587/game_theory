import random

## global list of teams. i've been warned against using global variables, but seemed like the best way
teamlist = []
## don't know why i chose to call the entities 'teams'
numteams = 20
## variables to be used in stochastic strategies
percentagecoop = 0.7
percentagedefect = 0.9
percentage2 = 0.9
percentage3 = 0.5
mutation_parameter = 0.02
## decide which program to run
simplesimulation = False
evolution = True

## prisoner's dilemma parameters
##defect payoff if opp cooperates
d = 7
## both cooperate payoff
c = 5
## both defect payoff, n for nash equilib
n = 1

## strategies defined in strategies file
def mostlyrandomplay(team1,team2):
    # print 'first function invoked'
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    if team2.plays[team1.index][-3:] == ['defect','defect','defect']:
        return 'defect'
    else:
        l = ['coop','defect']
        return random.choice(l)
    
def always_coop(team1,team2):
    # print 'second function invoked'
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    return 'coop'
    
def clever(team1,team2):
    if team2.plays[team1.index][-2:] == ['coop','coop']:
        return 'defect'
    elif team2.plays[team1.index][-2:] == ['defect','defect']:
        return 'defect'
    else:
        return 'coop'
    
    
def always_defect(team1,team2):
    # print 'third function invoked'
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    return 'defect'   
    
def mostly_defect(team1,team2):
    if random.random() < percentagedefect:
        return 'defect'
    else:
        return 'coop'


def t_for_t_1(team1,team2):
    
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    # print 'non tit for tat 1 team plays', team2.plays
    if len(team2.allplays) == 0:
        return 'coop'
    elif team2.allplays[-1] == 'coop':
        return 'coop'
    elif team2.allplays[-1] == 'defect':
        return 'defect'
    else:
        raise 'second team index error, t for t 1'

def t_for_t_2(team1,team2):
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    # print 'other team plays against tit for tat 2 team', team2.plays[team1.index]
    if team2.plays[team1.index] == []:
        return 'coop'
    elif team2.plays[team1.index][-1] == 'coop':
        return 'coop'
    elif team2.plays[team1.index][-1] == 'defect':
        return 'defect'
    else:
        raise 'second team index error, t for t 2'
        
def t_for_t_opp(team1,team2):
    if team2.plays[team1.index] == []:
        l = ['coop','defect']
        play = random.choice(l)
        return play
    elif team2.plays[team1.index][-2:] == ['defect','defect']:
        return 'defect'
    elif team2.plays[team1.index][-1] == 'coop':
        return 'defect'
    elif team2.plays[team1.index][-1] == 'defect':
        return 'coop'
    else:
        raise 'second team index error, t for t 2'
    
        
        

def stoch_strat1(team1,team2):
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    if team2.plays[team1.index][-3:] == ['defect','defect','defect']:
        return 'defect'
    elif random.random() <  percentagecoop:
        return 'coop'
    else:
        return 'defect'

def stoch_strat2(team1,team2):
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    if random.random() < percentage2:
        return t_for_t_2(team1,team2)
    else:
        # print 'randomly determined play'
        return 'defect'
        
def stoch_strat3(team1,team2):
    # print 'team1 plays against team2', team1.plays[team2.index]
    # print 'team2 plays against team1', team2.plays[team1.index]
    if random.random() < percentage3:
        return t_for_t_2(team1,team2)
    else:
        return always_defect(team1,team2)
        
## list with all strategies
strat_list = [stoch_strat2,stoch_strat1,t_for_t_opp,t_for_t_2,always_defect,mostlyrandomplay,clever,mostly_defect] 


 

## team class defined in file classes

class Team(object):
    def __init__(self,name,strat,points = 0, plays = None, allplays = None):
        self.name = name
        self.strat = strat
        self.points = points
        if plays == None:
            self.plays = []
            for i in range(numteams):
                self.plays.append([])
        else:
            self.plays = plays
        if allplays == None:
            self.allplays = []
        else:
            self.allplays = allplays
        global teamlist
        teamlist.append(self)
        self.index = teamlist.index(self)
        self.nextplay = None
    def addpoints(self,points):
        self.points += points
    
    def decideplay(self,opp):
        play = self.strat(self,opp)
        self.nextplay = play
        return play
    def makeplay(self,opp):
        play = self.nextplay
        # play = self.strat(self,opp)
        #         self.plays[opp.index].append(play)
        #         self.allplays.append(play)
        #         print 'play has been made'
        #         print 'debugging the makeplay method of Team class'
        #         print 'self play = ', play
        #         print 'same play should be added here', self.play[opp.index][-1]
        self.allplays.append(play)
        self.plays[opp.index].append(play)
        return play
    def __lt__(self,other):
        return self.points < other.points
    def endgen(self):
        self.points = 0
    def __str__(self):
        return self.name
        

## game functions


## a single encounter consists of 1 game, described below
def play(team1,team2, toPrint1 = False, toPrint2 = False):
    if toPrint2:
        print 'team '+str(team1.__str__())+' vs '+str(team2.__str__())
        print 'team1 points before playing ', team1.points
        print 'team2 points before playing ', team2.points
        if len(team1.allplays) >= numteams - 1:
            print 'last matchup between the teams', team1.plays[team2.index][-1],team2.plays[team1.index][-1]
        
    if team1 == team2:
        return None
    
    if toPrint1:
        
        print 'team '+team1.__str__()+'all plays=', team1.allplays
        print 'team '+team1.__str__()+'plays', team1.plays
        print 'team '+team1.__str__()+'plays against opp', team1.plays[team2.index]
        print 'team '+team2.__str__()+'all plays=', team2.allplays
        print 'team '+team2.__str__()+'plays', team2.plays
        print 'team '+team2.__str__()+'plays against opp', team2.plays[team1.index]
    team1.decideplay(team2)
    team2.decideplay(team1)
    team1play = team1.makeplay(team2)
    team2play = team2.makeplay(team1)
    
    if team1play == team2play == 'defect':
        team1.addpoints(n)
        team2.addpoints(n)
        #print 'both defect'
    elif team1play == 'defect' and team2play == 'coop':
        team1.addpoints(d)
        #print 'first team defects, second cooperates'
    elif team2play == 'defect' and team1play == 'coop':
        team2.addpoints(d)
        #print 'first team cooperates, second defects'
    else:
        #print 'both cooperate'
        team1.addpoints(c)
        team2.addpoints(c)
    if toPrint2:
        print 'team1 points after playing ', team1.points
        print 'team2 points after playing ', team2.points
        print '############# next match ##########'


## define some teams for a simple simulation
if simplesimulation:
    team1 = Team(1,t_for_t_2)
    team2 = Team('titfortat2',t_for_t_2)
    team3 = Team('defect',mostly_defect)
    team4 = Team('clever',clever)
    team5 = Team('mostly random',mostlyrandomplay)
    team6 = Team('titfortat opp',t_for_t_opp)
    team7 = Team('mostly coop',stoch_strat1)
    team8 = Team('mostly titfortat',stoch_strat2)


## for the evolution scenario
## some strategies impossible to invade, surprisingly, like tit for tat opposite
if evolution:
    initial_strat = mostly_defect
    for i in range(numteams):
        Team(i,initial_strat)
    for team in teamlist:
        print team.strat
        

print len(teamlist)


        
teamorder = range(numteams)


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
        play(teamlist[tup[0]],teamlist[tup[1]])
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

def order_teams(teams = teamlist):
    teams.sort()   
    #for team in teams:
        #print team.strat        

cruel_selection = 3

def evolve1(numgens,numyears_pergen):
    teamnum = numteams + 1
    for i in range(numgens):
        play_multiple_rounds(numyears_pergen)
        order_teams()
        for j in range(cruel_selection):
            teamlist.pop(0)
            newstrat = random.choice(strat_list)
            Team(i,newstrat)
            print 'new strategy ', newstrat
        for team in teamlist:
            team.endgen()
    ## play one more generation without replacing
    play_multiple_rounds(numyears_pergen)
    order_teams()
    for j in range(cruel_selection):
        teamlist.pop(0)
    for team in teamlist:
        print team.strat
 
## incredibly variable results!!        
def evolve2(numgens,numyears_pergen):
    '''boots out the losing teams, replicates the winning teams, and mutates each with a defined probability'''
    teamnum = numteams + 1
    for i in range(numgens):
        for t in range(len(teamlist)):
            if random.random() < mutation_parameter:
                teamlist[t].strat = random.choice(strat_list)
                print 'mutation!!!!'
                print 'new strategy= ', teamlist[t].strat
        play_multiple_rounds(numyears_pergen)
        order_teams()
        for j in range(cruel_selection):
            teamlist.pop(0)
            newstrat = teamlist[-j].strat
            Team(i,newstrat)
            print 'new strategy = winning strategy =  ', newstrat
        for team in teamlist:
            team.endgen()
    ## play one more generation without replacing
    play_multiple_rounds(numyears_pergen)
    order_teams()
    for j in range(cruel_selection):
        teamlist.pop(0)
    for team in teamlist:
        print team.strat
        
def evolve3(numgens,numyears_pergen):
    
    
        
## these results are kinda crazy. sometimes tit for tat opposite totally invades the population. wtf?? bug?       
evolve2(1000,10)
        
  
      
        




# if __name__ == '__main__':
# 
#     play_multiple_rounds(10)
#     for i in range(len(teamlist)):
#         print str(teamlist[i].__str__()) + '\'s'+'points=' + str(teamlist[i].points) + '   ',str(teamlist[i].strat)
#     order_teams()
#     
#   
#     
#    
#     
#     

    # print str(teamlist)
    #     for team in teamlist:
    #     print team.index
    #     play(team2,team4)
    #     play(team2,team4)
    #     play(team4,team5) 
    #     print 'team 4 plays', team4.plays
    #     print 'team 2 plays', team2.plays
    #     print 'team 5 plays', team5.plays
    # 
    #     
    #     print 'team2 points', team2.points
    #     print 'team 4 points',team4.points
    #     print 'team 5 points', team5.points


    
    