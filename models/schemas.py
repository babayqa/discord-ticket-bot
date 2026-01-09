from dataclasses import dataclass
from typing import Optional

@dataclass
class TicketSettings:
    review_category: Optional[int] = None
    support_category: Optional[int] = None
    ticket_channel: Optional[int] = None
    review_channel: Optional[int] = None
    log_channel: Optional[int] = None
    closer_role: Optional[int] = None
    
@dataclass
class PanelSettings:
    title: str = "Оставьте отзыв о нашем приложении"
    description: str = "С вами мы становимся лучше )_)"
    review_button: str = "Оставить отзыв"
    support_button: str = "Поддержка"
    embed_color: str = "3498db"

@dataclass
class TicketData:
    user_id: int
    guild_id: int
    channel_id: int
    ticket_type: str  # "review" или "support"
    status: str = "open"  # "open", "closed", "published"
    message_link: Optional[str] = None