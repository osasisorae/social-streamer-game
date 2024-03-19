import streamlit as st
from content_library import game_content_library  # Make sure this import matches your setup

st.title('Social Media Aggregator Game')

# Function to get the current scenario and choices from the game content library
def get_current_scenario(current_state):
    scenario = game_content_library.get(current_state, game_content_library['start'])
    return scenario['description'], scenario['choices']

# Initialize game state if not already set
if 'current_state' not in st.session_state:
    st.session_state.current_state = 'start'

# Display current scenario description and choices
description, choices = get_current_scenario(st.session_state.current_state)
st.write(description)

# If there are choices, display them as options for the user to select
if choices:
    option = st.selectbox("What do you do?", options=list(choices.keys()))

    if st.button("Proceed"):
        if option in choices:
            next_state = choices[option]
            st.session_state.current_state = next_state
            # Fetch and display the new scenario based on the chosen option
            description, choices = get_current_scenario(next_state)
            st.write(description)
else:
    st.write("There seems to be no way forward from here...")

# Sidebar for game stats - This could be dynamically updated based on the game's progress
st.sidebar.markdown("### Game Stats")
st.sidebar.markdown("**Followers:** 100")  # Placeholder for follower count
