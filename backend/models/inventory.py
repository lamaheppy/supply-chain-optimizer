"""Inventory model."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InventoryItem:
    """Represents an inventory item."""
    
    item_id: str
    name: str
    quantity: int = 0
    max_quantity: int = 10000
    unit_holding_cost: float = 0.5
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "quantity": self.quantity,
            "max_quantity": self.max_quantity,
            "unit_holding_cost": self.unit_holding_cost,
        }


@dataclass
class Inventory:
    """Represents a player's inventory."""
    
    player_id: str
    items: Dict[str, InventoryItem] = field(default_factory=dict)
    
    def add_item(self, item: InventoryItem) -> None:
        """Add or update an inventory item."""
        self.items[item.item_id] = item
    
    def get_item(self, item_id: str) -> InventoryItem:
        """Get an inventory item by ID."""
        if item_id not in self.items:
            self.items[item_id] = InventoryItem(item_id=item_id, name=item_id)
        return self.items[item_id]
    
    def get_quantity(self, item_id: str) -> int:
        """Get quantity of an item."""
        return self.get_item(item_id).quantity
    
    def add_quantity(self, item_id: str, quantity: int) -> bool:
        """Add quantity to an item."""
        item = self.get_item(item_id)
        new_quantity = item.quantity + quantity
        if new_quantity <= item.max_quantity:
            item.quantity = new_quantity
            return True
        return False
    
    def remove_quantity(self, item_id: str, quantity: int) -> int:
        """Remove quantity from an item.
        
        Returns:
            Actual quantity removed
        """
        item = self.get_item(item_id)
        removed = min(item.quantity, quantity)
        item.quantity -= removed
        return removed
    
    def get_total_cost(self) -> float:
        """Calculate total inventory holding cost."""
        return sum(
            max(0, item.quantity) * item.unit_holding_cost
            for item in self.items.values()
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "player_id": self.player_id,
            "items": {k: v.to_dict() for k, v in self.items.items()},
            "total_cost": self.get_total_cost(),
        }
