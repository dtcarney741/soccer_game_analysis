import football_game_data as fgd
import os
import football_game_reports

DATA_FILE_FOLDER = './game_files/'

def choose_file(folder):
    all_files = [f for f in os.listdir(folder) if os.path.isfile(folder+f)]
    filtered_files = []
    i = 0
    for f in all_files:
        file_extension = f.partition('.')[2]
        if file_extension == "csv":
            print("(",i,")",f)
            filtered_files.append(f)
            i = i + 1

    choice = input("Choose file to analyze by index or type filename: ")
    try:
        index = int(choice)
        file_name = filtered_files[index]
    except ValueError:
        file_name = choice
        
    return(folder+file_name)
    
def print_results_by_half(stat, list):
    COL1 = 30
    COL2 = 40
    COL3 = 50
    COL4 = 60
    COL5 = 70
    for i in range(len(list)):
        if not isinstance(list[i], str):
            list[i] = str(list[i])
            
    if (stat == "HEADER"):
        home_team = list[0].center(COL3-COL1," ")
        away_team = list[1].center(COL4-COL2," ")
        print(str(" ").rjust(COL1), home_team,away_team)
        print(str("H1").rjust(int(COL1+(COL2-COL1)/2)), str("H2").rjust(COL2-COL1), str("H1").rjust(COL3-COL2), str("H2").rjust(COL4-COL3))
    else:
        print(stat.rjust(COL1), list[0].center(COL2-COL1), list[1].center(COL3-COL2), list[2].center(COL4-COL3), list[3].center(COL5-COL4))

def print_results(stat, list):
    COL1 = 30
    COL2 = 50
    COL3 = 70
    for i in range(len(list)):
        if not isinstance(list[i], str):
            list[i] = str(list[i])
            
    if (stat == "HEADER"):
        home_team = list[0].center(COL2-COL1," ")
        away_team = list[1].center(COL3-COL2," ")
        print(str(" ").rjust(COL1), home_team,away_team)
    else:
        print(stat.rjust(COL1), list[0].center(COL2-COL1), list[1].center(COL3-COL2))

        
file_name = choose_file(DATA_FILE_FOLDER)
print("File Chosen = ",file_name)

g1 = fgd.Game_Data(file_name)
#try:
#    g1 = fgd.Game_Data(file_name)
#except:
#    print("ERROR: Unable to import ", file_name)
#    quit()

