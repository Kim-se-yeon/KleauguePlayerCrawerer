import os
import csv
from myconstants import *
from crawler import Crawler
import pprint
from active_player_crawler import ActivePlayerCrawler
from player_info_crawler import PlayerInfoCrawler
import pandas as pd


class PlayerSeasonInfoCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.fname = os.path.join(self.path, self.dirname, f"player_season_info_ex.csv")
        self.header = player_header

    def run(self):
        self.create_folder()
        self.write_header(header=player_season_info_header, fname=self.fname)

        f = open(self.fname, "a+", newline='')
        csv_writer = csv.writer(f)
        player_id = 20210077

        while True:

            bs_obj = self.get_bs_obj_player_info(player_id=player_id)
            active_players = load_active_player()

            if bs_obj is not None:
                player_season = self.get_player_season_info(bs_obj=bs_obj, player_id=player_id)
                if player_season != '':
                    player_info = [player_season[0][4], int(player_season[0][3])]
            if player_season is None:
                break
            else:
                if player_info in active_players:
                    pprint.pprint(player_season)
                    print(' # '*5 + str(player_id))
                    csv_writer.writerows(player_season)
                if player_id % 500 == 0:
                    player_id = player_id + 9501
                else:
                    player_id += 1

        f.close()
        self.drop_duplicate_rows(fname=self.fname)

    def get_player_season_info(self, bs_obj, player_id):
        player_season = []

        for i, j in enumerate(bs_obj.select('body > div.sub-contents-wrap > div > div:nth-child(2) > div > table > tbody > tr')):
            season = bs_obj.select('div.table-wrap > table > tbody > tr')[i].get_text().strip().split('\n')[0]
            team_name = bs_obj.select('div.table-wrap > table > tbody > tr')[i].get_text().strip().split('\n')[2]
            player_name = bs_obj.select('table.style2 > tbody > tr > td')[0].get_text().strip()
            player_english_name = bs_obj.select('table.style2 > tbody > tr > td')[1].get_text().strip()

            squad_num = bs_obj.select('table.style2 > tbody > tr > td')[4].get_text().strip()
            national = bs_obj.select('table.style2 > tbody > tr > td')[5].get_text().strip()

            player_season_info = [
                season,
                team_name,
                player_id,
                squad_num,
                player_name,
                player_english_name,
                national
            ]
            if player_season_info[3] != '-' and player_season_info[4] != '':
                player_season.append(player_season_info)

        # 선수 없으면 필터링
        if not player_season:
            player_season = ''
            print(f"No Season Info")
        else:
            print('\n')
        return player_season

def load_active_player():
    active_player = pd.read_csv('/Users/kimseyeon/PycharmProjects/KleaguePlayersCrawler /results/active_players.csv')
    active_player_name = active_player['Player_name']
    active_player_num = active_player['Squad_num']
    active_players = pd.concat([active_player_name, active_player_num], axis=1)
    active_players = active_players.values.tolist()
    #pprint.pprint(active_players)
    return active_players
