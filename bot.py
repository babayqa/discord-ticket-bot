import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()

class TicketBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(command_prefix="/", intents=intents, help_command=None)
        
    async def setup_hook(self):
        # Загружаем все коги
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"✅ Загружена кога: {filename[:-3]}")
                except Exception as e:
                    print(f"❌ Ошибка загрузки коги {filename}: {e}")
        
        try:
            synced = await self.tree.sync()
            print(f"✅ Синхронизировано {len(synced)} команд")
        except Exception as e:
            print(f"❌ Ошибка синхронизации команд: {e}")

    async def on_ready(self):
        print(f"Бот готов к работе!")
        print(f"Имя: {self.user.name}")
        print(f"ID: {self.user.id}")
        print(f"Приглашение: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot+applications.commands")
        
bot = TicketBot()

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ Ошибка: Токен не найден в .env файле")
        print("Создайте файл .env с содержимым: DISCORD_TOKEN=ваш_токен")
    else:
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ Неверный токен бота!")
        except Exception as e:
            print(f"❌ Ошибка запуска бота: {e}")