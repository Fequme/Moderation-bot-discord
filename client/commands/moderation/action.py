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

# Connecting DB

mongo = config.SWEETNESS['MONGO']
cluster = MotorClient(mongo)
collection = cluster.sweetness.users
staff = cluster.sweetness.staff
warns = cluster.sweetness.warns

# Convert time

def convert_str(seconds: int) -> str:
    if seconds < 60:
        return "%sсек." % seconds
    minutes, _ = divmod(seconds, 60)
    return "%s мин." % (minutes)

class OneSeven(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message

        super().__init__(timeout=None)

    @sweetness.ui.button(label="Бан роль", style=sweetness.ButtonStyle.grey)
    async def banrole(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        if role is not None:
            try:
                await self.member.add_roles(role)
            except:
                pass 
        else:
            print("I can't find ban mute role???")

        date = (datetime.datetime.now() + datetime.timedelta(seconds=365 * 86400))

        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"TOS", "moderator": interaction.user.id}}})
        await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{convert_str(365 * 86400)}**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n {convert_str(365 * 86400)} \n```")
        lembed.add_field(name="Причина :", value=f"```\n 1.7 \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

    @sweetness.ui.button(label="Пермаментный бан", style=sweetness.ButtonStyle.grey)
    async def permbannnnn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        await self.member.ban(reason="1.7")

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**."
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n Навсегда \n```")
        lembed.add_field(name="Причина :", value=f"```\n 1.7 \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)


class BackButton(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message

        super().__init__(timeout=None)

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backbbb(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))


