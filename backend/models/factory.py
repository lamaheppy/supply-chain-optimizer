"""Factory model for Factory Game mode."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime


@dataclass
class Machine:
    """Represents a machine in the factory."""
    
    machine_id: str
    machine_type: str  # "miner", "smelter", "assembler", "conveyor", "chest", etc.
    x: int  # Grid position
    y: int  # Grid position
    width: int = 1
    height: int = 1
    rotation: int = 0  # 0, 90, 180, 270
    power_level: float = 1.0  # 0.0 to 1.0
    is_active: bool = True
    input_items: Dict[str, int] = field(default_factory=dict)
    output_items: Dict[str, int] = field(default_factory=dict)
    current_recipe: Optional[str] = None
    progress: float = 0.0  # 0.0 to 1.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "rotation": self.rotation,
            "power_level": self.power_level,
            "is_active": self.is_active,
            "input_items": self.input_items,
            "output_items": self.output_items,
            "current_recipe": self.current_recipe,
            "progress": self.progress,
            "created_at": self.created_at,
        }


@dataclass
class Factory:
    """Represents a player's factory."""
    
    factory_id: str
    player_id: str
    game_id: str
    width: int = 100
    height: int = 100
    machines: Dict[str, Machine] = field(default_factory=dict)
    global_inventory: Dict[str, int] = field(default_factory=dict)
    power_available: float = 10.0
    power_used: float = 0.0
    production_rate: float = 0.0
    efficiency: float = 1.0
    current_week: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def add_machine(self, machine: Machine) -> bool:
        """Add a machine to the factory.
        
        Returns:
            True if machine was added successfully
        """
        # Check if position is valid
        if self._is_position_valid(machine.x, machine.y, machine.width, machine.height):
            self.machines[machine.machine_id] = machine
            return True
        return False
    
    def remove_machine(self, machine_id: str) -> bool:
        """Remove a machine from the factory."""
        if machine_id in self.machines:
            del self.machines[machine_id]
            return True
        return False
    
    def _is_position_valid(self, x: int, y: int, width: int, height: int) -> bool:
        """Check if position is valid (no overlap, within bounds)."""
        if x < 0 or y < 0 or x + width > self.width or y + height > self.height:
            return False
        
        # Check for overlap with existing machines
        for machine in self.machines.values():
            if self._check_overlap(x, y, width, height, machine.x, machine.y, machine.width, machine.height):
                return False
        
        return True
    
    @staticmethod
    def _check_overlap(x1: int, y1: int, w1: int, h1: int,
                      x2: int, y2: int, w2: int, h2: int) -> bool:
        """Check if two rectangles overlap."""
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)
    
    def get_total_power_consumption(self) -> float:
        """Calculate total power consumption."""
        from ..core.constants import FACTORY_MACHINES
        total = 0.0
        for machine in self.machines.values():
            if machine.is_active and machine.machine_type in FACTORY_MACHINES:
                consumption = FACTORY_MACHINES[machine.machine_type]["power_consumption"]
                total += consumption * machine.power_level
        return total
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "factory_id": self.factory_id,
            "player_id": self.player_id,
            "game_id": self.game_id,
            "width": self.width,
            "height": self.height,
            "machines": {k: v.to_dict() for k, v in self.machines.items()},
            "global_inventory": self.global_inventory,
            "power_available": self.power_available,
            "power_used": self.get_total_power_consumption(),
            "production_rate": self.production_rate,
            "efficiency": self.efficiency,
            "current_week": self.current_week,
            "created_at": self.created_at,
        }
