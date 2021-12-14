import os
import csv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen



class Crawler:
    def __init__(self):
        self.path = os.getcwd()
        self.dirname = "results"

    def get_bs_obj_active_player(self, page_num):
        url = f'https://www.kleague.com/player.do?page={page_num}&type=active&pos=all'
        html = urlopen(url)
        bs_obj = BeautifulSoup(html, "html.parser")
        return bs_obj

    def get_bs_obj_player_info(self, player_id):
        url = f"https://www.kleague.com/record/playerDetail.do?playerId={player_id}"
        try:
            html = urlopen(url)
            bs_obj = BeautifulSoup(html, "html.parser")
        except:
            return None
        return bs_obj

    def create_folder(self):
        direct = os.path.join(self.path, self.dirname)
        print('\n', direct)
        if os.path.exists(direct):
            print("Folder Already Exists. Skip Create.")
        else:
            os.mkdir(direct)
            print("Folder Created.")

    def write_header(self, header, fname):
        print('\n', fname)
        if os.path.isfile(fname) is False:
            f = open(fname, 'a+', newline='')
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            print("File created. Write header")
            f.close()
        else:
            print('File already exists. Skip writing header')

    def drop_duplicate_rows(self, fname):
        df = pd.read_csv(fname)
        df = df.drop_duplicates()
        df.to_csv(fname, index=False)
        print("\nDrop duplicates Done.")
