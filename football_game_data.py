from collections import Counter
import csv
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

class Heat_Map_Stats(object):
    """Description: This class is used to collect passing and shooting statistics by processing a heat map
    """
    def __init__(self):
        self.teamDefendingZone = 0
        self.zoneShotsOffTarget = {}                # dictionary containing number of shots not on target in each zone (zone #: # shots)
        self.zoneShotsOnTarget = {}                 # dictionary containing number of shots on target but not scored in each zone (zone #: # shots]
        self.zoneShotsScored = {}                   # dictionary containing number of shots scored in each zone (zone #: # goals)
        self.zoneOwnGoals = {}                          # dictionary containing number of shots scored as own goals in each zone (zone#: # own goals)
        self.zoneAssists = {}                       # dictionary containing number of assist passes completed in each zone (zone#: # assists)
        self.zonePasses = {}                        # dictionary containing number of passes completed in each zone (zone #: # passes)
        self.zonePossessionInstances = {}           # dictionary containing number of possession instances (3 consecutive passes) in each zone (zone #: # possessions)
        self.zoneLostPossessionInstances = {}       # dictionary containing number of times lost possession in each zone (zone#: # lost possessions)

    def set_team_defending_zone(self, zoneNum):
        """Description: Set the zone number that the team that this heat map is for is defending
        Inputs: zoneNum - the zone number to set to
        Outputs:
            Sets member variable self.teamDefendingZone to zoneNum
        """
        self.teamDefendingZone = zoneNum
        
    def add_zone(self, zoneNum, shotsOffTarget, shotsOnTarget, shotsScored, ownGoals, assists, passes, possessions, lostPossession):
        """Description: Extract statistics from a zone and accumulate them into the statistics counters
        Inputs: zoneNum - the zone number to add
                shotsOffTarget - the number of shots off target for this zone
                shotsOnTarget - the number of shots on target for this zone
                shotsScored - the number of shots scored for this zone
                ownGoals - the number of shots scored as own goals for this zone
                assists - the number of assist passes into this zone
                passes - the number of passes into this zone
                possessions - the number of possession instances ended in this zone
                lostPossession - the number of times possession lost in the this zone
        Outputs:
            Adds zone to the dictionary if it isn't already in. If the zone is already in the dictionary, then it overwrites the values with the new values
        """
        self.zoneShotsOffTarget[zoneNum] = shotsOffTarget
        self.zoneShotsOnTarget[zoneNum] = shotsOnTarget
        self.zoneShotsScored[zoneNum] = shotsScored
        self.zoneOwnGoals[zoneNum] = ownGoals
        self.zoneAssists[zoneNum] = assists
        self.zonePasses[zoneNum] = passes
        self.zonePossessionInstances[zoneNum] = possessions
        self.zoneLostPossessionInstances[zoneNum] = lostPossession
        
    def total_passes(self):
        """Description: Add the passes from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the passes in all zones
        """
        totalPasses = 0
        for zone in self.zonePasses:
            totalPasses = totalPasses + self.zonePasses[zone]
        return(totalPasses)

    def total_possession_instances(self):
        """Description: Add the possession instances from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the possession instances in all zones
        """
        totalPossession = 0
        for zone in self.zonePossessionInstances:
            totalPossession = totalPossession + self.zonePossessionInstances[zone]
        return(totalPossession)

    def total_lost_possession_instances(self):
        """Description: Add the lost possession instances from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the lost possession instances in all zones
        """
        totalLostPossession = 0
        for zone in self.zoneLostPossessionInstances:
            totalLostPossession = totalLostPossession + self.zoneLostPossessionInstances[zone]
        return(totalLostPossession)

    def total_shots_on_target(self):
        """Description: Add the shots on target from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the shots on target in all zones
        """
        totalShots = 0
        for zone in self.zoneShotsOnTarget:
            totalShots = totalShots + self.zoneShotsOnTarget[zone]
            
        for zone in self.zoneShotsScored:
            totalShots = totalShots + self.zoneShotsScored[zone]

        for zone in self.zoneOwnGoals:
            totalShots = totalShots + self.zoneOwnGoals[zone]
        return(totalShots)

    def total_shots(self):
        """Description: Add the shots from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the shots in all zones
        """
        totalShots = 0
        for zone in self.zoneShotsOffTarget:
            totalShots = totalShots + self.zoneShotsOffTarget[zone]

        for zone in self.zoneShotsOnTarget:
            totalShots = totalShots + self.zoneShotsOnTarget[zone]
            
        for zone in self.zoneShotsScored:
            totalShots = totalShots + self.zoneShotsScored[zone]

        for zone in self.zoneOwnGoals:
            totalShots = totalShots + self.zoneOwnGoals[zone]
        return(totalShots)
        
    def total_goals(self):
        """Description: Add the shots scored from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the goals in all zones
        """
        totalShots = 0
        for zone in self.zoneShotsScored:
            totalShots = totalShots + self.zoneShotsScored[zone]

        for zone in self.zoneOwnGoals:
            totalShots = totalShots + self.zoneOwnGoals[zone]
        return(totalShots)

        
    def total_assists(self):
        """Description: Add the assists from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the assists in all zones
        """
        totalAssists = 0
        for zone in self.zoneAssists:
            totalAssists = totalAssists + self.zoneAssists[zone]
        return(totalAssists)
        

class Passing_Stats(object):
    """Description: This object is used to collect passing statistics by processing passing tree branches
    """
    def __init__(self):
        self.totalPasses = 0                         # Total number of passes completed
        self.possessionInstances = 0                 # Number of times 3 consecutive passes reached
        self.maxConsecutivePasses = 0                # Max number of passes in a passing sequence
        self.passingSequenceHistogram = {}           # Dictionary for histogram of how many instances each passing sequence length there are {1: x, 2: y, 3: z, ...}
        self.treeRoots = []                          # array of passing nodes that were the root of a passing sequence
        self.treeTips = []                           # array of passing nodes that were the end of a passing sequence
        self.resetPossessionInstances = True         # flag to reset the possession instances variable the first time process_tree_branch is called
        
    def process_tree_branch(self,graph,treeBranch):
        # graph is a directed graph to add the path in the tree branch to
        # treeBranch is a list of nodes in order of pass propagation
        if self.resetPossessionInstances == True:
            self.possessionInstances = 0
            self.resetPossessionInstances = False
        passes = 0
        tip = treeBranch[len(treeBranch)-1]
        for i in range(0,len(treeBranch)-1):
            if treeBranch[i+1] == "":
                tip = treeBranch[i]
                break
            passes = passes+1
            if graph.has_edge(treeBranch[i],treeBranch[i+1]):
                x = graph[treeBranch[i]][treeBranch[i+1]]['weight']
                graph[treeBranch[i]][treeBranch[i+1]]['weight'] = x+1
            else:
                graph.add_weighted_edges_from([(treeBranch[i],treeBranch[i+1],1)])

        self.possessionInstances = self.possessionInstances + int(passes / 3)
        
        # update the histogram entry for the number of passes in this sequence
        if passes in self.passingSequenceHistogram:
            self.passingSequenceHistogram[passes] = self.passingSequenceHistogram[passes] + 1
        else:
            self.passingSequenceHistogram[passes] = 1
            
        self.treeRoots.append(treeBranch[0])
        self.treeTips.append(tip)
        self.totalPasses = self.totalPasses + passes
        if passes > self.maxConsecutivePasses:
            self.maxConsecutivePasses = passes

    def passing_roots(self):
        treeRootsFreq = Counter(self.treeRoots)
        c = treeRootsFreq.most_common()
        return c

    def passing_tips(self):
        treeTipsFreq = Counter(self.treeTips)
        c = treeTipsFreq.most_common()
        return c
        
