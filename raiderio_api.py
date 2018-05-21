"""
Raider.io API info at https://raider.io/api#!/
"""

import html
import json
import requests
import utils

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from utils import emify_info

API_URL_BASE = "https://raider.io/api/v1/"
HEADERS = {'Content-Type': 'application/json'}

INFO_DATA = ['name', 'class', 'active_spec_name', 'region',
             'realm', 'faction', 'gear', 'guild', 'profile_url', 'thumbnail_url']
IOSCORE_DATA = ['name', 'realm', 'class', 'active_spec_name',
                'mythic_plus_scores', 'thumbnail_url', 'all', 'dps', 'healer', 'tank']
BEST_DATA = ['name', 'class', 'active_spec_name', 'realm', 'mythic_plus_best_runs', 'mythic_plus_highest_level_runs', 'dungeon',
             'mythic_level', 'num_keystone_upgrades', 'score', 'thumbnail_url']


def get_character_info(name: str, realm: str, prefix, region: str="US"):
    """ Return Character Info from Raider.io """
    fields = []

    if prefix == '#info':
        fields.extend(('gear', 'guild'))
    elif prefix == '#ioscore':
        fields.append('mythic_plus_scores')
    elif prefix == '#best':
        fields.append('mythic_plus_best_runs')
    elif prefix == '#highest':
        fields.append('mythic_plus_highest_level_runs')

    field_str = ""
    if len(fields) > 0:
        field_str += "&fields="
        for field in fields:
            field_str += "{}%2C%20".format(field)

    if field_str.endswith("0"):
        field_str = field_str[:-6]

    api_url = "{}characters/profile?region={}&realm={}&name={}{}".format(
        API_URL_BASE, region, realm, name, field_str)

    # print(api_url)

    response = requests.get(api_url, headers=HEADERS)

    if response.status_code == 200:
        # print(json.loads(response.content.decode('utf-8')))
        return json.loads(response.content.decode('utf-8'))
    return None


def char_api_request(li: list, prefix: str, em):
    if len(li) == 2:
        user_info = get_character_info(li[0], li[1], prefix)

    elif len(li) == 3:
        user_info = get_character_info(li[0], li[1], prefix, li[2])

    if(user_info is not None):
        # Gets character Info
        if prefix == '#info':
            return emify_info(em, INFO_DATA, **user_info)

        # Gets character IO Score
        if prefix == '#ioscore':
            return emify_info(em, IOSCORE_DATA, **user_info)

        if prefix == '#best' or prefix == '#highest':
            return emify_info(em, BEST_DATA, **user_info)

    return None
