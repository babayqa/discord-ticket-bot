import discord
from discord.ext import commands
from discord import app_commands
from config.config import config
from utils.buttons import SetupView

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setup", description="Настройка системы тикетов")
    @app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """Команда для настройки системы тикетов"""
        embed = discord.Embed(
            title="⚙️ Панель управления системой тикетов",
            description="Выберите опцию для настройки:",
            color=0x3498db
        )
        
        view = SetupView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetupCog(bot))