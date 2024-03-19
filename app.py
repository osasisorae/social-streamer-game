import streamlit as st

st.title('Social Media Aggregator Game')

# Game state management
if 'current_state' not in st.session_state:
    st.session_state.current_state = None

# Start game
if st.button('Start'):
    st.session_state.current_state = "start"
    st.session_state.game_content = "You wake up in a forest."

# Display game content
if 'game_content' in st.session_state:
    st.write(st.session_state.game_content)

# Interactive elements
user_input = st.text_input("What do you do?")
if st.button('Submit'):
    if user_input.lower() == "move left":
        st.session_state.game_content = "You find a path leading to a mysterious cave."
    elif user_input.lower() == "move right":
        st.session_state.game_content = "You stumble upon a river with clear water."
    else:
        st.session_state.game_content = "You wander around, unsure of what to do."
    
    # Display the updated game content
    st.write(st.session_state.game_content)

# Placeholder for game stats
st.sidebar.markdown("### Game Stats")
st.sidebar.markdown("**Followers:** 100")
