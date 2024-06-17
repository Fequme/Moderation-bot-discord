#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Main Lib 

import disnake as sweetness 
from disnake.ext import commands, tasks
from disnake.ext.commands import InteractionBot

# Standart Import

from client import config
import asyncio

# Other Lib

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
import datetime

mongo = config.SWEETNESS['MONGO']
cluster = MotorClient(mongo)
collection = cluster.sweetness.users
staff = cluster.sweetness.staff
warns = cluster.sweetness.warns

# Class

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print("READY")

    @commands.slash_command(name="stats", description="Статистика стафф-пользователя")
    async def stats(self, inter, member: sweetness.Member = None):
        staffr = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['STAFF_ROLE'])
        r1 = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if member is None:
            if staffr in inter.author.roles:
                if await staff.find_one({"id": inter.author.id}) is None:
                    await staff.insert_one({
                        "id": inter.author.id,
                        "voice_mutes": 0,
                        "text_mutes": 0,
                        "bans": 0,
                        "voice_warns": 0,
                        "text_warns": 0,
                        "ban_warns": 0,
                        "gender_give": 0,
                        "gender_change": 0,
                        "accept_tickets": 0,
                        "decline_tickets": 0,
                        "rate_tickets": 0,
                        "accept_reports": 0,
                        "decline_reports": 0,
                        "rate_reports": 0
                    })

                stats = await staff.find_one({"id": inter.author.id})
                if stats is None:
                    embed = sweetness.Embed()
                    embed.description = "> Ваша статистика пуста!"
                    await inter.response.send_message(embed=embed)
                else:
                    text_warns = stats['text_warns']
                    voice_warns = stats['voice_warns']
                    ban_warns = stats['ban_warns']

                    text_mutes = stats['text_mutes']
                    voice_mutes = stats['voice_mutes']
                    bans = stats['bans']

                    gender_give = stats['gender_give']
                    gender_change = stats['gender_change']
                    
                    accept_tickets = stats['accept_tickets']
                    decline_tickets = stats['decline_tickets']
                    rate_tickets = stats['rate_tickets']

                    try:
                        goto_tickets = rate_tickets / accept_tickets
                    except:
                        goto_tickets = "0.0"
                    
                    accept_reports = stats['accept_reports']
                    decline_reports = stats['decline_reports']
                    rate_reports = stats['rate_reports']

                    try:
                        goto_reports = rate_reports / accept_reports
                    except:
                        goto_reports = "0.0"

                    if r1 in inter.author.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {inter.author}", icon_url=inter.author.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r2 in inter.author.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {inter.author}", icon_url=inter.author.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r3 in inter.author.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {inter.author}", icon_url=inter.author.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r4 in inter.author.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {inter.author}", icon_url=inter.author.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r5 in inter.author.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.set_footer(text=f"Статистика - {inter.author}", icon_url=inter.author.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass
                    if r6 in inter.author.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {inter.author}", icon_url=inter.author.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass    
            else:
                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = "> Для просмотра своей статистики, вам нужно быть участником стаффа."
                await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            if staffr in member.roles:
                if await staff.find_one({"id": member.id}) is None:
                    await staff.insert_one({
                        "id": member.id,
                        "voice_mutes": 0,
                        "text_mutes": 0,
                        "bans": 0,
                        "voice_warns": 0,
                        "text_warns": 0,
                        "ban_warns": 0,
                        "gender_give": 0,
                        "gender_change": 0,
                        "accept_tickets": 0,
                        "decline_tickets": 0,
                        "rate_tickets": 0,
                        "accept_reports": 0,
                        "decline_reports": 0,
                        "rate_reports": 0
                    })

                stats = await staff.find_one({"id": member.id})
                if stats is None:
                    embed = sweetness.Embed()
                    embed.color = 0x2f3136
                    embed.description = "> Ваша статистика пуста!"
                    await inter.response.send_message(embed=embed)
                else:
                    text_warns = stats['text_warns']
                    voice_warns = stats['voice_warns']
                    ban_warns = stats['ban_warns']

                    text_mutes = stats['text_mutes']
                    voice_mutes = stats['voice_mutes']
                    bans = stats['bans']

                    gender_give = stats['gender_give']
                    gender_change = stats['gender_change']
                    
                    accept_tickets = stats['accept_tickets']
                    decline_tickets = stats['decline_tickets']
                    rate_tickets = stats['rate_tickets']

                    try:
                        goto_tickets = rate_tickets / accept_tickets
                    except:
                        goto_tickets = "0.0"
                    
                    accept_reports = stats['accept_reports']
                    decline_reports = stats['decline_reports']
                    rate_reports = stats['rate_reports']

                    try:
                        goto_reports = rate_reports / accept_reports
                    except:
                        goto_reports = "0.0"

                    if r1 in member.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {member}", icon_url=member.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r2 in member.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {member}", icon_url=member.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r3 in member.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {member}", icon_url=member.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r4 in member.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {member}", icon_url=member.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass 
                    if r5 in member.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**\n> Голосовые: **`{voice_warns}`**\n> Серверные: **`{ban_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**\n> Голосовые: **`{voice_mutes}`**\n> Серверные: **`{bans}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Репорты", value=f"> Принятых: **`{accept_reports}`**\n> Отклоненных: **`{decline_reports}`**", inline=True)
                        
                        # Need Connect ^

                        embed.set_footer(text=f"Статистика - {member}", icon_url=member.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass
                    if r6 in member.roles:
                        embed = sweetness.Embed()
                        embed.color = 0x2f3136
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4149/4149634.png")
                        embed.add_field(name="Предупреждения", value=f"> Текстовые: **`{text_warns}`**", inline=True)
                        embed.add_field(name="Наказания", value=f"> Текстовые: **`{text_mutes}`**", inline=True)
                        
                        # Need Connect

                        embed.add_field(name="Тикеты", value=f"> Принятых: **`{accept_tickets}`**\n> Отклоненных: **`{decline_tickets}`**\n> Оценка: **`{goto_tickets}`**", inline=True)
                        
                        # Need Connect ^

                        embed.add_field(name="Гендерные роли", value=f"> Выдано: **`{gender_give}`**\n> Изменено: **`{gender_change}`**")
                        embed.set_footer(text=f"Статистика - {member}", icon_url=member.display_avatar)
                        try:
                            await inter.response.send_message(embed=embed)
                        except:
                            pass   
            else:
                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = "> Упомянутый пользователь не является стаффом."
                await inter.response.send_message(embed=embed, ephemeral=True)

                

def setup(client):
    client.add_cog(Stats(client))             