"""Main game engine for Supply Chain Optimizer."""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from backend.core.constants import (
    BEER_GAME_CONFIG, BEER_GAME_ROLES, BEER_GAME_SCORING,
    GameMode, ORDER_DELAY_WEEKS
)
from backend.core.utils import (
    generate_id, generate_game_id, generate_player_id,
    calculate_demand, calculate_inventory_cost, calculate_backorder_cost,
    get_timestamp
)
from backend.models import (
    SupplyChain, SupplyChainNode, Order, OrderStatus
)

logger = logging.getLogger(__name__)


class BeerGameEngine:
    """Game engine for Beer Game mode."""
    
    def __init__(self):
        """Initialize the Beer Game engine."""
        self.games: Dict[str, Dict] = {}  # game_id -> game state
        self.supply_chains: Dict[str, SupplyChain] = {}  # chain_id -> supply chain
        self.orders: Dict[str, List[Order]] = {}  # chain_id -> orders list
        self.order_queue: Dict[str, List[int]] = {}  # chain_id -> upcoming orders
        
    def create_game(self, num_chains: int = 1, weeks: int = 52,
                   demand_pattern: str = "sine_wave") -> str:
        """Create a new Beer Game.
        
        Args:
            num_chains: Number of competing supply chains
            weeks: Number of weeks to play
            demand_pattern: Customer demand pattern
            
        Returns:
            Game ID
        """
        game_id = generate_game_id()
        
        self.games[game_id] = {
            "game_id": game_id,
            "num_chains": num_chains,
            "weeks": weeks,
            "demand_pattern": demand_pattern,
            "current_week": 0,
            "started_at": get_timestamp(),
            "status": "waiting",  # waiting, playing, finished
            "supply_chains": [],
        }
        
        # Create supply chains
        for i in range(num_chains):
            chain_id = f"{game_id}_chain_{i}"
            supply_chain = SupplyChain(chain_id=chain_id, game_id=game_id)
            self.supply_chains[chain_id] = supply_chain
            self.games[game_id]["supply_chains"].append(chain_id)
            self.orders[chain_id] = []
            self.order_queue[chain_id] = []
        
        logger.info(f"Created game {game_id} with {num_chains} supply chains")
        return game_id
    
    def join_game(self, game_id: str, supply_chain_id: str, role: str,
                 player_name: str) -> Optional[str]:
        """Join a game as a specific role.
        
        Args:
            game_id: Game ID
            supply_chain_id: Supply chain to join
            role: Role to play (Shop, Retailer, Wholesaler, Factory)
            player_name: Player name
            
        Returns:
            Player ID if successful
        """
        if game_id not in self.games:
            logger.error(f"Game {game_id} not found")
            return None
        
        if role not in BEER_GAME_ROLES:
            logger.error(f"Invalid role: {role}")
            return None
        
        chain_id = f"{game_id}_{supply_chain_id}"
        if chain_id not in self.supply_chains:
            logger.error(f"Supply chain {chain_id} not found")
            return None
        
        player_id = generate_player_id()
        supply_chain = self.supply_chains[chain_id]
        
        # Create player node
        node = SupplyChainNode(
            role=role,
            player_id=player_id,
            player_name=player_name,
            inventory=BEER_GAME_CONFIG["initial_inventory"],
        )
        
        supply_chain.set_node(role, node)
        logger.info(f"Player {player_name} ({player_id}) joined as {role}")
        
        return player_id
    
    def place_customer_order(self, game_id: str, chain_id: str, week: int,
                            quantity: int) -> bool:
        """Place a customer order for the supply chain.
        
        Args:
            game_id: Game ID
            chain_id: Supply chain ID
            week: Week number
            quantity: Order quantity
            
        Returns:
            True if order was placed
        """
        full_chain_id = f"{game_id}_{chain_id}"
        if full_chain_id not in self.supply_chains:
            logger.error(f"Supply chain {full_chain_id} not found")
            return False
        
        supply_chain = self.supply_chains[full_chain_id]
        if supply_chain.shop:
            supply_chain.shop.incoming_order = quantity
            return True
        
        return False
    
    def process_order(self, game_id: str, chain_id: str, from_role: str,
                     to_role: str, quantity: int) -> Optional[str]:
        """Process an order from one role to another.
        
        Args:
            game_id: Game ID
            chain_id: Supply chain ID
            from_role: Role placing the order
            to_role: Role receiving the order
            quantity: Order quantity
            
        Returns:
            Order ID if successful
        """
        full_chain_id = f"{game_id}_{chain_id}"
        supply_chain = self.supply_chains.get(full_chain_id)
        
        if not supply_chain:
            return None
        
        from_node = supply_chain.get_node(from_role)
        to_node = supply_chain.get_node(to_role)
        
        if not from_node or not to_node:
            return None
        
        # Create order
        order_id = generate_id("order")
        current_week = supply_chain.current_week
        delivery_week = current_week + ORDER_DELAY_WEEKS
        
        order = Order(
            order_id=order_id,
            from_role=from_role,
            to_role=to_role,
            supply_chain_id=full_chain_id,
            game_id=game_id,
            quantity=quantity,
            created_week=current_week,
            delivery_week=delivery_week,
        )
        
        self.orders[full_chain_id].append(order)
        from_node.current_order = quantity
        
        logger.info(f"Order created: {order_id} from {from_role} to {to_role} ({quantity} units)")
        return order_id
    
    def advance_week(self, game_id: str) -> bool:
        """Advance game by one week.
        
        Args:
            game_id: Game ID
            
        Returns:
            True if week was advanced
        """
        if game_id not in self.games:
            logger.error(f"Game {game_id} not found")
            return False
        
        game = self.games[game_id]
        game["current_week"] += 1
        
        # Process all supply chains
        for chain_id in game["supply_chains"]:
            self._process_supply_chain_week(game_id, chain_id, game["current_week"])
        
        logger.info(f"Game {game_id} advanced to week {game['current_week']}")
        return True
    
    def _process_supply_chain_week(self, game_id: str, chain_index: int,
                                  current_week: int) -> None:
        """Process a supply chain for one week.
        
        Args:
            game_id: Game ID
            chain_index: Supply chain index
            current_week: Current week number
        """
        chain_id = f"{game_id}_chain_{chain_index}"
        supply_chain = self.supply_chains.get(chain_id)
        
        if not supply_chain:
            return
        
        supply_chain.current_week = current_week
        
        # Process each node
        for node in supply_chain.get_nodes():
            if node:
                self._process_node_week(supply_chain, node, current_week)
    
    def _process_node_week(self, supply_chain: SupplyChain,
                          node: SupplyChainNode, current_week: int) -> None:
        """Process a node for one week.
        
        Args:
            supply_chain: Supply chain instance
            node: Node to process
            current_week: Current week number
        """
        # 1. Receive incoming items from orders placed 4 weeks ago
        incoming = self._get_incoming_orders(supply_chain.chain_id, node.role, current_week)
        node.inventory += sum(order.quantity for order in incoming)
        
        # 2. Fulfill outgoing demand
        # Get demand from downstream (or incoming order for shop)
        demand = node.incoming_order
        
        # Fulfill as much as possible
        fulfilled = min(node.inventory, demand)
        node.inventory -= fulfilled
        
        # Track backorder
        if fulfilled < demand:
            node.backorder += demand - fulfilled
        else:
            node.backorder = 0
        
        # 3. Calculate costs
        holding_cost = calculate_inventory_cost(
            node.inventory,
            BEER_GAME_CONFIG["holding_cost_per_unit"]
        )
        stockout_cost = calculate_backorder_cost(
            node.backorder,
            BEER_GAME_CONFIG["stockout_cost_per_unit"]
        )
        node.total_cost += holding_cost + stockout_cost
        
        # 4. Track history
        node.orders_history.append(node.current_order)
        node.inventory_history.append(node.inventory)
    
    def _get_incoming_orders(self, chain_id: str, role: str,
                            current_week: int) -> List[Order]:
        """Get orders that arrive this week.
        
        Args:
            chain_id: Supply chain ID
            role: Role receiving orders
            current_week: Current week
            
        Returns:
            List of incoming orders
        """
        incoming = []
        for order in self.orders.get(chain_id, []):
            if order.to_role == role and order.delivery_week == current_week:
                order.status = OrderStatus.DELIVERED
                order.actual_delivery_week = current_week
                incoming.append(order)
        return incoming
    
    def get_game_state(self, game_id: str) -> Optional[Dict]:
        """Get current game state.
        
        Args:
            game_id: Game ID
            
        Returns:
            Game state dictionary
        """
        if game_id not in self.games:
            return None
        
        game = self.games[game_id]
        chains = []
        
        for chain_id in game["supply_chains"]:
            supply_chain = self.supply_chains[chain_id]
            chains.append(supply_chain.to_dict())
        
        return {
            "game_id": game["game_id"],
            "status": game["status"],
            "current_week": game["current_week"],
            "weeks": game["weeks"],
            "demand_pattern": game["demand_pattern"],
            "supply_chains": chains,
        }


# Constants that should be in core/constants.py
ORDER_DELAY_WEEKS = 4
