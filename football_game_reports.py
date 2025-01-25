import docx
import docxtpl

class football_game_reports(object):
    """Description: This class is used to create reports based off data in
    Game_Data object of football_game_data.py file
    """
    
    def __init__(self, game_object):
        self.game_object = game_object
        self.report_template_file = "game_report_template.docx"

    def __create_template_dictionary__(self, template):
        """Description: Creates a dictionary context for docxtpl to use
        Inputs: template - docxtpl template that the dictionary will be used on
        Outputs:
            returns - template_dict - dictionary that contains all the values in the template file that will be updated
        """
        # create dictionary of values in the template
        template_dict = {}
        template_dict["home_team"] = self.game_object.homeTeam
        template_dict["away_team"] = self.game_object.awayTeam
        template_dict["game_date"] = self.game_object.gameDate
        template_dict["goals"] = {}
        template_dict["goals"]["home_h1"] = self.game_object.homeTeamGoals["H1"]
        template_dict["goals"]["home_h2"] = self.game_object.homeTeamGoals["H2"]
        template_dict["goals"]["away_h1"] = self.game_object.awayTeamGoals["H1"]
        template_dict["goals"]["away_h2"] = self.game_object.awayTeamGoals["H2"]
        template_dict["assists"] = {}
        template_dict["assists"]["home_h1"] = self.game_object.homeTeamAssists["H1"]
        template_dict["assists"]["home_h2"] = self.game_object.homeTeamAssists["H2"]
        template_dict["assists"]["away_h1"] = self.game_object.awayTeamAssists["H1"]
        template_dict["assists"]["away_h2"] = self.game_object.awayTeamAssists["H2"]
        template_dict["shots"] = {}
        template_dict["shots"]["home_h1"] = self.game_object.homeTeamShots["H1"]
        template_dict["shots"]["home_h2"] = self.game_object.homeTeamShots["H2"]
        template_dict["shots"]["away_h1"] = self.game_object.awayTeamShots["H1"]
        template_dict["shots"]["away_h2"] = self.game_object.awayTeamShots["H2"]
        template_dict["saves"] = {}
        template_dict["saves"]["home_h1"] = self.game_object.homeTeamSaves["H1"]
        template_dict["saves"]["home_h2"] = self.game_object.homeTeamSaves["H2"]
        template_dict["saves"]["away_h1"] = self.game_object.awayTeamSaves["H1"]
        template_dict["saves"]["away_h2"] = self.game_object.awayTeamSaves["H2"]
        template_dict["corners"] = {}
        template_dict["corners"]["home_h1"] = self.game_object.homeTeamCorners["H1"]
        template_dict["corners"]["home_h2"] = self.game_object.homeTeamCorners["H2"]
        template_dict["corners"]["away_h1"] = self.game_object.awayTeamCorners["H1"]
        template_dict["corners"]["away_h2"] = self.game_object.awayTeamCorners["H2"]
        template_dict["yellows"] = {}
        template_dict["yellows"]["home_h1"] = self.game_object.homeTeamYellowCards["H1"]
        template_dict["yellows"]["home_h2"] = self.game_object.homeTeamYellowCards["H2"]
        template_dict["yellows"]["away_h1"] = self.game_object.awayTeamYellowCards["H1"]
        template_dict["yellows"]["away_h2"] = self.game_object.awayTeamYellowCards["H2"]
        template_dict["reds"] = {}
        template_dict["reds"]["home_h1"] = self.game_object.homeTeamRedCards["H1"]
        template_dict["reds"]["home_h2"] = self.game_object.homeTeamRedCards["H2"]
        template_dict["reds"]["away_h1"] = self.game_object.awayTeamRedCards["H1"]
        template_dict["reds"]["away_h2"] = self.game_object.awayTeamRedCards["H2"]
        template_dict["formation"] = {}
        template_dict["formation"]["home_h1"] = self.game_object.homeTeamFormationName["H1"]
        template_dict["formation"]["home_h2"] = self.game_object.homeTeamFormationName["H2"]
        template_dict["formation"]["away_h1"] = self.game_object.awayTeamFormationName["H1"]
        template_dict["formation"]["away_h2"] = self.game_object.awayTeamFormationName["H2"]
        template_dict["ht_h1_comments"] = self.game_object.homeTeamH1Comments
        template_dict["ht_h2_comments"] = self.game_object.homeTeamH2Comments
        template_dict["at_h1_comments"] = self.game_object.awayTeamH1Comments
        template_dict["at_h2_comments"] = self.game_object.awayTeamH2Comments
        template_dict["hm_goals"] = {}
        template_dict["hm_goals"]["home_h1"] = self.game_object.homeTeamH1HeatMapStats.total_goals()
        template_dict["hm_goals"]["home_h2"] = self.game_object.homeTeamH2HeatMapStats.total_goals()
        template_dict["hm_goals"]["away_h1"] = self.game_object.awayTeamH1HeatMapStats.total_goals()
        template_dict["hm_goals"]["away_h2"] = self.game_object.awayTeamH2HeatMapStats.total_goals()
        template_dict["hm_assists"] = {}
        template_dict["hm_assists"]["home_h1"] = self.game_object.homeTeamH1HeatMapStats.total_assists()
        template_dict["hm_assists"]["home_h2"] = self.game_object.homeTeamH2HeatMapStats.total_assists()
        template_dict["hm_assists"]["away_h1"] = self.game_object.awayTeamH1HeatMapStats.total_assists()
        template_dict["hm_assists"]["away_h2"] = self.game_object.awayTeamH2HeatMapStats.total_assists()
        template_dict["hm_shots"] = {}
        template_dict["hm_shots"]["home_h1"] = self.game_object.homeTeamH1HeatMapStats.total_shots()
        template_dict["hm_shots"]["home_h2"] = self.game_object.homeTeamH2HeatMapStats.total_shots()
        template_dict["hm_shots"]["away_h1"] = self.game_object.awayTeamH1HeatMapStats.total_shots()
        template_dict["hm_shots"]["away_h2"] = self.game_object.awayTeamH2HeatMapStats.total_shots()
        template_dict["hm_shots_ot"] = {}
        template_dict["hm_shots_ot"]["home_h1"] = self.game_object.homeTeamH1HeatMapStats.total_shots_on_target()
        template_dict["hm_shots_ot"]["home_h2"] = self.game_object.homeTeamH2HeatMapStats.total_shots_on_target()
        template_dict["hm_shots_ot"]["away_h1"] = self.game_object.awayTeamH1HeatMapStats.total_shots_on_target()
        template_dict["hm_shots_ot"]["away_h2"] = self.game_object.awayTeamH2HeatMapStats.total_shots_on_target()
        template_dict["hm_possession"] = {}
        template_dict["hm_possession"]["home_h1"] = self.game_object.homeTeamH1HeatMapStats.total_possession_instances()
        template_dict["hm_possession"]["home_h2"] = self.game_object.homeTeamH2HeatMapStats.total_possession_instances()
        template_dict["hm_possession"]["away_h1"] = self.game_object.awayTeamH1HeatMapStats.total_possession_instances()
        template_dict["hm_possession"]["away_h2"] = self.game_object.awayTeamH2HeatMapStats.total_possession_instances()
        template_dict["hm_passing_rate"] = {}
        template_dict["hm_passing_rate"]["home_h1"] = round(self.game_object.home_team_passing_rate_from_heat_map('H1'), 2)
        template_dict["hm_passing_rate"]["home_h2"] = round(self.game_object.home_team_passing_rate_from_heat_map('H2'), 2)
        template_dict["hm_passing_rate"]["away_h1"] = round(self.game_object.away_team_passing_rate_from_heat_map('H1'), 2)
        template_dict["hm_passing_rate"]["away_h2"] = round(self.game_object.away_team_passing_rate_from_heat_map('H2'), 2)
        template_dict["hm_max_passes"] = {}
        template_dict["hm_max_passes"]["home_h1"] = self.game_object.homeTeamH1PassingStats.maxConsecutivePasses
        template_dict["hm_max_passes"]["home_h2"] = self.game_object.homeTeamH2PassingStats.maxConsecutivePasses
        template_dict["hm_max_passes"]["away_h1"] = self.game_object.awayTeamH1PassingStats.maxConsecutivePasses
        template_dict["hm_max_passes"]["away_h2"] = self.game_object.awayTeamH2PassingStats.maxConsecutivePasses
        template_dict["hm_lost_possession"] = {}
        template_dict["hm_lost_possession"]["home_h1"] = self.game_object.homeTeamH1HeatMapStats.total_lost_possession_instances()
        template_dict["hm_lost_possession"]["home_h2"] = self.game_object.homeTeamH2HeatMapStats.total_lost_possession_instances()
        template_dict["hm_lost_possession"]["away_h1"] = self.game_object.awayTeamH1HeatMapStats.total_lost_possession_instances()
        template_dict["hm_lost_possession"]["away_h2"] = self.game_object.awayTeamH2HeatMapStats.total_lost_possession_instances()

        self.game_object.draw_heat_map('B',1,'P','hm_h1_pass.png')
        self.game_object.draw_heat_map('B',2,'P','hm_h2_pass.png')
        self.game_object.draw_heat_map('B',1,'S','hm_h1_shot.png')
        self.game_object.draw_heat_map('B',2,'S','hm_h2_shot.png')
        self.game_object.draw_heat_map('B',1,'L','hm_h1_lost_possession.png')
        self.game_object.draw_heat_map('B',2,'L','hm_h2_lost_possession.png')
        
        h1_pass_heat_map = docxtpl.InlineImage(template, 'hm_h1_pass.png')
        template_dict["h1_pass_heat_map"] = h1_pass_heat_map
        h2_pass_heat_map = docxtpl.InlineImage(template, 'hm_h2_pass.png')
        template_dict["h2_pass_heat_map"] = h2_pass_heat_map
        h1_shot_heat_map = docxtpl.InlineImage(template, 'hm_h1_shot.png')
        template_dict["h1_shot_heat_map"] = h1_shot_heat_map
        h2_shot_heat_map = docxtpl.InlineImage(template, 'hm_h2_shot.png')
        template_dict["h2_shot_heat_map"] = h2_shot_heat_map
        h1_lost_possession_heat_map = docxtpl.InlineImage(template, 'hm_h1_lost_possession.png')
        template_dict["h1_lost_possession_heat_map"] = h1_lost_possession_heat_map
        h2_lost_possession_heat_map = docxtpl.InlineImage(template, 'hm_h2_lost_possession.png')
        template_dict["h2_lost_possession_heat_map"] = h2_lost_possession_heat_map
        
        return template_dict
        
    def create_report_from_template(self, output_file):
        template = docxtpl.DocxTemplate(self.report_template_file)
        
        template_dict = self.__create_template_dictionary__(template)
    
        template.render(template_dict)

        template.save(output_file)
