"""Game constants and configuration."""

from enum import Enum
from typing import Dict, List

# ======================
# Game Modes
# ======================


class GameMode(str, Enum):
    """Game mode enumeration."""
    BEER_GAME = "beer_game"
    FACTORY_MODE = "factory_mode"
    CAMPAIGN = "campaign"


# ======================
# Beer Game Constants
# ======================

BEER_GAME_CONFIG = {
    "roles": ["Shop", "Retailer", "Wholesaler", "Factory"],
    "max_players_per_chain": 4,
    "order_delay_weeks": 4,
    "default_weeks": 52,
    "default_demand_pattern": "sine_wave",
    "initial_inventory": 100,
    "holding_cost_per_unit": 0.5,
    "stockout_cost_per_unit": 2.0,
}

# Beer Game Role constants
ROLE_SHOP = "Shop"
ROLE_RETAILER = "Retailer"
ROLE_WHOLESALER = "Wholesaler"
ROLE_FACTORY = "Factory"

BEER_GAME_ROLES = [ROLE_SHOP, ROLE_RETAILER, ROLE_WHOLESALER, ROLE_FACTORY]

# Demand patterns
DEMAND_PATTERNS = {
    "sine_wave": "Sine wave pattern",
    "step": "Step function pattern",
    "random": "Random pattern",
    "constant": "Constant demand",
}


# ======================
# Factory Game Constants
# ======================


class MachineType(str, Enum):
    """Machine types in factory."""
    MINER = "miner"
    SMELTER = "smelter"
    ASSEMBLER = "assembler"
    CRAFTER = "crafter"
    CHEST = "chest"
    CONVEYOR = "conveyor"
    POWER_PLANT = "power_plant"
    LAB = "lab"


FACTORY_MACHINES: Dict[str, Dict] = {
    "miner": {
        "name": "Miner",
        "description": "Extract raw ores from the ground",
        "width": 1,
        "height": 1,
        "power_consumption": 0.3,
        "speed": 0.5,
        "inputs": [],
        "outputs": ["iron_ore", "copper_ore", "stone"],
    },
    "smelter": {
        "name": "Smelter",
        "description": "Smelt ores into metals",
        "width": 1,
        "height": 1,
        "power_consumption": 1.5,
        "speed": 1.0,
        "inputs": ["iron_ore", "copper_ore"],
        "outputs": ["iron_plate", "copper_plate"],
    },
    "assembler": {
        "name": "Assembler",
        "description": "Assemble complex items",
        "width": 2,
        "height": 1,
        "power_consumption": 2.0,
        "speed": 1.0,
        "inputs": ["iron_plate", "copper_plate", "plastic"],
        "outputs": ["gears", "circuits", "motors"],
    },
    "conveyor": {
        "name": "Conveyor Belt",
        "description": "Transport items between machines",
        "width": 1,
        "height": 1,
        "power_consumption": 0.1,
        "speed": 5.0,
        "inputs": ["*"],
        "outputs": ["*"],
    },
    "chest": {
        "name": "Chest",
        "description": "Store items",
        "width": 1,
        "height": 1,
        "power_consumption": 0,
        "speed": 0,
        "inputs": ["*"],
        "outputs": ["*"],
        "capacity": 1000,
    },
    "power_plant": {
        "name": "Power Plant",
        "description": "Generate electrical power",
        "width": 1,
        "height": 1,
        "power_consumption": -5.0,  # Negative = produces power
        "speed": 1.0,
        "inputs": ["coal"],
        "outputs": [],
    },
}

FACTORY_RECIPES = {
    "iron_plate": {
        "name": "Iron Plate",
        "inputs": {"iron_ore": 1},
        "output": 1,
        "time": 3.2,
        "machine": "smelter",
    },
    "copper_plate": {
        "name": "Copper Plate",
        "inputs": {"copper_ore": 1},
        "output": 1,
        "time": 3.2,
        "machine": "smelter",
    },
    "gears": {
        "name": "Gears",
        "inputs": {"iron_plate": 2},
        "output": 1,
        "time": 0.5,
        "machine": "assembler",
    },
    "circuits": {
        "name": "Electronic Circuits",
        "inputs": {"copper_plate": 3, "iron_plate": 1},
        "output": 1,
        "time": 0.5,
        "machine": "assembler",
    },
    "motors": {
        "name": "Motors",
        "inputs": {"iron_plate": 2, "copper_plate": 1, "gears": 3},
        "output": 1,
        "time": 5.0,
        "machine": "assembler",
    },
}

FACTORY_DIFFICULTY_LEVELS = {
    "easy": {"production_target": 10,
             "time_limit_minutes": 30,
             "starting_resources": {"iron_ore": 100, "copper_ore": 50}},
    "normal": {"production_target": 50,
               "time_limit_minutes": 20,
               "starting_resources": {"iron_ore": 50, "copper_ore": 25}},
    "hard": {"production_target": 100,
             "time_limit_minutes": 10,
             "starting_resources": {"iron_ore": 25, "copper_ore": 10}},
}

# ======================
# Game Grid
# ======================

GRID_WIDTH = 100
GRID_HEIGHT = 100
GRID_CELL_SIZE = 32  # pixels

# ======================
# Scoring
# ======================

BEER_GAME_SCORING = {
    "inventory_holding_cost": 0.5,
    "backorder_cost": 2.0,
    "excess_production_penalty": 0.1,
}

FACTORY_SCORING = {
    "time_bonus_per_second": 1.0,
    "efficiency_factor": 2.0,
    "resource_waste_penalty": 1.0,
}

# ======================
# Database
# ======================

MONGO_COLLECTIONS = {
    "games": "games",
    "players": "players",
    "supply_chains": "supply_chains",
    "orders": "orders",
    "inventory": "inventory",
    "factory_states": "factory_states",
    "analytics": "analytics",
}

# ======================
# Logging
# ======================

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
