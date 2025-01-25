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
        self.team_defending_zone = 0
        self.zone_shots_off_target = {}                # dictionary containing number of shots not on target in each zone (zone #: # shots)
        self.zone_shots_on_target = {}                 # dictionary containing number of shots on target but not scored in each zone (zone #: # shots]
        self.zone_shots_scored = {}                   # dictionary containing number of shots scored in each zone (zone #: # goals)
        self.zone_own_goals = {}                          # dictionary containing number of shots scored as own goals in each zone (zone#: # own goals)
        self.zone_assists = {}                       # dictionary containing number of assist passes completed in each zone (zone#: # assists)
        self.zone_passes = {}                        # dictionary containing number of passes completed in each zone (zone #: # passes)
        self.zone_possession_instances = {}           # dictionary containing number of possession instances (3 consecutive passes) in each zone (zone #: # possessions)
        self.zone_lost_possession_instances = {}       # dictionary containing number of times lost possession in each zone (zone#: # lost possessions)

    def set_team_defending_zone(self, zone_num):
        """Description: Set the zone number that the team that this heat map is for is defending
        Inputs: zone_num - the zone number to set to
        Outputs:
            Sets member variable self.team_defending_zone to zone_num
        """
        self.team_defending_zone = zone_num
        
    def add_zone(self, zone_num, shots_off_target, shots_on_target, shots_scored, own_goals, assists, passes, possessions, lost_possession):
        """Description: Extract statistics from a zone and accumulate them into the statistics counters
        Inputs: zone_num - the zone number to add
                shots_off_target - the number of shots off target for this zone
                shots_on_target - the number of shots on target for this zone
                shots_scored - the number of shots scored for this zone
                own_goals - the number of shots scored as own goals for this zone
                assists - the number of assist passes into this zone
                passes - the number of passes into this zone
                possessions - the number of possession instances ended in this zone
                lost_possession - the number of times possession lost in the this zone
        Outputs:
            Adds zone to the dictionary if it isn't already in. If the zone is already in the dictionary, then it overwrites the values with the new values
        """
        self.zone_shots_off_target[zone_num] = shots_off_target
        self.zone_shots_on_target[zone_num] = shots_on_target
        self.zone_shots_scored[zone_num] = shots_scored
        self.zone_own_goals[zone_num] = own_goals
        self.zone_assists[zone_num] = assists
        self.zone_passes[zone_num] = passes
        self.zone_possession_instances[zone_num] = possessions
        self.zone_lost_possession_instances[zone_num] = lost_possession
        
    def total_passes(self):
        """Description: Add the passes from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the passes in all zones
        """
        total_passes = 0
        for zone in self.zone_passes:
            total_passes = total_passes + self.zone_passes[zone]
        return(total_passes)

    def total_possession_instances(self):
        """Description: Add the possession instances from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the possession instances in all zones
        """
        total_possession = 0
        for zone in self.zone_possession_instances:
            total_possession = total_possession + self.zone_possession_instances[zone]
        return(total_possession)

    def total_lost_possession_instances(self):
        """Description: Add the lost possession instances from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the lost possession instances in all zones
        """
        total_lost_possession = 0
        for zone in self.zoneLost_possession_instances:
            total_lost_possession = total_lost_possession + self.zoneLost_possession_instances[zone]
        return(total_lost_possession)

    def total_shots_on_target(self):
        """Description: Add the shots on target from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the shots on target in all zones
        """
        total_shots = 0
        for zone in self.zone_shots_on_target:
            total_shots = total_shots + self.zone_shots_on_target[zone]
            
        for zone in self.zone_shots_scored:
            total_shots = total_shots + self.zone_shots_scored[zone]

        for zone in self.zone_own_goals:
            total_shots = total_shots + self.zone_own_goals[zone]
        return(total_shots)

    def total_shots(self):
        """Description: Add the shots from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the shots in all zones
        """
        total_shots = 0
        for zone in self.zone_shots_off_target:
            total_shots = total_shots + self.zone_shots_off_target[zone]

        for zone in self.zoneShots_on_target:
            total_shots = total_shots + self.zone_shots_on_target[zone]
            
        for zone in self.zone_shots_scored:
            total_shots = total_shots + self.zone_shots_scored[zone]

        for zone in self.zone_own_goals:
            total_shots = total_shots + self.zone_own_goals[zone]
        return(total_shots)
        
    def total_goals(self):
        """Description: Add the shots scored from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the goals in all zones
        """
        total_shots = 0
        for zone in self.zone_shots_scored:
            total_shots = total_shots + self.zone_shots_scored[zone]

        for zone in self.zone_own_goals:
            total_shots = total_shots + self.zone_own_goals[zone]
        return(total_shots)

        
    def total_assists(self):
        """Description: Add the assists from all zones and return the total value
        Inputs: None
        Outputs:
            Returns - Sum of all the assists in all zones
        """
        total_assists = 0
        for zone in self.zone_assists:
            total_assists = total_assists + self.zone_assists[zone]
        return(total_assists)
        

