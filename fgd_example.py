import football_game_data as fgd


g1 = fgd.Game_Data('2017-10-28_UWGB_vs_Belmont.csv')
#g1 = fgd.Game_Data('2017-09-03_Lawrence_vs_Marion.csv')


g1.draw_passing_graph('H',1,4,False)

print ("Home Team: ", g1.homeTeam, ": ", g1.final_home_team_score())
print ("Away Team: ", g1.awayTeam, ": ", g1.final_away_team_score())
