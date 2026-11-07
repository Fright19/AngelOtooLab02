# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)


tab1, tab2 =  st.tabs(["Bedwars", "Survey"])
# PAGE TITLE
with tab1:
    st.title("Bedwars Statistics Dashboard")

    st.image("Images/stats.png", width=500, caption="My Minecraft Character Stats")

    st.write("""
    This dashboard displays my Bedwars statistics
    for several game modes.
    """)
    # PART 1: GRAPHS FROM data.json
    # --- YOUR CODE GOES HERE ---
    with open("data.json", "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data["data_points"])
    st.header("Static Visualization")

    colors = [
        "#00BFFF",  # Solo
        "#32CD32",  # Doubles
        "#FFD700",  # 3v3v3v3
        "#FF4500"   # 4v4v4v4
    ]

    fig, ax = plt.subplots()
    ax.bar(df["name"], df["Wins"],
           color=colors)
    ax.set_title("Hypixel Wins")
    ax.set_xlabel("Game Mode")
    ax.set_ylabel("Wins")

    st.pyplot(fig)

    if "selected_stat" not in st.session_state:
        st.session_state.selected_stat = "Wins"

    selected = st.selectbox(
        "Choose a stat",
        ["Wins", "Kills", "Final Kills", "Losses", "Deaths", "Final Deaths"]
    )

    st.session_state.selected_stat = selected
    st.header("Dynamic Visualization")
    fig, ax = plt.subplots()



    ax.bar(
        df["name"],
        df[st.session_state.selected_stat],
        color=colors
    )

    ax.set_title(f"{st.session_state.selected_stat} by Game Mode")
    ax.set_xlabel("Game Mode")
    ax.set_ylabel(st.session_state.selected_stat)

    st.pyplot(fig)

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
with tab2:
    st.title("Mob Vote Results!")
    df = pd.read_csv("data.csv")
    df.columns = ["Mob", "Reason"]

    st.subheader("Vote Count (Static)")


    
    voteCount = df["Mob"].value_counts()
    

    fig, ax = plt.subplots()
    ax.bar(voteCount.index, voteCount.values, color=["#4CAF50", "#2196F3", "#FF9800"])
    ax.set_title("Overall Mob Vote Results")
    ax.set_xlabel("Mob")
    ax.set_ylabel("Votes")

    st.pyplot(fig)

    colu, col2 = st.columns(2)
    with colu:
        st.metric("Total Votes", len(df))
    with col2:
        st.metric("Different Mobs", df["Mob"].nunique())

    st.divider()

    if len(voteCount) > 0:
        st.subheader("Why People Voted For Each Mob (Dynamic)")
            
        chosenMob = st.radio("Choose a mob", voteCount.index, horizontal=True)
        st.session_state["chosenMob"] = chosenMob # session state that updates dynamic graph
        ooga = df[df["Mob"] == chosenMob]
        
        loveMobs = {"Penguin": "Images/penguin_vote.png",
                    "Armadillo": "Images/armadillo_vote.png",
                    "Crab": "Images/crab_vote.png"}
        if chosenMob in loveMobs:

            colbum, colrum = st.columns([2, 1])

            with colbum:
                st.image(loveMobs[chosenMob],
                         caption=chosenMob,
                         width=300)

            with colrum:
                voteNum = voteCount[chosenMob]
                st.metric("Votes for this Mob", voteNum)

                winning = voteCount.idxmax()
                st.metric("Who's winning?", winning)

        st.subheader("Reasons People Voted For This Mob")

        for reason in ooga["Reason"]:
            st.info(reason)
    else:
        st.warning("No votes submitted yet!")