class Passing_Stats(object):
    """Description: This object is used to collect passing statistics by processing passing tree branches
    """
    def __init__(self):
        self.total_passes = 0                         # Total number of passes completed
        self.possession_instances = 0                 # Number of times 3 consecutive passes reached
        self.max_consecutive_passes = 0                # Max number of passes in a passing sequence
        self.passing_sequence_histogram = {}           # Dictionary for histogram of how many instances each passing sequence length there are {1: x, 2: y, 3: z, ...}
        self.tree_roots = []                          # array of passing nodes that were the root of a passing sequence
        self.tree_tips = []                           # array of passing nodes that were the end of a passing sequence
        self.reset_possession_instances = True         # flag to reset the possession instances variable the first time process_tree_branch is called
        
    def process_tree_branch(self,graph,tree_branch):
        # graph is a directed graph to add the path in the tree branch to
        # tree_branch is a list of nodes in order of pass propagation
        if self.reset_possession_instances == True:
            self.possession_instances = 0
            self.reset_possession_instances = False
        passes = 0
        tip = tree_branch[len(tree_branch)-1]
        for i in range(0,len(tree_branch)-1):
            if tree_branch[i+1] == "":
                tip = tree_branch[i]
                break
            passes = passes+1
            if graph.has_edge(tree_branch[i],tree_branch[i+1]):
                x = graph[tree_branch[i]][tree_branch[i+1]]['weight']
                graph[tree_branch[i]][tree_branch[i+1]]['weight'] = x+1
            else:
                graph.add_weighted_edges_from([(tree_branch[i],tree_branch[i+1],1)])

        self.possession_instances = self.possession_instances + int(passes / 3)
        
        # update the histogram entry for the number of passes in this sequence
        if passes in self.passing_sequence_histogram:
            self.passing_sequence_histogram[passes] = self.passing_sequence_histogram[passes] + 1
        else:
            self.passing_sequence_histogram[passes] = 1
            
        self.tree_roots.append(tree_branch[0])
        self.tree_tips.append(tip)
        self.total_passes = self.total_passes + passes
        if passes > self.max_consecutive_passes:
            self.max_consecutive_passes = passes

    def passing_roots(self):
        tree_roots_freq = Counter(self.tree_roots)
        c = tree_roots_freq.most_common()
        return c

    def passing_tips(self):
        tree_tips_freq = Counter(self.tree_tips)
        c = tree_tips_freq.most_common()
        return c
        
