import html
import re
import traceback
from pathlib import Path

from loguru import logger
from nonebot import get_driver, on_startswith
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.log import logger
from nonebot.params import CommandArg


from command_select import select_command

__plugin_name__ = "nonebot_plugin_kokomi"
__plugin_des__ = "战舰世界水表机器人"
__plugin_usage__ = ""
__plugin_author__ = "Maoyu <a20110123@163.com>"
__plugin_version__ = "3.1.0"
dir_path = Path(__file__).parent

bot = on_startswith("wws", block=False, aliases={"WWS"}, priority=10)
driver = get_driver()


@bot.handle()
async def main(bot: Bot, ev: MessageEvent, matchmsg: Message = CommandArg()):
    try:
        msg = ""
        qq_id = ev.user_id
        replace_name = None
        searchtag = html.unescape(str(matchmsg)).strip()
        match = re.search(r"(\(|（)(.*?)(\)|）)", searchtag)
        if match:
            replace_name = match.group(2)
            search_list = searchtag.replace(match.group(0), "").split()
        else:
            search_list = searchtag.split()
        command, search_list, qq_id = await select_command(search_list, qq_id)
        msg = await command(search_list, bot, ev)
        if isinstance(msg, str):
            await bot.send(ev, msg)
            return True
        else:
            await bot.send(ev, MessageSegment.image(msg))
            return True
    except ActionFailed:
        logger.warning(traceback.format_exc())
        try:
            await bot.send(ev, "send message error")
            return True
        except Exception:
            pass
        return False
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, "error")


async def get_uid():
    return None
