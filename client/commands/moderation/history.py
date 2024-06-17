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

import os
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
import datetime

mongo = config.SWEETNESS['MONGO']
cluster = MotorClient(mongo)
collection = cluster.sweetness.users
staff = cluster.sweetness.staff
warns = cluster.sweetness.warns

class Menu(sweetness.ui.View):
    def __init__(self, embeds: List[sweetness.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Страница {i + 1} из {len(self.embeds)}")

        self._update_state()

    def _update_state(self) -> None:
        self.first_page.disabled = self.prev_page.disabled = self.index == 0
        self.last_page.disabled = self.next_page.disabled = self.index == len(self.embeds) - 1

    @sweetness.ui.button(emoji="⏪", style=sweetness.ButtonStyle.blurple)
    async def first_page(self, button: sweetness.ui.Button, inter: sweetness.MessageInteraction):
        self.index = 0
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @sweetness.ui.button(emoji="◀", style=sweetness.ButtonStyle.secondary)
    async def prev_page(self, button: sweetness.ui.Button, inter: sweetness.MessageInteraction):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @sweetness.ui.button(emoji="🗑️", style=sweetness.ButtonStyle.red)
    async def remove(self, button: sweetness.ui.Button, inter: sweetness.MessageInteraction):
        await inter.response.edit_message(view=None)

    @sweetness.ui.button(emoji="▶", style=sweetness.ButtonStyle.secondary)
    async def next_page(self, button: sweetness.ui.Button, inter: sweetness.MessageInteraction):
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @sweetness.ui.button(emoji="⏩", style=sweetness.ButtonStyle.blurple)
    async def last_page(self, button: sweetness.ui.Button, inter: sweetness.MessageInteraction):
        self.index = len(self.embeds) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

# Class

class History(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print("READY")

    @commands.slash_command(name="history", description="История наказаний пользователя")
    async def history(self, inter, member: sweetness.Member = None):  
        if member is None:
            if await collection.find_one({"id": inter.author.id}) is None:
                await collection.insert_one({
                    "id": inter.author.id,
                    "ban": None,
                    "voice": None,
                    "text": None,
                    "warns": [],
                    "punishments": []
                })
        else:
            if member == inter.author:
                if await collection.find_one({"id": inter.author.id}) is None:
                    await collection.insert_one({
                        "id": inter.author.id,
                        "ban": None,
                        "voice": None,
                        "text": None,
                        "warns": [],
                        "punishments": []
                    })                
            else:
                if await collection.find_one({"id": member.id}) is None:
                    await collection.insert_one({
                        "id": member.id,
                        "ban": None,
                        "voice": None,
                        "text": None,
                        "warns": [],
                        "punishments": []
                    })
        if member is None:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.set_thumbnail(url=inter.author.display_avatar)
            if inter.guild.icon is not None:
                embed.set_footer(text="🦋 SweetNess", icon_url=inter.guild.icon)
            else:
                embed.set_footer(text="🦋 SweetNess")
            types = {
                "BanW": "Серверное предупреждение",
                "BanM": "Серверное наказание",
                "VoiceW": "Голосовое предупреждение",
                "VoiceM": "Голосовое наказание",
                "TextW": "Текстовое предупреждение",
                "TextM": "Текстовое наказание"
            }
            punishments = (await collection.find_one({"id": inter.author.id}))['punishments']
            if not punishments:
                embed.description = "⠀\n> Вас можно причислить к лицу святых, ваша история наказаний пуста."
                await inter.send(embed=embed, ephemeral=True)
                return 
                
            embed.set_author(name=f"История наказаний {inter.author}")
            embeds = []
            punishments.reverse()

            separation_sort = lambda lst, sz: [lst[element:element + sz] for element in range(0, len(lst), sz)]
            documents_sorted = separation_sort(punishments, 5)

            for i in documents_sorted:
                emb = sweetness.Embed()
                emb.color = 0x2f3136 
                emb.set_author(name=f"История наказаний {inter.author}")
                emb.set_thumbnail(url=inter.author.display_avatar)
                if inter.guild.icon is not None:
                    emb.set_footer(text="🦋 SweetNess", icon_url=inter.guild.icon)
                else:
                    emb.set_footer(text="🦋 SweetNess")
                    
                for doc in i:
                    value = f"Модератор: <@{doc['moderator']}>\nПричина: **{doc['reason']}**\nДата выдачи: <t:{int(doc['data_issue'].timestamp())}:D>"
                    if 'date_expired' in doc:
                        value +=f"\nДата окончания: <t:{int(doc['date_expired'].timestamp())}:D>"
                        
                    emb.add_field(name=types[doc['type']], value=value, inline=False)
                    
                if doc == i[-1]:
                    embeds.append(emb)
                
            await inter.send(embed=embeds[0], view=Menu(embeds), ephemeral=True)
        else:
            if not member.bot:
                if member == inter.author:
                    embed = sweetness.Embed()
                    embed.color = 0x2f3136
                    embed.set_thumbnail(url=inter.author.display_avatar)
                    if inter.guild.icon is not None:
                        embed.set_footer(text="🦋 SweetNess", icon_url=inter.guild.icon)
                    else:
                        embed.set_footer(text="🦋 SweetNess")
                    types = {
                        "BanW": "Серверное предупреждение",
                        "BanM": "Серверное наказание",
                        "VoiceW": "Голосовое предупреждение",
                        "VoiceM": "Голосовое наказание",
                        "TextW": "Текстовое предупреждение",
                        "TextM": "Текстовое наказание"
                    }
                    punishments = (await collection.find_one({"id": inter.author.id}))['punishments']
                    if not punishments:
                        embed.description = "⠀\n> Вас можно причислить к лицу святых, ваша история наказаний пуста."
                        await inter.send(embed=embed, ephemeral=True)
                        return 
                        
                    embed.set_author(name=f"История наказаний {inter.author}")
                    embeds = []
                    punishments.reverse()

                    separation_sort = lambda lst, sz: [lst[element:element + sz] for element in range(0, len(lst), sz)]
                    documents_sorted = separation_sort(punishments, 5)

                    for i in documents_sorted:
                        emb = sweetness.Embed()
                        emb.color = 0x2f3136 
                        emb.set_author(name=f"История наказаний {inter.author}")
                        emb.set_thumbnail(url=inter.author.display_avatar)
                        if inter.guild.icon is not None:
                            emb.set_footer(text="🦋", icon_url=inter.guild.icon)
                        else:
                            emb.set_footer(text="🦋")
                            
                        for doc in i:
                            value = f"Модератор: <@{doc['moderator']}>\nПричина: **{doc['reason']}**\nДата выдачи: <t:{int(doc['data_issue'].timestamp())}:D>"
                            if 'date_expired' in doc:
                                value +=f"\nДата окончания: <t:{int(doc['date_expired'].timestamp())}:D>"
                                
                            emb.add_field(name=types[doc['type']], value=value, inline=False)
                            
                        if doc == i[-1]:
                            embeds.append(emb)
                        
                    await inter.send(embed=embeds[0], view=Menu(embeds), ephemeral=True)                        
                else:
                    embed = sweetness.Embed()
                    embed.color = 0x2f3136
                    embed.set_thumbnail(url=member.display_avatar)
                    if inter.guild.icon is not None:
                        embed.set_footer(text="🦋", icon_url=inter.guild.icon)
                    else:
                        embed.set_footer(text="🦋")
                    types = {
                        "BanW": "Серверное предупреждение",
                        "BanM": "Серверное наказание",
                        "VoiceW": "Голосовое предупреждение",
                        "VoiceM": "Голосовое наказание",
                        "TextW": "Текстовое предупреждение",
                        "TextM": "Текстовое наказание"
                    }
                    punishments = (await collection.find_one({"id": member.id}))['punishments']   
                    if not punishments:
                        embed.description = "⠀\n> У пользователя нету наказаний!"
                        await inter.send(embed=embed, ephemeral=True)
                        return 
                        
                    embed.set_author(name=f"История наказаний {member}")
                    embeds = []
                    punishments.reverse()

                    separation_sort = lambda lst, sz: [lst[element:element + sz] for element in range(0, len(lst), sz)]
                    documents_sorted = separation_sort(punishments, 5)

                    for i in documents_sorted:
                        emb = sweetness.Embed()
                        emb.color = 0x2f3136 
                        emb.set_author(name=f"История наказаний {member}")
                        emb.set_thumbnail(url=member.display_avatar)
                        if inter.guild.icon is not None:
                            emb.set_footer(text="🦋 SweetNess", icon_url=inter.guild.icon)
                        else:
                            emb.set_footer(text="🦋 SweetNess")
                            
                        for doc in i:
                            value = f"Модератор: <@{doc['moderator']}>\nПричина: **{doc['reason']}**\nДата выдачи: <t:{int(doc['data_issue'].timestamp())}:D>"
                            if 'date_expired' in doc:
                                value +=f"\nДата окончания: <t:{int(doc['date_expired'].timestamp())}:D>"
                                
                            emb.add_field(name=types[doc['type']], value=value, inline=False)
                            
                        if doc == i[-1]:
                            embeds.append(emb)
                        
                    await inter.send(embed=embeds[0], view=Menu(embeds), ephemeral=True)
            else:
                emb = sweetness.Embed()
                emb.description = f"> Вы не можете просматривать историю нарушений бота!"
                await inter.send(embed=emb, ephemeral=True)


def setup(client):
    client.add_cog(History(client))             