class TextButtons(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message 

        super().__init__(timeout=None)

    async def checkmember(self, member: sweetness.Member):
        if await collection.find_one({"id": member.id}) is None:
            await collection.insert_one({
                "id": member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })

    async def checkstaff(self, member: sweetness.Member):
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

    async def givewarn(self, member: sweetness.Member, secondss: int):
        date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
        await warns.insert_one({
            "id": member.id,
            "type": "text",
            "warn": secondss,
            "time": date
        })

    async def givevoicewarn(self, member: sweetness.Member, secondss: int):
        date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
        await warns.insert_one({
            "id": member.id,
            "type": "voice",
            "warn": secondss,
            "time": date
        })

    @sweetness.ui.button(label="3.1", style=sweetness.ButtonStyle.grey)
    async def three_one(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 7200
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))
        

        if await warns.find_one({"id": self.member.id, "type": "text"}) is None:
            await self.givewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_warns": 1}})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано текстовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            memberdata = await collection.find_one({"id": self.member.id})
            oldtext = memberdata['oldtext']
            if oldtext is None:
                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_mutes": 1}})

                memberdoc = await warns.find_one({"id": self.member.id, "type": "text"})
                prewarn = memberdoc['warn']
                preresult = int(prewarn) + warntime 
                result = preresult / 2
                converted = convert_str(result)

                membed = sweetness.Embed()
                membed.color = 0x2f3136
                membed.set_thumbnail(url=interaction.author.display_avatar)
                membed.set_author(name="Вам был выдан текстовый мут", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
                membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                membed.timestamp = datetime.datetime.now()
                membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                try:
                    await self.member.send(embed=membed)
                except:
                    pass

                role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE'])
                if role is not None:
                    try:
                        await self.member.add_roles(role)
                    except:
                        pass 
                else:
                    print("I can't find text mute role???")

                role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
                if role2 is not None:
                    try:
                        await self.member.remove_roles(role2)
                    except:
                        pass 
                else:
                    print("I can't find text warn role???")

                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = f"> Пользователю {self.member.mention} был выдан текстовый мут на **{converted}**"
                await self.message.edit(embed=embed, view=None)

                myobject = config.SWEETNESS['MOD_LOGS']
                channel = self.client.get_channel(int(myobject))
                lembed = sweetness.Embed()
                lembed.color = 0x2f3136
                lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                lembed.set_author(name="Выдача текстового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
                lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
                lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                lembed.add_field(name="Причина :", value=f"```\n {button.label}\n```")
                lembed.timestamp = datetime.datetime.now()
                lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
                await channel.send(embed=lembed)

                date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

                if await warns.find_one({"id": self.member.id, "type": "text"}) is not None:
                    await warns.delete_one({"id": self.member.id, "type": "text"})
                await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
                await collection.update_one({"id": self.member.id}, {"$set": {"text": date, "oldtext": "3.1"}})
            else:
                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"bans": 1}})

                converted = convert_str(14*86400)

                membed = sweetness.Embed()
                membed.color = 0x2f3136
                membed.set_thumbnail(url=interaction.author.display_avatar)
                membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532719738040341/4021693.png")
                membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
                membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                membed.timestamp = datetime.datetime.now()
                membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                try:
                    await self.member.send(embed=membed)
                except:
                    pass

                role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
                if role is not None:
                    try:
                        await self.member.add_roles(role)
                    except:
                        pass 
                else:
                    print("I can't find text mute role???")

                role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
                if role2 is not None:
                    try:
                        await self.member.remove_roles(role2)
                    except:
                        pass 
                else:
                    print("I can't find text warn role???")

                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{converted}**"
                await self.message.edit(embed=embed, view=None)

                myobject = config.SWEETNESS['MOD_LOGS']
                channel = self.client.get_channel(int(myobject))
                lembed = sweetness.Embed()
                lembed.color = 0x2f3136
                lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                lembed.set_author(name="Выдача бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
                lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
                lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                lembed.add_field(name="Причина :", value=f"```\n {button.label}\n```")
                lembed.timestamp = datetime.datetime.now()
                lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
                await channel.send(embed=lembed)

                date = (datetime.datetime.now() + datetime.timedelta(seconds=14*86400))

                if await warns.find_one({"id": self.member.id, "type": "text"}) is not None:
                    await warns.delete_one({"id": self.member.id, "type": "text"})
                await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
                await collection.update_one({"id": self.member.id}, {"$set": {"ban": date, "oldtext": None}})

    @sweetness.ui.button(label="3.2", style=sweetness.ButtonStyle.grey)
    async def three_two(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 2400
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))
        

        if await warns.find_one({"id": self.member.id, "type": "text"}) is None:
            await self.givewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_warns": 1}})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано текстовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_mutes": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "text"})
            prewarn = memberdoc['warn']
            preresult = int(prewarn) + warntime 
            result = preresult / 2
            converted = convert_str(result)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан текстовый мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532719738040341/4021693.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} был выдан текстовый мут на **{converted}**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label}\n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "text"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "text"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"text": date}})

    @sweetness.ui.button(label="3.3", style=sweetness.ButtonStyle.grey)
    async def three_threeeeeee(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 1200
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))
        

        if await warns.find_one({"id": self.member.id, "type": "text"}) is None:
            await self.givewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_warns": 1}})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано текстовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_mutes": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "text"})
            prewarn = memberdoc['warn']
            preresult = int(prewarn) + warntime 
            result = preresult / 2
            converted = convert_str(result)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан текстовый мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532719738040341/4021693.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} был выдан текстовый мут на **{converted}**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label}\n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "text"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "text"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"text": date}})

    @sweetness.ui.button(label="3.4", style=sweetness.ButtonStyle.grey)
    async def three_threefour(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 2400
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))
        

        if await warns.find_one({"id": self.member.id, "type": "text"}) is None:
            await self.givewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_warns": 1}})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано текстовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"text_mutes": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "text"})
            prewarn = memberdoc['warn']
            preresult = int(prewarn) + warntime 
            result = preresult / 2
            converted = convert_str(result)

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан текстовый мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532719738040341/4021693.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png1")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} был выдан текстовый мут на **{converted}**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача текстового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label}\n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "text"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "text"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "TextM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"text": date}})

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backwarns(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

class VoiceButtons(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message 

        super().__init__(timeout=None)

    async def checkmember(self, member: sweetness.Member):
        if await collection.find_one({"id": member.id}) is None:
            await collection.insert_one({
                "id": member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })

    async def checkstaff(self, member: sweetness.Member):
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

    async def givewarn(self, member: sweetness.Member, secondss: int):
        date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
        await warns.insert_one({
            "id": member.id,
            "type": "text",
            "warn": secondss,
            "time": date
        })

    async def givevoicewarn(self, member: sweetness.Member, secondss: int):
        date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
        await warns.insert_one({
            "id": member.id,
            "type": "voice",
            "warn": secondss,
            "time": date
        })

    @sweetness.ui.button(label="2.1", style=sweetness.ButtonStyle.grey)
    async def two_one_v(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 7200
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))
        memberdddd = await collection.find_one({"id": self.member.id})
        oldvoice = memberdddd['oldvoice']
        
        if await warns.find_one({"id": self.member.id, "type": "voice"}) is None:
            await self.givevoicewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано голосовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            if oldvoice is None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_mutes": 1}})

                memberdoc = await warns.find_one({"id": self.member.id, "type": "voice"})
                prewarn = memberdoc['warn']
                preresult = int(prewarn) + warntime 
                result = preresult / 2
                converted = convert_str(result)
            
                await self.member.move_to(None)
                membed = sweetness.Embed()
                membed.color = 0x2f3136
                membed.set_thumbnail(url=interaction.author.display_avatar)
                membed.set_author(name="Вам был выдан голосовой мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532805461225532/1680177.png")
                membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
                membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                membed.timestamp = datetime.datetime.now()
                membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                try:
                    await self.member.send(embed=membed)
                except:
                    pass

                role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE'])
                if role is not None:
                    try:
                        await self.member.add_roles(role)
                    except:
                        pass 
                else:
                    print("I can't find text mute role???")

                role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
                if role2 is not None:
                    try:
                        await self.member.remove_roles(role2)
                    except:
                        pass 
                else:
                    print("I can't find text warn role???")

                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = f"> Пользователю {self.member.mention} был выдан голосовой мут на **{converted}**"
                await self.message.edit(embed=embed, view=None)

                myobject = config.SWEETNESS['MOD_LOGS']
                channel = self.client.get_channel(int(myobject))
                lembed = sweetness.Embed()
                lembed.color = 0x2f3136
                lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                lembed.set_author(name="Выдача голосового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
                lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
                lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                lembed.timestamp = datetime.datetime.now()
                lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
                await channel.send(embed=lembed)

                date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

                if await warns.find_one({"id": self.member.id, "type": "voice"}) is not None:
                    await warns.delete_one({"id": self.member.id, "type": "voice"})
                await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
                await collection.update_one({"id": self.member.id}, {"$set": {"voice": date, "oldvoice": "2.1"}})
            else:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"bans": 1}})

                memberdoc = await warns.find_one({"id": self.member.id, "type": "voice"})
                converted = convert_str(14 * 86400)
            
                await self.member.move_to(None)
                membed = sweetness.Embed()
                membed.color = 0x2f3136
                membed.set_thumbnail(url=interaction.author.display_avatar)
                membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532805461225532/1680177.png")
                membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
                membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                membed.add_field(name="Причина :", value=f"```\n 2.1 \n```")
                membed.timestamp = datetime.datetime.now()
                membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                try:
                    await self.member.send(embed=membed)
                except:
                    pass

                role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
                if role is not None:
                    try:
                        await self.member.add_roles(role)
                    except:
                        pass 
                else:
                    print("I can't find text mute role???")

                role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
                if role2 is not None:
                    try:
                        await self.member.remove_roles(role2)
                    except:
                        pass 
                else:
                    print("I can't find text warn role???")

                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{converted}**"
                await self.message.edit(embed=embed, view=None)

                myobject = config.SWEETNESS['MOD_LOGS']
                channel = self.client.get_channel(int(myobject))
                lembed = sweetness.Embed()
                lembed.color = 0x2f3136
                lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
                lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
                lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                lembed.add_field(name="Причина :", value=f"```\n 2.1 \n```")
                lembed.timestamp = datetime.datetime.now()
                lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
                await channel.send(embed=lembed)

                date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

                if await warns.find_one({"id": self.member.id, "type": "voice"}) is not None:
                    await warns.delete_one({"id": self.member.id, "type": "voice"})
                await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"2.1", "moderator": interaction.user.id}}})
                await collection.update_one({"id": self.member.id}, {"$set": {"ban": date, "oldvoice": None}})         

    @sweetness.ui.button(label="2.2", style=sweetness.ButtonStyle.grey)
    async def two_tww_v(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 2400
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))

        if await warns.find_one({"id": self.member.id, "type": "voice"}) is None:
            await self.givevoicewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано голосовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋 Unique", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_mutes": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "voice"})
            prewarn = memberdoc['warn']
            preresult = int(prewarn) + warntime 
            result = preresult / 2
            converted = convert_str(result)
           
            await self.member.move_to(None)
            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан голосовой мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532805461225532/1680177.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} был выдан голосовой мут на **{converted}**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "voice"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "voice"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"voice": date}})

    @sweetness.ui.button(label="2.3", style=sweetness.ButtonStyle.grey)
    async def two_three_v(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 3600
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))

        if await warns.find_one({"id": self.member.id, "type": "voice"}) is None:
            await self.givevoicewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано голосовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_mutes": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "voice"})
            prewarn = memberdoc['warn']
            preresult = int(prewarn) + warntime 
            result = preresult / 2
            converted = convert_str(result)
           
            await self.member.move_to(None)
            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан голосовой мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532805461225532/1680177.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} был выдан голосовой мут на **{converted}**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "voice"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "voice"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"voice": date}})

    @sweetness.ui.button(label="2.4", style=sweetness.ButtonStyle.grey)
    async def two_ffff_v(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        warntime = 1200
        await self.checkmember(self.member)
        await self.checkstaff(interaction.author)
        date = (datetime.datetime.now() + datetime.timedelta(seconds=warntime))

        if await warns.find_one({"id": self.member.id, "type": "voice"}) is None:
            await self.givevoicewarn(self.member, warntime)
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано голосовое предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {convert_str(warntime)} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋 Unique", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            await staff.update_one({"id": interaction.author.id}, {"$inc": {"voice_mutes": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "voice"})
            prewarn = memberdoc['warn']
            preresult = int(prewarn) + warntime 
            result = preresult / 2
            converted = convert_str(result)
           
            await self.member.move_to(None)
            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан голосовой мут", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532805461225532/1680177.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} был выдан голосовой мут на **{converted}**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача голосового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "voice"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "voice"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "VoiceM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"voice": date}})    

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backvoice(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

# Ban Buttons

class BanButtons(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message 

        super().__init__(timeout=None)

    @sweetness.ui.button(label="1.1", style=sweetness.ButtonStyle.grey)
    async def one_one_b(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        await self.member.move_to(None)
        membed = sweetness.Embed()
        membed.color = 0x2f3136
        membed.set_thumbnail(url=interaction.author.display_avatar)
        membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532878421143563/3119346.png")
        membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
        membed.add_field(name="Длительность :", value="```\nнавсегда\n```")
        membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
        membed.timestamp = datetime.datetime.now()
        membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        try:
            await self.member.send(embed=membed)
        except:
            pass


        await self.member.ban(reason=button.label)

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
        lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

        date = (datetime.datetime.now() + datetime.timedelta(seconds=999999999999))

        if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
            await warns.delete_one({"id": self.member.id, "type": "ban"})
        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": "1.1", "moderator": interaction.user.id}}})

    @sweetness.ui.button(label="1.2", style=sweetness.ButtonStyle.grey)
    async def one_twww_b(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        membed = sweetness.Embed()
        membed.color = 0x2f3136
        membed.set_thumbnail(url=interaction.author.display_avatar)
        membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532878421143563/3119346.png")
        membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
        membed.add_field(name="Длительность :", value="```\nнавсегда\n```")
        membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
        membed.timestamp = datetime.datetime.now()
        membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        try:
            await self.member.send(embed=membed)
        except:
            pass


        await self.member.ban(reason=button.label)

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
        lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

        date = (datetime.datetime.now() + datetime.timedelta(seconds=999999999999))

        if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
            await warns.delete_one({"id": self.member.id, "type": "ban"})
        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": "1.1", "moderator": interaction.user.id}}})

    @sweetness.ui.button(label="1.3", style=sweetness.ButtonStyle.grey)
    async def one_thhhh_b(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        membed = sweetness.Embed()
        membed.color = 0x2f3136
        membed.set_thumbnail(url=interaction.author.display_avatar)
        membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1064532878421143563/3119346.png")
        membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
        membed.add_field(name="Длительность :", value="```\nнавсегда\n```")
        membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
        membed.timestamp = datetime.datetime.now()
        membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        try:
            await self.member.send(embed=membed)
        except:
            pass


        await self.member.ban(reason=button.label)

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
        lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

        date = (datetime.datetime.now() + datetime.timedelta(seconds=999999999999))

        if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
            await warns.delete_one({"id": self.member.id, "type": "ban"})
        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": "1.1", "moderator": interaction.user.id}}})

    @sweetness.ui.button(label="1.4", style=sweetness.ButtonStyle.grey)
    async def pne_four_tttttt(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        if await warns.find_one({"id": self.member.id, "type": "ban"}) is None:
            date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
            await warns.insert_one({
                "id": self.member.id,
                "type": "ban",
                "warn": 14 * 86400,
                "time": date
            })

            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"ban_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано серверное предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n 60 минут \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋 Unique", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача серверного предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            mmmmmmdata = await collection.find_one({"id": self.member.id})
            oldvoice2 = mmmmmmdata['oldvoice2']
            if oldvoice2 is None:
                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"bans": 1}})

                memberdoc = await warns.find_one({"id": self.member.id, "type": "ban"})
                prewarn = memberdoc['warn']
                days14 = 14 * 86400
                preresult = int(prewarn) + days14
                result = preresult / 2
                converted = convert_str(result)

                await self.member.move_to(None)
                membed = sweetness.Embed()
                membed.color = 0x2f3136
                membed.set_thumbnail(url=interaction.author.display_avatar)
                membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100286005299/3119346.png")
                membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
                if not result > 9999999:
                    membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                else:
                    membed.add_field(name="Длительность :", value="```\nнавсегда\n```")
                membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                membed.timestamp = datetime.datetime.now()
                membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                try:
                    await self.member.send(embed=membed)
                except:
                    pass

                role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
                if role is not None:
                    try:
                        await self.member.add_roles(role)
                    except:
                        pass 
                else:
                    print("I can't find ban mute role???")

                role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
                if role2 is not None:
                    try:
                        await self.member.remove_roles(role2)
                    except:
                        pass 
                else:
                    print("I can't find ban warn role???")

                embed = sweetness.Embed()
                embed.color = 0x2f3136
                if not result > 9999999:
                    embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{converted}**"
                else:
                    embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
                await self.message.edit(embed=embed, view=None)

                myobject = config.SWEETNESS['MOD_LOGS']
                channel = self.client.get_channel(int(myobject))
                lembed = sweetness.Embed()
                lembed.color = 0x2f3136
                lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
                lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
                if not result > 9999999:
                    lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
                else:
                    lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
                lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                lembed.timestamp = datetime.datetime.now()
                lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
                await channel.send(embed=lembed)

                date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

                if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
                    await warns.delete_one({"id": self.member.id, "type": "ban"})
                await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
                await collection.update_one({"id": self.member.id}, {"$set": {"ban": date, "oldvoice2": "1.4"}})
            else:
                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"bans": 1}})

                await self.member.move_to(None)
                membed = sweetness.Embed()
                membed.color = 0x2f3136
                membed.set_thumbnail(url=interaction.author.display_avatar)
                membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100286005299/3119346.png")
                membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
                membed.add_field(name="Длительность :", value="```\nнавсегда\n```")
                membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                membed.timestamp = datetime.datetime.now()
                membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                try:
                    await self.member.send(embed=membed)
                except:
                    pass

                await self.member.ban(reason="1.4")

                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
                await self.message.edit(embed=embed, view=None)

                myobject = config.SWEETNESS['MOD_LOGS']
                channel = self.client.get_channel(int(myobject))
                lembed = sweetness.Embed()
                lembed.color = 0x2f3136
                lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
                lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
                lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
                lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
                lembed.timestamp = datetime.datetime.now()
                lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
                await channel.send(embed=lembed)

                date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

                if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
                    await warns.delete_one({"id": self.member.id, "type": "ban"})
                await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"1.4", "moderator": interaction.user.id}}})
                await collection.update_one({"id": self.member.id}, {"$set": {"ban": date, "oldvoice2": None}})

    @sweetness.ui.button(label="1.5", style=sweetness.ButtonStyle.grey)
    async def two_one_b(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        if await warns.find_one({"id": self.member.id, "type": "ban"}) is None:
            date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
            await warns.insert_one({
                "id": self.member.id,
                "type": "ban",
                "warn": 14 * 86400,
                "time": date
            })

            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"ban_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано серверное предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n 60 минут \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋 Unique", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача серверного предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"bans": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "ban"})
            prewarn = memberdoc['warn']
            days14 = 14 * 86400
            preresult = int(prewarn) + days14
            result = preresult / 2
            converted = convert_str(result)

            await self.member.move_to(None)
            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100286005299/3119346.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            if not result > 9999999:
                membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            else:
                membed.add_field(name="Длительность :", value="```\nнавсегда\n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find ban mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find ban warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            if not result > 9999999:
                embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{converted}**"
            else:
                embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            if not result > 9999999:
                lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            else:
                lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "ban"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

    @sweetness.ui.button(label="1.5", style=sweetness.ButtonStyle.grey)
    async def two_one_b(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        if await warns.find_one({"id": self.member.id, "type": "ban"}) is None:
            date = (datetime.datetime.now() + datetime.timedelta(seconds=3600))
            await warns.insert_one({
                "id": self.member.id,
                "type": "ban",
                "warn": 7 * 86400,
                "time": date
            })

            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"ban_warns": 1}})

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = f"> Пользователю {self.member.mention} успешно было выдано предупреждение по причине **` {button.label} `** (Пункт правил)."
            await self.message.edit(embed=embed, view=None)
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanW", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})

            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам было выдано серверное предупреждение", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            membed.add_field(name="Кем выдано :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            membed.add_field(name="Длительность :", value=f"```\n 60 минут \n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text="🦋 Unique", icon_url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find text warn role???")

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача серверного предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id}```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)
        else:
            if await staff.find_one({"id": interaction.author.id}) is not None:
                await staff.update_one({"id": interaction.author.id}, {"$inc": {"bans": 1}})

            memberdoc = await warns.find_one({"id": self.member.id, "type": "ban"})
            prewarn = memberdoc['warn']
            days14 = 7 * 86400
            preresult = int(prewarn) + days14
            result = preresult / 2
            converted = convert_str(result)

            await self.member.move_to(None)
            membed = sweetness.Embed()
            membed.color = 0x2f3136
            membed.set_thumbnail(url=interaction.author.display_avatar)
            membed.set_author(name="Вам был выдан бан", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100286005299/3119346.png")
            membed.add_field(name="Кем выдан :", value=f"```\n{interaction.author}\n{interaction.author.id}```")
            if not result > 9999999:
                membed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            else:
                membed.add_field(name="Длительность :", value="```\nНавсегда\n```")
            membed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            membed.timestamp = datetime.datetime.now()
            membed.set_footer(text=f"🦋 Выдал - {interaction.author} ", icon_url="https://media.discordapp.net/attachments/1096423396893544448/1100394033563578479/a_431a3be54fc30406c87de2ee9ef23d97.gif?width=281&height=281")
            try:
                await self.member.send(embed=membed)
            except:
                pass

            role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
            if role is not None:
                try:
                    await self.member.add_roles(role)
                except:
                    pass 
            else:
                print("I can't find ban mute role???")

            role2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
            if role2 is not None:
                try:
                    await self.member.remove_roles(role2)
                except:
                    pass 
            else:
                print("I can't find ban warn role???")

            embed = sweetness.Embed()
            embed.color = 0x2f3136
            if not result > 9999999:
                embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{converted}**"
            else:
                embed.description = f"> Пользователю {self.member.mention} был выдан бан **навсегда**"
            await self.message.edit(embed=embed, view=None)

            myobject = config.SWEETNESS['MOD_LOGS']
            channel = self.client.get_channel(int(myobject))
            lembed = sweetness.Embed()
            lembed.color = 0x2f3136
            lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
            lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
            lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
            if not result > 9999999:
                lembed.add_field(name="Длительность :", value=f"```\n {converted} \n```")
            else:
                lembed.add_field(name="Длительность :", value="```\nНавсегда\n```")
            lembed.add_field(name="Причина :", value=f"```\n {button.label} \n```")
            lembed.timestamp = datetime.datetime.now()
            lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
            await channel.send(embed=lembed)

            date = (datetime.datetime.now() + datetime.timedelta(seconds=result))

            if await warns.find_one({"id": self.member.id, "type": "ban"}) is not None:
                await warns.delete_one({"id": self.member.id, "type": "ban"})
            await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"{button.label}", "moderator": interaction.user.id}}})
            await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

    @sweetness.ui.button(label="1.7", style=sweetness.ButtonStyle.grey)
    async def one_seveeneearara(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Модерационная панель")
        embed.set_thumbnail(url=interaction.author.display_avatar)
        embed.color = 0x2f3136
        embed.description = f"> Выберите какой вид бана, хотите выдать пользователю :"
        await self.message.edit(embed=embed, view=OneSeven(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backban(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

# Unwarn Modal

class RemoveWModal(sweetness.ui.Modal):
    def __init__(self, client, member: sweetness.Member, message, type) -> None:
        self.client = client 
        self.member = member
        self.message = message 
        self.type = type

        components = [
            sweetness.ui.TextInput(
                label = "Причина",
                placeholder = "Причина по которой вы хотите снять предупреждение",
                custom_id = "reason",
                style = sweetness.TextInputStyle.short,
                min_length = 10,
                max_length = 50
            ),
        ]
        super().__init__(title="Снятие предупреждения", custom_id="remove_push", components=components)

    async def callback(self, inter: sweetness.ModalInteraction) -> None:
        embed = sweetness.Embed()
        if self.type == "text":
            embed.set_author(name="Снятие текстового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
        if self.type == "voice":
            embed.set_author(name="Снятие голосового предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
        if self.type == "ban":
            embed.set_author(name="Снятие серверного предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
        
        channel = self.client.get_channel(config.SWEETNESS['MOD_LOGS'])

        embed.color = 0x2f3136 
        embed.add_field(name=f"Кому сняли :", value=f"```\n{self.member} \n {self.member.id}```")
        embed.add_field(name=f"Причина снятия :", value=f"```\n{inter.text_values['reason']}```")
        embed.set_footer(text=f"Снял - {inter.author}", icon_url=inter.author.display_avatar)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)

        if self.type == "text":
            role = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])
        if self.type == "voice":
            role = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])
        if self.type == "ban":
            role = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])
        
        await self.member.remove_roles(role)
        adminembed = sweetness.Embed()
        adminembed.color = 0x2f3136 
        adminembed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
         
        if await warns.find_one({"id": self.member.id}) is not None:
            if self.type == "text":
                await warns.delete_one({"id": self.member.id, "type": "text"})
            if self.type == "voice":
                await warns.delete_one({"id": self.member.id, "type": "voice"})
            if self.type == "ban":
                await warns.delete_one({"id": self.member.id, "type": "ban"})

        if self.type == "text":
            adminembed.description = f"> Пользователю {self.member.mention} был снято текстовое предупреждение."
        if self.type == "voice":
            adminembed.description = f"> Пользователю {self.member.mention} был снято голосовое предупреждение."
        if self.type == "ban":
            adminembed.description = f"> Пользователю {self.member.mention} был снято серверное предупреждение."
        
        await self.message.edit(embed=adminembed, view=None)
    
        memberembed = sweetness.Embed()
        memberembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        if self.type == "text":
            memberembed.set_author(name="Текстовое предупреждение было снято", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        if self.type == "voice":
            memberembed.set_author(name="Голосовое предупреждение было снято", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        if self.type == "ban":
            memberembed.set_author(name="Серверное предупреждение было снято", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        
        memberembed.color = 0x2f3136 
        memberembed.description = "> Наша модерация приносит вам свои извинения за неправильную выдачу предупреждения."
        memberembed.set_footer(text=f"Снял - {inter.author}", icon_url=inter.author.display_avatar)
        try:
            await inter.send("")
        except:
            pass
        
        try:
            await self.member.send(embed=memberembed)
        except:
            pass 


# UnWarn Buttonns

class UnWarn(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message
    
        super().__init__(timeout=None)

    @sweetness.ui.button(label="Текст", style=sweetness.ButtonStyle.grey, custom_id="text_unwarn")
    async def textunwarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        text = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['TEXT_WARN'])

        if text in self.member.roles:
            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
            embed.description = "ᅠ\n> Укажите причину по которой нужно снять предупреждение ( У вас открылось окно )"
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
            await interaction.response.send_modal(RemoveWModal(client=self.client, member=self.member, message=self.message, type="text"))
        else:
            try:
                await interaction.send("")
            except:
                pass

            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
            embed.description = f"> У пользователя {self.member.mention} нет текстового предупреждения."
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))



    @sweetness.ui.button(label="Войс", style=sweetness.ButtonStyle.grey, custom_id="voice_unwarn")
    async def voiceunwarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        voice = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['VOICE_WARN'])

        if voice in self.member.roles:
            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
            embed.description = "> Укажите причину по которой нужно снять предупреждение ( У вас открылось окно )"
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
            await interaction.response.send_modal(RemoveWModal(client=self.client, member=self.member, message=self.message, type="voice"))
        else:
            try:
                await interaction.send("")
            except:
                pass

            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
            embed.description = f"> У пользователя {self.member.mention} нет голосового предупреждения."
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))



    @sweetness.ui.button(label="Бан", style=sweetness.ButtonStyle.grey, custom_id="ban_unwarn")
    async def banunwarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        ban = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['TIME_ROLES']['BAN_WARN'])

        if ban in self.member.roles:
            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
            embed.description = "ᅠ\n> Укажите причину по которой нужно снять предупреждение ( У вас открылось окно )"
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
            await interaction.response.send_modal(RemoveWModal(client=self.client, member=self.member, message=self.message, type="ban"))
        else:
            try:
                await interaction.send("")
            except:
                pass

            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
            embed.description = f"ᅠ\n> У пользователя {self.member.mention} нет серверного предупреждения."
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))


    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backu(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

# Helper Buttons

class HWarn(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message
    
        super().__init__(timeout=None)

    @sweetness.ui.button(label="Текст", style=sweetness.ButtonStyle.grey)
    async def textwarnh(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        document = await collection.find_one({"id": self.member.id})
        text = document['text']
        if text is None:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.set_author(name="Выдача предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.set_footer(text=f"Взаимодействие с пользователем - {self.member.name}", icon_url=self.member.display_avatar)
            embed.description = "> Выберите пункт правил, которое нарушил пользователь"
            await self.message.edit(embed=embed, view=TextButtons(client=self.client, member=self.member, message=self.message))
        else:
            embed2 = sweetness.Embed()
            embed2.color = 0x2f3136
            embed2.description = f"> Вы не можете выдать пользователю {self.member.mention} текстовое предупреждение, так как он уже получил текстовый мут."
            await self.message.edit(embed=embed2, view=BackButton(client=self.client, member=self.member, message=self.message))


    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backh(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))


# Tos Buttons

class TosBanButtons(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message
    
        super().__init__(timeout=None)

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backbbbutooon(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="1 месяц", style=sweetness.ButtonStyle.grey)
    async def onemonth(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        if role is not None:
            try:
                await self.member.add_roles(role)
            except:
                pass 
        else:
            print("I can't find ban mute role???")

        date = (datetime.datetime.now() + datetime.timedelta(seconds=30 * 86400))

        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"TOS", "moderator": interaction.user.id}}})
        await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{convert_str(30 * 86400)}**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n {convert_str(30 * 86400)} \n```")
        lembed.add_field(name="Причина :", value=f"```\n ToS \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

    @sweetness.ui.button(label="3 месяцев", style=sweetness.ButtonStyle.grey)
    async def threemonth(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        if role is not None:
            try:
                await self.member.add_roles(role)
            except:
                pass 
        else:
            print("I can't find ban mute role???")

        date = (datetime.datetime.now() + datetime.timedelta(seconds=90 * 86400))

        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"TOS", "moderator": interaction.user.id}}})
        await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{convert_str(90 * 86400)}**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n {convert_str(90 * 86400)} \n```")
        lembed.add_field(name="Причина :", value=f"```\n ToS \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

    @sweetness.ui.button(label="5 месяцев", style=sweetness.ButtonStyle.grey)
    async def fivemonth(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        if role is not None:
            try:
                await self.member.add_roles(role)
            except:
                pass 
        else:
            print("I can't find ban mute role???")

        date = (datetime.datetime.now() + datetime.timedelta(seconds=150 * 86400))

        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"TOS", "moderator": interaction.user.id}}})
        await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{convert_str(150 * 86400)}**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n {convert_str(150 * 86400)} \n```")
        lembed.add_field(name="Причина :", value=f"```\n ToS \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

    @sweetness.ui.button(label="7 месяцев", style=sweetness.ButtonStyle.grey)
    async def sevenmonth(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        if role is not None:
            try:
                await self.member.add_roles(role)
            except:
                pass 
        else:
            print("I can't find ban mute role???")

        date = (datetime.datetime.now() + datetime.timedelta(seconds=220 * 86400))

        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"TOS", "moderator": interaction.user.id}}})
        await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{convert_str(220 * 86400)}**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n {convert_str(220 * 86400)} \n```")
        lembed.add_field(name="Причина :", value=f"```\n ToS \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

    @sweetness.ui.button(label="12 месяцев", style=sweetness.ButtonStyle.grey)
    async def sevenmonth(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        role = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        if role is not None:
            try:
                await self.member.add_roles(role)
            except:
                pass 
        else:
            print("I can't find ban mute role???")

        date = (datetime.datetime.now() + datetime.timedelta(seconds=360 * 86400))

        await collection.update_one({"id": self.member.id}, {"$push": {"punishments": {"type": "BanM", "date_expired": date, "data_issue": datetime.datetime.now(), "reason": f"TOS", "moderator": interaction.user.id}}})
        await collection.update_one({"id": self.member.id}, {"$set": {"ban": date}})

        embed = sweetness.Embed()
        embed.color = 0x2f3136
        embed.description = f"> Пользователю {self.member.mention} был выдан бан на **{convert_str(360 * 86400)}**"
        await self.message.edit(embed=embed, view=None)

        myobject = config.SWEETNESS['MOD_LOGS']
        channel = self.client.get_channel(int(myobject))
        lembed = sweetness.Embed()
        lembed.color = 0x2f3136
        lembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        lembed.set_author(name="Выдача бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691101267468328/4021693.png")
        lembed.add_field(name="Кому выдано :", value=f"```\n {self.member} \n {self.member.id} \n ```")
        lembed.add_field(name="Длительность :", value=f"```\n {convert_str(360 * 86400)} \n```")
        lembed.add_field(name="Причина :", value=f"```\n ToS \n```")
        lembed.timestamp = datetime.datetime.now()
        lembed.set_footer(text=f"🦋 Выдал - {interaction.author}", icon_url=interaction.author.display_avatar)
        await channel.send(embed=lembed)

# Warn Buttons

class Warn(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message
    
        super().__init__(timeout=None)

    @sweetness.ui.button(label="Текст", style=sweetness.ButtonStyle.grey)
    async def textwarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        document = await collection.find_one({"id": self.member.id})
        text = document['text']
        if text is None:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.set_author(name="Выдача предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.set_footer(text=f"Взаимодействие с пользователем - {self.member.name}", icon_url=self.member.display_avatar)
            embed.description = "> Выберите пункт правил, которое нарушил пользователь"
            await self.message.edit(embed=embed, view=TextButtons(client=self.client, member=self.member, message=self.message))
        else:
            embed2 = sweetness.Embed()
            embed2.color = 0x2f3136
            embed2.description = f"> Вы не можете выдать пользователю {self.member.mention} текстовое предупреждение, так как он уже получил текстовый мут."
            await self.message.edit(embed=embed2, view=BackButton(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="Войс", style=sweetness.ButtonStyle.grey)
    async def voicewarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        document = await collection.find_one({"id": self.member.id})
        voice = document['voice']
        if voice is None:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.set_author(name="Выдача предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.set_footer(text=f"Взаимодействие с пользователем - {self.member.name}", icon_url=self.member.display_avatar)
            embed.description = "> Выберите пункт правил, которое нарушил пользователь"
            await self.message.edit(embed=embed, view=VoiceButtons(client=self.client, member=self.member, message=self.message))
        else:
            embed2 = sweetness.Embed()
            embed2.color = 0x2f3136
            embed2.description = f"> Вы не можете выдать пользователю {self.member.mention} голосовое предупреждение, так как он уже получил голосовой мут."
            await self.message.edit(embed=embed2, view=BackButton(client=self.client, member=self.member, message=self.message))


    @sweetness.ui.button(label="Бан", style=sweetness.ButtonStyle.grey)
    async def banwarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        document = await collection.find_one({"id": self.member.id})
        ban = document['ban']
        if ban is None:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.set_author(name="Выдача предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.set_footer(text=f"Взаимодействие с пользователем - {self.member.name}", icon_url=self.member.display_avatar)
            embed.description = "> Выберите пункт правил, которое нарушил пользователь"
            await self.message.edit(embed=embed, view=BanButtons(client=self.client, member=self.member, message=self.message))
        else:
            embed2 = sweetness.Embed()
            embed2.color = 0x2f3136
            embed2.description = f"> Вы не можете выдать пользователю {self.member.mention} серверное предупреждение, так как он уже получил бан."
            await self.message.edit(embed=embed2, view=BackButton(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="TOS", style=sweetness.ButtonStyle.grey)
    async def toswarn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        if await collection.find_one({"id": self.member.id}) is None:
            await collection.insert_one({
                "id": self.member.id,
                "ban": None,
                "voice": None,
                "text": None,
                "oldtext": None,
                "oldtext2": None,
                "oldvoice": None,
                "oldvoice2": None,
                "warns": [],
                "punishments": []
            })
        
        if await staff.find_one({"id": interaction.author.id}) is None:
            await staff.insert_one({
                "id": interaction.author.id,
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
        
        document = await collection.find_one({"id": self.member.id})
        ban = document['ban']
        if ban is None:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.set_author(name="Выдача предупреждения", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.set_footer(text=f"Взаимодействие с пользователем - {self.member.name}", icon_url=self.member.display_avatar)
            embed.description = "> Выберите время, на которое пользователь будет отстранён от сервера :"
            await self.message.edit(embed=embed, view=TosBanButtons(client=self.client, member=self.member, message=self.message))
        else:
            embed2 = sweetness.Embed()
            embed2.color = 0x2f3136
            embed2.description = f"> Вы не можете выдать пользователю {self.member.mention} ToS бан, так как он уже получил бан."
            await self.message.edit(embed=embed2, view=BackButton(client=self.client, member=self.member, message=self.message))



    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def back(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

# Modal Reason

class RemovePModal(sweetness.ui.Modal):
    def __init__(self, client, member: sweetness.Member, message, type) -> None:
        self.client = client 
        self.member = member
        self.message = message 
        self.type = type

        components = [
            sweetness.ui.TextInput(
                label = "Причина",
                placeholder = "Причина по которой вы хотите снять наказание",
                custom_id = "reason",
                style = sweetness.TextInputStyle.short,
                min_length = 10,
                max_length = 50
            ),
        ]
        super().__init__(title="Снятие наказания", custom_id="remove_push", components=components)

    async def callback(self, inter: sweetness.ModalInteraction) -> None:
        embed = sweetness.Embed()
        if self.type == "text":
            embed.set_author(name="Снятие текстового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
        if self.type == "voice":
            embed.set_author(name="Снятие голосового мута", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
        if self.type == "ban":
            embed.set_author(name="Снятие бана", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691099870773288/1960087.png")
        
        channel = self.client.get_channel(config.SWEETNESS['MOD_LOGS'])

        embed.color = 0x2f3136 
        embed.add_field(name=f"Кому сняли :", value=f"```\n{self.member} \n {self.member.id}```")
        embed.add_field(name=f"Причина снятия :", value=f"```\n{inter.text_values['reason']}```")
        embed.set_footer(text=f"Снял - {inter.author}", icon_url=inter.author.display_avatar)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)

        if self.type == "text":
            role = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE'])
        if self.type == "voice":
            role = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE'])
        if self.type == "ban":
            role = sweetness.utils.get(inter.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])
        
        await self.member.remove_roles(role)
        adminembed = sweetness.Embed()
        adminembed.color = 0x2f3136 
        adminembed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
         
        if await collection.find_one({"id": self.member.id}) is not None:
            if self.type == "text":
                await collection.update_one({"id": self.member.id}, {"$set": {"text": None}})
            if self.type == "voice":
                await collection.update_one({"id": self.member.id}, {"$set": {"voice": None}})
            if self.type == "ban":
                await collection.update_one({"id": self.member.id}, {"$set": {"ban": None}})

        if self.type == "text":
            adminembed.description = f"> Пользователю {self.member.mention} был снят текстовый мут."
        if self.type == "voice":
            adminembed.description = f"> Пользователю {self.member.mention} был снят голосовой мут."
        if self.type == "ban":
            adminembed.description = f"> Пользователю {self.member.mention} был снят бан."
        
        await self.message.edit(embed=adminembed, view=None)
    
        memberembed = sweetness.Embed()
        memberembed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
        if self.type == "text":
            memberembed.set_author(name="Текстовый мут был снят", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        if self.type == "voice":
            memberembed.set_author(name="Голосовой мут был снят", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        if self.type == "ban":
            memberembed.set_author(name="Бан был снят", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        
        memberembed.color = 0x2f3136 
        memberembed.description = "> Наша модерация приносит вам свои извинения за неправильную выдачу наказания."
        memberembed.set_footer(text=f"Снял - {inter.author}", icon_url=inter.author.display_avatar)
        try:
            await inter.send("")
        except:
            pass
        
        try:
            await self.member.send(embed=memberembed)
        except:
            pass 



# Remove Punishments

class RemoveP(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client 
        self.member = member
        self.message = message

        super().__init__(timeout=None)

    @sweetness.ui.button(label="Текст", style=sweetness.ButtonStyle.grey, custom_id="text_unmute")
    async def textunmute(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        mute = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE'])

        if mute in self.member.roles:
            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
            embed.description = "> Укажите причину по которой нужно снять наказание ( У вас открылось окно )"
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
            await interaction.response.send_modal(RemovePModal(client=self.client, member=self.member, message=self.message, type="text"))
        else:
            try:
                await interaction.send("")
            except:
                pass

            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
            embed.description = f"> У пользователя {self.member.mention} нет текстового мута."
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="Войс", style=sweetness.ButtonStyle.grey, custom_id="voice_unmute")
    async def voiceunmute(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        voice = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE'])

        if voice in self.member.roles:
            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
            embed.description = "> Укажите причину по которой нужно снять наказание ( У вас открылось окно )"
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
            await interaction.response.send_modal(RemovePModal(client=self.client, member=self.member, message=self.message, type="voice"))
        else:
            try:
                await interaction.send("")
            except:
                pass

            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
            embed.description = f"> У пользователя {self.member.mention} нет голосового мута."
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="Бан", style=sweetness.ButtonStyle.grey, custom_id="ban_unmute")
    async def banunmute(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        ban = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['PUNISHMENT_ROLES']['BAN'])

        if ban in self.member.roles:
            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
            embed.description = "> Укажите причину по которой нужно снять наказание ( У вас открылось окно )"
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
            await interaction.response.send_modal(RemovePModal(client=self.client, member=self.member, message=self.message, type="ban"))
        else:
            try:
                await interaction.send("")
            except:
                pass

            embed = sweetness.Embed()
            embed.color = 0x2f3136 
            embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
            embed.description = f"> У пользователя {self.member.mention} нет бана."
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backre(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))


# Gender Roles

class GenderButtons(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client 
        self.member = member 
        self.message = message 

        super().__init__(timeout=None)

    @sweetness.ui.button(label="♀️", style=sweetness.ButtonStyle.grey)
    async def girl(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        female = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['GENDER_ROLES']['FEMALE'])
        male = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['GENDER_ROLES']['MALE'])        

        if female in self.member.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
            embed.description = f"> У пользователя {self.member.mention} уже имеется женская гендерная роль."
            embed.color = 0x2f3136  
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
        else:
            if male in self.member.roles:
                try:
                    await self.member.remove_roles(male)
                except:
                    pass 

                try:
                    await self.member.add_roles(female)
                except:
                    pass

                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"gender_change": 1}})

                embed = sweetness.Embed()
                embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
                embed.description = f"> Пользователю {self.member.mention} была выдана женская гендерная роль."
                embed.color = 0x2f3136  
                await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))                
            else:
                try:
                    await self.member.add_roles(female)
                except:
                    pass

                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"gender_give": 1}})

                embed = sweetness.Embed()
                embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
                embed.description = f"> Пользователю {self.member.mention} была выдана женская гендерная роль."
                embed.color = 0x2f3136  
                await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))                

    @sweetness.ui.button(label="♂️", style=sweetness.ButtonStyle.grey)
    async def boy(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        female = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['GENDER_ROLES']['FEMALE'])
        male = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['GENDER_ROLES']['MALE'])

        if male in self.member.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
            embed.description = f"> У пользователя {self.member.mention} уже имеется мужская гендерная роль."
            embed.color = 0x2f3136  
            await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))
        else:
            if female in self.member.roles:
                try:
                    await self.member.remove_roles(female)
                except:
                    pass 

                try:
                    await self.member.add_roles(male)
                except:
                    pass

                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"gender_change": 1}})

                embed = sweetness.Embed()
                embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
                embed.description = f"> Пользователю {self.member.mention} была выдана мужская гендерная роль."
                embed.color = 0x2f3136  
                await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))                
            else:
                try:
                    await self.member.add_roles(male)
                except:
                    pass

                if await staff.find_one({"id": interaction.author.id}) is not None:
                    await staff.update_one({"id": interaction.author.id}, {"$inc": {"gender_give": 1}})

                embed = sweetness.Embed()
                embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
                embed.description = f"> Пользователю {self.member.mention} была выдана мужская гендерная роль."
                embed.color = 0x2f3136  
                await self.message.edit(embed=embed, view=BackButton(client=self.client, member=self.member, message=self.message))   

    @sweetness.ui.button(emoji="🔙", style=sweetness.ButtonStyle.red)
    async def backgender(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])

        if r1 in interaction.author.roles:
            embed = sweetness.Embed()
            embed.set_author(name="Модерационная панель")
            embed.set_thumbnail(url=interaction.author.display_avatar)
            embed.color = 0x2f3136
            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
            await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if r2 in interaction.author.roles:
                embed = sweetness.Embed()
                embed.set_author(name="Модерационная панель")
                embed.set_thumbnail(url=interaction.author.display_avatar)
                embed.color = 0x2f3136
                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if r3 in interaction.author.roles:
                    embed = sweetness.Embed()
                    embed.set_author(name="Модерационная панель")
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                    await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles:
                    if r4 in interaction.author.roles:
                        embed = sweetness.Embed()
                        embed.set_author(name="Модерационная панель")
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                        await self.message.edit(embed=embed, view=Buttons(client=self.client, member=self.member, message=self.message))
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles:
                if not r3 in interaction.author.roles: 
                    if not r4 in interaction.author.roles:
                        if r5 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                            await self.message.edit(embed=embed, view=Warden(client=self.client, member=self.member, message=self.message))     
        if not r1 in interaction.author.roles:
            if not r2 in interaction.author.roles: 
                if not r3 in interaction.author.roles:
                    if not r4 in interaction.author.roles:
                        if not r5 in interaction.author.roles:
                            if r6 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {self.member.mention} нужно выбрать одну из операций указанных ниже."
                                await self.message.edit(embed=embed, view=Helper(client=self.client, member=self.member, message=self.message))

