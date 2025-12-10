# 🏭 Supply Chain Optimizer

> A comprehensive supply chain optimization game combining strategic Beer Game turn-based mechanics with real-time PyFactory-style factory building.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-orange.svg)]()

## 🎮 Overview

**Supply Chain Optimizer** merges two powerful supply chain concepts:

### Beer Game Mode 🍺
- **Turn-based multiplayer supply chain management**
- Multiple competing supply chains racing against each other
- Roles: Shop, Retailer, Wholesaler, Factory
- Strategic ordering and inventory management
- 4-week order fulfillment delays
- Real-time host dashboard

### Factory Mode 🏗️
- **Real-time factory building and optimization**
- Place production machines (conveyor belts, assemblers, furnaces)
- Recipe-based crafting system
- Resource management and optimization puzzles
- Grid-based factory layout system
- Production efficiency metrics

### Campaign Mode 🎯
- **Combined gameplay**: Integrate Beer Game decision-making with Factory optimization
- Manage supply chains while optimizing factory production
- Balance strategic planning with real-time execution
- Progressive difficulty levels

---

## 🚀 Features

### Core Gameplay
- ✅ Multiplayer turn-based supply chain management (Beer Game)
- ✅ Real-time factory building system (PyFactory)
- ✅ Idempotent operations for data consistency
- ✅ MongoDB integration for game persistence
- ✅ WebSocket real-time synchronization
- ✅ Advanced analytics and performance tracking

### UI/UX
- 📊 Host dashboard with all supply chains visible
- ⏱️ Player-specific countdown timers
- 📈 Historical charts and trend analysis
- 🎨 Intuitive factory grid interface
- 📱 Responsive design for multiple devices

### Architecture
- 🏗️ Modular, extensible design
- 🔄 Event-driven system for state management
- 📋 Comprehensive logging and debugging
- 🧪 >90% test coverage (target)
- 🐳 Docker support for easy deployment

---

## 📦 Project Structure

```
supply-chain-optimizer/
├── backend/
│   ├── core/
│   │   ├── game_engine.py          # Main game loop and state management
│   │   ├── constants.py            # Game constants and config
│   │   └── utils.py                # Utility functions
│   ├── models/
│   │   ├── supply_chain.py         # Beer Game supply chain logic
│   │   ├── factory.py              # Factory system and machines
│   │   ├── inventory.py            # Inventory management
│   │   ├── recipes.py              # Production recipes
│   │   └── orders.py               # Order management system
│   ├── services/
│   │   ├── game_service.py         # Game flow orchestration
│   │   ├── multiplayer_service.py  # Multiplayer synchronization
│   │   ├── analytics_service.py    # Performance metrics
│   │   └── persistence_service.py  # Database operations
│   ├── database/
│   │   ├── mongo_client.py         # MongoDB operations
│   │   └── migrations/             # Database schemas
│   └── api/
│       └── routes.py               # API endpoints
├── frontend/
│   ├── pages/
│   │   ├── 01_beer_game.py         # Beer Game UI (Streamlit)
│   │   ├── 02_factory_game.py      # Factory Mode UI
│   │   ├── 03_campaign.py          # Campaign Mode
│   │   └── 04_analytics.py         # Analytics Dashboard
│   ├── components/
│   │   ├── beer_components.py      # Beer Game UI components
│   │   ├── factory_components.py   # Factory UI components
│   │   └── shared.py               # Shared UI components
│   └── app.py                      # Main Streamlit app
├── tests/
│   ├── unit/
│   │   ├── test_supply_chain.py
│   │   ├── test_factory.py
│   │   ├── test_inventory.py
│   │   └── test_orders.py
│   ├── integration/
│   │   ├── test_game_flow.py
│   │   └── test_multiplayer.py
│   └── conftest.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── requirements-test.txt
├── Makefile
├── .gitignore
├── .env.example
└── LICENSE
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**
- **Streamlit** - Web framework
- **MongoDB** - Database
- **Redis** - Real-time state management
- **FastAPI** (optional) - REST API
- **WebSocket** - Real-time communication

### Testing
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **pytest-asyncio** - Async testing
- **mongomock** - MongoDB mocking

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD

---

## 📋 Game Mechanics

### Beer Game Mechanics 🍺

**Supply Chain Structure:**
```
Customer → Shop → Retailer → Wholesaler → Factory
```

**Weekly Cycle:**
1. **Host Phase**
   - Refresh to see current status
   - Place customer orders (triggers shop to buy)
   
2. **Shop Phase** (Player 1)
   - Refresh inventory (items arrive from 4 weeks ago)
   - View customer demand
   - Place wholesale order
   
3. **Retailer Phase** (Player 2)
   - Refresh inventory
   - View shop orders
   - Place order to wholesaler
   
4. **Wholesaler Phase** (Player 3)
   - Refresh inventory
   - View retailer orders
   - Place order to factory
   
5. **Factory Phase** (Player 4)
   - Refresh inventory
   - View wholesaler orders
   - Produce items

**Scoring System:**
- Lower inventory holding cost = better score
- Lower backorder cost = better score
- Efficiency penalty for excess production
- Supply chain bullwhip effect penalties

---

### Factory Game Mechanics 🏗️

**Machine Types:**
- 🪛 **Miners** - Extract raw resources
- 🏭 **Smelters** - Process ore into metal
- ⚙️ **Assemblers** - Combine items into products
- 🔧 **Crafters** - Transform materials
- 📦 **Chests** - Storage buffers
- 🚚 **Conveyor Belts** - Item transport
- 🔌 **Power Generation** - Energy system

**Factory Optimization:**
- Place machines on grid
- Connect with conveyor belts
- Manage energy/resources
- Optimize production ratios
- Balance supply and demand

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional)
- MongoDB (local or Atlas)
- Redis (local or Cloud)

### Local Setup

```bash
# Clone repository
git clone https://github.com/lamaheppy/supply-chain-optimizer.git
cd supply-chain-optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB and Redis credentials

