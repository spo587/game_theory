import random

## prisoner's dilemma game, with evolution and selection
## if executed without modification, instantiates 20 players who mostly defect, but the population can 
## be invaded by the other strategies over the 1000 'generations' iterated in the function 'evolve2'
## prints out initial strategies and strategies of the 15 survivors at the end


## global list of players. i've been warned against using global variables, but seemed like the best way
playerlist = []

numplayers = 20
## variables to be used in stochastic strategies
percentagecooperate = 0.7
percentagedefect = 0.9
percentage_tit_for_tat = 0.9
tit_for_tat_param = 0.1
mutation_parameter = 0.02
## decide which program to run
simplesimulation = False
evolution = True

## prisoner's dilemma parameters
##defect payoff if opp cooperateerates
d = 7
## both cooperateerate payoff
c = 5
## both defect payoff, n for nash equilib
n = 1

## strategies 
def mostlyrandomplay(player1,player2):
    ## check if last three plays by the opponent against you were defect
    if player2.plays[player1.index][-3:] == ['defect','defect','defect']:
        return 'defect'
    else:
        l = ['cooperate','defect']
        return random.choice(l)
    
def always_cooperate(player1,player2):
    return 'cooperate'
    
def clever(player1,player2):
    ## check if last two plays were cooperate. if so, take advantage!
    if player2.plays[player1.index][-2:] == ['cooperate','cooperate']:
        return 'defect'
    ## if opponent appears to be a defector, don't cooperate
    elif player2.plays[player1.index][-2:] == ['defect','defect']:
        return 'defect'
    else:
        return 'cooperate'
    
def always_defect(player1,player2):
    return 'defect'   
    
def mostly_defect(player1,player2):
    if random.random() < percentagedefect:
        return 'defect'
    else:
        return 'cooperate'


def tit_for_tat_1(player1,player2):
    '''smart tit for tat, can see player's last move against any opponent'''
    ## not using this strategy in simulation below
    if len(player2.allplays) == 0:
        return 'cooperate'
    elif player2.allplays[-1] == 'cooperate':
        return 'cooperate'
    elif player2.allplays[-1] == 'defect':
        return 'defect'
    else:
        raise 'second player index error, t for t 1'

def tit_for_tat_2(player1,player2):
    '''traditional tit for tat, plays whatever opponent last played against you'''
    if player2.plays[player1.index] == []:
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'cooperate':
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'defect':
        return 'defect'

        
def tit_for_tat_opp(player1,player2):
    '''opposite of tit for tat, with exceptions'''
    ## initial play
    if player2.plays[player1.index] == []:
        l = ['cooperate','defect']
        play = random.choice(l)
        return play
    ## if opponent is a serial defector, don't cooperate
    elif player2.plays[player1.index][-2:] == ['defect','defect']:
        return 'defect'
    ## otherwise, do the opposite of tit for tat
    elif player2.plays[player1.index][-1] == 'cooperate':
        return 'defect'
    elif player2.plays[player1.index][-1] == 'defect':
        return 'cooperate'
    

def mostly_cooperate(player1,player2):
    ## check for serial defector
    if player2.plays[player1.index][-3:] == ['defect','defect','defect']:
        return 'defect'
    ## otherwise, cooperate stochastically
    elif random.random() <  percentagecooperate:
        return 'cooperate'
    else:
        return 'defect'

def mostly_tit_for_tat(player1,player2):
    if random.random() < percentage_tit_for_tat:
        return tit_for_tat_2(player1,player2)
    else:
        return 'defect'
        
def tit_for_two_tat(player1,player2):
    '''more forgiving'''
    if len(player2.plays[player1.index]) <= 1:
        return 'cooperate'
    elif player2.plays[player1.index][-2:] == ['defect','defect']:
        return 'defect'
    else:
        return 'cooperate'
        
def tit_for_tat_forgiving(player1,player2):
    if player2.plays[player1.index] == []:
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'cooperate':
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'defect':
        if random.random() < tit_for_tat_param:
            return 'cooperate'
        else:
            return 'defect'
    

    
        
## list with strategies to be used in simulation (modify to include more or fewer strategies)
strat_list = [mostly_tit_for_tat,mostly_cooperate,tit_for_tat_opp,tit_for_tat_2,always_defect,mostlyrandomplay,clever,mostly_defect,tit_for_two_tat,tit_for_tat_forgiving] 


 

