"""Utility functions for the game."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID."""
    unique_id = str(uuid4())[:8]
    return f"{prefix}_{unique_id}" if prefix else unique_id


def generate_game_id() -> str:
    """Generate a unique game ID."""
    return generate_id("game")


def generate_player_id() -> str:
    """Generate a unique player ID."""
    return generate_id("player")


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def calculate_demand(pattern: str, week: int, amplitude: int = 10, offset: int = 5) -> int:
    """Calculate demand based on pattern.
    
    Args:
        pattern: Demand pattern type (sine_wave, step, random, constant)
        week: Week number
        amplitude: Amplitude of demand variation
        offset: Base demand offset
        
    Returns:
        Demand value for the week
    """
    import math
    import random
    
    if pattern == "sine_wave":
        return int(amplitude * math.sin(week * 0.1) + offset)
    elif pattern == "step":
        return amplitude if (week // 10) % 2 == 0 else offset
    elif pattern == "random":
        return random.randint(offset - amplitude // 2, offset + amplitude // 2)
    elif pattern == "constant":
        return offset
    else:
        return offset


def calculate_inventory_cost(quantity: int, cost_per_unit: float) -> float:
    """Calculate inventory holding cost.
    
    Args:
        quantity: Inventory quantity
        cost_per_unit: Cost per unit per week
        
    Returns:
        Total holding cost
    """
    return max(0, quantity) * cost_per_unit


def calculate_backorder_cost(quantity: int, cost_per_unit: float) -> float:
    """Calculate backorder cost.
    
    Args:
        quantity: Backorder quantity (negative inventory)
        cost_per_unit: Cost per unit per week
        
    Returns:
        Total backorder cost
    """
    return max(0, -quantity) * cost_per_unit


def safe_json_encode(obj: Any) -> str:
    """Safely encode object to JSON.
    
    Args:
        obj: Object to encode
        
    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, default=str)
    except Exception as e:
        logger.error(f"JSON encoding error: {e}")
        return "{}"


def safe_json_decode(json_str: str) -> Dict[str, Any]:
    """Safely decode JSON string.
    
    Args:
        json_str: JSON string to decode
        
    Returns:
        Decoded dictionary
    """
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"JSON decoding error: {e}")
        return {}


def deep_merge(base: Dict, updates: Dict) -> Dict:
    """Recursively merge dictionaries.
    
    Args:
        base: Base dictionary
        updates: Updates to merge
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    for key, value in updates.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_email(email: str) -> bool:
    """Validate email format.
    
    Args:
        email: Email address
        
    Returns:
        True if valid email format
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))
