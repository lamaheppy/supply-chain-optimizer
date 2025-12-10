"""Supply chain model for Beer Game."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class SupplyChainNode:
    """Represents a node in the supply chain (Shop, Retailer, etc.)."""
    
    role: str  # "Shop", "Retailer", "Wholesaler", "Factory"
    player_id: str
    player_name: str
    inventory: int = 100
    backorder: int = 0
    current_order: int = 0
    incoming_order: int = 0  # Order from downstream (upstream perspective)
    total_cost: float = 0.0
    orders_history: List[int] = field(default_factory=list)
    inventory_history: List[int] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "role": self.role,
            "player_id": self.player_id,
            "player_name": self.player_name,
            "inventory": self.inventory,
            "backorder": self.backorder,
            "current_order": self.current_order,
            "incoming_order": self.incoming_order,
            "total_cost": self.total_cost,
            "orders_history": self.orders_history[-52:],  # Keep last year
            "inventory_history": self.inventory_history[-52:],
        }


@dataclass
class SupplyChain:
    """Represents a supply chain with multiple nodes."""
    
    chain_id: str
    game_id: str
    shop: Optional[SupplyChainNode] = None
    retailer: Optional[SupplyChainNode] = None
    wholesaler: Optional[SupplyChainNode] = None
    factory: Optional[SupplyChainNode] = None
    current_week: int = 0
    total_cost: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def get_node(self, role: str) -> Optional[SupplyChainNode]:
        """Get a node by role."""
        nodes = {
            "Shop": self.shop,
            "Retailer": self.retailer,
            "Wholesaler": self.wholesaler,
            "Factory": self.factory,
        }
        return nodes.get(role)
    
    def set_node(self, role: str, node: SupplyChainNode) -> None:
        """Set a node by role."""
        if role == "Shop":
            self.shop = node
        elif role == "Retailer":
            self.retailer = node
        elif role == "Wholesaler":
            self.wholesaler = node
        elif role == "Factory":
            self.factory = node
    
    def get_nodes(self) -> List[SupplyChainNode]:
        """Get all nodes."""
        return [n for n in [self.shop, self.retailer, self.wholesaler, self.factory] if n]
    
    def calculate_total_cost(self) -> float:
        """Calculate total supply chain cost."""
        return sum(node.total_cost for node in self.get_nodes())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "chain_id": self.chain_id,
            "game_id": self.game_id,
            "shop": self.shop.to_dict() if self.shop else None,
            "retailer": self.retailer.to_dict() if self.retailer else None,
            "wholesaler": self.wholesaler.to_dict() if self.wholesaler else None,
            "factory": self.factory.to_dict() if self.factory else None,
            "current_week": self.current_week,
            "total_cost": self.calculate_total_cost(),
            "created_at": self.created_at,
        }
