from dataclasses import dataclass
from typing import Protocol, Tuple

from .scripts.wws_ship import wws_ship


class Func(Protocol):
    async def __call__(self, **kwargs):
        ...


@dataclass
class command:
    keywords: Tuple[str, ...]
    func: Func
    default_func: Func = None


command_list = [
    command(("ship"), wws_ship),
]


async def findFunction(match_list, command_List):
    for com in command_List:
        for kw in com.keywords:
            for i, match_kw in enumerate(match_list):
                if match_kw.find(kw) + 1:
                    match_list[i] = str(match_kw).replace(kw, "")
                    if match_list[i] == "":
                        match_list.remove("")
                    return com, match_list
    return command(None, default_func, None), match_list


async def select_command(search_list):
    command, search_list = await findFunction(
        search_list, command_list
    )
    return command.func, search_list


async def default_func():
    """
    无匹配时的默认函数
    """
    return None
