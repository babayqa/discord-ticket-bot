import json
import aiofiles
from pathlib import Path
from typing import Dict, List
import datetime

class Config:
    def __init__(self):
        self.data_path = Path("data/settings.json")
        self.tickets_path = Path("data/active_tickets.json")
        self.data_path.parent.mkdir(exist_ok=True)
        
        # Значения по умолчанию
        self.default_settings = {
            "review_category": None,
            "support_category": None,
            "ticket_channel": None,
            "review_channel": None,
            "log_channel": None,
            "closer_role": None,
            "panel_title": "Оставьте отзыв о нашем приложении",
            "panel_description": "С вами мы становимся лучше )_)",
            "review_button": "Оставить отзыв",
            "support_button": "Поддержка",
            "embed_color": "3498db"
        }
        
    async def load_settings(self, guild_id: int):
        """Загружает настройки для гильдии"""
        try:
            async with aiofiles.open(self.data_path, "r", encoding="utf-8") as f:
                data = json.loads(await f.read())
                return data.get(str(guild_id), self.default_settings.copy())
        except (FileNotFoundError, json.JSONDecodeError):
            return self.default_settings.copy()
    
    async def save_settings(self, guild_id: int, settings: dict):
        """Сохраняет настройки для гильдии"""
        try:
            async with aiofiles.open(self.data_path, "r", encoding="utf-8") as f:
                data = json.loads(await f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        data[str(guild_id)] = settings
        
        async with aiofiles.open(self.data_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    async def update_setting(self, guild_id: int, key: str, value):
        """Обновляет конкретную настройку"""
        settings = await self.load_settings(guild_id)
        settings[key] = value
        await self.save_settings(guild_id, settings)
    
    # Методы для управления активными тикетами
    async def load_active_tickets(self, guild_id: int) -> Dict:
        """Загружает активные тикеты для гильдии"""
        try:
            async with aiofiles.open(self.tickets_path, "r", encoding="utf-8") as f:
                data = json.loads(await f.read())
                return data.get(str(guild_id), {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    async def save_active_tickets(self, guild_id: int, tickets: Dict):
        """Сохраняет активные тикеты для гильдии"""
        try:
            async with aiofiles.open(self.tickets_path, "r", encoding="utf-8") as f:
                data = json.loads(await f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        data[str(guild_id)] = tickets
        
        async with aiofiles.open(self.tickets_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    async def add_active_ticket(self, guild_id: int, user_id: int, channel_id: int, ticket_type: str):
        """Добавляет активный тикет"""
        tickets = await self.load_active_tickets(guild_id)
        
        if str(user_id) not in tickets:
            tickets[str(user_id)] = []
        
        tickets[str(user_id)].append({
            "channel_id": channel_id,
            "type": ticket_type,
            "created_at": datetime.datetime.utcnow().isoformat()
        })
        
        await self.save_active_tickets(guild_id, tickets)
    
    async def remove_active_ticket(self, guild_id: int, channel_id: int):
        """Удаляет активный тикет по ID канала"""
        tickets = await self.load_active_tickets(guild_id)
        
        for user_id, user_tickets in list(tickets.items()):
            user_tickets = [t for t in user_tickets if t["channel_id"] != channel_id]
            if user_tickets:
                tickets[user_id] = user_tickets
            else:
                tickets.pop(user_id, None)
        
        await self.save_active_tickets(guild_id, tickets)
    
    async def get_user_active_tickets(self, guild_id: int, user_id: int) -> List:
        """Получает активные тикеты пользователя"""
        tickets = await self.load_active_tickets(guild_id)
        return tickets.get(str(user_id), [])
    
    async def has_active_ticket(self, guild_id: int, user_id: int) -> bool:
        """Проверяет, есть ли у пользователя активные тикеты"""
        user_tickets = await self.get_user_active_tickets(guild_id, user_id)
        return len(user_tickets) > 0
    
    async def get_ticket_count(self, guild_id: int, user_id: int) -> int:
        """Получает количество активных тикетов пользователя"""
        user_tickets = await self.get_user_active_tickets(guild_id, user_id)
        return len(user_tickets)

config = Config()