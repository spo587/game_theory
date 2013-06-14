from titfortat import *

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
    def __str__(self):
        return self.name
        