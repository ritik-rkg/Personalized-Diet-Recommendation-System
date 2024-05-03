import streamlit as st

st.set_page_config(
    page_title="Diet Recommendation System",
    # initial_sidebar_state="collapsed",
    page_icon="👋",
)

st.write("# Welcome to Diet Recommendation System! 👋")

# st.sidebar.success("Select a recommendation app.")

st.markdown(
    """
    Algorithm used: Contextual Greedy Epsilon Multi Arm Bandits
    """
)

st.markdown(
    """
    [Github repository](https://github.com/ritik-rkg/Personalized-Diet-Recommendation-System)
    """
)