class Game_Data(object):  
    h1Duration = 45
    h2Duration = 45
    ot1Duration = 15
    ot2Duration = 15
    homeTeamPenalty_shootout_goals = "NA"
    awayTeamPenalty_shootout_goals = "NA"
    
    def __init__(self,file_name):
        self.home_team = ""
        self.away_team = ""
        self.game_date = ""
        self.home_team_goals = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.away_team_goals = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.home_team_assists = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.away_team_assists = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.home_team_shots = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.away_team_shots = {"H1":0, "H2":0, "OT1":0, "OT2":0}        
        self.home_team_saves = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.away_team_saves = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.home_team_corners = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.away_team_corners = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeam_yellow_cards = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeam_yellow_cards = {"H1":0, "H2":0, "OT1":0, "OT2":0}        
        self.homeTeam_red_cards = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.awayTeam_red_cards = {"H1":0, "H2":0, "OT1":0, "OT2":0}
        self.homeTeam_formation_name = {"H1":"", "H2":"", "OT1":"", "OT2":""}
        self.awayTeam_formation_name = {"H1":"", "H2":"", "OT1":"", "OT2":""}
        self.homeTeamH1Formation = {}
        self.awayTeamH1Formation = {}
        self.homeTeamH2Formation = {}
        self.awayTeamH2Formation = {}
        self.homeTeamH1Passing_graph = nx.DiGraph()
        self.homeTeamH2Passing_graph = nx.DiGraph()
        self.awayTeamH1Passing_graph = nx.DiGraph()
        self.awayTeamH2Passing_graph = nx.DiGraph()
        self.homeTeamH1Passing_stats = Passing_Stats()
        self.homeTeamH2Passing_stats = Passing_Stats()
        self.awayTeamH1Passing_stats = Passing_Stats()
        self.awayTeamH2Passing_stats = Passing_Stats()
        self.homeTeamH1Heat_map_stats = Heat_Map_Stats()
        self.homeTeamH2Heat_map_stats = Heat_Map_Stats()
        self.awayTeamH1Heat_map_stats = Heat_Map_Stats()
        self.awayTeamH2Heat_map_stats = Heat_Map_Stats()
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

        self.__read_file__(file_name)

    # Data file parsing functions
    def __parse_home_team__(self, _, row):
        self.home_team = row[1]
    
    def __parse_away_team__(self, _, row):
        self.away_team = row[1]
    
    def __parse_game_date__(self, _, row):
        self.game_date = row[1]
        
    def __parse_duration__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[0]
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
    
    def __parse_goals__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.home_team_goals[period] = value
        elif parse_string[0] == "AT":
            self.away_team_goals[period] = value

    def __parse_assists__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.home_team_assists[period] = value
        elif parse_string[0] == "AT":
            self.away_team_assists[period] = value

    def __parse_shots__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.home_team_shots[period] = value
        elif parse_string[0] == "AT":
            self.away_team_shots[period] = value

    def __parse_saves__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.home_team_saves[period] = value
        elif parse_string[0] == "AT":
            self.away_team_saves[period] = value

    def __parse_corners__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.home_team_corners[period] = value
        elif parse_string[0] == "AT":
            self.away_team_corners[period] = value

    def __parse_yellow_cards__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.homeTeam_yellow_cards[period] = value
        elif parse_string[0] == "AT":
            self.awayTeam_yellow_cards[period] = value

    def __parse_red_cards__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.homeTeam_red_cards[period] = value
        elif parse_string[0] == "AT":
            self.awayTeam_red_cards[period] = value

    def __parse_possession__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if (parse_string[0] == "HT" and period == "H1"):
            self.homeTeamH1Passing_stats.possession_instances = value
        elif (parse_string[0] == "AT" and period == "H1"):
            self.awayTeamH1Passing_stats.possession_instances = value
        elif (parse_string[0] == "HT" and period == "H2"):
            self.homeTeamH2Passing_stats.possession_instances = value
        elif (parse_string[0] == "AT" and period == "H2"):
            self.awayTeamH2Passing_stats.possession_instances = value

    def __parse_max_passes__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        try:
            value = int(row[1])
        except:
            value = 0
        if (parse_string[0] == "HT" and period == "H1"):
            self.homeTeamH1Passing_stats.max_consecutive_passes = value
        elif (parse_string[0] == "AT" and period == "H1"):
            self.awayTeamH1Passing_stats.max_consecutive_passes = value
        elif (parse_string[0] == "HT" and period == "H2"):
            self.homeTeamH2Passing_stats.max_consecutive_passes = value
        elif (parse_string[0] == "AT" and period == "H2"):
            self.awayTeamH2Passing_stats.max_consecutive_passes = value
            
    def __parse_formation__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        if (key_val[0] == row[0]):              # this is the first row
            if parse_string[0] == "HT":
                self.homeTeam_formation_name[period] = row[1]
            elif parse_string[0] == "AT":
                self.awayTeam_formation_name[period] = row[1]
        else:                               # this is a row after the first row so add the nodes
            if (parse_string[0] == "HT" and period == "H1"):
                self.homeTeamH1Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.homeTeamH1Passing_graph.add_nodes_from([row[2]])
            elif (parse_string[0] == "AT" and period == "H1"):
                self.awayTeamH1Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.awayTeamH1Passing_graph.add_nodes_from([row[2]])
            elif (parse_string[0] == "HT" and period == "H2"):
                self.homeTeamH2Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.homeTeamH2Passing_graph.add_nodes_from([row[2]])
            elif (parse_string[0] == "AT" and period == "H2"):
                self.awayTeamH2Formation[row[2]] = np.array([float(row[3]),float(row[4])])
                self.awayTeamH2Passing_graph.add_nodes_from([row[2]])

    def __parse_passing_graph__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        if (parse_string[0] == "HT" and period == "H1"):
            self.homeTeamH1Passing_graph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])
        elif (parse_string[0] == "AT" and period == "H1"):
            self.awayTeamH1Passing_graph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])
        elif (parse_string[0] == "HT" and period == "H2"):
            self.homeTeamH2Passing_graph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])
        elif (parse_string[0] == "AT" and period == "H2"):
            self.awayTeamH2Passing_graph.add_weighted_edges_from([(row[1],row[2],float(row[3]))])

    def __parse_passing_tree__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        if (parse_string[0] == "HT" and period == "H1"):
            self.homeTeamH1Passing_stats.process_tree_branch(self.homeTeamH1Passing_graph, row[1:len(row)])
        elif (parse_string[0] == "AT" and period == "H1"):
            self.awayTeamH1Passing_stats.process_tree_branch(self.awayTeamH1Passing_graph, row[1:len(row)])
        elif (parse_string[0] == "HT" and period == "H2"):
            self.homeTeamH2Passing_stats.process_tree_branch(self.homeTeamH2Passing_graph, row[1:len(row)])
        elif (parse_string[0] == "AT" and period == "H2"):
            self.awayTeamH2Passing_stats.process_tree_branch(self.awayTeamH2Passing_graph, row[1:len(row)])
    
    def __parse_team_defending_zone__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]

        if (parse_string[0] == "HT" and period == "H1"):
            self.homeTeamH1Heat_map_stats.set_team_defending_zone(int(row[1]))
        elif (parse_string[0] == "AT" and period == "H1"):
            self.awayTeamH1Heat_map_stats.set_team_defending_zone(int(row[1]))
        elif (parse_string[0] == "HT" and period == "H2"):
            self.homeTeamH2Heat_map_stats.set_team_defending_zone(int(row[1]))
        elif (parse_string[0] == "AT" and period == "H2"):
            self.awayTeamH2Heat_map_stats.set_team_defending_zone(int(row[1]))

    def __parse_heat_map__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[1]
        
        # set default column numbers
        zone_col = 1
        passes_col = 2
        assists_col = 3
        possessions_col = 4
        shots_off_target_col = 5
        shots_on_target_col = 6
        shots_scored_col = 7
        own_goals_col = 8
        lost_possession_col = 9
        
        # update column numbers based on header row
        i = 0
        for heading in key_val:
            if heading.upper() == "PASSES COMPLETED":
                passes_col = i
            elif heading.upper() == "ASSISTS":
                assists_col = i
            elif heading.upper() == "3RD CONSECUTIVE PASS INSTANCES":
                possessions_col = i
            elif heading.upper() == "SHOTS OFF TARGET":
                shots_off_target_col = i
            elif heading.upper() == "SHOTS ON TARGET":
                shots_on_target_col = i
            elif heading.upper() == "SHOTS SCORED":
                shots_scored_col = i
            elif heading.upper() == "OWN GOALS SCORED":
                own_goals_col = i
            elif heading.upper() == "LOST POSSESSION":
                lost_possession_col = i
            i = i + 1
        try:
            passes = int(row[passes_col])
        except:
            passes = 0
        try:
            assists = int(row[assists_col])
        except:
            assists = 0
        try:
            possessions = int(row[possessions_col])
        except:
            possessions = 0
        try:
            shots_off_target = int(row[shots_off_target_col])
        except:
            shots_off_target = 0
        try:
            shots_on_target = int(row[shots_on_target_col])
        except:
            shots_on_target = 0
        try:
            shots_scored = int(row[shots_scored_col])
        except:
            shots_scored = 0
        try:
            own_goals = int(row[own_goals_col])
        except:
            own_goals = 0
        try:
            lost_possession = int(row[lost_possession_col])
        except:
            lost_possession = 0
            
        if (parse_string[0] == "HT" and period == "H1"):
            self.homeTeamH1Heat_map_stats.add_zone(int(row[zone_col]), shots_off_target, shots_on_target, shots_scored, own_goals, assists, passes, possessions, lost_possession)
        elif (parse_string[0] == "AT" and period == "H1"):
            self.awayTeamH1Heat_map_stats.add_zone(int(row[zone_col]), shots_off_target, shots_on_target, shots_scored, own_goals, assists, passes, possessions, lost_possession)
        elif (parse_string[0] == "HT" and period == "H2"):
            self.homeTeamH2Heat_map_stats.add_zone(int(row[zone_col]), shots_off_target, shots_on_target, shots_scored, own_goals, assists, passes, possessions, lost_possession)
        elif (parse_string[0] == "AT" and period == "H2"):
            self.awayTeamH2Heat_map_stats.add_zone(int(row[zone_col]), shots_off_target, shots_on_target, shots_scored, own_goals, assists, passes, possessions, lost_possession)

    def __parse_pk_shootout__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        try:
            value = int(row[1])
        except:
            value = 0
        if parse_string[0] == "HT":
            self.homeTeamPenalty_shootout_goals = value
        elif parse_string[0] == "AT":
            self.awayTeamPenalty_shootout_goals = value
        
    def __parse_comments__(self, key_val, row):
        parse_string = key_val[0].split(' ')
        period = parse_string[0]
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
    
    def __read_file__(self,file_name):
        csv_file_obj = open(file_name)
        reader_obj = csv.reader(csv_file_obj)
        current_field = None
        first_row = True
        for row in reader_obj:
            if row[0] in self.__dataFileFields__:
                # start of new field to parse
                current_field = row
                first_row = True
                valid_entry = True
            elif row[0] != "":
                valid_entry = False
            else:
                first_row = False

            if valid_entry == True:
                if (first_row == True and self.__dataFileFields__[current_field[0]][1] == False):
                    self.__dataFileFields__[current_field[0]][0](current_field, row)
                    first_row = False
                elif (first_row == False and self.__dataFileFields__[current_field[0]][2] == False):
                    self.__dataFileFields__[current_field[0]][0](current_field, row)


    def __draw_passing_sequence_histogram__(self, homeTeam_passing_stats, awayTeam_passing_stats, histogram_min_range, histogram_max_range, plot_title):
        """Description: Public API function to draw a histogram of number of passes in sequence
        Inputs: 
            homeTeam_passing_stats - Passing_Stats object with the data to be used for the histogram for the home team
            awayTeam_passing_stats - Passing_Stats object with the data to be used for the histogram for the home team
            histogram_min_range - the min number of passes in sequence to start the histogram at (usually 1)
            histogram_max_range - the max number of passes in sequence to end the histogram at
            plot_title - string with title to put at the top of the graph
        Outputs:
            a plot containing the specified histogram
        """
        home_team_color = "green"
        away_team_color = "blue"
        sequence_labels = []
        ht_values = []
        at_values = []
        for i in range (histogram_min_range, histogram_max_range+1):
            sequence_labels.append(i)
            if i in homeTeam_passing_stats.passing_sequence_histogram:
                ht_values.append(homeTeam_passing_stats.passing_sequence_histogram[i])
            else:
                ht_values.append(0)
                
            if i in awayTeam_passing_stats.passing_sequence_histogram:
                at_values.append(awayTeam_passing_stats.passing_sequence_histogram[i])
            else:
                at_values.append(0)

        x = np.arange(len(sequence_labels))
        width = 0.35
        
        max_value = max([max(ht_values), max(at_values)])
        y_val = 0
        y = []
        while y_val < (max_value+4):
            y.append(y_val)
            y_val = y_val + int(max_value/4)
            
        print(y)
        
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, ht_values, width, label = self.home_team, color=home_team_color)
        rects2 = ax.bar(x + width/2, at_values, width, label = self.away_team, color=away_team_color)
        ax.set_ylabel("Number of Occurrences")
        ax.set_title(plot_title)
        ax.set_xticks(x)
        ax.set_xticklabels(sequence_labels)
        ax.set_yticks(y)
        ax.legend()
        fig.tight_layout()
        plt.show()
        
        
    def draw_passing_sequence_histogram(self, half, histogram_min_range, histogram_max_range):
        """Description: Public API function to draw a histogram of number of passes in sequence
        Inputs: 
            half - 1 for first half, 2 for second half
            histogram_min_range - the min number of passes in sequence to start the histogram at (usually 1)
            histogram_max_range - the max number of passes in sequence to end the histogram at
        Outputs:
            calls private function self.__draw_passing_sequence_histogram__ with the appropriate arguments
            to plot the histogram
        """
        plot_title = "Passing Sequence Histogram - " + self.home_team + " vs. " + self.away_team
        if half == 1:
            plot_title = plot_title + ", for 1st Half"
            self.__draw_passing_sequence_histogram__(self.homeTeamH1Passing_stats, self.awayTeamH1Passing_stats, histogram_min_range, histogram_max_range, plot_title)
        elif half == 2:
            plot_title = plot_title + ", for 2nd Half"
            self.__draw_passing_sequence_histogram__(self.homeTeamH2Passing_stats, self.awayTeamH2Passing_stats, histogram_min_range, histogram_max_range, plot_title)
            
    def __draw_passing_graph__(self,graph,formation,elarge,esmall,plot_title):
        nx.draw_networkx_nodes(graph, formation)
        nx.draw_networkx_labels(graph, formation)
        nx.draw_networkx_edges(graph, formation, edgelist=elarge, width=1)
        nx.draw_networkx_edges(graph, formation, edgelist=esmall, width=1, alpha=0.5, edge_color='b', style='dashed')
        plt.title(plot_title)
        plt.show()
    
    def draw_passing_graph(self,team,half,weight,omit):
        # weight is the value for number passes >= to display prominently and < to either not display or display less prominently
        # omit: true = don't display passes < weight at all
        if team == 'H':
            if half == 1:
                formation = self.homeTeamH1Formation
                elarge=[(u,v) for (u,v,d) in self.homeTeamH1Passing_graph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.homeTeamH1Passing_graph.edges(data=True) if d['weight'] < weight]
                graph = self.homeTeamH1Passing_graph
                plot_title = "Passing Graph - " + self.home_team + " vs. " + self.away_team + ",for " + self.home_team + ", 1st Half"
            elif half == 2:
                formation = self.homeTeamH2Formation
                elarge=[(u,v) for (u,v,d) in self.homeTeamH2Passing_graph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.homeTeamH2Passing_graph.edges(data=True) if d['weight'] < weight]
                graph = self.homeTeamH2Passing_graph
                plot_title = "Passing Graph - " + self.home_team + " vs. " + self.away_team + ",for " + self.home_team + ", 2nd Half"
        elif team == 'A':
            if half == 1:
                formation = self.awayTeamH1Formation
                elarge=[(u,v) for (u,v,d) in self.awayTeamH1Passing_graph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.awayTeamH1Passing_graph.edges(data=True) if d['weight'] < weight]
                graph = self.awayTeamH1Passing_graph
                plot_title = "Passing Graph - " + self.home_team + " vs. " + self.away_team + ",for " + self.away_team + ", 1st Half"
            elif half == 2:
                formation = self.awayTeamH2Formation
                elarge=[(u,v) for (u,v,d) in self.awayTeamH2Passing_graph.edges(data=True) if d['weight'] >= weight ]
                esmall=[(u,v) for (u,v,d) in self.awayTeamH2Passing_graph.edges(data=True) if d['weight'] < weight]
                graph = self.awayTeamH2Passing_graph
                plot_title = "Passing Graph - " + self.home_team + " vs. " + self.away_team + ", for " + self.away_team + ", 2nd Half"
        if omit == False:
            self.__draw_passing_graph__(graph,formation,elarge,esmall,plot_title)
        else:
            no_small = []
            self.__draw_passing_graph__(graph,formation,elarge,no_small,plot_title)

            
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
        centre_circle = plt.Circle((PITCH_WIDTH/2,PITCH_LENGTH/2),9.15,color="black",fill=False)

        #Draw Circles
        ax.add_patch(centre_circle)

        #Prepare Arcs
        left_arc = Arc((45,17),height=18.3,width=18.3,angle=0,theta1=28,theta2=152,color="black")
        right_arc = Arc((45,133),height=18.3,width=18.3,angle=0,theta1=208,theta2=332,color="black")

        #Draw Arcs
        ax.add_patch(left_arc)
        ax.add_patch(right_arc)

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
        zone_map = []
        zoneX = PITCH_WIDTH / 3 / 2
        zoneY = PITCH_LENGTH / 6 / 2
        zone_width = PITCH_WIDTH / 3
        zone_length = PITCH_LENGTH / 6
        zone_zero = [zone_width*zone_length, zone_width, zone_length]
        zone_map.append(zone_zero)                                                # No Zone 0, but this element contains the following list: 
                                                                                #   [0] = the maximum bubble size (area) that can be plotted in any of the zones, 
                                                                                #   [1] = the zone width
                                                                                #   [2] = the zone length
        zone_map.append([zoneX, zoneY])                                          # Zone 1 [x,y]
        zone_map.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 2 [x,y]
        zone_map.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 3 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zone_map.append([zoneX, zoneY])                                          # Zone 4 [x,y]
        zone_map.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 5 [x,y]
        zone_map.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 6 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zone_map.append([zoneX, zoneY])                                          # Zone 7 [x,y]
        zone_map.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 8 [x,y]
        zone_map.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 9 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zone_map.append([zoneX, zoneY])                                          # Zone 10 [x,y]
        zone_map.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 11 [x,y]
        zone_map.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 12 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zone_map.append([zoneX, zoneY])                                          # Zone 13 [x,y]
        zone_map.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 14 [x,y]
        zone_map.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 15 [x,y]
        zoneY = zoneY + PITCH_LENGTH/6
        zone_map.append([zoneX, zoneY])                                          # Zone 16 [x,y]
        zone_map.append([zoneX + PITCH_WIDTH/3, zoneY])                          # Zone 17 [x,y]
        zone_map.append([zoneX + 2*PITCH_WIDTH/3, zoneY])                        # Zone 18 [x,y]
        
        return(zone_map)

    def __draw_heat_map__(self,zone_map,homeTeamHeat_map_stats,awayTeamHeat_map_stats,map_type,plot_title,filename):
        """Description: Draws a diagram of a field split into zones
        Preconditions: Assumes that __draw_pitch__ has been called ahead of this function being called
        Inputs: zone_map - a list of x and y coordinates of the center point in each zone ([zone#][x,y])
                          zone_map[0] contains the radius of the zone
                homeTeamHeat_map_stats - a Heat_Map_Stats object containing the stats to be plotted
                awayTeamHeat_map_stats - a Heat_Map_Stats object containing the stats to be plotted
                map_type - the type of map to draw (either "S" for shot, "P" for pass, "G" for goal, "L" for lost possession)
                plot_title - string with title to place on the map
                filename - name of a graphics file to output the heat map to (if None, then will open the heat map in a window on screen)
        Outputs:
            plots a graph of the pitch with zones labeled
        """
        home_team_color = "green"
        away_team_color = "blue"
        # if multiple heat maps are to be plotted on the same graph, set the offset for each one in each zone
        if homeTeamHeat_map_stats == None:
            offset = 0
            total_passes = awayTeamHeat_map_stats.total_passes()
            total_lost_possession = awayTeamHeat_map_stats.total_lost_possession_instances()
        elif awayTeamHeat_map_stats == None:
            offset = 0
            total_passes = homeTeamHeat_map_stats.total_passes()
            total_lost_possession = homeTeamHeat_map_stats.total_lost_possession_instances()
        else:
            offset = 5
            total_passes = homeTeamHeat_map_stats.total_passes() + awayTeamHeat_map_stats.total_passes()
            total_lost_possession = homeTeamHeat_map_stats.total_lost_possession_instances() + awayTeamHeat_map_stats.total_lost_possession_instances()               
 
        if map_type == "P":
            # plot home team heat map pass stats
            if total_passes > 0:                     # only plot this if there is no danger of divide by 0
                if homeTeamHeat_map_stats:
                    for i in range (1, len(zone_map)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        size_val = 3 * zone_map[0][0] * homeTeamHeat_map_stats.zone_passes[i] / total_passes
                        plt.scatter(x=zone_map[i][0]+offset, y=zone_map[i][1], s=size_val, alpha=0.5, color=home_team_color)
    
                # plot away team heat map pass stats
                if awayTeamHeat_map_stats:
                    for i in range (1, len(zone_map)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        size_val = 3 * zone_map[0][0] * awayTeamHeat_map_stats.zone_passes[i] / total_passes
                        plt.scatter(x=zone_map[i][0]-offset, y=zone_map[i][1], s=size_val, alpha=0.5, color=away_team_color)

            # Print the Legend
            legXVal = zone_map[1][0]
            legYVal = zone_map[1][1] - 50
            plt.text(legXVal,legYVal,"Legend")
            plt.text(legXVal+10,legYVal-15,self.home_team)
            plt.text(legXVal+10,legYVal-30,self.away_team)
            plt.scatter(x=legXVal+5, y=legYVal-12, s=10, color=home_team_color)
            plt.scatter(x=legXVal+5, y=legYVal-27, s=10, color=away_team_color)

        if map_type == "L":
            # plot home team heat map lost possession stats
            if total_lost_possession > 0:                 # only plot this if no danger of divide by 0
                if homeTeamHeat_map_stats:
                    for i in range (1, len(zone_map)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        size_val = 3 * zone_map[0][0] * homeTeamHeat_map_stats.zoneLost_possession_instances[i] / total_lost_possession
                        plt.scatter(x=zone_map[i][0]+offset, y=zone_map[i][1], s=size_val, alpha=0.5, color=home_team_color)
    
                # plot away team heat map lost possession stats
                if awayTeamHeat_map_stats:
                    for i in range (1, len(zone_map)):
                        # TODO with the 3x factor it's possible to have the bubbles exceed the area of a zone.  Consider some other implementation or maybe maxing out at the maximum area
                        size_val = 3 * zone_map[0][0] * awayTeamHeat_map_stats.zoneLost_possession_instances[i] / total_lost_possession
                        plt.scatter(x=zone_map[i][0]-offset, y=zone_map[i][1], s=size_val, alpha=0.5, color=away_team_color)

            # Print the Legend
            legXVal = zone_map[1][0]
            legYVal = zone_map[1][1] - 50
            plt.text(legXVal,legYVal,"Legend")
            plt.text(legXVal+10,legYVal-15,self.home_team)
            plt.text(legXVal+10,legYVal-30,self.away_team)
            plt.scatter(x=legXVal+5, y=legYVal-12, s=10, color=home_team_color)
            plt.scatter(x=legXVal+5, y=legYVal-27, s=10, color=away_team_color)
            
        elif map_type == "S":
            # plot home team heat map shooting stats
            if homeTeamHeat_map_stats:
                for i in range (1, len(zone_map)):
                    if (homeTeamHeat_map_stats.zone_own_goals[i] > 0 or homeTeamHeat_map_stats.zone_shots_scored[i] > 0 or
                       homeTeamHeat_map_stats.zoneShots_off_target[i] > 0 or homeTeamHeat_map_stats.zoneShots_on_target[i] > 0):
                        x_val = zone_map[i][0] + offset
                        y_val = zone_map[i][1]
                        plt.text(x_val,y_val+5,"OG: " + str(homeTeamHeat_map_stats.zone_own_goals[i]), fontsize=6, color=home_team_color)
                        plt.text(x_val,y_val+1,"SS: " + str(homeTeamHeat_map_stats.zone_shots_scored[i]), fontsize=6, color=home_team_color)
                        plt.text(x_val,y_val-3,"ON: " + str(homeTeamHeat_map_stats.zoneShots_on_target[i]), fontsize=6, color=home_team_color)
                        plt.text(x_val,y_val-7,"OFF: " + str(homeTeamHeat_map_stats.zoneShots_off_target[i]), fontsize=6, color=home_team_color)

            if awayTeamHeat_map_stats:
                for i in range (1, len(zone_map)):
                    if (awayTeamHeat_map_stats.zone_own_goals[i] > 0 or awayTeamHeat_map_stats.zone_shots_scored[i] > 0 or
                       awayTeamHeat_map_stats.zoneShots_off_target[i] > 0 or awayTeamHeat_map_stats.zoneShots_on_target[i] > 0):
                        x_val = zone_map[i][0] - offset
                        y_val = zone_map[i][1]
                        plt.text(x_val,y_val+5,"OG: " + str(awayTeamHeat_map_stats.zone_own_goals[i]), fontsize=6, color=away_team_color)
                        plt.text(x_val,y_val+1,"SS: " + str(awayTeamHeat_map_stats.zone_shots_scored[i]), fontsize=6, color=away_team_color)
                        plt.text(x_val,y_val-3,"ON: " + str(awayTeamHeat_map_stats.zoneShots_on_target[i]), fontsize=6, color=away_team_color)
                        plt.text(x_val,y_val-7,"OFF: " + str(awayTeamHeat_map_stats.zoneShots_off_target[i]), fontsize=6, color=away_team_color)
                       
            # Print the Legend
            legXVal = zone_map[1][0]
            legYVal = zone_map[1][1] - 50
            plt.text(legXVal,legYVal,"Legend")
            plt.text(legXVal+10,legYVal-15,self.home_team + " Shots", color=home_team_color)
            plt.text(legXVal+10,legYVal-30,self.away_team + " Shots", color=away_team_color)
            plt.text(legXVal+50,legYVal-10,"OG: Own Goals", fontsize=6)
            plt.text(legXVal+50,legYVal-14,"SS: Shots Scored", fontsize=6)
            plt.text(legXVal+50,legYVal-18,"ON: Shots On Target", fontsize=6)
            plt.text(legXVal+50,legYVal-22,"OFF: Shots Off Target", fontsize=6)

            # set extents of plot so legend is visible
            plotYLimits = [legYVal-30, zone_map[18][1] + zone_map[0][2] + 10]
            plt.ylim(plotYLimits)
            
                
        # Print team defending each goal
        if homeTeamHeat_map_stats:
            defending_zone = homeTeamHeat_map_stats.team_defending_zone
            x_val = zone_map[defending_zone][0] - zone_map[0][1] / 2
            if defending_zone <= 9:
                y_val = zone_map[defending_zone][1] - zone_map[0][2]
            else:
                y_val = zone_map[defending_zone][1] + zone_map[0][2]
            plt.text(x_val,y_val,self.home_team)

        if awayTeamHeat_map_stats:
            defending_zone = awayTeamHeat_map_stats.team_defending_zone
            x_val = zone_map[defending_zone][0] - zone_map[0][1] / 2
            if defending_zone <= 9:
                y_val = zone_map[defending_zone][1] - zone_map[0][2]
            else:
                y_val = zone_map[defending_zone][1] + zone_map[0][2]
            plt.text(x_val,y_val,self.away_team)
                    


        plt.title(plot_title,pad=30)
        
        if filename == None:
            #Display Heat Map
            plt.show()
        else:
            plt.tight_layout()
            plt.savefig(filename,dpi=600)
            plt.close()


    def draw_heat_map(self,team,half,map_type,filename=None):
        """Description: Draws a heat map graph for the specified team in the specified half of the game
        Inputs: team - the team to draw the map for (either "H" for home team or "A" for away team or "B" for both on same graph)
                half - the half to draw the map for (either 1 for first half or 2 for second half)
                map_type - the type of map to draw (either "S" for shot, "P" for pass, "L" for lost possession)
                filename - optional parameter if you want the map output to a file instead of opening a window
        Outputs:
            plots a graph
        """
        zone_map = self.__draw_pitch__()
        if map_type == "S":
            plot_title = "Shot Heat Map - "
        elif map_type == "P":
            plot_title = "Passing Heat Map - "
        elif map_type == "L":
            plot_title = "Lost Possession Heat Map - "
        else:
            return
            
        if team == 'H':
            if half == 1:
                plot_title = plot_title + self.home_team + " vs. " + self.away_team + ",for " + self.home_team + ", 1st Half"
                self.__draw_heat_map__(zone_map, self.homeTeamH1Heat_map_stats, None, map_type, plot_title, filename)
            elif half == 2:
                plot_title = plot_title + self.home_team + " vs. " + self.away_team + ",for " + self.home_team + ", 2nd Half"
                self.__draw_heat_map__(zone_map, self.homeTeamH2Heat_map_stats, None, map_type, plot_title, filename)
        elif team == 'A':
            if half == 1:
                plot_title = plot_title + self.home_team + " vs. " + self.away_team + ",for " + self.away_team + ", 1st Half"
                self.__draw_heat_map__(zone_map, None, self.awayTeamH1Heat_map_stats, map_type, plot_title, filename)
            elif half == 2:
                plot_title = plot_title + self.home_team + " vs. " + self.away_team + ",for " + self.away_team + ", 2nd Half"
                self.__draw_heat_map__(zone_map, None, self.awayTeamH2Heat_map_stats, map_type, plot_title, filename)
        elif team == 'B':
            if half == 1:
                plot_title = plot_title + self.home_team + " vs. " + self.away_team + ",for both teams, 1st Half"
                self.__draw_heat_map__(zone_map, self.homeTeamH1Heat_map_stats, self.awayTeamH1Heat_map_stats, map_type, plot_title, filename)
            elif half == 2:
                plot_title = plot_title + self.home_team + " vs. " + self.away_team + ",for both teams, 2nd Half"
                self.__draw_heat_map__(zone_map, self.homeTeamH2Heat_map_stats, self.awayTeamH2Heat_map_stats, map_type, plot_title, filename)

         
    def final_home_team_score(self):
        score = 0
        for period in self.home_team_goals:
            score = score + self.home_team_goals[period]
        return score
        
    def final_away_team_score(self):
        score = 0
        for period in self.away_team_goals:
            score = score + self.away_team_goals[period]
        return score
    
    def __total_passes__(self, passing_graph):
        passes = 0
        for u,v,weight in passing_graph.edges(data=True):
            passes = passes + weight['weight']
        return passes
        
    def __top_passer__(self, passing_graph):
        degrees = passing_graph.out_degree(weight='weight')
        passers = sorted(degrees, key=lambda x: x[1], reverse=True)
        return passers[0]

    def __hub_player__(self, passing_graph):
        degrees = passing_graph.degree(weight='weight')
        passers = sorted(degrees, key=lambda x: x[1], reverse=True)
        return passers[0]
    
    def home_team_passing_rate(self, period):
        if (period == "H1"):
            total_passes = self.__total_passes__(self.homeTeamH1Passing_graph)
            passing_rate = total_passes / self.h1Duration
        elif (period == "H2"):
            total_passes = self.__total_passes__(self.homeTeamH2Passing_graph)
            passing_rate = total_passes / self.h2Duration
        else:
            return(0)
        return(passing_rate)

    def away_team_passing_rate(self, period):
        if (period == "H1"):
            total_passes = self.__total_passes__(self.awayTeamH1Passing_graph)
            passing_rate = total_passes / self.h1Duration
        elif (period == "H2"):
            total_passes = self.__total_passes__(self.awayTeamH2Passing_graph)
            passing_rate = total_passes / self.h2Duration
        else:
            return(0)
        return(passing_rate)
            
    def home_team_top_passer(self, period):
        if (period == "H1"):
            top_passer = self.__top_passer__(self.homeTeamH1Passing_graph)
        elif (period == "H2"):
            top_passer = self.__top_passer__(self.homeTeamH2Passing_graph)
        return top_passer
 
    def away_team_top_passer(self, period):
        if (period == "H1"):
            top_passer = self.__top_passer__(self.awayTeamH1Passing_graph)
        elif (period == "H2"):
            top_passer = self.__top_passer__(self.awayTeamH2Passing_graph)
        return top_passer

    def home_team_hub_player(self, period):
        if (period == "H1"):
            top_hub = self.__hub_player__(self.homeTeamH1Passing_graph)
        elif (period == "H2"):
            top_hub = self.__hub_player__(self.homeTeamH2Passing_graph)
        return top_hub

    def away_team_hub_player(self, period):
        if (period == "H1"):
            top_hub = self.__hub_player__(self.awayTeamH1Passing_graph)
        elif (period == "H2"):
            top_hub = self.__hub_player__(self.awayTeamH2Passing_graph)
        return top_hub
    
    def home_team_passing_rate_from_heat_map(self, period):
        if (period == "H1"):
            total_passes = self.homeTeamH1Heat_map_stats.total_passes()
            passing_rate = total_passes / self.h1Duration
        elif (period == "H2"):
            total_passes = self.homeTeamH2Heat_map_stats.total_passes()
            passing_rate = total_passes / self.h2Duration
        else:
            return(0)
        return(passing_rate)

    def away_team_passing_rate_from_heat_map(self, period):
        if (period == "H1"):
            total_passes = self.awayTeamH1Heat_map_stats.total_passes()
            passing_rate = total_passes / self.h1Duration
        elif (period == "H2"):
            total_passes = self.awayTeamH2Heat_map_stats.total_passes()
            passing_rate = total_passes / self.h2Duration
        else:
            return(0)
        return(passing_rate)