choice = ''
while (choice.upper() != 'Q'):
    print("")
    print("Options")
    print("(S)core, (G)ame Statistics, (P)assing Graph, P(a)ssing Statistics, Passing Seque(n)ce Histogram")
    print("(H)eat Map Statistics, Heat (M)ap")
    print("Output Reports:")
    print("    (1) Report to Template")
    print("(Q)uit")
    choice = input("What is your choice? ")
    
    if (choice.upper() == 'S'):
        print("")
        print_results("HEADER", [g1.home_team,g1.away_team])
        print_results("Score", [g1.final_home_team_score(), g1.final_away_team_score()])
        if (g1.homeTeamPenalty_shootout_goals != "NA"):
            print_results("Penalty Shootout", [g1.homeTeamPenalty_shootout_goals, g1.awayTeamPenalty_shootout_goals])

    elif (choice.upper() == 'G'):
        print("")
        print_results_by_half("HEADER", [g1.home_team,g1.away_team])
        print_results_by_half("Goals", [g1.home_team_goals["H1"],g1.home_team_goals["H2"],g1.away_team_goals["H1"],g1.away_team_goals["H2"]])
        print_results_by_half("Assists", [g1.home_team_assists["H1"],g1.home_team_assists["H2"],g1.away_team_assists["H1"],g1.away_team_assists["H2"]])
        print_results_by_half("Shots", [g1.home_team_shots["H1"],g1.home_team_shots["H2"],g1.away_team_shots["H1"],g1.away_team_shots["H2"]])        
        print_results_by_half("Saves", [g1.home_team_saves["H1"],g1.home_team_saves["H2"],g1.away_team_saves["H1"],g1.away_team_saves["H2"]])
        print_results_by_half("Corners",[g1.home_team_corners["H1"],g1.home_team_corners["H2"],g1.away_team_corners["H1"],g1.away_team_corners["H2"]])
        print_results_by_half("Yellow Cards", [g1.homeTeam_yellow_cards["H1"],g1.homeTeam_yellow_cards["H2"],g1.awayTeam_yellow_cards["H1"],g1.awayTeam_yellow_cards["H2"]])
        print_results_by_half("Red Cards", [g1.homeTeam_red_cards["H1"],g1.homeTeam_red_cards["H2"],g1.awayTeam_red_cards["H1"],g1.awayTeam_red_cards["H2"]])
        print_results_by_half("Formation", [g1.homeTeam_formation_name["H1"],g1.homeTeam_formation_name["H2"],g1.awayTeam_formation_name["H1"],g1.awayTeam_formation_name["H2"]])
                
        print("")
        print("Coach comments H1:")
        for comment in g1.homeTeamH1Comments:
            print("\t", g1.home_team, ": ", comment)
        for comment in g1.awayTeamH1Comments:
            print("\t", g1.away_team, ": ", comment)

        print("")
        print("Coach comments H2:")
        for comment in g1.homeTeamH2Comments:
            print("\t", g1.home_team, ": ", comment)
        for comment in g1.awayTeamH2Comments:
            print("\t", g1.away_team, ": ", comment)
            
    elif (choice.upper() == 'P'):
        team = input("(H)ome or (A)way? ")
        half = int(input("(1)st Half or (2)nd Half? "))
        weight = int(input("Minimum passing weight: "))
        omit = input("Omit edges less than weight (Y)es or (N)o? ")
        if (omit.upper() == 'Y'):
            g1.draw_passing_graph(team.upper(),half,weight,True)
        else:
            g1.draw_passing_graph(team.upper(),half,weight,False)
    elif (choice.upper() == 'A'):
        print("")
        print_results_by_half("HEADER", [g1.home_team,g1.away_team])
        print_results_by_half("Possession Instances", [g1.homeTeamH1Passing_stats.possession_instances, g1.homeTeamH2Passing_stats.possession_instances, g1.awayTeamH1Passing_stats.possession_instances, g1.awayTeamH2Passing_stats.possession_instances])
        print_results_by_half("Max Consecutive Passes", [g1.homeTeamH1Passing_stats.max_consecutive_passes, g1.homeTeamH2Passing_stats.max_consecutive_passes, g1.awayTeamH1Passing_stats.max_consecutive_passes, g1.awayTeamH2Passing_stats.max_consecutive_passes])
        print_results_by_half("Passing Rate (passes/min)", [round(g1.home_team_passing_rate('H1'),2), round(g1.home_team_passing_rate('H2'),2), round(g1.away_team_passing_rate('H1'),2), round(g1.away_team_passing_rate('H2'),2)])
        ht_H1_roots = g1.homeTeamH1Passing_stats.passing_roots()
        ht_H2_roots = g1.homeTeamH2Passing_stats.passing_roots()
        at_H1_roots = g1.awayTeamH1Passing_stats.passing_roots()
        at_H2_roots = g1.awayTeamH2Passing_stats.passing_roots()
        for i in range(5):
            stat = "Top Passing Root " + str(i+1)
            stat_list = []
            if len(ht_H1_roots) > i:
                stat_list.append(ht_H1_roots[i][0] + "-" + str(ht_H1_roots[i][1]))
            else:
                stat_list.append("NA")
            if len(ht_H2_roots) > i:
                stat_list.append(ht_H2_roots[i][0] + "-" + str(ht_H2_roots[i][1]))
            else:
                stat_list.append("NA")
            if len(at_H1_roots) > i:
                stat_list.append(at_H1_roots[i][0] + "-" + str(at_H1_roots[i][1]))
            else:
                stat_list.append("NA")
            if len(at_H2_roots) > i:
                stat_list.append(at_H2_roots[i][0] + "-" + str(at_H2_roots[i][1]))
            else:
                stat_list.append("NA")            
            print_results_by_half(stat, stat_list)
        
        ht_H1_tips = g1.homeTeamH1Passing_stats.passing_tips()
        ht_H2_tips = g1.homeTeamH2Passing_stats.passing_tips()
        at_H1_tips = g1.awayTeamH1Passing_stats.passing_tips()
        at_H2_tips = g1.awayTeamH2Passing_stats.passing_tips()
        for i in range (5):
            stat = "Player Possession Ends At " + str(i+1)
            stat_list = []
            if len(ht_H1_tips) > i:
                stat_list.append(ht_H1_tips[i][0] + "-" + str(ht_H1_tips[i][1]))
            else:
                stat_list.append("NA")
            if len(ht_H2_tips) > i:
                stat_list.append(ht_H2_tips[i][0] + "-" + str(ht_H2_tips[i][1]))
            else:
                stat_list.append("NA")
            if len(at_H1_tips) > i:
                stat_list.append(at_H1_tips[i][0] + "-" + str(at_H1_tips[i][1]))
            else:
                stat_list.append("NA")
            if len(at_H2_tips) > i:
                stat_list.append(at_H2_tips[i][0] + "-" + str(at_H2_tips[i][1]))
            else:
                stat_list.append("NA")
            print_results_by_half(stat, stat_list)
                
        print_results_by_half("Top Passer", [g1.home_team_top_passer("H1")[0]+"-"+str(g1.home_team_top_passer("H1")[1]), g1.home_team_top_passer("H2")[0]+"-"+str(g1.home_team_top_passer("H2")[1]), g1.away_team_top_passer("H1")[0]+"-"+str(g1.away_team_top_passer("H1")[1]), g1.away_team_top_passer("H2")[0]+"-"+str(g1.away_team_top_passer("H2")[1])])
        print_results_by_half("Team Passing Hub", [g1.home_team_hub_player("H1")[0]+"-"+str(g1.home_team_hub_player("H1")[1]), g1.home_team_hub_player("H2")[0]+"-"+str(g1.home_team_hub_player("H2")[1]), g1.away_team_hub_player("H1")[0]+"-"+str(g1.away_team_hub_player("H1")[1]), g1.away_team_hub_player("H2")[0]+"-"+str(g1.away_team_hub_player("H2")[1])])
    elif (choice.upper() == 'N'):
        half = int(input("(1)st Half or (2)nd Half? "))
        g1.draw_passing_sequence_histogram(half, 1, 10)
    elif (choice.upper() == 'H'):
        print("")
        print_results_by_half("HEADER", [g1.home_team,g1.away_team])
        print_results_by_half("Goals", [g1.homeTeamH1Heat_map_stats.total_goals(), g1.homeTeamH2Heat_map_stats.total_goals(), g1.awayTeamH1Heat_map_stats.total_goals(), g1.awayTeamH2Heat_map_stats.total_goals()])
        print_results_by_half("Assists", [g1.homeTeamH1Heat_map_stats.total_assists(), g1.homeTeamH2Heat_map_stats.total_assists(), g1.awayTeamH1Heat_map_stats.total_assists(), g1.awayTeamH2Heat_map_stats.total_assists()])
        print_results_by_half("Shots", [g1.homeTeamH1Heat_map_stats.total_shots(), g1.homeTeamH2Heat_map_stats.total_shots(), g1.awayTeamH1Heat_map_stats.total_shots(), g1.awayTeamH2Heat_map_stats.total_shots()])
        print_results_by_half("Shots on Target", [g1.homeTeamH1Heat_map_stats.total_shots_on_target(), g1.homeTeamH2Heat_map_stats.total_shots_on_target(), g1.awayTeamH1Heat_map_stats.total_shots_on_target(), g1.awayTeamH2Heat_map_stats.total_shots_on_target()])
        print_results_by_half("Possession Instances", [g1.homeTeamH1Heat_map_stats.total_possession_instances(), g1.homeTeamH2Heat_map_stats.total_possession_instances(), g1.awayTeamH1Heat_map_stats.total_possession_instances(), g1.awayTeamH2Heat_map_stats.total_possession_instances()])
        print_results_by_half("Passing Rate (passes/min)", [round(g1.home_team_passing_rate_from_heat_map('H1'),2), round(g1.home_team_passing_rate_from_heat_map('H2'),2), round(g1.away_team_passing_rate_from_heat_map('H1'),2), round(g1.away_team_passing_rate_from_heat_map('H2'),2)])
        print_results_by_half("Max Consecutive Passes", [g1.homeTeamH1Passing_stats.max_consecutive_passes, g1.homeTeamH2Passing_stats.max_consecutive_passes, g1.awayTeamH1Passing_stats.max_consecutive_passes, g1.awayTeamH2Passing_stats.max_consecutive_passes])
    elif (choice.upper() == 'M'):
        team = input("(H)ome or (A)way or (B)oth? ")
        half = int(input("(1)st Half or (2)nd Half? "))
        map_type = input("(S)hot, (P)ass, (l)ost Possession? ")
        g1.draw_heat_map(team.upper(),half,map_type.upper())
    elif (choice == "1"):
        reports_object = football_game_reports.football_game_reports(g1)
        reports_object.create_report_from_template("report.docx")