# Run tests
make test

# Run application
streamlit run frontend/app.py
```

### Docker Setup

```bash
docker-compose up -d

# Access at http://localhost:8501
```

---

## 📖 Usage

### Starting a Beer Game

1. **Host creates game**
   - Set `game_id`
   - Select number of supply chains (1-4)
   - Set game parameters (weeks, demand pattern)

2. **Players join**
   - Enter `game_id`
   - Select `player_id` (supply chain)
   - Select `player_role` (Shop/Retailer/Wholesaler/Factory)

3. **Play each week**
   - Host: Click "Refresh" → "Place Order" → "Next Week"
   - Players: Click "Refresh" → view demand → "Place Order"

### Starting Factory Mode

1. **Select scenario**
   - Choose production target (e.g., "produce 100 gears/min")
   - Select difficulty level

2. **Build factory**
   - Drag machines onto grid
   - Place conveyor belts
   - Connect production chains

3. **Optimize**
   - Monitor production rates
   - Adjust ratios
   - Solve production puzzles

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/unit/test_supply_chain.py

# Run integration tests only
pytest tests/integration/
```

---

## 📊 Game Analytics

The analytics dashboard provides:
- 📈 **Supply Chain Charts**: Inventory, costs, demand over time
- 🎯 **Factory Metrics**: Production rate, efficiency, bottlenecks
- 🏆 **Player Rankings**: Scores and performance comparison
- 🔍 **Detailed Breakdown**: Cost analysis, resource flows

---

## 🎯 Roadmap

### Phase 1 ✅ (MVP)
- [x] Beer Game core mechanics
- [x] Factory system basics
- [x] Multiplayer synchronization
- [x] Basic UI

### Phase 2 🏗️ (Current)
- [ ] Advanced factory recipes
- [ ] Campaign mode integration
- [ ] UI test coverage
- [ ] Performance optimization
- [ ] Mobile responsiveness

### Phase 3 📋 (Future)
- [ ] AI opponents
- [ ] Advanced tutorials
- [ ] Leaderboards
- [ ] Replay system
- [ ] Mod support
- [ ] Graph visualization

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Original Beer Game** - [wirelessr/beer_game](https://github.com/wirelessr/beer_game)
- **Original PyFactory** - [chanrt/py-factory](https://github.com/chanrt/py-factory)
- **Combined Project** - Supply Chain Optimizer Contributors

---

## 📧 Contact

Have questions or suggestions? 
- Open an issue on GitHub
- Check discussions for questions
- See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

## 🙏 Acknowledgments

- Beer Game concept from MIT System Dynamics
- Factorio by Wube Software
- Inspired by supply chain management and operations research

---

**Built with ❤️ for supply chain enthusiasts and game developers**
