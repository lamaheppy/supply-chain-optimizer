"""Main Streamlit application for Supply Chain Optimizer."""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="Supply Chain Optimizer",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-text {
        color: #09ab3b;
        font-weight: bold;
    }
    .error-text {
        color: #d33c3c;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    
    # Sidebar navigation
    st.sidebar.title("🏭 Supply Chain Optimizer")
    
    if "session_initialized" not in st.session_state:
        st.session_state.session_initialized = True
        st.session_state.game_mode = None
        st.session_state.game_id = None
        st.session_state.player_id = None
        st.session_state.role = None
    
    mode = st.sidebar.radio(
        "Select Game Mode",
        options=["🏠 Home", "🍺 Beer Game", "🏭 Factory Mode", "⚔️ Campaign", "📊 Analytics"],
        index=0,
    )
    
    # Route to appropriate page
    if mode == "🏠 Home":
        show_home()
    elif mode == "🍺 Beer Game":
        show_beer_game()
    elif mode == "🏭 Factory Mode":
        show_factory_mode()
    elif mode == "⚔️ Campaign":
        show_campaign()
    elif mode == "📊 Analytics":
        show_analytics()


def show_home():
    """Display home page."""
    st.title("🏭 Supply Chain Optimizer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://img.icons8.com/color/96/000000/factory.png", width=100)
        st.markdown("""
        ## Welcome!
        
        Choose a game mode to get started:
        
        ### 🍺 Beer Game
        Turn-based multiplayer supply chain management. 
        Compete with other players to minimize costs while satisfying demand.
        
        **Features:**
        - Multiple competing supply chains
        - Real-time host dashboard
        - Strategic ordering with 4-week delays
        - Detailed analytics
        """)
    
    with col2:
        st.image("https://img.icons8.com/color/96/000000/production.png", width=100)
        st.markdown("""
        ### 🏭 Factory Mode
        Real-time factory building and optimization.
        Design efficient production lines using machines and conveyors.
        
        **Features:**
        - Place machines and design layouts
        - Recipe-based production system
        - Resource optimization puzzles
        - Progressive difficulty levels
        """)
    
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        ### ⚔️ Campaign Mode
        Combine both game modes for ultimate challenge.
        Manage supply chains while optimizing factory production.
        """)
    
    with col4:
        st.markdown("""
        ### 📊 Analytics
        View detailed game statistics and performance metrics.
        - Supply chain cost analysis
        - Factory efficiency reports
        - Player rankings and comparisons
        """)
    
    st.divider()
    st.markdown("""
    ### 📖 How to Play
    
    **Beer Game:**
    1. Host creates a game with multiple supply chains
    2. Players join as different roles (Shop, Retailer, Wholesaler, Factory)
    3. Each week: refresh inventory → view orders → place new orders
    4. Orders take 4 weeks to arrive
    5. Goal: Minimize total supply chain costs
    
    **Factory Mode:**
    1. Select a production scenario and difficulty
    2. Build your factory by placing machines
    3. Connect machines with conveyor belts
    4. Optimize production to meet targets
    5. Achieve bonuses for efficiency and speed
    
    ---
    
    **Need Help?** Check the [GitHub Repository](https://github.com/lamaheppy/supply-chain-optimizer)
    """)


def show_beer_game():
    """Display Beer Game."""
    st.title("🍺 Beer Game")
    
    mode_tab = st.radio("Select Mode", ["Host", "Player"], horizontal=True)
    
    if mode_tab == "Host":
        show_beer_game_host()
    else:
        show_beer_game_player()


def show_beer_game_host():
    """Display Beer Game host interface."""
    st.subheader("Host Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📊 Create or manage games here")
        
        with st.form("create_game_form"):
            st.write("Create New Game")
            num_chains = st.slider("Number of Supply Chains", 1, 4, 2)
            weeks = st.slider("Number of Weeks", 10, 52, 20)
            demand_pattern = st.selectbox(
                "Demand Pattern",
                ["sine_wave", "step", "random", "constant"]
            )
            
            if st.form_submit_button("Create Game"):
                st.success(f"Game created! Share ID with players")
                st.write(f"Game ID: `GAME_12345`") # Placeholder
    
    with col2:
        st.info("👥 Monitor players joining")
        st.write("Active Players:")
        st.write("- Player 1 (Shop)")
        st.write("- Player 2 (Retailer)")
        st.write("- Player 3 (Wholesaler)")
    
    with col3:
        st.info("⏱️ Game Status")
        st.metric("Current Week", "5/20", delta="+1")
        st.metric("Status", "In Progress")


def show_beer_game_player():
    """Display Beer Game player interface."""
    st.subheader("Player Dashboard")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.write("### Join Game")
        with st.form("join_game_form"):
            game_id = st.text_input("Game ID")
            chain_id = st.number_input("Chain ID", 0, 3)
            role = st.selectbox("Role", ["Shop", "Retailer", "Wholesaler", "Factory"])
            player_name = st.text_input("Your Name")
            
            if st.form_submit_button("Join Game"):
                st.success(f"Joined as {role}!")
    
    with col2:
        st.write("### Game State (Example)")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Inventory", "150 units", delta="+20")
        col_b.metric("Incoming Order", "80 units", delta="-5")
        col_c.metric("Cost", "$750", delta="-$50")


def show_factory_mode():
    """Display Factory Mode."""
    st.title("🏭 Factory Mode")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.write("### Select Scenario")
        scenario = st.selectbox(
            "Production Target",
            ["Produce 10 gears/min", "Produce 50 motors/min", "Mixed production"]
        )
        
        difficulty = st.select_slider(
            "Difficulty",
            options=["Easy", "Normal", "Hard"]
        )
        
        if st.button("Start Factory", use_container_width=True):
            st.success("Factory started!")
    
    with col2:
        st.write("### Factory Grid")
        st.info("🔨 Grid-based factory editor coming soon...")
        st.write("Features:")
        st.write("- Drag & drop machine placement")
        st.write("- Conveyor belt connections")
        st.write("- Real-time production monitoring")


def show_campaign():
    """Display Campaign Mode."""
    st.title("⚔️ Campaign Mode")
    st.info("Combine Beer Game and Factory Mode for ultimate challenge!")
    st.write("Choose a campaign scenario:")
    
    cols = st.columns(3)
    scenarios = [
        "🌍 Global Supply Chain (Beginner)",
        "🚀 Startup Growth (Intermediate)",
        "👑 Enterprise Challenge (Expert)",
    ]
    
    for col, scenario in zip(cols, scenarios):
        with col:
            st.write(f"**{scenario}**")
            if st.button("Play", key=scenario, use_container_width=True):
                st.success(f"Starting {scenario}!")


def show_analytics():
    """Display Analytics Dashboard."""
    st.title("📊 Analytics Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Supply Chains", "Factory", "Rankings"])
    
    with tab1:
        st.write("### Supply Chain Analysis")
        col1, col2 = st.columns(2)
        col1.metric("Avg Inventory Cost", "$450", delta="-$50")
        col2.metric("Bullwhip Effect", "1.2x", delta="-0.1x")
        st.write("📈 Charts coming soon...")
    
    with tab2:
        st.write("### Factory Performance")
        col1, col2 = st.columns(2)
        col1.metric("Production Rate", "95 items/min", delta="+5")
        col2.metric("Efficiency", "92%", delta="+3%")
        st.write("📈 Charts coming soon...")
    
    with tab3:
        st.write("### Player Rankings")
        st.write("Coming soon...")


if __name__ == "__main__":
    main()
