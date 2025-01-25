import football_game_data as fgd
import os
import football_game_reports

DATA_FILE_FOLDER = './game_files/'

def choose_file(folder):
    allFiles = [f for f in os.listdir(folder) if os.path.isfile(folder+f)]
    filteredFiles = []
    i = 0
    for f in allFiles:
        fileExtension = f.partition('.')[2]
        if fileExtension == "csv":
            print("(",i,")",f)
            filteredFiles.append(f)
            i = i + 1

    choice = input("Choose file to analyze by index or type filename: ")
    try:
        index = int(choice)
        fileName = filteredFiles[index]
    except ValueError:
        fileName = choice
        
    return(folder+fileName)
    
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
        homeTeam = list[0].center(COL3-COL1," ")
        awayTeam = list[1].center(COL4-COL2," ")
        print(str(" ").rjust(COL1), homeTeam,awayTeam)
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
        homeTeam = list[0].center(COL2-COL1," ")
        awayTeam = list[1].center(COL3-COL2," ")
        print(str(" ").rjust(COL1), homeTeam,awayTeam)
    else:
        print(stat.rjust(COL1), list[0].center(COL2-COL1), list[1].center(COL3-COL2))

        
fileName = choose_file(DATA_FILE_FOLDER)
print("File Chosen = ",fileName)

