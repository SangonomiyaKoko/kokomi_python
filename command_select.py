from dataclasses import dataclass
from typing import Protocol, Tuple
import asyncio
import re

from scripts.wws_ship import wws_ship


class Func(Protocol):
    async def __call__(self, **kwargs):
        ...


@dataclass
class command:
    keywords: Tuple[str, ...]
    func: Func


"""
wws [me/@] ship [ship_name]
wws [me/@] recent [date]
wws [me/@] rank recent [date]
wws [me/@] info
wws [me/@] [ship_type]
wws [me/@] 日历
wws [me/@] 绑定列表
wws [me/@] ship.rank [ship_name]

wws [server] set [id]
wws 切绑 [num]
wws skill [ship_name]
wws ship server [ship_type]
wws [server] ship [ship_name]

不支持通过[server] [id]方式入参
"""
"""
msg匹配func规则,判断优先级从上至下
1.带[me/@]优先级最高
2.命令词越长，优先级越高
3.无参>有参>不定参
"""

first_command_list = [
    # 带[me/@]的命令
    command(("info",), None,),
    command(("日历",), None,),
    command(("绑定列表",), None,),
    command(("ship",), None,),
    command(("ship.rank",), None,),
    command(("rank", "recent",), None,),
    command(("recent",), None,),
]
second_command_list = [
    # 不带[me/@]的命令
    command(("set",), None,),
    command(("skill",), None,),
    command(("ship", "server",), None,),
    command(("ship",), None,),
    command(("切绑",), None,),
]


async def default_func():
    """
    无匹配时的默认函数
    """
    return None


async def findFunction(match_list, command_list):
    for com in command_list:
        is_matching = True
        for key in com.keywords:
            if key not in match_list:
                is_matching = False
                break
            else:
                del match_list[match_list.index(key)]
        if is_matching:
            return com, match_list
    return command(None, default_func,), match_list


async def select_command(search_list, qq_id):
    if(
        search_list[0] == 'me'
        or re.search('CQ:at', search_list[0])
    ):
        if re.search('CQ:at', search_list[0]):
            qqid_compile = re.compile(
                "\[CQ:at,qq=(?P<qqid>[0-9]*)\]"
            )
            qqid_content = qqid_compile.search(search_list[0])
            qq_id = qqid_content.group("qqid")
        else:
            qq_id = qq_id
        del search_list[0]
        command, search_list = await findFunction(
            search_list, first_command_list
        )
    else:
        command, search_list = await findFunction(
            search_list, second_command_list
        )
    return command.func, search_list, qq_id

print(asyncio.run(select_command(
    ['[CQ:at,qq=2694522387]', 'recent', '10'], '3197206779')))
