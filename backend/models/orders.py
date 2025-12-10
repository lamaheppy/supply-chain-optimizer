"""Order model for supply chain."""

from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Order:
    """Represents an order in the supply chain."""
    
    order_id: str
    from_role: str  # "Shop", "Retailer", "Wholesaler", "Factory"
    to_role: str
    supply_chain_id: str
    game_id: str
    quantity: int
    status: OrderStatus = OrderStatus.PENDING
    created_week: int = 0
    delivery_week: int = 0  # Week when order arrives
    actual_delivery_week: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def is_delayed(self, current_week: int) -> bool:
        """Check if order is delayed."""
        if self.status == OrderStatus.DELIVERED:
            return (self.actual_delivery_week or 0) > self.delivery_week
        return current_week > self.delivery_week and self.status != OrderStatus.DELIVERED
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "order_id": self.order_id,
            "from_role": self.from_role,
            "to_role": self.to_role,
            "supply_chain_id": self.supply_chain_id,
            "game_id": self.game_id,
            "quantity": self.quantity,
            "status": self.status.value,
            "created_week": self.created_week,
            "delivery_week": self.delivery_week,
            "actual_delivery_week": self.actual_delivery_week,
            "created_at": self.created_at,
        }
