import discord
import asyncio
import datetime

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Основные настройки", style=discord.ButtonStyle.primary, emoji="⚙️", custom_id="main_settings_button")
    async def main_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        class SettingsModal(discord.ui.Modal, title="Основные настройки"):
            review_category = discord.ui.TextInput(
                label="ID категории отзывов",
                placeholder="123456789012345678",
                required=True,
                custom_id="review_category"
            )
            
            support_category = discord.ui.TextInput(
                label="ID категории поддержки",
                placeholder="123456789012345678",
                required=True,
                custom_id="support_category"
            )
            
            review_channel = discord.ui.TextInput(
                label="ID канала отзывов",
                placeholder="123456789012345678",
                required=True,
                custom_id="review_channel"
            )
            
            log_channel = discord.ui.TextInput(
                label="ID канала логов",
                placeholder="123456789012345678",
                required=True,
                custom_id="log_channel"
            )
            
            closer_role = discord.ui.TextInput(
                label="ID роли закрытия",
                placeholder="123456789012345678",
                required=True,
                custom_id="closer_role"
            )
            
            async def on_submit(self, interaction: discord.Interaction):
                try:
                    from config.config import config
                    
                    # Получаем значения
                    review_category = self.review_category.value
                    support_category = self.support_category.value
                    review_channel = self.review_channel.value
                    log_channel = self.log_channel.value
                    closer_role = self.closer_role.value
                    
                    # Сохраняем настройки
                    await config.update_setting(interaction.guild_id, "review_category", int(review_category))
                    await config.update_setting(interaction.guild_id, "support_category", int(support_category))
                    await config.update_setting(interaction.guild_id, "review_channel", int(review_channel))
                    await config.update_setting(interaction.guild_id, "log_channel", int(log_channel))
                    await config.update_setting(interaction.guild_id, "closer_role", int(closer_role))
                    
                    await interaction.response.send_message("✅ Основные настройки сохранены!", ephemeral=True)
                    
                except ValueError:
                    await interaction.response.send_message("❌ Ошибка: Неверный формат ID. ID должны быть числами.", ephemeral=True)
                except Exception as e:
                    print(f"Ошибка: {e}")
                    await interaction.response.send_message("❌ Произошла ошибка при сохранении настроек.", ephemeral=True)
        
        modal = SettingsModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Настроить интерфейс", style=discord.ButtonStyle.secondary, emoji="🎨", custom_id="interface_settings_button")
    async def interface_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        class InterfaceModal(discord.ui.Modal, title="Настройки интерфейса"):
            panel_title = discord.ui.TextInput(
                label="Заголовок панели",
                placeholder="Оставьте отзыв о нашем приложении",
                default="Оставьте отзыв о нашем приложении",
                required=True,
                max_length=256,
                custom_id="panel_title"
            )
            
            panel_description = discord.ui.TextInput(
                label="Описание панели",
                placeholder="С вами мы становимся лучше )_)",
                default="С вами мы становимся лучше )_)",
                style=discord.TextStyle.paragraph,
                required=True,
                max_length=2000,
                custom_id="panel_description"
            )
            
            review_button = discord.ui.TextInput(
                label="Текст кнопки отзыва",
                placeholder="Оставить отзыв",
                default="Оставить отзыв",
                required=True,
                max_length=80,
                custom_id="review_button"
            )
            
            support_button = discord.ui.TextInput(
                label="Текст кнопки поддержки",
                placeholder="Поддержка",
                default="Поддержка",
                required=True,
                max_length=80,
                custom_id="support_button"
            )
            
            embed_color = discord.ui.TextInput(
                label="Цвет embed (HEX без #)",
                placeholder="3498db",
                default="3498db",
                required=True,
                max_length=6,
                custom_id="embed_color"
            )
            
            async def on_submit(self, interaction: discord.Interaction):
                try:
                    from config.config import config
                    
                    # Сохраняем настройки
                    await config.update_setting(interaction.guild_id, "panel_title", self.panel_title.value)
                    await config.update_setting(interaction.guild_id, "panel_description", self.panel_description.value)
                    await config.update_setting(interaction.guild_id, "review_button", self.review_button.value)
                    await config.update_setting(interaction.guild_id, "support_button", self.support_button.value)
                    await config.update_setting(interaction.guild_id, "embed_color", self.embed_color.value.replace("#", ""))
                    
                    await interaction.response.send_message("✅ Настройки интерфейса сохранены!", ephemeral=True)
                    
                except Exception as e:
                    print(f"Ошибка: {e}")
                    await interaction.response.send_message("❌ Произошла ошибка при сохранении настроек.", ephemeral=True)
        
        modal = InterfaceModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Показать настройки", style=discord.ButtonStyle.success, emoji="📋", custom_id="show_settings_button")
    async def show_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        from config.config import config
        settings = await config.load_settings(interaction.guild_id)
        
        embed = discord.Embed(
            title="⚙️ Текущие настройки",
            color=0x3498db
        )
        
        # Основные настройки
        main_settings = []
        if settings.get('review_category'):
            main_settings.append(f"**Категория отзывов:** <#{settings['review_category']}>")
        else:
            main_settings.append("**Категория отзывов:** Не настроено")
        
        if settings.get('support_category'):
            main_settings.append(f"**Категория поддержки:** <#{settings['support_category']}>")
        else:
            main_settings.append("**Категория поддержки:** Не настроено")
        
        if settings.get('review_channel'):
            main_settings.append(f"**Канал отзывов:** <#{settings['review_channel']}>")
        else:
            main_settings.append("**Канал отзывов:** Не настроено")
        
        if settings.get('log_channel'):
            main_settings.append(f"**Канал логов:** <#{settings['log_channel']}>")
        else:
            main_settings.append("**Канал логов:** Не настроено")
        
        if settings.get('closer_role'):
            main_settings.append(f"**Роль закрытия:** <@&{settings['closer_role']}>")
        else:
            main_settings.append("**Роль закрытия:** Не настроено")
        
        embed.add_field(
            name="Основные настройки", 
            value="\n".join(main_settings), 
            inline=False
        )
        
        # Настройки интерфейса
        interface_settings = [
            f"**Заголовок:** {settings.get('panel_title', 'Не настроено')}",
            f"**Описание:** {settings.get('panel_description', 'Не настроено')}",
            f"**Кнопка отзыва:** {settings.get('review_button', 'Не настроено')}",
            f"**Кнопка поддержки:** {settings.get('support_button', 'Не настроено')}",
            f"**Цвет embed:** #{settings.get('embed_color', '3498db')}"
        ]
        
        embed.add_field(
            name="Настройки интерфейса", 
            value="\n".join(interface_settings), 
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Создать панель", style=discord.ButtonStyle.danger, emoji="📝", custom_id="create_panel_button")
    async def create_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        from config.config import config
        settings = await config.load_settings(interaction.guild_id)
        
        # Проверяем настройки
        if not settings.get("review_category") or not settings.get("support_category"):
            await interaction.response.send_message(
                "⚠️ Сначала настройте категории для тикетов в основных настройках!",
                ephemeral=True
            )
            return
        
        # Создаем панель
        try:
            color = int(settings.get("embed_color", "3498db").replace("#", ""), 16)
        except ValueError:
            color = 0x3498db  # Синий по умолчанию
        
        embed = discord.Embed(
            title=settings.get("panel_title", "Оставьте отзыв о нашем приложении"),
            description=settings.get("panel_description", "С вами мы становимся лучше )_)"),
            color=color
        )
        
        view = PanelView()
        
        await interaction.response.send_message("✅ Панель создана! Проверьте текущий канал.", ephemeral=True)
        await interaction.channel.send(embed=embed, view=view)

class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Оставить отзыв", style=discord.ButtonStyle.success, emoji="📝", custom_id="create_review_ticket")
    async def create_review(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        from config.config import config
        guild = interaction.guild
        user = interaction.user
        
        # Проверяем, есть ли у пользователя уже активный тикет
        has_active_ticket = await config.has_active_ticket(guild.id, user.id)
        if has_active_ticket:
            await interaction.followup.send(
                "❌ У вас уже есть активный тикет! Закройте текущий тикет перед созданием нового.",
                ephemeral=True
            )
            return
        
        # Загружаем настройки
        settings = await config.load_settings(guild.id)
        
        # Получаем категорию для отзывов
        category_id = settings.get("review_category")
        
        if not category_id:
            await interaction.followup.send(
                "❌ Категория для отзывов не настроена! Используйте /setup для настройки.",
                ephemeral=True
            )
            return
        
        category = guild.get_channel(category_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            await interaction.followup.send(
                "❌ Категория для отзывов не найдена! Проверьте настройки.",
                ephemeral=True
            )
            return
        
        # Создаем канал тикета
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        # Добавляем роль для закрытия если есть
        closer_role_id = settings.get("closer_role")
        if closer_role_id:
            closer_role = guild.get_role(closer_role_id)
            if closer_role:
                overwrites[closer_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        
        try:
            # Ограничиваем длину имени
            username = user.name[:20]  # Ограничиваем до 20 символов
            ticket_channel = await guild.create_text_channel(
                name=f"отзыв-{username}",
                category=category,
                overwrites=overwrites
            )
            
            # Добавляем тикет в активные
            await config.add_active_ticket(guild.id, user.id, ticket_channel.id, "review")
            
            # Создаем embed для тикета
            embed = discord.Embed(
                title="📝 Тикет отзыва",
                description=f"Пользователь {user.mention} хочет оставить отзыв",
                color=0x2ecc71
            )
            embed.add_field(
                name="📝 Инструкция",
                value="Напишите свой отзыв в этом канале. Администратор может опубликовать его или закрыть тикет.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Ограничение",
                value="Вы можете иметь только один активный тикет одновременно.",
                inline=False
            )
            embed.set_footer(text=f"ID пользователя: {user.id}")
            embed.timestamp = discord.utils.utcnow()
            
            view = TicketControlView("review")
            await ticket_channel.send(embed=embed, view=view)
            
            # Логируем создание тикета
            log_channel_id = settings.get("log_channel")
            if log_channel_id:
                log_channel = guild.get_channel(log_channel_id)
                if log_channel:
                    log_embed = discord.Embed(
                        title=f"📝 Создан новый тикет",
                        description=f"Тип: Отзыв",
                        color=0x2ecc71
                    )
                    log_embed.add_field(name="Пользователь", value=f"{user.mention} ({user.id})", inline=True)
                    log_embed.add_field(name="Канал", value=ticket_channel.mention, inline=True)
                    log_embed.set_footer(text=f"ID канала: {ticket_channel.id}")
                    log_embed.timestamp = discord.utils.utcnow()
                    await log_channel.send(embed=log_embed)
            
            await interaction.followup.send(
                f"✅ Тикет для отзыва создан! Перейдите в {ticket_channel.mention}.",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Ошибка при создании тикета: {e}")
            await interaction.followup.send(
                "❌ Не удалось создать тикет. Проверьте права бота.",
                ephemeral=True
            )
    
    @discord.ui.button(label="Поддержка", style=discord.ButtonStyle.primary, emoji="🔧", custom_id="create_support_ticket")
    async def create_support(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        from config.config import config
        guild = interaction.guild
        user = interaction.user
        
        # Проверяем, есть ли у пользователя уже активный тикет
        has_active_ticket = await config.has_active_ticket(guild.id, user.id)
        if has_active_ticket:
            await interaction.followup.send(
                "❌ У вас уже есть активный тикет! Закройте текущий тикет перед созданием нового.",
                ephemeral=True
            )
            return
        
        # Загружаем настройки
        settings = await config.load_settings(guild.id)
        
        # Получаем категорию для поддержки
        category_id = settings.get("support_category")
        
        if not category_id:
            await interaction.followup.send(
                "❌ Категория для поддержки не настроена! Используйте /setup для настройки.",
                ephemeral=True
            )
            return
        
        category = guild.get_channel(category_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            await interaction.followup.send(
                "❌ Категория для поддержки не найдена! Проверьте настройки.",
                ephemeral=True
            )
            return
        
        # Создаем канал тикета
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        # Добавляем роль для закрытия если есть
        closer_role_id = settings.get("closer_role")
        if closer_role_id:
            closer_role = guild.get_role(closer_role_id)
            if closer_role:
                overwrites[closer_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        
        try:
            # Ограничиваем длину имени
            username = user.name[:20]
            ticket_channel = await guild.create_text_channel(
                name=f"поддержка-{username}",
                category=category,
                overwrites=overwrites
            )
            
            # Добавляем тикет в активные
            await config.add_active_ticket(guild.id, user.id, ticket_channel.id, "support")
            
            # Создаем embed для тикета
            embed = discord.Embed(
                title="🔧 Тикет поддержки",
                description=f"Пользователь {user.mention} нуждается в помощи",
                color=0xe74c3c
            )
            embed.add_field(
                name="🔧 Инструкция",
                value="Опишите вашу проблему подробно. Администратор поможет вам решить её.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Ограничение",
                value="Вы можете иметь только один активный тикет одновременно.",
                inline=False
            )
            embed.set_footer(text=f"ID пользователя: {user.id}")
            embed.timestamp = discord.utils.utcnow()
            
            view = TicketControlView("support")
            await ticket_channel.send(embed=embed, view=view)
            
            # Логируем создание тикета
            log_channel_id = settings.get("log_channel")
            if log_channel_id:
                log_channel = guild.get_channel(log_channel_id)
                if log_channel:
                    log_embed = discord.Embed(
                        title=f"🔧 Создан новый тикет",
                        description=f"Тип: Поддержка",
                        color=0xe74c3c
                    )
                    log_embed.add_field(name="Пользователь", value=f"{user.mention} ({user.id})", inline=True)
                    log_embed.add_field(name="Канал", value=ticket_channel.mention, inline=True)
                    log_embed.set_footer(text=f"ID канала: {ticket_channel.id}")
                    log_embed.timestamp = discord.utils.utcnow()
                    await log_channel.send(embed=log_embed)
            
            await interaction.followup.send(
                f"✅ Тикет поддержки создан! Перейдите в {ticket_channel.mention}.",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Ошибка при создании тикета: {e}")
            await interaction.followup.send(
                "❌ Не удалось создать тикет. Проверьте права бота.",
                ephemeral=True
            )

class TicketControlView(discord.ui.View):
    def __init__(self, ticket_type: str):
        super().__init__(timeout=None)
        self.ticket_type = ticket_type
        
        if ticket_type == "review":
            # Добавляем кнопку "Опубликовать" для отзывов
            publish_button = discord.ui.Button(
                label="Опубликовать", 
                style=discord.ButtonStyle.success, 
                emoji="📢", 
                custom_id="publish_review_button"
            )
            
            async def publish_callback(interaction: discord.Interaction):
                class PublishModal(discord.ui.Modal, title="Опубликовать отзыв"):
                    message_link = discord.ui.TextInput(
                        label="Ссылка на сообщение",
                        placeholder="https://discord.com/channels/...",
                        required=True
                    )
                    
                    async def on_submit(self, interaction: discord.Interaction):
                        await interaction.response.defer(ephemeral=True)
                        
                        from config.config import config
                        guild = interaction.guild
                        channel = interaction.channel
                        
                        # Проверяем права
                        closer_role_id = (await config.load_settings(guild.id)).get("closer_role")
                        if closer_role_id:
                            closer_role = guild.get_role(closer_role_id)
                            if closer_role and closer_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
                                await interaction.followup.send("❌ У вас нет прав для публикации отзывов!", ephemeral=True)
                                return
                        
                        # Получаем настройки
                        settings = await config.load_settings(guild.id)
                        review_channel_id = settings.get("review_channel")
                        
                        if not review_channel_id:
                            await interaction.followup.send("❌ Канал для публикации отзывов не настроен!", ephemeral=True)
                            return
                        
                        review_channel = guild.get_channel(review_channel_id)
                        if not review_channel:
                            await interaction.followup.send("❌ Канал для публикации отзывов не найден!", ephemeral=True)
                            return
                        
                        try:
                            # Парсим ссылку на сообщение
                            parts = self.message_link.value.split("/")
                            if len(parts) < 7:
                                await interaction.followup.send("❌ Неверный формат ссылки! Пример: https://discord.com/channels/...", ephemeral=True)
                                return
                            
                            message_id = int(parts[-1])
                            
                            # Получаем сообщение из текущего канала
                            try:
                                message = await channel.fetch_message(message_id)
                            except discord.NotFound:
                                await interaction.followup.send("❌ Сообщение не найдено! Убедитесь, что ссылка правильная.", ephemeral=True)
                                return
                            
                            # Создаем embed для публикации
                            embed = discord.Embed(
                                title="📝 Новый отзыв",
                                description=message.content,
                                color=0x2ecc71
                            )
                            embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else None)
                            embed.set_footer(text=f"Опубликовано {interaction.user.name}")
                            embed.timestamp = discord.utils.utcnow()
                            
                            # Добавляем вложения если есть
                            if message.attachments:
                                attachments_text = "\n".join([f"[{att.filename}]({att.url})" for att in message.attachments])
                                embed.add_field(name="📎 Вложения", value=attachments_text, inline=False)
                            
                            # Публикуем
                            await review_channel.send(embed=embed)
                            
                            # Логируем публикацию
                            log_channel_id = settings.get("log_channel")
                            if log_channel_id:
                                log_channel = guild.get_channel(log_channel_id)
                                if log_channel:
                                    log_embed = discord.Embed(
                                        title="📢 Отзыв опубликован",
                                        description=f"Отзыв от {message.author.mention} был опубликован",
                                        color=0x9b59b6
                                    )
                                    log_embed.add_field(name="Канал", value=review_channel.mention, inline=True)
                                    log_embed.add_field(name="Опубликовал", value=interaction.user.mention, inline=True)
                                    log_embed.set_footer(text=f"ID сообщения: {message_id}")
                                    log_embed.timestamp = discord.utils.utcnow()
                                    await log_channel.send(embed=log_embed)
                            
                            # Подтверждаем публикацию
                            await interaction.followup.send("✅ Отзыв успешно опубликован! Тикет будет закрыт...", ephemeral=True)
                            
                            # Удаляем тикет из активных
                            await config.remove_active_ticket(guild.id, channel.id)
                            
                            # Закрываем тикет (отдельно, чтобы не мешать ответу)
                            await close_ticket_after_publish(interaction, channel, guild)
                            
                        except ValueError:
                            await interaction.followup.send("❌ Неверный формат ID сообщения в ссылке!", ephemeral=True)
                        except Exception as e:
                            print(f"Ошибка при публикации отзыва: {e}")
                            await interaction.followup.send(f"❌ Произошла ошибка: {str(e)[:100]}", ephemeral=True)
                
                modal = PublishModal()
                await interaction.response.send_modal(modal)
            
            publish_button.callback = publish_callback
            self.add_item(publish_button)
        
        # Добавляем кнопку "Закрыть"
        close_button = discord.ui.Button(
            label="Закрыть", 
            style=discord.ButtonStyle.danger, 
            emoji="🔒", 
            custom_id="close_ticket_button"
        )
        
        async def close_callback(interaction: discord.Interaction):
            await close_ticket(interaction)
        
        close_button.callback = close_callback
        self.add_item(close_button)

async def close_ticket_after_publish(interaction: discord.Interaction, channel: discord.TextChannel, guild: discord.Guild):
    """Закрывает тикет после публикации (без отправки ответа)"""
    from config.config import config
    
    # Получаем настройки
    settings = await config.load_settings(guild.id)
    
    # Создаем архив
    log_channel_id = settings.get("log_channel")
    
    try:
        # Собираем историю сообщений
        messages = []
        async for message in channel.history(limit=100, oldest_first=True):
            attachments = ""
            if message.attachments:
                attachments = f" [Вложения: {', '.join([a.filename for a in message.attachments])}]"
            messages.append(f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.author.name}: {message.content}{attachments}")
        
        # Отправляем в лог
        if log_channel_id:
            log_channel = guild.get_channel(log_channel_id)
            if log_channel:
                # Отправляем embed о закрытии
                close_embed = discord.Embed(
                    title="🔒 Тикет закрыт после публикации",
                    description=f"Канал: {channel.name}",
                    color=0x9b59b6  # Фиолетовый для отличия
                )
                close_embed.add_field(name="Закрыл", value=interaction.user.mention, inline=True)
                close_embed.set_footer(text=f"ID канала: {channel.id}")
                close_embed.timestamp = discord.utils.utcnow()
                await log_channel.send(embed=close_embed)
                
                # Отправляем лог сообщений
                if messages:
                    log_text = f"Лог тикета {channel.name}:\n" + "\n".join(messages)
                    # Разбиваем длинный текст на части
                    for i in range(0, len(log_text), 1900):
                        await log_channel.send(f"```{log_text[i:i+1900]}```")
        
        # Удаляем канал
        await channel.delete()
        
    except Exception as e:
        print(f"Ошибка при закрытии тикета после публикации: {e}")

async def close_ticket(interaction: discord.Interaction):
    """Закрывает тикет"""
    from config.config import config
    
    channel = interaction.channel
    guild = interaction.guild
    
    # Проверяем права
    closer_role_id = (await config.load_settings(guild.id)).get("closer_role")
    if closer_role_id:
        closer_role = guild.get_role(closer_role_id)
        if closer_role and closer_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ У вас нет прав для закрытия тикетов!", ephemeral=True)
            return
    
    # Получаем настройки
    settings = await config.load_settings(guild.id)
    
    # Создаем архив
    log_channel_id = settings.get("log_channel")
    
    try:
        # Отправляем начальный ответ
        await interaction.response.send_message("🔒 Закрытие тикета...", ephemeral=True)
        
        # Удаляем тикет из активных
        await config.remove_active_ticket(guild.id, channel.id)
        
        # Собираем историю сообщений
        messages = []
        async for message in channel.history(limit=100, oldest_first=True):
            attachments = ""
            if message.attachments:
                attachments = f" [Вложения: {', '.join([a.filename for a in message.attachments])}]"
            messages.append(f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.author.name}: {message.content}{attachments}")
        
        # Отправляем в лог
        if log_channel_id:
            log_channel = guild.get_channel(log_channel_id)
            if log_channel:
                # Отправляем embed о закрытии
                close_embed = discord.Embed(
                    title="🔒 Тикет закрыт",
                    description=f"Канал: {channel.name}",
                    color=0xe74c3c
                )
                close_embed.add_field(name="Закрыл", value=interaction.user.mention, inline=True)
                close_embed.set_footer(text=f"ID канала: {channel.id}")
                close_embed.timestamp = discord.utils.utcnow()
                await log_channel.send(embed=close_embed)
                
                # Отправляем лог сообщений
                if messages:
                    log_text = f"Лог тикета {channel.name}:\n" + "\n".join(messages)
                    # Разбиваем длинный текст на части
                    for i in range(0, len(log_text), 1900):
                        await log_channel.send(f"```{log_text[i:i+1900]}```")
        
        # Обновляем сообщение о закрытии
        await interaction.followup.send("✅ Тикет закрыт и удален!", ephemeral=True)
        
        # Небольшая задержка перед удалением
        await asyncio.sleep(1)
        
        # Удаляем канал
        await channel.delete()
        
    except Exception as e:
        print(f"Ошибка при закрытии тикета: {e}")
        try:
            await interaction.followup.send("❌ Произошла ошибка при закрытии тикета!", ephemeral=True)
        except Exception:
            pass