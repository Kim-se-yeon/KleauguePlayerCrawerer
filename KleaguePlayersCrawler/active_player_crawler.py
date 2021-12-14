import os
import csv
from myconstants import *
from crawler import Crawler
import pprint


class ActivePlayerCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.fname = os.path.join(self.path, self.dirname, f"active_players.csv")
        self.header = player_header

    def run(self):
        self.create_folder()
        self.write_header(header=player_header, fname=self.fname)

        f = open(self.fname, "a+", newline='')
        csv_writer = csv.writer(f)
        page_num = 1

        while True:
            bs_obj = self.get_bs_obj_active_player(page_num=page_num)
            players = self.get_player(bs_obj=bs_obj, page_num=page_num)
            if players is None:
                break
            else:
                csv_writer.writerows(players)
                page_num += 1

            pprint.pprint(players)
        f.close()
        self.drop_duplicate_rows(fname=self.fname)

    def get_player(self, bs_obj, page_num):
        players = []

        for i, j in enumerate(bs_obj.select('.txt')):
            team_name = bs_obj.select('span.small')[i].get_text()
            player_team_name = bs_obj.select('span.name')[i].get_text()
            player_name = player_team_name.replace(team_name, '')
            squad_num = bs_obj.select('.txt')[i].get_text().replace(player_team_name, '').replace('No.','').strip()

            try:
                squad_num = int(squad_num)
            except:
                continue

            player = [
                page_num,
                team_name,
                player_name,
                squad_num,
            ]

            if type(player[3]) == int:
                players.append(player)

        # 선수 없으면 필터링
        if not players:
            players = None
            print(f"No Player Exist ")
        else:
            print('\n')
            #pprint.pprint(players)
        return players







