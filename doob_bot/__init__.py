"""
 Doob Bot, A simple discord bot for Raider.io

 Author: Stephen Onnen

 Github: https://github.com/onnenon/doob_bot

"""

import os
import datetime

import discord
from discord.ext import commands
from spylogger import get_logger

from doob_bot.raiderio_api import char_api_request

BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT = commands.Bot(command_prefix="#")

LOGGER = get_logger(log_level="DEBUG")

CHAR_PREFIX = ['#info', '#ioscore', '#best', '#highest']
MYTHIC_PLUS_PREFIX = []


@BOT.event
async def on_ready():
    """Prints to console when bot is running successfully. """
    LOGGER.info(f"{BOT.user.name} Is Running. ID: {BOT.user.id}")


@BOT.event
async def on_message(message):
    """Scans messages in text channels of a server and calls the Raider.io API
       when a defined prefix is used.

    Args:
        message: Message object recieved by discord bot.

    Returns:
        Sends a message to the channel of the message arg with an embed object
        if data was returned, or an error message and exeption was thrown while
        attempting to call Raider.io's API
    """
    # Split the message into a list
    args = message.content.split(" ")

    # If first index of that list is in the defined prefixes prep the message
    if args[0] in CHAR_PREFIX or args[0] in MYTHIC_PLUS_PREFIX:
        prefix = args.pop(0)
        arg_fix = [arg.replace("_", "-") for arg in args]

        if prefix in CHAR_PREFIX:
            embed = discord.Embed(
                title="Doob Bot",
                colour=discord.Colour(0x52472b),
                url="http://github.com/onnenon/doob_bot",
                description="A simple Discord bot for getting Raider.io Data\n",
                timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=("-" * 115))
            try:
                message_embed = char_api_request(arg_fix, prefix, embed)
                await message.channel.send(embed=message_embed)
            except ValueError as e:
                LOGGER.error({"Exception:": str(e)})
                await message.channel.send("Invalid number of arguments!")
            except Exception as e:
                LOGGER.error({"Exception:": str(e)})
                await message.channel.send(
                    "No data was returned from Raider.io, check your spelling!!"
                )

        if prefix in MYTHIC_PLUS_PREFIX:
            # TODO Create commands that get non-characterinfo from API
            pass


if __name__ == "__main__":
    BOT.run(BOT_TOKEN)