# Helper Panel

class Helper(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message

        super().__init__(timeout=None)
    
    @sweetness.ui.button(label="Выдача предупреждения", style=sweetness.ButtonStyle.grey)
    async def warnh(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Тип предупреждения", icon_url = "https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
        embed.description = "> Для того, чтобы выдать предупреждение, вам нужно выбрать тип предупреждения указаные ниже."
        embed.set_footer(text=f"Взаимодействие с пользователем - {self.member}", icon_url=self.member.display_avatar.url)
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=HWarn(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="Выдача / Смена гендерой роли", style=sweetness.ButtonStyle.grey, row=2)
    async def genderh(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
        embed.description = f"> Выберите гендерную роль, которую хотите выдать / сменить пользователю {self.member.mention}"
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=GenderButtons(client=self.client, member=self.member, message=self.message))

# Warden Panel

class Warden(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message

        super().__init__(timeout=None)

    @sweetness.ui.button(label="Выдача предупреждения", style=sweetness.ButtonStyle.grey)
    async def warnd(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Тип предупреждения", icon_url = "https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png")
        embed.description = "> Для того, чтобы выдать предупреждение, вам нужно выбрать тип предупреждения указаные ниже."
        embed.set_footer(text=f"Взаимодействие с пользователем - {self.member}", icon_url=self.member.display_avatar.url)
        embed.set_thumbnail(url=interaction.author.display_avatar)
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=Warn(client=self.client, member=self.member, message=self.message))

# SweetNess, Administrator, MWarden, MHelper panel

class Buttons(sweetness.ui.View):
    def __init__(self, client, member: sweetness.Member, message):
        self.client = client
        self.member = member 
        self.message = message

        super().__init__(timeout=None)

    @sweetness.ui.button(label="Выдача предупреждения", style=sweetness.ButtonStyle.grey)
    async def warn(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Тип предупреждения", icon_url='https://cdn.discordapp.com/attachments/1058100296590557266/1062691100973871145/3899594.png')
        embed.description = "> Для того, чтобы выдать предупреждение, вам нужно выбрать тип предупреждения указаные ниже."
        embed.set_footer(text=f"Взаимодействие с пользователем - {self.member}", icon_url=self.member.display_avatar.url)
        embed.set_thumbnail(url=interaction.author.display_avatar)
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=Warn(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="Снятие предупреждения", style=sweetness.ButtonStyle.grey)
    async def warnd(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Снятие предупреждения", icon_url = "https://cdn.discordapp.com/attachments/1058100296590557266/1062691296004808734/1484582.png")
        embed.description = "ᅠ\n> Выберите тип предупреждения, который хотите снять :"
        embed.set_footer(text=f"Взаимодействие с пользователем - {self.member}", icon_url=self.member.display_avatar.url)
        embed.set_thumbnail(url=interaction.author.display_avatar)
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=UnWarn(client=self.client, member=self.member, message=self.message))

    @sweetness.ui.button(label="Снятие наказания", style=sweetness.ButtonStyle.grey)
    async def unmute(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Снятие наказания", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232373018694/3115609.png")
        embed.description = "> Выберите тип наказания, который хотите снять."
        embed.set_footer(text=f"Взаимодействие с пользователем - {self.member}", icon_url=self.member.display_avatar.url)
        embed.set_thumbnail(url=interaction.author.display_avatar)
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=RemoveP(client=self.client, member=self.member, message=self.message))


    @sweetness.ui.button(label="Выдача / Смена гендерной роли", style=sweetness.ButtonStyle.grey, row=2)
    async def genderr(self, button: sweetness.ui.Button, interaction: sweetness.MessageInteraction):
        embed = sweetness.Embed()
        embed.set_author(name="Смена / Выдача гендерной роли", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062691232721154138/2517450.png")
        embed.description = f"> Выберите гендерную роль, которую хотите выдать / сменить пользователю {self.member.mention}"
        embed.color = 0x2f3136
        await self.message.edit(embed=embed, view=GenderButtons(client=self.client, member=self.member, message=self.message))

# Class

class Action(commands.Cog):
    def __init__(self, client):
        self.client = client 
        
        self.checkwarns.start()
        self.checkdocs.start()

    @tasks.loop(seconds=60)
    async def checkwarns(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(config.SWEETNESS['GUILD_ID'])
        async for document in warns.find({}):
            try:
                member = guild.get_member(document["id"])
                if member is None:
                    # member has left the guild or cannot be found
                    continue
                if document['time'] <= datetime.datetime.now():
                    type = document['type']
                    if type == "text":
                        await warns.delete_one({"id": document["id"]})
                        if await collection.find_one({"id": document["id"]}) is not None:
                            await collection.update_one({"id": document["id"]}, {"$set": {"text": None}})
                        role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['TIME_ROLES']['TEXT_WARN']))
                        if role is not None:
                            try:
                                await member.remove_roles(role)
                            except:
                                print(f"Can't remove text warn for {document['id']}")
                    if type == "voice":
                        await warns.delete_one({"id": document["id"]})
                        if await collection.find_one({"id": document["id"]}) is not None:
                            await collection.update_one({"id": document["id"]}, {"$set": {"voice": None}})
                        role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['TIME_ROLES']['VOICE_WARN']))
                        if role is not None:
                            try:
                                await member.remove_roles(role)
                            except:
                                print(f"Can't remove voice warn for {document['id']}")
                    if type == "ban":
                        await warns.delete_one({"id": document["id"]})
                        if await collection.find_one({"id": document["id"]}) is not None:
                            await collection.update_one({"id": document["id"]}, {"$set": {"ban": None}})
                        role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['TIME_ROLES']['BAN_WARN']))
                        if role is not None:
                            try:
                                await member.remove_roles(role)
                            except:
                                print(f"Can't remove ban warn for {document['id']}")
            except Exception as e:
                print(e)
                print("??? [CHECK-WARNS]")

    @tasks.loop(seconds=60)
    async def checkdocs(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(config.SWEETNESS['GUILD_ID'])
        async for document in collection.find({}):
            try:
                if document['text'] is not None and document['text'] <= datetime.datetime.now():
                    await collection.update_one({"id": document["id"]}, {"$set": {"text": None}})
                    try:
                        member = await guild.fetch_member(document["id"])
                    except sweetness.NotFound:
                        continue
                            
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE']))
                    if role is not None:
                        try:
                            await member.remove_roles(role)
                        except sweetness.HTTPException:
                            print(f"I can't remove text mute for {document['id']}")
                        
                        try:
                            membed = sweetness.Embed()
                            membed.set_author(name="Время наказания истекло !", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062770252292833352/6290515.png")
                            membed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                            membed.set_footer(text="🦋 SweetNess")
                            membed.timestamp = datetime.datetime.now()
                            membed.color = 0x2f3136
                            membed.description = "ᅠ\n > Текстовый мут был снят."
                            await member.send(embed=membed)
                        except:
                            pass

                    else:
                        print("Role not found for text mute")

                if document['voice'] is not None and document['voice'] <= datetime.datetime.now():
                    await collection.update_one({"id": document["id"]}, {"$set": {"voice": None}})
                    try:
                        member = await guild.fetch_member(document["id"])
                    except sweetness.NotFound:
                        continue
                    
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE']))
                    if role is not None:
                        try:
                            await member.remove_roles(role)
                        except sweetness.HTTPException:
                            print(f"I can't remove voice mute for {document['id']}")
                        
                        try:
                            membed = sweetness.Embed()
                            membed.set_author(name="Время наказания истекло !", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062770252292833352/6290515.png")
                            membed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                            membed.set_footer(text="🦋 SweetNess")
                            membed.timestamp = datetime.datetime.now()
                            membed.color = 0x2f3136
                            membed.description = "ᅠ\n > Голосовой мут был снят."
                            await member.send(embed=membed)
                        except:
                            pass
                    else:
                        print("Role not found for voice mute")

                if document['ban'] is not None and document['ban'] <= datetime.datetime.now():
                    await collection.update_one({"id": document["id"]}, {"$set": {"ban": None}})
                    try:
                        member = await guild.fetch_member(document["id"])
                    except sweetness.NotFound:
                        continue

                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['PUNISHMENT_ROLES']['BAN']))
                    if role is not None:
                        try:
                            await member.remove_roles(role)
                        except sweetness.HTTPException:
                            print(f"I can't remove voice mute for {document['id']}")

                        try:
                            membed = sweetness.Embed()
                            membed.set_author(name="Время наказания истекло !", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062770252292833352/6290515.png")
                            membed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1107679980634263572/b55d389670ad9784e2ae319e70edfffb.png")
                            membed.set_footer(text="🦋 SweetNess")
                            membed.color = 0x2f3136
                            membed.timestamp = datetime.datetime.now()
                            membed.description = "ᅠ\n > Бан был снят."
                            await member.send(embed=membed)
                        except:
                            pass         
                    else:
                        print("Role not found for ban")
            except:
                print("??? [CHECK-DOCS]")

    @commands.guild_only()
    @commands.slash_command(name="action", description="Модерирование пользователя")
    async def action(self, interaction: sweetness.ApplicationCommandInteraction, member: sweetness.Member = commands.Param(name='пользователь', description="Укажите пользователя")):
        r1 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['SWEETNESS'])
        r2 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['ADMINISTRATOR'])
        r3 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_WARDEN']) 
        r4 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['M_HELPER'])
        r5 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['WARDEN'])
        r6 = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['ACTION_ROLES']['HELPER'])
        staffr = sweetness.utils.get(interaction.guild.roles, id=config.SWEETNESS['STAFF_ROLE'])

        #await interaction.response.defer()
        if member.bot:
            embed = sweetness.Embed()
            embed.color = 0x2f3136
            embed.description = "> Вы не можете взаимодействовать с ботом."
            await interaction.send(embed=embed, ephemeral=True)
        else:
            if member == interaction.author:
                embed = sweetness.Embed()
                embed.color = 0x2f3136
                embed.description = "> Вы не можете взаимодействовать с самим собой."
                await interaction.send(embed=embed, ephemeral=True)
            else:
                if await staff.find_one({"id": interaction.author.id}) is None:
                    await staff.insert_one({
                        "id": interaction.author.id,
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

                if not staffr in member.roles:
                    if r1 in interaction.author.roles or r2 in interaction.author.roles or r3 in interaction.author.roles or r4 in interaction.author.roles or r5 in interaction.author.roles or r6 in interaction.author.roles:
                        if r1 in interaction.author.roles:
                            embed = sweetness.Embed()
                            embed.set_author(name="Модерационная панель", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062709497308659842/2592443.png")
                            embed.set_thumbnail(url=interaction.author.display_avatar)
                            embed.color = 0x2f3136
                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {member.mention} нужно выбрать одну из операций указанных ниже."
                            await interaction.send(embed=embed, ephemeral=True)
                            msg = await interaction.original_message()
                            await msg.edit(embed=embed, view=Buttons(client=self.client, member=member, message=msg))
                        if not r1 in interaction.author.roles:
                            if r2 in interaction.author.roles:
                                embed = sweetness.Embed()
                                embed.set_author(name="Модерационная панель")
                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                embed.color = 0x2f3136
                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {member.mention} нужно выбрать одну из операций указанных ниже."
                                await interaction.send(embed=embed, ephemeral=True)
                                message = await interaction.original_message()
                                await message.edit(embed=embed, view=Buttons(client=self.client, member=member, message=message))
                        if not r1 in interaction.author.roles:
                            if not r2 in interaction.author.roles:
                                if r3 in interaction.author.roles:
                                    embed = sweetness.Embed()
                                    embed.set_author(name="Модерационная панель", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062709497308659842/2592443.png")
                                    embed.set_thumbnail(url=interaction.author.display_avatar)
                                    embed.color = 0x2f3136
                                    embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {member.mention} нужно выбрать одну из операций указанных ниже."
                                    await interaction.send(embed=embed, ephemeral=True)
                                    message = await interaction.original_message()
                                    await message.edit(embed=embed, view=Buttons(client=self.client, member=member, message=message))
                        if not r1 in interaction.author.roles:
                            if not r2 in interaction.author.roles:
                                if not r3 in interaction.author.roles:
                                    if r4 in interaction.author.roles:
                                        embed = sweetness.Embed()
                                        embed.set_author(name="Модерационная панель", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062709497308659842/2592443.png")
                                        embed.set_thumbnail(url=interaction.author.display_avatar)
                                        embed.color = 0x2f3136
                                        embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {member.mention} нужно выбрать одну из операций указанных ниже."
                                        await interaction.send(embed=embed, ephemeral=True)
                                        message = await interaction.original_message()
                                        await message.edit(embed=embed, view=Buttons(client=self.client, member=member, message=message)) 
                        if not r1 in interaction.author.roles:
                            if not r2 in interaction.author.roles:
                                if not r3 in interaction.author.roles: 
                                    if not r4 in interaction.author.roles:
                                        if r5 in interaction.author.roles:
                                            embed = sweetness.Embed()
                                            embed.set_author(name="Модерационная панель", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062709497308659842/2592443.png")
                                            embed.set_thumbnail(url=interaction.author.display_avatar)
                                            embed.color = 0x2f3136
                                            embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {member.mention} нужно выбрать одну из операций указанных ниже."
                                            await interaction.send(embed=embed, ephemeral=True)
                                            message = await interaction.original_message()
                                            await message.edit(embed=embed, view=Warden(client=self.client, member=member, message=message))     
                        if not r1 in interaction.author.roles:
                            if not r2 in interaction.author.roles: 
                                if not r3 in interaction.author.roles:
                                    if not r4 in interaction.author.roles:
                                        if not r5 in interaction.author.roles:
                                            if r6 in interaction.author.roles:
                                                embed = sweetness.Embed()
                                                embed.set_author(name="Модерационная панель", icon_url="https://cdn.discordapp.com/attachments/1058100296590557266/1062709497308659842/2592443.png")
                                                embed.set_thumbnail(url=interaction.author.display_avatar)
                                                embed.color = 0x2f3136
                                                embed.description = f"> Для того, чтобы начать взаимодействие с пользователем {member.mention} нужно выбрать одну из операций указанных ниже."
                                                await interaction.send(embed=embed, ephemeral=True)
                                                message = await interaction.original_message()
                                                await message.edit(embed=embed, view=Helper(client=self.client, member=member, message=message))
                    else:
                        embed = sweetness.Embed()
                        embed.set_thumbnail(url=interaction.author.display_avatar)
                        embed.color = 0x2f3136
                        embed.description = "⠀\n> Вы не можете использовать использовать панель модерации, так как не являетесь ей."
                        await interaction.response.send_message(embed=embed, ephemeral=True)       
                else:
                    embed = sweetness.Embed()
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    embed.color = 0x2f3136
                    embed.description = "> Взаимодействие возможно только с обычными пользователями. Если у вас возникла спорная / конфликтная ситуация с участником стаффа - обращайтесь к вышестоящему."
                    await interaction.response.send_message(embed=embed, ephemeral=True)             

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(config.SWEETNESS['GUILD_ID'])
        if await warns.find_one({"id": member.id}) is not None:
            async for document in warns.find({"id": member.id}):
                typee = document['type']
                if typee == "text":
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['TIME_ROLES']['TEXT_WARN']))
                    try:
                        await member.add_roles(role)
                    except:
                        pass
                if typee == "voice":
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['TIME_ROLES']['VOICE_WARN']))
                    try:
                        await member.add_roles(role)
                    except:
                        pass                    
                if typee == "ban":
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['TIME_ROLES']['BAN_WARN']))
                    try:
                        await member.add_roles(role)
                    except:
                        pass     
        if await collection.find_one({"id": member.id}) is not None:
            async for document in collection.find({"id": member.id}):
                text = document['text']
                voice = document['voice']
                ban = document['ban']
                if text is not None:
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['PUNISHMENT_ROLES']['TEXT_MUTE']))
                    try:
                        await member.add_roles(role)
                    except:
                        pass 

                if voice is not None:
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['PUNISHMENT_ROLES']['VOICE_MUTE']))
                    try:
                        await member.add_roles(role)
                    except: 
                        pass

                if ban is not None:
                    role = sweetness.utils.get(await guild.fetch_roles(), id=int(config.SWEETNESS['PUNISHMENT_ROLES']['BAN']))
                    try:
                        await member.add_roles(role)
                    except:
                        pass    

                    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        try:
            try:
                if inter.component.custom_id == "text_unmute" or inter.component.custom_id == "text_unwarn" or inter.component.custom_id == "voice_unmute" or inter.component.custom_id == "voice_unwarn" or inter.component.custom_id == "ban_unmute" or inter.component.custom_id == "ban_unwarn":
                    print(inter.data)
                else:
                    try:
                        await inter.send("")
                    except:
                        pass
            except Exception as e:
                print(e)       
        except:
            pass

def setup(client):
    client.add_cog(Action(client))     