class Game_Data(object):  
    h1Duration = 45
    h2Duration = 45
    ot1Duration = 15
    ot2Duration = 15
    homeTeamPenaltyShootoutGoals = "NA"
    awayTeamPenaltyShootoutGoals = "NA"
    
    def __init__(self,fileName):
        self.homeTeam = ""
        self.awayTeam = ""
        self.gameDate = ""
        self.homeTeamGoals = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamGoals = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeamAssists = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamAssists = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeamShots = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamShots = {"H1":0, "H2":0, "OT1":0, "OT2":0}        
        self.homeTeamSaves = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamSaves = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeamCorners = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamCorners = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeamYellowCards = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamYellowCards = {"H1":0, "H2":0, "OT1":0, "OT2":0}        
        self.homeTeamRedCards = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeamRedCards = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeamFormationName = {"H1":"", "H2":"", "OT1":"", "OT2":""}
        self.awayTeamFormationName = {"H1":"", "H2":"", "OT1":"", "OT2":""}
        self.homeTeamH1Formation = {}
        self.awayTeamH1Formation = {}
        self.homeTeamH2Formation = {}
        self.awayTeamH2Formation = {}
        self.homeTeamH1PassingGraph = nx.DiGraph()
        self.homeTeamH2PassingGraph = nx.DiGraph()
        self.awayTeamH1PassingGraph = nx.DiGraph()
        self.awayTeamH2PassingGraph = nx.DiGraph()
        self.homeTeamH1PassingStats = Passing_Stats()
        self.homeTeamH2PassingStats = Passing_Stats()
        self.awayTeamH1PassingStats = Passing_Stats()
        self.awayTeamH2PassingStats = Passing_Stats()
        self.homeTeamH1HeatMapStats = Heat_Map_Stats()
        self.homeTeamH2HeatMapStats = Heat_Map_Stats()
        self.awayTeamH1HeatMapStats = Heat_Map_Stats()
        self.awayTeamH2HeatMapStats = Heat_Map_Stats()
        self.homeTeamH1Comments = []
        self.awayTeamH1Comments = []
        self.homeTeamH2Comments = []
        self.awayTeamH2Comments = []

        # Dictionary for field types in data file for parser
        # each dictionary key has a list with the following values:
        #       parse function - the function that gets called to parse this entry
        #       skip first line - if the first line that contained the key does not contain valid data to parse
        #       only one line - if the field only contains data on the first line and ignore any subsequent lines
        self.__dataFileFields__ = {"HOME TEAM": [self.__parse_home_team__, False, True],
                                   "AWAY TEAM": [self.__parse_away_team__, False, True],
                                   "GAME DATE": [self.__parse_game_date__, False, True],
                                   "H1 DURATION": [self.__parse_duration__, False, True],
                                   "H2 DURATION": [self.__parse_duration__, False, True],
                                   "OT1 DURATION": [self.__parse_duration__, False, True],
                                   "OT2 DURATION": [self.__parse_duration__, False, True],
                                   "HT H1 GOALS": [self.__parse_goals__, False, True],
                                   "AT H1 GOALS": [self.__parse_goals__, False, True],
                                   "HT H2 GOALS": [self.__parse_goals__, False, True],
                                   "AT H2 GOALS": [self.__parse_goals__, False, True],
                                   "HT OT1 GOALS": [self.__parse_goals__, False, True],
                                   "AT OT1 GOALS": [self.__parse_goals__, False, True],
                                   "HT OT2 GOALS": [self.__parse_goals__, False, True],
                                   "AT OT2 GOALS": [self.__parse_goals__, False, True],
                                   "HT H1 ASSISTS": [self.__parse_assists__, False, True],
                                   "AT H1 ASSISTS": [self.__parse_assists__, False, True],
                                   "HT H2 ASSISTS": [self.__parse_assists__, False, True],
                                   "AT H2 ASSISTS": [self.__parse_assists__, False, True],
                                   "HT OT1 ASSISTS": [self.__parse_assists__, False, True],
                                   "AT OT1 ASSISTS": [self.__parse_assists__, False, True],
                                   "HT OT2 ASSISTS": [self.__parse_assists__, False, True],
                                   "AT OT2 ASSISTS": [self.__parse_assists__, False, True],
                                   "HT H1 SHOTS": [self.__parse_shots__, False, True],
                                   "AT H1 SHOTS": [self.__parse_shots__, False, True],
                                   "HT H2 SHOTS": [self.__parse_shots__, False, True],
                                   "AT H2 SHOTS": [self.__parse_shots__, False, True],
                                   "HT OT1 SHOTS": [self.__parse_shots__, False, True],
                                   "AT OT1 SHOTS": [self.__parse_shots__, False, True],
                                   "HT OT2 SHOTS": [self.__parse_shots__, False, True],
                                   "AT OT2 SHOTS": [self.__parse_shots__, False, True],
                                   "HT H1 SAVES": [self.__parse_saves__, False, True],
                                   "AT H1 SAVES": [self.__parse_saves__, False, True],
                                   "HT H2 SAVES": [self.__parse_saves__, False, True],
                                   "AT H2 SAVES": [self.__parse_saves__, False, True],
                                   "HT OT1 SAVES": [self.__parse_saves__, False, True],
                                   "AT OT1 SAVES": [self.__parse_saves__, False, True],
                                   "HT OT2 SAVES": [self.__parse_saves__, False, True],
                                   "AT OT2 SAVES": [self.__parse_saves__, False, True],
                                   "HT H1 CORNERS": [self.__parse_corners__, False, True],
                                   "AT H1 CORNERS": [self.__parse_corners__, False, True],
                                   "HT H2 CORNERS": [self.__parse_corners__, False, True],
                                   "AT H2 CORNERS": [self.__parse_corners__, False, True],
                                   "HT OT1 CORNERS": [self.__parse_corners__, False, True],
                                   "AT OT1 CORNERS": [self.__parse_corners__, False, True],
                                   "HT OT2 CORNERS": [self.__parse_corners__, False, True],
                                   "AT OT2 CORNERS": [self.__parse_corners__, False, True],
                                   "HT H1 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "AT H1 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "HT H2 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "AT H2 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "HT OT1 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "AT OT1 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "HT OT2 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "AT OT2 YELLOW CARDS": [self.__parse_yellow_cards__, False, True],
                                   "HT H1 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "AT H1 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "HT H2 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "AT H2 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "HT OT1 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "AT OT1 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "HT OT2 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "AT OT2 RED CARDS": [self.__parse_red_cards__, False, True],
                                   "HT H1 POSSESSION": [self.__parse_possession__, False, True],
                                   "AT H1 POSSESSION": [self.__parse_possession__, False, True],
                                   "HT H2 POSSESSION": [self.__parse_possession__, False, True],
                                   "AT H2 POSSESSION": [self.__parse_possession__, False, True],
                                   "HT OT1 POSSESSION": [self.__parse_possession__, False, True],
                                   "AT OT1 POSSESSION": [self.__parse_possession__, False, True],
                                   "HT OT2 POSSESSION": [self.__parse_possession__, False, True],
                                   "AT OT2 POSSESSION": [self.__parse_possession__, False, True],
                                   "HT H1 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "AT H1 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "HT H2 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "AT H2 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "HT OT1 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "AT OT1 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "HT OT2 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "AT OT2 MAX PASSES": [self.__parse_max_passes__, False, True],
                                   "HT H1 FORMATION": [self.__parse_formation__, False, False],
                                   "HT H2 FORMATION": [self.__parse_formation__, False, False],
                                   "AT H1 FORMATION": [self.__parse_formation__, False, False],
                                   "AT H2 FORMATION": [self.__parse_formation__, False, False],
                                   "HT H1 PASSING GRAPH": [self.__parse_passing_graph__, True, False],
                                   "AT H1 PASSING GRAPH": [self.__parse_passing_graph__, True, False],
                                   "HT H2 PASSING GRAPH": [self.__parse_passing_graph__, True, False],
                                   "AT H2 PASSING GRAPH": [self.__parse_passing_graph__, True, False],
                                   "HT H1 PASSING TREE": [self.__parse_passing_tree__, True, False],
                                   "HT H2 PASSING TREE": [self.__parse_passing_tree__, True, False],
                                   "AT H1 PASSING TREE": [self.__parse_passing_tree__, True, False],
                                   "AT H2 PASSING TREE": [self.__parse_passing_tree__, True, False],
                                   "HT H1 DEFENDING ZONE": [self.__parse_team_defending_zone__, False, True],
                                   "HT H2 DEFENDING ZONE": [self.__parse_team_defending_zone__, False, True],
                                   "AT H1 DEFENDING ZONE": [self.__parse_team_defending_zone__, False, True],
                                   "AT H2 DEFENDING ZONE": [self.__parse_team_defending_zone__, False, True],                                   
                                   "HT H1 HEAT MAP": [self.__parse_heat_map__, True, False],
                                   "HT H2 HEAT MAP": [self.__parse_heat_map__, True, False],
                                   "AT H1 HEAT MAP": [self.__parse_heat_map__, True, False],
                                   "AT H2 HEAT MAP": [self.__parse_heat_map__, True, False],                                   
                                   "HT PENALTY SHOOTOUT GOALS": [self.__parse_pk_shootout__, False, True],
                                   "AT PENALTY SHOOTOUT GOALS": [self.__parse_pk_shootout__, False, True],
                                   "H1 COMMENTS": [self.__parse_comments__, True, False],
                                   "H2 COMMENTS": [self.__parse_comments__, True, False]
                                  }

        self.__read_file__(fileName)

    # Data file parsing functions
    def __parse_home_team__(self, _, row):
        self.homeTeam = row[1]
    
    def __parse_away_team__(self, _, row):
        self.awayTeam = row[1]
    
    def __parse_game_date__(self, _, row):
        self.gameDate = row[1]
        
    def __parse_duration__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[0]
        try:
            value = int(row[1])
        except:
            value = 0
        if (period == 'H1'):
            self.h1Duration = value
        elif (period == 'H2'):
            self.h2Duration = value
        elif (period == 'OT1'):
            self.ot1Duration = value
        elif (period == 'OT2'):
            self.ot2Duration = value
    
    def __parse_goals__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamGoals[period] = value
        elif parseString[0] == "AT":
            self.awayTeamGoals[period] = value

    def __parse_assists__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamAssists[period] = value
        elif parseString[0] == "AT":
            self.awayTeamAssists[period] = value

    def __parse_shots__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamShots[period] = value
        elif parseString[0] == "AT":
            self.awayTeamShots[period] = value

    def __parse_saves__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamSaves[period] = value
        elif parseString[0] == "AT":
            self.awayTeamSaves[period] = value

    def __parse_corners__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamCorners[period] = value
        elif parseString[0] == "AT":
            self.awayTeamCorners[period] = value

    def __parse_yellow_cards__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamYellowCards[period] = value
        elif parseString[0] == "AT":
            self.awayTeamYellowCards[period] = value

    def __parse_red_cards__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamRedCards[period] = value
        elif parseString[0] == "AT":
            self.awayTeamRedCards[period] = value

    def __parse_possession__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if (parseString[0] == "HT" and period == "H1"):
            self.homeTeamH1PassingStats.possessionInstances = value
        elif (parseString[0] == "AT" and period == "H1"):
            self.awayTeamH1PassingStats.possessionInstances = value
        elif (parseString[0] == "HT" and period == "H2"):
            self.homeTeamH2PassingStats.possessionInstances = value
        elif (parseString[0] == "AT" and period == "H2"):
            self.awayTeamH2PassingStats.possessionInstances = value

    def __parse_max_passes__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if (parseString[0] == "HT" and period == "H1"):
            self.homeTeamH1PassingStats.maxConsecutivePasses = value
        elif (parseString[0] == "AT" and period == "H1"):
            self.awayTeamH1PassingStats.maxConsecutivePasses = value
        elif (parseString[0] == "HT" and period == "H2"):
            self.homeTeamH2PassingStats.maxConsecutivePasses = value
        elif (parseString[0] == "AT" and period == "H2"):
            self.awayTeamH2PassingStats.maxConsecutivePasses = value
            
    def __parse_formation__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        if (keyVal[0] == row[0]):              # this is the first row
            if parseString[0] == "HT":
                self.homeTeamFormationName[period] = row[1]
            elif parseString[0] == "AT":
                self.awayTeamFormationName[period] = row[1]
        else:                               # this is a row after the first row so add the nodes
            if (parseString[0] == "HT" and period == "H1"):
                self.homeTeamH1Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.homeTeamH1PassingGraph.add_nodes_from([row[2]])
            elif (parseString[0] == "AT" and period == "H1"):
                self.awayTeamH1Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.awayTeamH1PassingGraph.add_nodes_from([row[2]])
            elif (parseString[0] == "HT" and period == "H2"):
                self.homeTeamH2Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.homeTeamH2PassingGraph.add_nodes_from([row[2]])
            elif (parseString[0] == "AT" and period == "H2"):
                self.awayTeamH2Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.awayTeamH2PassingGraph.add_nodes_from([row[2]])

    def __parse_passing_graph__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        if (parseString[0] == "HT" and period == "H1"):
            self.homeTeamH1PassingGraph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])
        elif (parseString[0] == "AT" and period == "H1"):
            self.awayTeamH1PassingGraph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])
        elif (parseString[0] == "HT" and period == "H2"):
            self.homeTeamH2PassingGraph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])
        elif (parseString[0] == "AT" and period == "H2"):
            self.awayTeamH2PassingGraph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])

    def __parse_passing_tree__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        if (parseString[0] == "HT" and period == "H1"):
            self.homeTeamH1PassingStats.process_tree_branch(self.homeTeamH1PassingGraph, row[1:len(row)])
        elif (parseString[0] == "AT" and period == "H1"):
            self.awayTeamH1PassingStats.process_tree_branch(self.awayTeamH1PassingGraph, row[1:len(row)])
        elif (parseString[0] == "HT" and period == "H2"):
            self.homeTeamH2PassingStats.process_tree_branch(self.homeTeamH2PassingGraph, row[1:len(row)])
        elif (parseString[0] == "AT" and period == "H2"):
            self.awayTeamH2PassingStats.process_tree_branch(self.awayTeamH2PassingGraph, row[1:len(row)])
    
    def __parse_team_defending_zone__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]

        if (parseString[0] == "HT" and period == "H1"):
            self.homeTeamH1HeatMapStats.set_team_defending_zone(int(row[1]))
        elif (parseString[0] == "AT" and period == "H1"):
            self.awayTeamH1HeatMapStats.set_team_defending_zone(int(row[1]))
        elif (parseString[0] == "HT" and period == "H2"):
            self.homeTeamH2HeatMapStats.set_team_defending_zone(int(row[1]))
        elif (parseString[0] == "AT" and period == "H2"):
            self.awayTeamH2HeatMapStats.set_team_defending_zone(int(row[1]))

    def __parse_heat_map__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[1]
        
        # set default column numbers
        zoneCol = 1
        passesCol = 2
        assistsCol = 3
        possessionsCol = 4
        shotsOffTargetCol = 5
        shotsOnTargetCol = 6
        shotsScoredCol = 7
        ownGoalsCol = 8
        lostPossessionCol = 9
        
        # update column numbers based on header row
        i = 0
        for heading in keyVal:
            if heading.upper() == "PASSES COMPLETED":
                passesCol = i
            elif heading.upper() == "ASSISTS":
                assistsCol = i
            elif heading.upper() == "3RD CONSECUTIVE PASS INSTANCES":
                possessionsCol = i
            elif heading.upper() == "SHOTS OFF TARGET":
                shotsOffTargetCol = i
            elif heading.upper() == "SHOTS ON TARGET":
                shotsOnTargetCol = i
            elif heading.upper() == "SHOTS SCORED":
                shotsScoredCol = i
            elif heading.upper() == "OWN GOALS SCORED":
                ownGoalsCol = i
            elif heading.upper() == "LOST POSSESSION":
                lostPossessionCol = i
            i = i + 1
        try:
            passes = int(row[passesCol])
        except:
            passes = 0
        try:
            assists = int(row[assistsCol])
        except:
            assists = 0
        try:
            possessions = int(row[possessionsCol])
        except:
            possessions = 0
        try:
            shotsOffTarget = int(row[shotsOffTargetCol])
        except:
            shotsOffTarget = 0
        try:
            shotsOnTarget = int(row[shotsOnTargetCol])
        except:
            shotsOnTarget = 0
        try:
            shotsScored = int(row[shotsScoredCol])
        except:
            shotsScored = 0
        try:
            ownGoals = int(row[ownGoalsCol])
        except:
            ownGoals = 0
        try:
            lostPossession = int(row[lostPossessionCol])
        except:
            lostPossession = 0
            
        if (parseString[0] == "HT" and period == "H1"):
            self.homeTeamH1HeatMapStats.add_zone(int(row[zoneCol]), shotsOffTarget, shotsOnTarget, shotsScored, ownGoals, assists, passes, possessions, lostPossession)
        elif (parseString[0] == "AT" and period == "H1"):
            self.awayTeamH1HeatMapStats.add_zone(int(row[zoneCol]), shotsOffTarget, shotsOnTarget, shotsScored, ownGoals, assists, passes, possessions, lostPossession)
        elif (parseString[0] == "HT" and period == "H2"):
            self.homeTeamH2HeatMapStats.add_zone(int(row[zoneCol]), shotsOffTarget, shotsOnTarget, shotsScored, ownGoals, assists, passes, possessions, lostPossession)
        elif (parseString[0] == "AT" and period == "H2"):
            self.awayTeamH2HeatMapStats.add_zone(int(row[zoneCol]), shotsOffTarget, shotsOnTarget, shotsScored, ownGoals, assists, passes, possessions, lostPossession)

    def __parse_pk_shootout__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        try:
            value = int(row[1])
        except:
            value = 0
        if parseString[0] == "HT":
            self.homeTeamPenaltyShootoutGoals = value
        elif parseString[0] == "AT":
            self.awayTeamPenaltyShootoutGoals = value
        
    def __parse_comments__(self, keyVal, row):
        parseString = keyVal[0].split(' ')
        period = parseString[0]
        if period == "H1":
            if (row[1] == "HT"):
                self.homeTeamH1Comments.append(row[2])
            elif (row[1] == "AT"):
                self.awayTeamH1Comments.append(row[2])
        elif period == "H2":
            if (row[1] == "HT"):
                self.homeTeamH2Comments.append(row[2])
            elif (row[1] == "AT"):
                self.awayTeamH2Comments.append(row[2])
    
    def __read_file__(self,fileName):
        csvFileObj = open(fileName)
        readerObj = csv.reader(csvFileObj)
        currentField = None
        firstRow = True
        for row in readerObj:
            if row[0] in self.__dataFileFields__:
                # start of new field to parse
                currentField = row
                firstRow = True
                validEntry = True
            elif row[0] != "":
                validEntry = False
            else:
                firstRow = False

            if validEntry == True:
                if (firstRow == True and self.__dataFileFields__[currentField[0]][1] == False):
                    self.__dataFileFields__[currentField[0]][0](currentField, row)
                    firstRow = False
                elif (firstRow == False and self.__dataFileFields__[currentField[0]][2] == False):
                    self.__dataFileFields__[currentField[0]][0](currentField, row)


    def __draw_passing_sequence_histogram__(self, homeTeamPassingStats, awayTeamPassingStats, histogramMinRange, histogramMaxRange, plotTitle):
        """Description: Public API function to draw a histogram of number of passes in sequence
        Inputs: 
            homeTeamPassingStats - Passing_Stats object with the data to be used for the histogram for the home team
            awayTeamPassingStats - Passing_Stats object with the data to be used for the histogram for the home team
            histogramMinRange - the min number of passes in sequence to start the histogram at (usually 1)
            histogramMaxRange - the max number of passes in sequence to end the histogram at
            plotTitle - string with title to put at the top of the graph
        Outputs:
            a plot containing the specified histogram
        """
        homeTeamColor = "green"
        awayTeamColor = "blue"
        sequenceLabels = []
        htValues = []
        atValues = []
        for i in range (histogramMinRange, histogramMaxRange+1):
            sequenceLabels.append(i)
            if i in homeTeamPassingStats.passingSequenceHistogram:
                htValues.append(homeTeamPassingStats.passingSequenceHistogram[i])
            else:
                htValues.append(0)
                
            if i in awayTeamPassingStats.passingSequenceHistogram:
                atValues.append(awayTeamPassingStats.passingSequenceHistogram[i])
            else:
                atValues.append(0)

        x = np.arange(len(sequenceLabels))
        width = 0.35
        
        maxValue = max([max(htValues), max(atValues)])
        yVal = 0
        y = []
        while yVal < (maxValue+4):
            y.append(yVal)
            yVal = yVal + int(maxValue/4)
            
        print(y)
        
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, htValues, width, label = self.homeTeam, color=homeTeamColor)
        rects2 = ax.bar(x + width/2, atValues, width, label = self.awayTeam, color=awayTeamColor)
        ax.set_ylabel("Number of Occurrences")
        ax.set_title(plotTitle)
        ax.set_xticks(x)
        ax.set_xticklabels(sequenceLabels)
        ax.set_yticks(y)
        ax.legend()
        fig.tight_layout()
        plt.show()
        
        
    def draw_passing_sequence_histogram(self, half, histogramMinRange, histogramMaxRange):
        """Description: Public API function to draw a histogram of number of passes in sequence
        Inputs: 
            half - 1 for first half, 2 for second half
            histogramMinRange - the min number of passes in sequence to start the histogram at (usually 1)
            histogramMaxRange - the max number of passes in sequence to end the histogram at
        Outputs:
            calls private function self.__draw_passing_sequence_histogram__ with the appropriate arguments
            to plot the histogram
        """
        plotTitle = "Passing Sequence Histogram - " + self.homeTeam + " vs. " + self.awayTeam
        if half == 1:
            plotTitle = plotTitle + ", for 1st Half"
            self.__draw_passing_sequence_histogram__(self.homeTeamH1PassingStats, self.awayTeamH1PassingStats, histogramMinRange, histogramMaxRange, plotTitle)
        elif half == 2:
            plotTitle = plotTitle + ", for 2nd Half"
            self.__draw_passing_sequence_histogram__(self.homeTeamH2PassingStats, self.awayTeamH2PassingStats, histogramMinRange, histogramMaxRange, plotTitle)
            
    def __draw_passing_graph__(self,graph,formation,elarge,esmall,plotTitle):
        nx.draw_networkx_nodes(graph, formation)
        nx.draw_networkx_labels(graph, formation)
        nx.draw_networkx_edges(graph, formation, edgelist=elarge, width=1)
        nx.draw_networkx_edges(graph, formation, edgelist=esmall, width=1, alpha=0.5, edge_color='b', style='dashed')
        plt.title(plotTitle)
        plt.show()
    
    def draw_passing_graph(self,team,half,weight,omit):
        # weight is the value for number passes >= to display prominently and < to either not display or display less prominently
        # omit: true = don't display passes < weight at all
        if team == 'H':
            if half == 1:
                formation = self.homeTeamH1Formation
                elarge=[(u,v) for (u,v,d) in self.homeTeamH1PassingGraph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.homeTeamH1PassingGraph.edges(data=True) if d['weight'] < weight]
                graph = self.homeTeamH1PassingGraph
                plotTitle = "Passing Graph - " + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.homeTeam + ", 1st Half"
            elif half == 2:
                formation = self.homeTeamH2Formation
                elarge=[(u,v) for (u,v,d) in self.homeTeamH2PassingGraph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.homeTeamH2PassingGraph.edges(data=True) if d['weight'] < weight]
                graph = self.homeTeamH2PassingGraph
                plotTitle = "Passing Graph - " + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.homeTeam + ", 2nd Half"
        elif team == 'A':
            if half == 1:
                formation = self.awayTeamH1Formation
                elarge=[(u,v) for (u,v,d) in self.awayTeamH1PassingGraph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.awayTeamH1PassingGraph.edges(data=True) if d['weight'] < weight]
                graph = self.awayTeamH1PassingGraph
                plotTitle = "Passing Graph - " + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.awayTeam + ", 1st Half"
            elif half == 2:
                formation = self.awayTeamH2Formation
                elarge=[(u,v) for (u,v,d) in self.awayTeamH2PassingGraph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.awayTeamH2PassingGraph.edges(data=True) if d['weight'] < weight]
                graph = self.awayTeamH2PassingGraph
                plotTitle = "Passing Graph - " + self.homeTeam + " vs. " + self.awayTeam + ", for " + self.awayTeam + ", 2nd Half"
        if omit == False:
            self.__draw_passing_graph__(graph,formation,elarge,esmall,plotTitle)
        else:
            noSmall = []
            self.__draw_passing_graph__(graph,formation,elarge,noSmall,plotTitle)

            
    def __draw_pitch__(self):
        """Description: Draws a diagram of a field split into zones
        Inputs: 
        Outputs:
            Returns - list of x,y coordinates by zone ([zone][x,y]) for the center point of each zone
            plots a graph of the pitch with zones labeled
        """
        #TODO: these currently can't be changed without messing up the plot because not all parameters are calculated off of them
        PITCH_LENGTH = 150
        PITCH_WIDTH = 90
        
        #Create figure
        fig=plt.figure(figsize=(7,8))
        ax=fig.add_subplot(1,1,1)

        #Pitch Outline & Centre Line
        plt.plot([0,0],[0,PITCH_LENGTH], color="black")
        plt.plot([0,PITCH_WIDTH],[PITCH_LENGTH,PITCH_LENGTH], color="black")
        plt.plot([PITCH_WIDTH,PITCH_WIDTH],[PITCH_LENGTH,0], color="black")
        plt.plot([PITCH_WIDTH,0],[0,0], color="black")
        plt.plot([0,PITCH_WIDTH],[PITCH_LENGTH/2,PITCH_LENGTH/2], color="black")

        #Left Penalty Area
        plt.plot([65,25],[21,21],color="black")
        plt.plot([65,65],[0,21],color="black")
        plt.plot([25,25],[21,0],color="black")

        #Right Penalty Area
        plt.plot([65,65],[PITCH_LENGTH,129],color="black")
        plt.plot([65,25],[129,129],color="black")
        plt.plot([25,25],[129,PITCH_LENGTH],color="black")

        #Prepare Circles
        centreCircle = plt.Circle((PITCH_WIDTH/2,PITCH_LENGTH/2),9.15,color="black",fill=False)

        #Draw Circles
        ax.add_patch(centreCircle)

        #Prepare Arcs
        leftArc = Arc((45,17),height=18.3,width=18.3,angle=0,theta1=28,theta2=152,color="black")
        rightArc = Arc((45,133),height=18.3,width=18.3,angle=0,theta1=208,theta2=332,color="black")

        #Draw Arcs
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)

        # Draw zones
        plt.plot([PITCH_WIDTH/3,PITCH_WIDTH/3],[0,PITCH_LENGTH],color="red")
        plt.plot([2*PITCH_WIDTH/3,2*PITCH_WIDTH/3],[0,PITCH_LENGTH],color="red")
        plt.plot([0,PITCH_WIDTH],[PITCH_LENGTH/6,PITCH_LENGTH/6],color="red")
        plt.plot([0,PITCH_WIDTH],[2*PITCH_LENGTH/6,2*PITCH_LENGTH/6],color="red")
        plt.plot([0,PITCH_WIDTH],[3*PITCH_LENGTH/6,3*PITCH_LENGTH/6],color="red")
        plt.plot([0,PITCH_WIDTH],[4*PITCH_LENGTH/6,4*PITCH_LENGTH/6],color="red")
        plt.plot([0,PITCH_WIDTH],[5*PITCH_LENGTH/6,5*PITCH_LENGTH/6],color="red")

        #Tidy Axes
        plt.axis('off')

        #create zone map points
        zoneMap = []
        zoneX = PITCH_WIDTH / 3 / 2
        zoneY = PITCH_LENGTH / 6 / 2
        zoneWidth = PITCH_WIDTH / 3
        zoneLength = PITCH_LENGTH / 6
        zoneZero = [zoneWidth*zoneLength, zoneWidth, zoneLength]
        zoneMap.append(zoneZero)                                                # No Zone 0, but this element contains the following list: 
                                                                                #   [0] = the maximum bubble size (area) that can be plotted in any of the zones, 
                                                                                #   [1] = the zone width
                                                                                #   [2] = the zone length
        zoneMap.append([zoneX, zoneY])                                          # Zone 1 [x,y]
        zoneMap.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 2 [x,y]
        zoneMap.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 3 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zoneMap.append([zoneX, zoneY])                                          # Zone 4 [x,y]
        zoneMap.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 5 [x,y]
        zoneMap.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 6 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zoneMap.append([zoneX, zoneY])                                          # Zone 7 [x,y]
        zoneMap.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 8 [x,y]
        zoneMap.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 9 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zoneMap.append([zoneX, zoneY])                                          # Zone 10 [x,y]
        zoneMap.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 11 [x,y]
        zoneMap.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 12 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zoneMap.append([zoneX, zoneY])                                          # Zone 13 [x,y]
        zoneMap.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 14 [x,y]
        zoneMap.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 15 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zoneMap.append([zoneX, zoneY])                                          # Zone 16 [x,y]
        zoneMap.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 17 [x,y]
        zoneMap.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 18 [x,y]
        
        return(zoneMap)

    def __draw_heat_map__(self,zoneMap,homeTeamHeatMapStats,awayTeamHeatMapStats,mapType,plotTitle,filename):
        """Description: Draws a diagram of a field split into zones
        Preconditions: Assumes that __draw_pitch__ has been called ahead of this function being called
        Inputs: zoneMap - a list of x and y coordinates of the center point in each zone ([zone#][x,y])
                          zoneMap[0] contains the radius of the zone
                homeTeamHeatMapStats - a Heat_Map_Stats object containing the stats to be plotted
                awayTeamHeatMapStats - a Heat_Map_Stats object containing the stats to be plotted
                mapType - the type of map to draw (either "S" for shot, "P" for pass, "G" for goal, "L" for lost possession)
                plotTitle - string with title to place on the map
                filename - name of a graphics file to output the heat map to (if None, then will open the heat map in a window on screen)
        Outputs:
            plots a graph of the pitch with zones labeled
        """
        homeTeamColor = "green"
        awayTeamColor = "blue"
        # if multiple heat maps are to be plotted on the same graph, set the offset for each one in each zone
        if homeTeamHeatMapStats == None:
            offset = 0
            totalPasses = awayTeamHeatMapStats.total_passes()
            totalLostPossession = awayTeamHeatMapStats.total_lost_possession_instances()
        elif awayTeamHeatMapStats == None:
            offset = 0
            totalPasses = homeTeamHeatMapStats.total_passes()
            totalLostPossession = homeTeamHeatMapStats.total_lost_possession_instances()
        else:
            offset = 5
            totalPasses = homeTeamHeatMapStats.total_passes() + awayTeamHeatMapStats.total_passes()
            totalLostPossession = homeTeamHeatMapStats.total_lost_possession_instances() + awayTeamHeatMapStats.total_lost_possession_instances()               
 
        if mapType == "P":
            # plot home team heat map pass stats
            if totalPasses > 0:                     # only plot this if there is no danger of divide by 0
                if homeTeamHeatMapStats:
                    for i in range (1, len(zoneMap)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        sizeVal = 3 * zoneMap[0][0] * homeTeamHeatMapStats.zonePasses[i] / totalPasses
                        plt.scatter(x=zoneMap[i][0]+offset, y=zoneMap[i][1], s=sizeVal, alpha=0.5, color=homeTeamColor)
    
                # plot away team heat map pass stats
                if awayTeamHeatMapStats:
                    for i in range (1, len(zoneMap)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        sizeVal = 3 * zoneMap[0][0] * awayTeamHeatMapStats.zonePasses[i] / totalPasses
                        plt.scatter(x=zoneMap[i][0]-offset, y=zoneMap[i][1], s=sizeVal, alpha=0.5, color=awayTeamColor)

            # Print the Legend
            legXVal = zoneMap[1][0]
            legYVal = zoneMap[1][1] - 50
            plt.text(legXVal,legYVal,"Legend")
            plt.text(legXVal+10,legYVal-15,self.homeTeam)
            plt.text(legXVal+10,legYVal-30,self.awayTeam)
            plt.scatter(x=legXVal+5, y=legYVal-12, s=10, color=homeTeamColor)
            plt.scatter(x=legXVal+5, y=legYVal-27, s=10, color=awayTeamColor)

        if mapType == "L":
            # plot home team heat map lost possession stats
            if totalLostPossession > 0:                 # only plot this if no danger of divide by 0
                if homeTeamHeatMapStats:
                    for i in range (1, len(zoneMap)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        sizeVal = 3 * zoneMap[0][0] * homeTeamHeatMapStats.zoneLostPossessionInstances[i] / totalLostPossession
                        plt.scatter(x=zoneMap[i][0]+offset, y=zoneMap[i][1], s=sizeVal, alpha=0.5, color=homeTeamColor)
    
                # plot away team heat map lost possession stats
                if awayTeamHeatMapStats:
                    for i in range (1, len(zoneMap)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        sizeVal = 3 * zoneMap[0][0] * awayTeamHeatMapStats.zoneLostPossessionInstances[i] / totalLostPossession
                        plt.scatter(x=zoneMap[i][0]-offset, y=zoneMap[i][1], s=sizeVal, alpha=0.5, color=awayTeamColor)

            # Print the Legend
            legXVal = zoneMap[1][0]
            legYVal = zoneMap[1][1] - 50
            plt.text(legXVal,legYVal,"Legend")
            plt.text(legXVal+10,legYVal-15,self.homeTeam)
            plt.text(legXVal+10,legYVal-30,self.awayTeam)
            plt.scatter(x=legXVal+5, y=legYVal-12, s=10, color=homeTeamColor)
            plt.scatter(x=legXVal+5, y=legYVal-27, s=10, color=awayTeamColor)
            
        elif mapType == "S":
            # plot home team heat map shooting stats
            if homeTeamHeatMapStats:
                for i in range (1, len(zoneMap)):
                    if (homeTeamHeatMapStats.zoneOwnGoals[i] > 0 or homeTeamHeatMapStats.zoneShotsScored[i] > 0 or
                       homeTeamHeatMapStats.zoneShotsOffTarget[i] > 0 or homeTeamHeatMapStats.zoneShotsOnTarget[i] > 0):
                        xVal = zoneMap[i][0] + offset
                        yVal = zoneMap[i][1]
                        plt.text(xVal,yVal+5,"OG: " + str(homeTeamHeatMapStats.zoneOwnGoals[i]), fontsize=6, color=homeTeamColor)
                        plt.text(xVal,yVal+1,"SS: " + str(homeTeamHeatMapStats.zoneShotsScored[i]), fontsize=6, color=homeTeamColor)
                        plt.text(xVal,yVal-3,"ON: " + str(homeTeamHeatMapStats.zoneShotsOnTarget[i]), fontsize=6, color=homeTeamColor)
                        plt.text(xVal,yVal-7,"OFF: " + str(homeTeamHeatMapStats.zoneShotsOffTarget[i]), fontsize=6, color=homeTeamColor)

            if awayTeamHeatMapStats:
                for i in range (1, len(zoneMap)):
                    if (awayTeamHeatMapStats.zoneOwnGoals[i] > 0 or awayTeamHeatMapStats.zoneShotsScored[i] > 0 or
                       awayTeamHeatMapStats.zoneShotsOffTarget[i] > 0 or awayTeamHeatMapStats.zoneShotsOnTarget[i] > 0):
                        xVal = zoneMap[i][0] - offset
                        yVal = zoneMap[i][1]
                        plt.text(xVal,yVal+5,"OG: " + str(awayTeamHeatMapStats.zoneOwnGoals[i]), fontsize=6, color=awayTeamColor)
                        plt.text(xVal,yVal+1,"SS: " + str(awayTeamHeatMapStats.zoneShotsScored[i]), fontsize=6, color=awayTeamColor)
                        plt.text(xVal,yVal-3,"ON: " + str(awayTeamHeatMapStats.zoneShotsOnTarget[i]), fontsize=6, color=awayTeamColor)
                        plt.text(xVal,yVal-7,"OFF: " + str(awayTeamHeatMapStats.zoneShotsOffTarget[i]), fontsize=6, color=awayTeamColor)
                       
            # Print the Legend
            legXVal = zoneMap[1][0]
            legYVal = zoneMap[1][1] - 50
            plt.text(legXVal,legYVal,"Legend")
            plt.text(legXVal+10,legYVal-15,self.homeTeam + " Shots", color=homeTeamColor)
            plt.text(legXVal+10,legYVal-30,self.awayTeam + " Shots", color=awayTeamColor)
            plt.text(legXVal+50,legYVal-10,"OG: Own Goals", fontsize=6)
            plt.text(legXVal+50,legYVal-14,"SS: Shots Scored", fontsize=6)
            plt.text(legXVal+50,legYVal-18,"ON: Shots On Target", fontsize=6)
            plt.text(legXVal+50,legYVal-22,"OFF: Shots Off Target", fontsize=6)

            # set extents of plot so legend is visible
            plotYLimits = [legYVal-30, zoneMap[18][1] + zoneMap[0][2] + 10]
            plt.ylim(plotYLimits)
            
                
        # Print team defending each goal
        if homeTeamHeatMapStats:
            defendingZone = homeTeamHeatMapStats.teamDefendingZone
            xVal = zoneMap[defendingZone][0] - zoneMap[0][1] / 2
            if defendingZone <= 9:
                yVal = zoneMap[defendingZone][1] - zoneMap[0][2]
            else:
                yVal = zoneMap[defendingZone][1] + zoneMap[0][2]
            plt.text(xVal,yVal,self.homeTeam)

        if awayTeamHeatMapStats:
            defendingZone = awayTeamHeatMapStats.teamDefendingZone
            xVal = zoneMap[defendingZone][0] - zoneMap[0][1] / 2
            if defendingZone <= 9:
                yVal = zoneMap[defendingZone][1] - zoneMap[0][2]
            else:
                yVal = zoneMap[defendingZone][1] + zoneMap[0][2]
            plt.text(xVal,yVal,self.awayTeam)
                    


        plt.title(plotTitle,pad=30)
        
        if filename == None:
            #Display Heat Map
            plt.show()
        else:
            plt.tight_layout()
            plt.savefig(filename,dpi=600)
            plt.close()


    def draw_heat_map(self,team,half,mapType,filename=None):
        """Description: Draws a heat map graph for the specified team in the specified half of the game
        Inputs: team - the team to draw the map for (either "H" for home team or "A" for away team or "B" for both on same graph)
                half - the half to draw the map for (either 1 for first half or 2 for second half)
                mapType - the type of map to draw (either "S" for shot, "P" for pass, "L" for lost possession)
                filename - optional parameter if you want the map output to a file instead of opening a window
        Outputs:
            plots a graph
        """
        zoneMap = self.__draw_pitch__()
        if mapType == "S":
            plotTitle = "Shot Heat Map - "
        elif mapType == "P":
            plotTitle = "Passing Heat Map - "
        elif mapType == "L":
            plotTitle = "Lost Possession Heat Map - "
        else:
            return
            
        if team == 'H':
            if half == 1:
                plotTitle = plotTitle + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.homeTeam + ", 1st Half"
                self.__draw_heat_map__(zoneMap, self.homeTeamH1HeatMapStats, None, mapType, plotTitle, filename)
            elif half == 2:
                plotTitle = plotTitle + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.homeTeam + ", 2nd Half"
                self.__draw_heat_map__(zoneMap, self.homeTeamH2HeatMapStats, None, mapType, plotTitle, filename)
        elif team == 'A':
            if half == 1:
                plotTitle = plotTitle + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.awayTeam + ", 1st Half"
                self.__draw_heat_map__(zoneMap, None, self.awayTeamH1HeatMapStats, mapType, plotTitle, filename)
            elif half == 2:
                plotTitle = plotTitle + self.homeTeam + " vs. " + self.awayTeam + ",for " + self.awayTeam + ", 2nd Half"
                self.__draw_heat_map__(zoneMap, None, self.awayTeamH2HeatMapStats, mapType, plotTitle, filename)
        elif team == 'B':
            if half == 1:
                plotTitle = plotTitle + self.homeTeam + " vs. " + self.awayTeam + ",for both teams, 1st Half"
                self.__draw_heat_map__(zoneMap, self.homeTeamH1HeatMapStats, self.awayTeamH1HeatMapStats, mapType, plotTitle, filename)
            elif half == 2:
                plotTitle = plotTitle + self.homeTeam + " vs. " + self.awayTeam + ",for both teams, 2nd Half"
                self.__draw_heat_map__(zoneMap, self.homeTeamH2HeatMapStats, self.awayTeamH2HeatMapStats, mapType, plotTitle, filename)

         
    def final_home_team_score(self):
        score = 0
        for period in self.homeTeamGoals:
            score = score + self.homeTeamGoals[period]
        return score
        
    def final_away_team_score(self):
        score = 0
        for period in self.awayTeamGoals:
            score = score + self.awayTeamGoals[period]
        return score
    
    def __total_passes__(self, passingGraph):
        passes = 0
        for u,v,weight in passingGraph.edges(data=True):
            passes = passes + weight['weight']
        return passes
        
    def __top_passer__(self, passingGraph):
        degrees = passingGraph.out_degree(weight='weight')
        passers = sorted(degrees, key=lambda x: x[1], reverse=True)
        return passers[0]

    def __hub_player__(self, passingGraph):
        degrees = passingGraph.degree(weight='weight')
        passers = sorted(degrees, key=lambda x: x[1], reverse=True)
        return passers[0]
    
    def home_team_passing_rate(self, period):
        if (period == "H1"):
            totalPasses = self.__total_passes__(self.homeTeamH1PassingGraph)
            passingRate = totalPasses / self.h1Duration
        elif (period == "H2"):
            totalPasses = self.__total_passes__(self.homeTeamH2PassingGraph)
            passingRate = totalPasses / self.h2Duration
        else:
            return(0)
        return(passingRate)

    def away_team_passing_rate(self, period):
        if (period == "H1"):
            totalPasses = self.__total_passes__(self.awayTeamH1PassingGraph)
            passingRate = totalPasses / self.h1Duration
        elif (period == "H2"):
            totalPasses = self.__total_passes__(self.awayTeamH2PassingGraph)
            passingRate = totalPasses / self.h2Duration
        else:
            return(0)
        return(passingRate)
            
    def home_team_top_passer(self, period):
        if (period == "H1"):
            topPasser = self.__top_passer__(self.homeTeamH1PassingGraph)
        elif (period == "H2"):
            topPasser = self.__top_passer__(self.homeTeamH2PassingGraph)
        return topPasser
 
    def away_team_top_passer(self, period):
        if (period == "H1"):
            topPasser = self.__top_passer__(self.awayTeamH1PassingGraph)
        elif (period == "H2"):
            topPasser = self.__top_passer__(self.awayTeamH2PassingGraph)
        return topPasser

    def home_team_hub_player(self, period):
        if (period == "H1"):
            topHub = self.__hub_player__(self.homeTeamH1PassingGraph)
        elif (period == "H2"):
            topHub = self.__hub_player__(self.homeTeamH2PassingGraph)
        return topHub

    def away_team_hub_player(self, period):
        if (period == "H1"):
            topHub = self.__hub_player__(self.awayTeamH1PassingGraph)
        elif (period == "H2"):
            topHub = self.__hub_player__(self.awayTeamH2PassingGraph)
        return topHub
    
    def home_team_passing_rate_from_heat_map(self, period):
        if (period == "H1"):
            totalPasses = self.homeTeamH1HeatMapStats.total_passes()
            passingRate = totalPasses / self.h1Duration
        elif (period == "H2"):
            totalPasses = self.homeTeamH2HeatMapStats.total_passes()
            passingRate = totalPasses / self.h2Duration
        else:
            return(0)
        return(passingRate)

    def away_team_passing_rate_from_heat_map(self, period):
        if (period == "H1"):
            totalPasses = self.awayTeamH1HeatMapStats.total_passes()
            passingRate = totalPasses / self.h1Duration
        elif (period == "H2"):
            totalPasses = self.awayTeamH2HeatMapStats.total_passes()
            passingRate = totalPasses / self.h2Duration
        else:
            return(0)
        return(passingRate)
