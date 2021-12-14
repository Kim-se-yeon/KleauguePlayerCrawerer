import os
import csv
from myconstants import *
from crawler import Crawler
import pprint
from active_player_crawler import ActivePlayerCrawler


class PlayerInfoCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.fname = os.path.join(self.path, self.dirname, f"player_info.csv")
        self.header = player_header

    def run(self):
        self.create_folder()
        self.write_header(header=player_info_header, fname=self.fname)

        f = open(self.fname, "a+", newline='')
        csv_writer = csv.writer(f)
        player_id = 19970001


        while True:

            bs_obj = self.get_bs_obj_player_info(player_id=player_id)
            if bs_obj is not None:
                players = self.get_player_info(bs_obj=bs_obj, player_id=player_id)
            if players is None:
                break
            else:
                csv_writer.writerows(players)
                # 선수 Id를 건너뛰기 위한 조건문 (선수가 1년에 최대500명 정도가 등록될거라 판단하여 500뒤에 다음년도로 건너뜀)
                if player_id % 500 == 0:
                    player_id = player_id + 9501
                else:
                    player_id += 1

        f.close()
        self.drop_duplicate_rows(fname=self.fname)

    def get_player_info(self, bs_obj, player_id):
        players = []

        player_name = bs_obj.select('table.style2>tbody>tr>td')[0].get_text().strip()
        player_english_name = bs_obj.select('table.style2>tbody>tr>td')[1].get_text().strip()
        team_name = bs_obj.select('table.style2>tbody>tr>td')[2].get_text().strip()
        position = bs_obj.select('table.style2>tbody>tr>td')[3].get_text().strip()
        squad_num = bs_obj.select('table.style2>tbody>tr>td')[4].get_text().strip()
        national = bs_obj.select('table.style2>tbody>tr>td')[5].get_text().strip()
        height = bs_obj.select('table.style2>tbody>tr>td')[6].get_text().strip()
        weight = bs_obj.select('table.style2>tbody>tr>td')[7].get_text().strip()
        birthday = bs_obj.select('table.style2>tbody>tr>td')[8].get_text().strip()

        player = [
            player_id,
            team_name,
            player_name,
            player_english_name,
            squad_num,
            position,
            national,
            height,
            weight,
            birthday
        ]
        players.append(player)

        # 선수 없으면 필터링
        if not players:
            players = ''
            print(f"No Player Exist ")
        else:
            print('\n')
            pprint.pprint(players)
        return players