## player class defined in file classes

class Player(object):
    def __init__(self,name,strat,points = 0, plays = None, allplays = None):
        '''points: stores points accrued in a single generation or set of games
        strat = strategy, defined above
        plays =  list of lists storing plays made against each opponent
        allplays = list of all plays made: this might be unnecessary'''
        self.name = name
        self.strat = strat
        self.points = points
        if plays == None:
            self.plays = []
            for i in range(numplayers):
                self.plays.append([])
        else:
            self.plays = plays
        if allplays == None:
            self.allplays = []
        else:
            self.allplays = allplays
        ## playerlist gets modified when a player is instantiated, and the correct index is assigned to the player
        global playerlist
        playerlist.append(self)
        self.index = playerlist.index(self)
        self.nextplay = None
    def addpoints(self,points):
        self.points += points
    
    def decideplay(self,opp):
        play = self.strat(self,opp)
        self.nextplay = play
        return play
    def makeplay(self,opp):
        play = self.nextplay
        self.allplays.append(play)
        self.plays[opp.index].append(play)
        return play
    def __lt__(self,other):
        return self.points < other.points
    def endgen(self):
        '''when a generation or full round is over, restore points to 0'''
        self.points = 0
    def __str__(self):
        return self.name
        

## game functions

## a single encounter consists of 1 game, described below
def play(player1,player2, toPrint1 = False, toPrint2 = False):
    ## debugging
    if toPrint2:
        print 'player '+str(player1.__str__())+' vs '+str(player2.__str__())
        print 'player1 points before playing ', player1.points
        print 'player2 points before playing ', player2.points
        if len(player1.allplays) >= numplayers - 1:
            print 'last matchup between the players', player1.plays[player2.index][-1],player2.plays[player1.index][-1]
        
    if player1 == player2:
        return None
    
    if toPrint1:
        
        print 'player '+player1.__str__()+'all plays=', player1.allplays
        print 'player '+player1.__str__()+'plays', player1.plays
        print 'player '+player1.__str__()+'plays against opp', player1.plays[player2.index]
        print 'player '+player2.__str__()+'all plays=', player2.allplays
        print 'player '+player2.__str__()+'plays', player2.plays
        print 'player '+player2.__str__()+'plays against opp', player2.plays[player1.index]
    ## play below
    player1.decideplay(player2)
    player2.decideplay(player1)
    player1play = player1.makeplay(player2)
    player2play = player2.makeplay(player1)
    ## assign points based on prisoner's dilemma 
    if player1play == player2play == 'defect':
        player1.addpoints(n)
        player2.addpoints(n)
        #print 'both defect'
    elif player1play == 'defect' and player2play == 'cooperate':
        player1.addpoints(d)
        #print 'first player defects, second cooperateerates'
    elif player2play == 'defect' and player1play == 'cooperate':
        player2.addpoints(d)
        #print 'first player cooperateerates, second defects'
    else:
        #print 'both cooperateerate'
        player1.addpoints(c)
        player2.addpoints(c)
    if toPrint2:
        print 'player1 points after playing ', player1.points
        print 'player2 points after playing ', player2.points
        print '############# next match ##########'


## define some players for a simple simulation
if simplesimulation:
    player1 = Player(1,tit_for_tat_2)
    player2 = Player('titfortat2',tit_for_tat_2)
    player3 = Player('defect',mostly_defect)
    player4 = Player('clever',clever)
    player5 = Player('mostly random',mostlyrandomplay)
    player6 = Player('titfortat opp',tit_for_tat_opp)
    player7 = Player('mostly cooperate',mostly_cooperate)
    player8 = Player('mostly titfortat',mostly_tit_for_tat)


## for the evolution scenario
## some strategies impossible to invade, surprisingly, like tit for tat opposite
if evolution:
    ## modify the initial strategy to see which strategies are prone to invasion, or make it random
    initial_strat = mostly_defect
    for i in range(numplayers):
        Player(i,initial_strat)
    ## comment out below for long simulations
    print '####### INITIAL PLAYERS ##########'
    for player in playerlist:
        print player.strat

## below, randomizing the order of the individual games in a round        
playerorder = range(numplayers)

