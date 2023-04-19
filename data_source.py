import re
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

dir_path = Path(__file__).parent


@dataclass
class matching:
    keywords: Tuple[str, ...]
    match_keywords: str


nations = [
    matching(("commonwealth", "英联邦",), "commonwealth",),
    matching(("europe", "欧洲",), "europe",),
    matching(("france", "法国",), "france",),
    matching(("germany", "德国",), "germany",),
    matching(("italy", "意大利",), "italy",),
    matching(("japan", "日本",), "japan",),
    matching(("pan_america", "泛美",), "pan_america",),
    matching(("pan_asia", "泛亚",), "pan_asia",),
    matching(("uk", "英国", "United_Kingdom"), "United_Kingdom"),
    matching(("usa", "美国",), "usa",),
    matching(("ussr", "苏联",), "Russia",),
    matching(("netherlands", "荷兰",), "netherlands",),
    matching(("spain", "西班牙",), "spain",),
]

shiptypes = [
    matching(("Cruiser", "巡洋舰", "巡洋", "CA"), "Cruiser"),
    matching(("Battleship", "战列舰", "战列", "BB"), "Battleship"),
    matching(("Destroyer", "驱逐舰", "驱逐", "DD"), "Destroyer"),
    matching(("Submarine", "潜艇", "SS"), "Submarine"),
    matching(("AirCarrier", "航空母舰", "航母", "CV"), "AirCarrier"),
]

levels = [
    matching(("1", "1级", "一级", "一", "I"), "1"),
    matching(("2", "2级", "二级", "二", "II"), "2"),
    matching(("3", "3级", "三级", "三", "III"), "3"),
    matching(("4", "4级", "四级", "四", "IV"), "4"),
    matching(("5", "5级", "五级", "五", "V"), "5"),
    matching(("6", "6级", "六级", "六", "VI"), "6"),
    matching(("7", "7级", "七级", "七", "VII"), "7"),
    matching(("8", "8级", "八级", "八", "VIII"), "8"),
    matching(("9", "9级", "九级", "九", "XI"), "9"),
    matching(("10", "10级", "十级", "十", "X"), "10"),
    matching(("11", "11级", "十一级", "十一", "XI"), "11"),
]

servers = [
    matching(("asia", "亚服", "asian", "亚"), "asia"),
    matching(("eu", "欧服", "europe", "欧"), "eu"),
    matching(("na", "美服", "NorthAmerican", "美"), "na"),
    matching(("ru", "俄服", "Russia", "俄"), "ru"),
    matching(("cn", "国服", "china", "国"), "cn"),
]