g1 = fgd.Game_Data(fileName)
#try:
#    g1 = fgd.Game_Data(fileName)
#except:
#    print("ERROR: Unable to import ", fileName)
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
        print_results("HEADER", [g1.homeTeam,g1.awayTeam])
        print_results("Score", [g1.final_home_team_score(), g1.final_away_team_score()])
        if (g1.homeTeamPenaltyShootoutGoals != "NA"):
            print_results("Penalty Shootout", [g1.homeTeamPenaltyShootoutGoals, g1.awayTeamPenaltyShootoutGoals])

    elif (choice.upper() == 'G'):
        print("")
        print_results_by_half("HEADER", [g1.homeTeam,g1.awayTeam])
        print_results_by_half("Goals", [g1.homeTeamGoals["H1"],g1.homeTeamGoals["H2"],g1.awayTeamGoals["H1"],g1.awayTeamGoals["H2"]])
        print_results_by_half("Assists", [g1.homeTeamAssists["H1"],g1.homeTeamAssists["H2"],g1.awayTeamAssists["H1"],g1.awayTeamAssists["H2"]])
        print_results_by_half("Shots", [g1.homeTeamShots["H1"],g1.homeTeamShots["H2"],g1.awayTeamShots["H1"],g1.awayTeamShots["H2"]])        
        print_results_by_half("Saves", [g1.homeTeamSaves["H1"],g1.homeTeamSaves["H2"],g1.awayTeamSaves["H1"],g1.awayTeamSaves["H2"]])
        print_results_by_half("Corners",[g1.homeTeamCorners["H1"],g1.homeTeamCorners["H2"],g1.awayTeamCorners["H1"],g1.awayTeamCorners["H2"]])
        print_results_by_half("Yellow Cards", [g1.homeTeamYellowCards["H1"],g1.homeTeamYellowCards["H2"],g1.awayTeamYellowCards["H1"],g1.awayTeamYellowCards["H2"]])
        print_results_by_half("Red Cards", [g1.homeTeamRedCards["H1"],g1.homeTeamRedCards["H2"],g1.awayTeamRedCards["H1"],g1.awayTeamRedCards["H2"]])
        print_results_by_half("Formation", [g1.homeTeamFormationName["H1"],g1.homeTeamFormationName["H2"],g1.awayTeamFormationName["H1"],g1.awayTeamFormationName["H2"]])
                
        print("")
        print("Coach comments H1:")
        for comment in g1.homeTeamH1Comments:
            print("\t", g1.homeTeam, ": ", comment)
        for comment in g1.awayTeamH1Comments:
            print("\t", g1.awayTeam, ": ", comment)

        print("")
        print("Coach comments H2:")
        for comment in g1.homeTeamH2Comments:
            print("\t", g1.homeTeam, ": ", comment)
        for comment in g1.awayTeamH2Comments:
            print("\t", g1.awayTeam, ": ", comment)
            
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
        print_results_by_half("HEADER", [g1.homeTeam,g1.awayTeam])
        print_results_by_half("Possession Instances", [g1.homeTeamH1PassingStats.possessionInstances, g1.homeTeamH2PassingStats.possessionInstances, g1.awayTeamH1PassingStats.possessionInstances, g1.awayTeamH2PassingStats.possessionInstances])
        print_results_by_half("Max Consecutive Passes", [g1.homeTeamH1PassingStats.maxConsecutivePasses, g1.homeTeamH2PassingStats.maxConsecutivePasses, g1.awayTeamH1PassingStats.maxConsecutivePasses, g1.awayTeamH2PassingStats.maxConsecutivePasses])
        print_results_by_half("Passing Rate (passes/min)", [round(g1.home_team_passing_rate('H1'),2), round(g1.home_team_passing_rate('H2'),2), round(g1.away_team_passing_rate('H1'),2), round(g1.away_team_passing_rate('H2'),2)])
        htH1Roots = g1.homeTeamH1PassingStats.passing_roots()
        htH2Roots = g1.homeTeamH2PassingStats.passing_roots()
        atH1Roots = g1.awayTeamH1PassingStats.passing_roots()
        atH2Roots = g1.awayTeamH2PassingStats.passing_roots()
        for i in range(5):
            stat = "Top Passing Root " + str(i+1)
            statList = []
            if len(htH1Roots) > i:
                statList.append(htH1Roots[i][0] + "-" + str(htH1Roots[i][1]))
            else:
                statList.append("NA")
            if len(htH2Roots) > i:
                statList.append(htH2Roots[i][0] + "-" + str(htH2Roots[i][1]))
            else:
                statList.append("NA")
            if len(atH1Roots) > i:
                statList.append(atH1Roots[i][0] + "-" + str(atH1Roots[i][1]))
            else:
                statList.append("NA")
            if len(atH2Roots) > i:
                statList.append(atH2Roots[i][0] + "-" + str(atH2Roots[i][1]))
            else:
                statList.append("NA")            
            print_results_by_half(stat, statList)
        
        htH1Tips = g1.homeTeamH1PassingStats.passing_tips()
        htH2Tips = g1.homeTeamH2PassingStats.passing_tips()
        atH1Tips = g1.awayTeamH1PassingStats.passing_tips()
        atH2Tips = g1.awayTeamH2PassingStats.passing_tips()
        for i in range (5):
            stat = "Player Possession Ends At " + str(i+1)
            statList = []
            if len(htH1Tips) > i:
                statList.append(htH1Tips[i][0] + "-" + str(htH1Tips[i][1]))
            else:
                statList.append("NA")
            if len(htH2Tips) > i:
                statList.append(htH2Tips[i][0] + "-" + str(htH2Tips[i][1]))
            else:
                statList.append("NA")
            if len(atH1Tips) > i:
                statList.append(atH1Tips[i][0] + "-" + str(atH1Tips[i][1]))
            else:
                statList.append("NA")
            if len(atH2Tips) > i:
                statList.append(atH2Tips[i][0] + "-" + str(atH2Tips[i][1]))
            else:
                statList.append("NA")
            print_results_by_half(stat, statList)
                
        print_results_by_half("Top Passer", [g1.home_team_top_passer("H1")[0]+"-"+str(g1.home_team_top_passer("H1")[1]), g1.home_team_top_passer("H2")[0]+"-"+str(g1.home_team_top_passer("H2")[1]), g1.away_team_top_passer("H1")[0]+"-"+str(g1.away_team_top_passer("H1")[1]), g1.away_team_top_passer("H2")[0]+"-"+str(g1.away_team_top_passer("H2")[1])])
        print_results_by_half("Team Passing Hub", [g1.home_team_hub_player("H1")[0]+"-"+str(g1.home_team_hub_player("H1")[1]), g1.home_team_hub_player("H2")[0]+"-"+str(g1.home_team_hub_player("H2")[1]), g1.away_team_hub_player("H1")[0]+"-"+str(g1.away_team_hub_player("H1")[1]), g1.away_team_hub_player("H2")[0]+"-"+str(g1.away_team_hub_player("H2")[1])])
    elif (choice.upper() == 'N'):
        half = int(input("(1)st Half or (2)nd Half? "))
        g1.draw_passing_sequence_histogram(half, 1, 10)
    elif (choice.upper() == 'H'):
        print("")
        print_results_by_half("HEADER", [g1.homeTeam,g1.awayTeam])
        print_results_by_half("Goals", [g1.homeTeamH1HeatMapStats.total_goals(), g1.homeTeamH2HeatMapStats.total_goals(), g1.awayTeamH1HeatMapStats.total_goals(), g1.awayTeamH2HeatMapStats.total_goals()])
        print_results_by_half("Assists", [g1.homeTeamH1HeatMapStats.total_assists(), g1.homeTeamH2HeatMapStats.total_assists(), g1.awayTeamH1HeatMapStats.total_assists(), g1.awayTeamH2HeatMapStats.total_assists()])
        print_results_by_half("Shots", [g1.homeTeamH1HeatMapStats.total_shots(), g1.homeTeamH2HeatMapStats.total_shots(), g1.awayTeamH1HeatMapStats.total_shots(), g1.awayTeamH2HeatMapStats.total_shots()])
        print_results_by_half("Shots on Target", [g1.homeTeamH1HeatMapStats.total_shots_on_target(), g1.homeTeamH2HeatMapStats.total_shots_on_target(), g1.awayTeamH1HeatMapStats.total_shots_on_target(), g1.awayTeamH2HeatMapStats.total_shots_on_target()])
        print_results_by_half("Possession Instances", [g1.homeTeamH1HeatMapStats.total_possession_instances(), g1.homeTeamH2HeatMapStats.total_possession_instances(), g1.awayTeamH1HeatMapStats.total_possession_instances(), g1.awayTeamH2HeatMapStats.total_possession_instances()])
        print_results_by_half("Passing Rate (passes/min)", [round(g1.home_team_passing_rate_from_heat_map('H1'),2), round(g1.home_team_passing_rate_from_heat_map('H2'),2), round(g1.away_team_passing_rate_from_heat_map('H1'),2), round(g1.away_team_passing_rate_from_heat_map('H2'),2)])
        print_results_by_half("Max Consecutive Passes", [g1.homeTeamH1PassingStats.maxConsecutivePasses, g1.homeTeamH2PassingStats.maxConsecutivePasses, g1.awayTeamH1PassingStats.maxConsecutivePasses, g1.awayTeamH2PassingStats.maxConsecutivePasses])
    elif (choice.upper() == 'M'):
        team = input("(H)ome or (A)way or (B)oth? ")
        half = int(input("(1)st Half or (2)nd Half? "))
        mapType = input("(S)hot, (P)ass, (l)ost Possession? ")
        g1.draw_heat_map(team.upper(),half,mapType.upper())
    elif (choice == "1"):
        reports_object = football_game_reports.football_game_reports(g1)
        reports_object.create_report_from_template("report.docx")