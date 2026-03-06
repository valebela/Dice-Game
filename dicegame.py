import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random


# Page Setup

st.set_page_config(
    page_title="Dice Battle Game & Analytics",
    layout="wide"
)


# Background & Text Style

st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #f0f2f6;
    }

    /* Force all text inside app to black */
    .stApp * {
        color: #000000 !important;
    }

    /* Buttons styling */
    .stButton>button {
        color: #000000 !important;
        background-color: #e0e0e0 !important;
        border-radius: 5px;
        border: 1px solid #ccc;
    }

    .stButton>button:hover {
        background-color: #d4d4d4 !important;
    }

    /* Sidebar background and text */
    .stSidebar {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }

    /* Sidebar input fields (text boxes, sliders, select boxes) */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div>select,
    .stSlider>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Sidebar labels */
    .stSidebar label {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and Intro

st.title("🎲 Dice Battle Game & Analytics")
st.caption("Vale Rodriguez • 2026\nPlay dice battles round by round and track scores and stats!")

# How It Works Section

st.markdown(
    """
### How It Works
- Two players roll dice one round at a time.
- Click 'Roll Dice!' to play a round.
- Scores and statistics update live, with charts showing cumulative results.
- Customize player names, dice count, and dice type in the sidebar.
"""
)


# Sidebar Controls

st.sidebar.markdown(
    " Click the arrow on the top-left to open the sidebar and enter player names or change dice settings!"
)

st.sidebar.header("🎲 Game Settings")
st.sidebar.markdown(
    "am Enter player names below and adjust dice settings before rolling!"
)

player1_name = st.sidebar.text_input("Player 1 Name", "Player 1")
player2_name = st.sidebar.text_input("Player 2 Name", "Player 2")

num_dice = st.sidebar.slider("Number of dice per player", 1, 5, 2)
dice_type = st.sidebar.selectbox("Type of dice", [6, 8, 10, 12, 20], index=0)


# Initialize Session State

if "rounds" not in st.session_state:
    st.session_state.rounds = []
if "player1_wins" not in st.session_state:
    st.session_state.player1_wins = 0
if "player2_wins" not in st.session_state:
    st.session_state.player2_wins = 0
if "ties" not in st.session_state:
    st.session_state.ties = 0
if "round_number" not in st.session_state:
    st.session_state.round_number = 0

# Dice Roll Function

def roll_dice(n_dice, sides):
    return [random.randint(1, sides) for _ in range(n_dice)]


# Roll & Reset Buttons

col1, col2 = st.columns(2)
with col1:
    if st.button("Roll Dice!"):
        st.session_state.round_number += 1

        p1_rolls = roll_dice(num_dice, dice_type)
        p2_rolls = roll_dice(num_dice, dice_type)
        p1_total = sum(p1_rolls)
        p2_total = sum(p2_rolls)

        if p1_total > p2_total:
            winner = player1_name
            st.session_state.player1_wins += 1
        elif p2_total > p1_total:
            winner = player2_name
            st.session_state.player2_wins += 1
        else:
            winner = "Tie"
            st.session_state.ties += 1

        st.session_state.rounds.append({
            "Round": st.session_state.round_number,
            f"{player1_name} Rolls": p1_rolls,
            f"{player1_name} Total": p1_total,
            f"{player2_name} Rolls": p2_rolls,
            f"{player2_name} Total": p2_total,
            "Winner": winner
        })

with col2:
    if st.button("Reset Game"):
        st.session_state.rounds = []
        st.session_state.player1_wins = 0
        st.session_state.player2_wins = 0
        st.session_state.ties = 0
        st.session_state.round_number = 0

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric(f"{player1_name} Wins", st.session_state.player1_wins)
col2.metric(f"{player2_name} Wins", st.session_state.player2_wins)
col3.metric("Ties", st.session_state.ties)

# Show Latest Round

if st.session_state.rounds:
    last_round = st.session_state.rounds[-1]
    st.subheader(f"Round {last_round['Round']} Results")
    st.write(f"{player1_name} Rolls: {last_round[f'{player1_name} Rolls']} → Total {last_round[f'{player1_name} Total']}")
    st.write(f"{player2_name} Rolls: {last_round[f'{player2_name} Rolls']} → Total {last_round[f'{player2_name} Total']}")
    st.write(f"Winner: **{last_round['Winner']}**")


# Round Results Table

if st.session_state.rounds:
    st.subheader("Round-by-Round Results")
    df = pd.DataFrame(st.session_state.rounds)
    st.dataframe(df)


# Visualizations

if st.session_state.rounds:
    # Dice totals
    st.subheader("Dice Total Distributions")
    fig, ax = plt.subplots(figsize=(8,4))
    ax.hist(df[f"{player1_name} Total"], bins=num_dice * dice_type, alpha=0.6, color="blue", label=player1_name)
    ax.hist(df[f"{player2_name} Total"], bins=num_dice * dice_type, alpha=0.6, color="orange", label=player2_name)
    ax.set_xlabel("Total Dice Roll")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

    # Cumulative Wins
    st.subheader("Cumulative Wins Over Rounds")
    df[player1_name] = df['Winner'].eq(player1_name).cumsum()
    df[player2_name] = df['Winner'].eq(player2_name).cumsum()
    st.line_chart(df[[player1_name, player2_name]])

# Download Results

if st.session_state.rounds:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Round Results (CSV)",
        data=csv,
        file_name="dice_battle_results.csv",
        mime="text/csv"
    )