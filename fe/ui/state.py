import streamlit as st


class PageState:
    """
    A class to manage the state of the Streamlit application.
    """

    def __init__(self):
        # Initialize state variables here with default values.
        self.current_page = "Upload Images/Video"  # Add state variables as needed

    def get(self, key, default=None):
        """
        Gets a value from the Streamlit session state.  If the key
        doesn't exist, it's initialized with the default value.

        Args:
            key (str): The key to retrieve from the session state.
            default (Any, optional): The default value to use if the key doesn't exist. Defaults to None.

        Returns:
            Any: The value from the session state, or the default value if the key doesn't exist.
        """
        if key not in st.session_state:
            st.session_state[key] = default
        return st.session_state[key]

    def set(self, key, value):
        """
        Sets a value in the Streamlit session state.

        Args:
            key (str): The key to set in the session state.
            value (Any): The value to set for the key.
        """
        st.session_state[key] = value
