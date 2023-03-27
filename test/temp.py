#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*** This is a file used to temporarily store some methods that are not currently used ***
@Time     : 2023-03-27
@Author   : Maoyu
@Name     : temp.py
@Verson   : 1.0.0
"""
import asyncio
import hashlib
import httpx
from nonebot.log import logger


"""

*** Download QQ user's avatar ***

async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise Exception(f"{url} Download failure！")


async def download_avatar(user_id: str) -> bytes:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download_url(url)
    if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download_url(url)
    return data
    
"""

"""

***No description***

"battles_count": 74,                    战斗总数
"wins": 46,                             胜利场数
"losses": 28,                           失败场数

"damage_dealt": 7097387,                总伤害
"ships_spotted": 20,                    船只侦查数
"frags": 51,                            总击杀数
"survived": 39,                         存活的场数
"scouting_damage": 2143362,             总侦查伤害
"original_exp": 98561,                  总经验（无高账加成）
"exp": 198718,                          经验（虽然不知道是啥，但留着吧）
"art_agro": 103257650,                  总潜在伤害
"tpd_agro": 4844414,                    总鱼雷潜在伤害
"win_and_survived": 29,                 胜利并存活场数
"control_dropped_points": 360,          总防御点数
"control_captured_points": 405,         总占领点数
"team_control_captured_points": 9036,   团队总占领点数
"team_control_dropped_points": 4115,    团队总防御点数
"planes_killed": 514,                   总飞机击落数


"max_frags_by_planes": 0,               最多通过飞机击杀数
"max_total_agro": 3552965,              最多潜在伤害
"max_ships_spotted": 3,                 最多船只侦查数
"max_frags_by_ram": 0,                  最多冲撞击杀
"max_scouting_damage": 103488,          最大侦查伤害
"max_frags_by_dbomb": 0,                深水炸弹最多击杀
"max_frags_by_main": 3,                 主炮最多击杀
"max_planes_killed": 34,                最多飞机击落
"max_damage_dealt": 241356,             最大伤害
"max_frags_by_tpd": 1,                  最躲鱼雷击杀
"max_exp": 2470,                        最多经验（无高账加成）
"max_frags_by_atba": 1,                 最多副炮击杀数
"max_frags": 3,                         最多击杀数


"frags_by_ram": 0,                      冲撞击杀数
"frags_by_tpd": 2,                      总鱼雷击杀数
"frags_by_planes": 0,                   通过飞机击杀数
"frags_by_dbomb": 0,                    深水炸弹的击杀数
"frags_by_atba": 1,                     副炮击杀数
"frags_by_main": 38,                    主炮击杀数

"hits_by_main": 6041,                   命中的主炮数
"shots_by_main": 18667,                 发射的主炮数
"hits_by_skip": 0,                      命中的跳弹数
"shots_by_skip": 0,                     发射的跳弹数
"hits_by_atba": 157,                    命中的副炮数
"shots_by_atba": 768                    发射的副炮数
"hits_by_rocket": 0,                    命中的火箭弹数
"shots_by_rocket": 0,                   发射的火箭弹数
"hits_by_bomb": 0,                      炸弹的命中数
"shots_by_bomb": 0,                     投掷的炸弹数
"hits_by_tpd": 15,                      命中的鱼雷数
"shots_by_tpd": 112,                    发射的鱼雷数
"hits_by_tbomb": 0,                     空袭炸弹的命中数
"shots_by_tbomb": 0,                    投掷的空袭炸弹数

# meaningless data

"damage_dealt_to_buildings": 0,         对建筑伤害总量
"max_damage_dealt_to_buildings": 0,     最大对建筑伤害
"max_premium_exp": 4076,                最大经验（有高账加成）
"premium_exp": 156963,                  总经验（有高账加成）
"dropped_capture_points": 0,            ......(什么勾八)
"capture_points": 0,                    ......(什么勾八)
"max_suppressions_count": 0,            ......(什么勾八)
"suppressions_count": 0,                ......(什么勾八)
"battles_count_0910": 74,               0.9.10版本后战斗场数
"battles_count_078": 74,                0.7.8版本后战斗场数
"battles_count_0711": 74,               0.7.11版本后的战斗场数
"battles_count_512": 74,                0.5.12版本后的战斗场数
"battles_count_510": 74,                0.5.10版本后的战斗场数
"""
