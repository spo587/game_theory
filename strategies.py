import random
 

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
        print 'randomly determined play'
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
