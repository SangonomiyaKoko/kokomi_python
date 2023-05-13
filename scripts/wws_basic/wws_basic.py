import json
import os
import httpx
import threading
import asyncio
import time
from datetime import date, timedelta
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import platform
import datetime
import gc
import yaml
import base64
from io import BytesIO

json_path = r'E:\kokomi_database_api\temp.json'
file_path = os.path.dirname(__file__)
read_json = open(json_path, "r", encoding="utf-8")
result = json.load(read_json)
read_json.close()
server = 'asia'
aid = '2023619512'

isWin = True if platform.system().lower() == 'windows' else False


class json_to_pic:
    def __init__(self) -> None:
        font2_path = os.path.join(file_path, 'SourceHanSansCN-Bold.ttf') if isWin else os.path.join(
            '/usr/share/fonts', 'SourceHanSansCN-Bold.ttf')
        self.font = {
            1: {
                20: ImageFont.truetype(font2_path, 20, encoding="utf-8"),
                35: ImageFont.truetype(font2_path, 35, encoding="utf-8"),
                45: ImageFont.truetype(font2_path, 45, encoding="utf-8"),
                55: ImageFont.truetype(font2_path, 55, encoding="utf-8"),
                80: ImageFont.truetype(font2_path, 80, encoding="utf-8"),
                100: ImageFont.truetype(font2_path, 100, encoding="utf-8")

            }
        }
        self.text_list = []

    def add_alpha_channel(self, img):
        '''给图片添加alpha通道'''
        b_channel, g_channel, r_channel = cv2.split(img)
        alpha_channel = np.ones(
            b_channel.shape, dtype=b_channel.dtype) * 255

        img_new = cv2.merge(
            (b_channel, g_channel, r_channel, alpha_channel))
        return img_new

    def merge_img(self, jpg_img, png_img, y1, y2, x1, x2):
        '''图片叠加'''
        if jpg_img.shape[2] == 3:
            jpg_img = self.add_alpha_channel(jpg_img)
        yy1 = 0
        yy2 = png_img.shape[0]
        xx1 = 0
        xx2 = png_img.shape[1]

        if x1 < 0:
            xx1 = -x1
            x1 = 0
        if y1 < 0:
            yy1 = - y1
            y1 = 0
        if x2 > jpg_img.shape[1]:
            xx2 = png_img.shape[1] - (x2 - jpg_img.shape[1])
            x2 = jpg_img.shape[1]
        if y2 > jpg_img.shape[0]:
            yy2 = png_img.shape[0] - (y2 - jpg_img.shape[0])
            y2 = jpg_img.shape[0]

        alpha_png = png_img[yy1:yy2, xx1:xx2, 3] / 255.0
        alpha_jpg = 1 - alpha_png

        for c in range(0, 3):
            jpg_img[y1:y2, x1:x2, c] = (
                (alpha_jpg*jpg_img[y1:y2, x1:x2, c]) + (alpha_png*png_img[yy1:yy2, xx1:xx2, c]))

        return jpg_img

    def x_coord(self, in_str: str, font: ImageFont.FreeTypeFont):
        '''获取文字的像素长度'''
        x = font.getsize(in_str)[0]
        out_coord = x
        return out_coord

    def add_text(self, res_img):
        draw = ImageDraw.Draw(res_img)
        for index in self.text_list:
            fontStyle = self.font[index[3]][index[4]]
            draw.text(index[0], index[1], index[2], font=fontStyle)
        return res_img

    def main(self, result):
        # Id卡
        self.text_list.append(
            [(158+14, 123+38), result['nickname'], (0, 0, 0), 1, 100])
        self.text_list.append(
            [(185+14, 237+38), f'{server.upper()} -- {aid}', (163, 163, 163), 1, 45])
        clan_color = {
            13477119: (186, 130, 255),
            12511165: (165, 219, 1163),
            14931616: (209, 163, 77),
            13427940: (169, 169, 169),
            11776947: (169, 169, 169),
            13408614: (192, 127, 114)
        }
        fontStyle = self.font[1][55]
        if result['data']['clans']['clan'] == {}:
            tag = 'None'
            tag_color = (179, 179, 179)
        else:
            tag = '['+result['data']['clans']['clan']['tag']+']'
            tag_color = clan_color[result['data']['clans']['clan']['color']]
        w = self.x_coord(tag, fontStyle)
        self.text_list.append(
            [(602-w/2+14, 317+38), tag, tag_color, 1, 55])
        creat_time = time.strftime(
            "%Y-%m-%d", time.localtime(result['data']['user']['created_at']))
        w = self.x_coord(creat_time, fontStyle)
        self.text_list.append(
            [(602-w/2+14, 405+38), creat_time, (255, 255, 255), 1, 55])
        # 主要数据
        avg_pr = int(result['data']['pr']['battle_type']['pvp']['personal_rating'] /
                     result['data']['pr']['battle_type']['pvp']['value_battles_count']) + 1
        pr_data = self.pr_info(avg_pr)
        pr_png_path = os.path.join(
            file_path, 'pr', '{}.png'.format(pr_data[0]))
        res_img = cv2.imread(os.path.join(
            file_path, 'background.png'), cv2.IMREAD_UNCHANGED)
        pr_png = cv2.imread(pr_png_path, cv2.IMREAD_UNCHANGED)
        pr_png = cv2.resize(pr_png, None, fx=0.787, fy=0.787)
        x1 = 118+14
        y1 = 590+38
        x2 = x1 + pr_png.shape[1]
        y2 = y1 + pr_png.shape[0]
        res_img = self.merge_img(res_img, pr_png, y1, y2, x1, x2)
        self.text_list.append(
            [(545+100*pr_data[3]+14, 653+38), pr_data[2]+str(pr_data[4]), (255, 255, 255), 1, 35])
        str_pr = '{:,}'.format(int(avg_pr))
        fontStyle = self.font[1][80]
        w = self.x_coord(str_pr, fontStyle)
        self.text_list.append(
            [(2270-w+14, 605+38), str_pr, (255, 255, 255), 1, 80])
        index = 'pvp'
        x0 = 310+14
        y0 = 823+38
        temp_data = result['data']['pr']['battle_type'][index]
        battles_count = '{:,}'.format(temp_data['battles_count'])
        if temp_data['battles_count'] != 0:
            avg_win = '{:.2f}%'.format(temp_data['wins']/temp_data['battles_count']*100)
            avg_wins = temp_data['wins'] / temp_data['battles_count']*100
            avg_damage = '{:,}'.format(int(temp_data['damage_dealt']/temp_data['battles_count'])).replace(',', ' ')
            avg_frag = '{:.2f}'.format(temp_data['frags']/temp_data['battles_count'])
            avg_xp = '{:,}'.format(int(temp_data['original_exp']/temp_data['battles_count'])).replace(',', ' ')
        else:
            avg_win = '{:.2f}%'.format(0.00)
            avg_wins = 0.00
            avg_damage = '{:,}'.format(0).replace(',', ' ')
            avg_frag = '{:.2f}'.format(0.00)
            avg_xp = '{:,}'.format(0).replace(',', ' ')
        if temp_data['value_battles_count'] == 0:
            avg_pr = -1
            avg_n_damage = -1
            avg_n_frag = -1
        else:
            avg_n_damage = temp_data['n_damage_dealt'] / \
                temp_data['battles_count']
            avg_n_frag = temp_data['n_frags'] / \
                temp_data['battles_count']
            avg_pr = temp_data['personal_rating'] / \
                temp_data['battles_count']

        fontStyle = self.font[1][80]
        w = self.x_coord(battles_count, fontStyle)
        self.text_list.append(
            [(x0+446*0-w/2, y0), battles_count, (0, 0, 0), 1, 80])
        w = self.x_coord(avg_win, fontStyle)
        self.text_list.append(
            [(x0+446*1-w/2, y0), avg_win, self.color_box(0, avg_wins)[1], 1, 80])
        w = self.x_coord(avg_damage, fontStyle)
        self.text_list.append(
            [(x0+446*2-w/2, y0), avg_damage, self.color_box(1, avg_n_damage)[1], 1, 80])
        w = self.x_coord(avg_frag, fontStyle)
        self.text_list.append(
            [(x0+446*3-w/2, y0), avg_frag, self.color_box(2, avg_n_frag)[1], 1, 80])
        w = self.x_coord(avg_xp, fontStyle)
        self.text_list.append(
            [(x0+446*4-w/2, y0), avg_xp, (0, 0, 0), 1, 80])
        # 数据总览
        i = 0
        for index in ['pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']:
            x0 = 0 + 14
            y0 = 1213+38
            temp_data = result['data']['pr']['battle_type'][index]
            battles_count = '{:,}'.format(temp_data['battles_count'])
            if temp_data['battles_count'] != 0:
                avg_win = '{:.2f}%'.format(
                    temp_data['wins']/temp_data['battles_count']*100)
                avg_wins = temp_data['wins'] / \
                    temp_data['battles_count']*100
                avg_damage = '{:,}'.format(int(
                    temp_data['damage_dealt']/temp_data['battles_count'])).replace(',', ' ')
                avg_frag = '{:.2f}'.format(
                    temp_data['frags']/temp_data['battles_count'])
                avg_xp = '{:,}'.format(int(
                    temp_data['original_exp']/temp_data['battles_count'])).replace(',', ' ')
            else:
                avg_win = '{:.2f}%'.format(0.00)
                avg_wins = 0.00
                avg_damage = '{:,}'.format(0).replace(',', ' ')
                avg_frag = '{:.2f}'.format(0.00)
                avg_xp = '{:,}'.format(0).replace(',', ' ')
            if temp_data['value_battles_count'] == 0:
                avg_pr = -1
                avg_n_damage = -1
                avg_n_frag = -1
            else:
                avg_n_damage = temp_data['n_damage_dealt'] / \
                    temp_data['battles_count']
                avg_n_frag = temp_data['n_frags'] / \
                    temp_data['battles_count']
                avg_pr = temp_data['personal_rating'] / \
                    temp_data['battles_count']
            str_pr = self.pr_info(
                avg_pr)[5] + '(+'+str(self.pr_info(avg_pr)[4])+')'

            fontStyle = self.font[1][55]
            w = self.x_coord(battles_count, fontStyle)
            self.text_list.append(
                [(572-w/2+x0, y0+90*i), battles_count, (0, 0, 0), 1, 55])
            w = self.x_coord(str_pr, fontStyle)
            self.text_list.append(
                [(937-w/2+x0, y0+90*i), str_pr, self.pr_info(avg_pr)[1], 1, 55])
            w = self.x_coord(avg_win, fontStyle)
            self.text_list.append(
                [(1291-w/2+x0, y0+90*i), avg_win, self.color_box(0, avg_wins)[1], 1, 55])
            w = self.x_coord(avg_damage, fontStyle)
            self.text_list.append(
                [(1595-w/2+x0, y0+90*i), avg_damage, self.color_box(1, avg_n_damage)[1], 1, 55])
            w = self.x_coord(avg_frag, fontStyle)
            self.text_list.append(
                [(1893-w/2+x0, y0+90*i), avg_frag, self.color_box(2, avg_n_frag)[1], 1, 55])
            w = self.x_coord(avg_xp, fontStyle)
            self.text_list.append(
                [(2160-w/2+x0, y0+90*i), avg_xp, (0, 0, 0), 1, 55])
            i += 1
        # 排位数据
        i = 0
        for season_stage, season_data in result['data']['season'].items():
            x0 = 0+14
            y0 = 2487+38
            temp_data = season_data
            battles_count = '{:,}'.format(temp_data['battles_count'])
            if temp_data['battles_count'] != 0:
                avg_win = '{:.2f}%'.format(
                    temp_data['wins']/temp_data['battles_count']*100)
                avg_wins = temp_data['wins'] / \
                    temp_data['battles_count']*100
                avg_damage = '{:,}'.format(int(
                    temp_data['damage_dealt']/temp_data['battles_count'])).replace(',', ' ')
                avg_frag = '{:.2f}'.format(
                    temp_data['frags']/temp_data['battles_count'])
                avg_xp = '{:,}'.format(int(
                    temp_data['original_exp']/temp_data['battles_count'])).replace(',', ' ')
            else:
                avg_win = '{:.2f}%'.format(0.00)
                avg_wins = 0.00
                avg_damage = '{:,}'.format(0).replace(',', ' ')
                avg_frag = '{:.2f}'.format(0.00)
                avg_xp = '{:,}'.format(0).replace(',', ' ')
            rank_list = {
                1: '黄金联盟',
                2: '白银联盟',
                3: '青铜联盟'
            }
            rank_color_list = {
                1: (209, 163, 77),
                2: (169, 169, 169),
                3: (192, 127, 114)
            }
            str_rank = rank_list[temp_data['best_season_rank']
                                 ] + ' ' + str(temp_data['best_rank'])

            fontStyle = self.font[1][55]
            w = self.x_coord(battles_count, fontStyle)
            self.text_list.append(
                [(572-w/2+x0, y0+90*i), battles_count, (0, 0, 0), 1, 55])
            w = self.x_coord(str_pr, fontStyle)
            self.text_list.append(
                [(934-w/2+x0, y0+90*i), str_rank, rank_color_list[temp_data['best_season_rank']], 1, 55])
            w = self.x_coord(avg_win, fontStyle)
            self.text_list.append(
                [(1291-w/2+x0, y0+90*i), avg_win, self.color_box(0, avg_wins)[1], 1, 55])
            w = self.x_coord(avg_damage, fontStyle)
            self.text_list.append(
                [(1595-w/2+x0, y0+90*i), avg_damage, (0, 0, 0), 1, 55])
            w = self.x_coord(avg_frag, fontStyle)
            self.text_list.append(
                [(1893-w/2+x0, y0+90*i), avg_frag, (0, 0, 0), 1, 55])
            w = self.x_coord(avg_xp, fontStyle)
            self.text_list.append(
                [(2160-w/2+x0, y0+90*i), avg_xp, (0, 0, 0), 1, 55])
            i += 1
        # 船只数据
        i = 0
        for index in ['AirCarrier', 'Battleship', 'Cruiser', 'Destroyer', 'Submarine']:
            x0 = 0+14
            y0 = 1805+38
            temp_data = result['data']['pr']['ship_type'][index]
            battles_count = '{:,}'.format(temp_data['battles_count'])
            if temp_data['battles_count'] != 0:
                avg_win = '{:.2f}%'.format(
                    temp_data['wins']/temp_data['battles_count']*100)
                avg_wins = temp_data['wins'] / \
                    temp_data['battles_count']*100
                avg_damage = '{:,}'.format(int(
                    temp_data['damage_dealt']/temp_data['battles_count'])).replace(',', ' ')
                avg_frag = '{:.2f}'.format(
                    temp_data['frags']/temp_data['battles_count'])
                avg_xp = '{:,}'.format(int(
                    temp_data['original_exp']/temp_data['battles_count'])).replace(',', ' ')
            else:
                avg_win = '{:.2f}%'.format(0.00)
                avg_wins = 0.00
                avg_damage = '{:,}'.format(0).replace(',', ' ')
                avg_frag = '{:.2f}'.format(0.00)
                avg_xp = '{:,}'.format(0).replace(',', ' ')
            if temp_data['value_battles_count'] == 0:
                avg_pr = -1
                avg_n_damage = -1
                avg_n_frag = -1
            else:
                avg_n_damage = temp_data['n_damage_dealt'] / \
                    temp_data['battles_count']
                avg_n_frag = temp_data['n_frags'] / \
                    temp_data['battles_count']
                avg_pr = temp_data['personal_rating'] / \
                    temp_data['battles_count']
            str_pr = self.pr_info(
                avg_pr)[5] + '(+'+str(self.pr_info(avg_pr)[4])+')'

            fontStyle = self.font[1][55]
            w = self.x_coord(battles_count, fontStyle)
            self.text_list.append(
                [(572-w/2+x0, y0+90*i), battles_count, (0, 0, 0), 1, 55])
            w = self.x_coord(str_pr, fontStyle)
            self.text_list.append(
                [(937-w/2+x0, y0+90*i), str_pr, self.pr_info(avg_pr)[1], 1, 55])
            w = self.x_coord(avg_win, fontStyle)
            self.text_list.append(
                [(1291-w/2+x0, y0+90*i), avg_win, self.color_box(0, avg_wins)[1], 1, 55])
            w = self.x_coord(avg_damage, fontStyle)
            self.text_list.append(
                [(1595-w/2+x0, y0+90*i), avg_damage, self.color_box(1, avg_n_damage)[1], 1, 55])
            w = self.x_coord(avg_frag, fontStyle)
            self.text_list.append(
                [(1893-w/2+x0, y0+90*i), avg_frag, self.color_box(2, avg_n_frag)[1], 1, 55])
            w = self.x_coord(avg_xp, fontStyle)
            self.text_list.append(
                [(2160-w/2+x0, y0+90*i), avg_xp, (0, 0, 0), 1, 55])
            i += 1
        if (isinstance(res_img, np.ndarray)):
            res_img = Image.fromarray(
                cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))
        # 图表
        max_num = 0
        num_list = []
        for tier, num in result['data']['pr']['ship_tier'].items():
            if num >= max_num:
                max_num = num
            num_list.append(num)
        max_index = (int(max_num/100) + 1)*100
        i = 0
        for index in num_list:
            pic_len = 500-index/max_index*500
            x1 = 258+129*i+14
            y1 = 2996+int(pic_len)+38
            x2 = 336+129*i+14
            y2 = 3500+38
            tier = ImageDraw.ImageDraw(res_img)
            tier.rectangle(((x1, y1), (x2, y2)),
                           fill=(137, 207, 240), outline=None)
            fontStyle = self.font[1][35]
            w = self.x_coord(str(index), fontStyle)
            self.text_list.append(
                [(297-w/2+129*i+14, y1-40), str(index), (0, 0, 0), 1, 35])
            i += 1
        res_img = self.add_text(res_img)

        res_img.show()
        #res_img.save('ss.png')

    def pr_info(self, pr: int):
        '''pr info'''
        if pr == -1:
            # [pic_num ,color_box, 描述, 字数差（add_text用），pr差值，评级]
            return [0, (128, 128, 128), '水平未知：', 0, -1, '水平未知']
        elif pr >= 0 and pr < 750:
            return [1, (205, 51, 51), '距离下一评级：+', 0, int(750-pr), '还需努力']
        elif pr >= 750 and pr < 1100:
            return [2, (254, 121, 3), '距离下一评级：+', 0, int(1100-pr), '低于平均']
        elif pr >= 1100 and pr < 1350:
            return [3, (255, 193, 7), '距离下一评级：+', 0, int(1350-pr), '平均水平']
        elif pr >= 1350 and pr < 1550:
            return [4, (68, 179, 0), '距离下一评级：+', -3, int(1550-pr), '好']
        elif pr >= 1550 and pr < 1750:
            return [5, (49, 128, 0), '距离下一评级：+', -2, int(1750-pr), '很好']
        elif pr >= 1750 and pr < 2100:
            return [6, (52, 186, 211), '距离下一评级：+', -1, int(2100-pr), '非常好']
        elif pr >= 2100 and pr < 2450:
            return [7, (121, 61, 182), '距离下一评级：+', 0, int(2450-pr), '大佬平均']
        elif pr >= 2450:
            return [8, (88, 43, 128), '已超过最高评级：+', 0, int(pr-2450), '神佬平均']

    def color_box(self, index: int, num: float):
        '''avg/server 自上向下为 win dmg frag xp plane_kill'''
        index_list = [
            [70, 60, 55, 52.5, 51, 49, 45],
            [1.7, 1.4, 1.2, 1.1, 1.0, 0.95, 0.8],
            [2, 1.5, 1.3, 1.0, 0.6, 0.3, 0.2],
            [1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.5],
            [2.0, 1.7, 1.5, 1.3, 1.0, 0.9, 0.7]
        ]
        data = index_list[index]
        if num == -1:
            return [0, (128, 128, 128)]
        elif num >= data[0]:
            return [8, (88, 43, 128)]
        elif num >= data[1] and num < data[0]:
            return [7, (121, 61, 182)]
        elif num >= data[2] and num < data[1]:
            return [6, (52, 186, 211)]
        elif num >= data[3] and num < data[2]:
            return [5, (49, 128, 0)]
        elif num >= data[4] and num < data[3]:
            return [4, (68, 179, 0)]
        elif num >= data[5] and num < data[4]:
            return [3, (255, 193, 7)]
        elif num >= data[6] and num < data[5]:
            return [2, (254, 121, 3)]
        elif num < data[6]:
            return [1, (205, 51, 51)]


json_to_pic().main(result)