## make a new list that's identical to playerlist, but that we can modify without modifying global playerlist
for i in range(numplayers):
    playerorder[i] = playerlist[playerorder[i]]


def all_matches():
    '''list of all matchups in a single round (that is, every player plays every other player once), numteams+1 choose 2 games'''
    list_tups = []
    # print numplayers  
    for j in range(numplayers):
        for i in range(j+1,numplayers):
            list_tups.append((i,j))
            
    random.shuffle(list_tups)
    return list_tups

   

def play_oneround_randomorder(toPrint = False):
    l = all_matches()
    for tup in l:
        play(playerlist[tup[0]],playerlist[tup[1]])
    if toPrint:
        print '!!!!!!!!!!!!!!!!!!!ROUND COMPLETED!!!!!!!!!!!!!!'
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

## i think the next two functions are identical. im not sure why i defined them both, now, but i'm worried
#3 they're actually different, so keeping them for now
        
def play_multiple_rounds(numrounds):
    for t in range(numrounds):
        play_oneround_randomorder()
    
    
def play_each_other(numrounds):
    for t in range(numrounds):
        random.shuffle(playerorder)
       
        
        for j in range(numplayers):
            for i in range(j+1,numplayers):
                play(playerorder[i],playerorder[j])

def order_players(players = playerlist):
    players.sort()   
       
## one more parameter to decide how many players 'die' after each full round (or 'generation')
cruel_selection = 3

def evolve1(numgens,numyears_pergen):
    '''numgens = int, number of iterations
    numyears_pergen = int, number of times each team will 'play' before the selection happens'''
    ## new team gets new name
    playernum = numplayers + 1
    for i in range(numgens):
        play_multiple_rounds(numyears_pergen)
        order_players()
        for j in range(cruel_selection):
            ## kill off the losers
            playerlist.pop(0)
            ## insert randoms
            newstrat = random.choice(strat_list)
            Player(i,newstrat)
            # print 'new strategy ', newstrat
        for player in playerlist:
            player.endgen()
    ## play one more generation without replacing
    play_multiple_rounds(numyears_pergen)
    order_players()
    for j in range(cruel_selection):
        playerlist.pop(0)
    for player in playerlist:
        print player.strat
 
## incredibly variable results!!        
def evolve2(numgens,numyears_pergen):
    '''boots out the losing players, replicates the winning players instead of random ones,
     and mutates each player with a fixed probability
     uncomment print statements to see it in action'''
    playernum = numplayers + 1
    for i in range(numgens):
        for t in range(len(playerlist)):
            if random.random() < mutation_parameter:
                playerlist[t].strat = random.choice(strat_list)
                # print 'mutation!!!!'
                # print 'new strategy= ', playerlist[t].strat
        play_multiple_rounds(numyears_pergen)
        order_players()
        for j in range(cruel_selection):
            playerlist.pop(0)
            newstrat = playerlist[-j].strat
            Player(i,newstrat)
            # print 'new strategy = winning strategy =  ', newstrat
        for player in playerlist:
            player.endgen()
    ## play one more generation without replacing
    play_multiple_rounds(numyears_pergen)
    order_players()
    for j in range(cruel_selection):
        playerlist.pop(0)
    print '#### FINAL SURVIVORS ########'
    for player in playerlist:
        print player.strat
        
# def evolve3(numgens,numyears_pergen):
    
    
        
## these results are kinda crazy. different each time. next step: run many versions of evolve2 and collect
## results in a histogram, find out distribution of results/ strategies that do well more often, etc.
      
evolve2(1000,10)
        
  
      
        




# if __name__ == '__main__':
# 
#     play_multiple_rounds(10)
#     for i in range(len(playerlist)):
#         print str(playerlist[i].__str__()) + '\'s'+'points=' + str(playerlist[i].points) + '   ',str(playerlist[i].strat)
#     order_players()
#     
#   
#     
#    
#     
#     

    # print str(playerlist)
    #     for player in playerlist:
    #     print player.index
    #     play(player2,player4)
    #     play(player2,player4)
    #     play(player4,player5) 
    #     print 'player 4 plays', player4.plays
    #     print 'player 2 plays', player2.plays
    #     print 'player 5 plays', player5.plays
    # 
    #     
    #     print 'player2 points', player2.points
    #     print 'player 4 points',player4.points
    #     print 'player 5 points', player5.points


    
    