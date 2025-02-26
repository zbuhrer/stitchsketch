import streamlit as st
import json
from pages import AccountsPage, GalleryPage, MediaItemPage, HomePage, SettingsPage
from database import DatabaseConnection  # Import the DatabaseConnection class


CONFIG_FILE = "config.json"


def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            # Validate config structure (at least 'database' key exists)
            if 'database' not in config:
                st.error("Invalid config.json: Missing 'database' section.")
                return {}
            return config
    except FileNotFoundError:
        st.warning(f"Config file not found: {
                   CONFIG_FILE}. Using default settings.")
        return {}
    except json.JSONDecodeError:
        st.error(f"Invalid JSON in config file: {CONFIG_FILE}.")
        return {}


# def update_config(config, new_database_path):  # Remove this function
#     try:
#         config['database']['path'] = new_database_path
#         with open(CONFIG_FILE, "w") as file:
#             json.dump(config, file, indent=4)
#         st.success("Configuration updated successfully!")
#         return True
#     except Exception as e:
#         st.error(f"Error updating config file: {e}")
#         return False


def main():
    st.title("Application Dashboard")

    # Load configuration
    config = load_config()
    # Store the config in session state
    st.session_state['config'] = config

    # Initialize database connection
    if 'db_connection' not in st.session_state:
        st.session_state['db_connection'] = DatabaseConnection()

    # Initialize session state
    if 'accounts' not in st.session_state:
        # Mock account data (replace with actual database retrieval later)
        st.session_state['accounts'] = [
            {"id": 1, "name": "Account A"},
            {"id": 2, "name": "Account B"},
        ]
    if 'selected_account_id' not in st.session_state:
        st.session_state['selected_account_id'] = None
    if 'media_items' not in st.session_state:
        # Mock media items
        st.session_state['media_items'] = [
            {"id": 101, "name": "Image 1", "account_id": 1},
            {"id": 102, "name": "Video 1", "account_id": 2},
            {"id": 103, "name": "Model 1", "account_id": 1},
        ]
    if 'selected_media_item_id' not in st.session_state:
        st.session_state['selected_media_item_id'] = None

    st.sidebar.title("Navigation")
    page_name = st.sidebar.radio(
        "Go to",
        ["Home", "Accounts", "Gallery", "Media Item", "Settings"]
    )

    # Add a reload config button
    if st.sidebar.button("Reload Config"):
        st.session_state['config'] = load_config()
        st.rerun()  # Force Streamlit to re-run the script

    # Instantiate and render the selected page
    if page_name == "Home":
        HomePage().render()
    elif page_name == "Accounts":
        AccountsPage().render()
    elif page_name == "Gallery":
        GalleryPage().render()
    elif page_name == "Media Item":
        MediaItemPage().render()
    elif page_name == "Settings":
        SettingsPage().render()

    # # Check if new database path was submitted # Remove this section
    # if 'new_database_path' in st.session_state:
    #     if update_config(st.session_state['config'], st.session_state['new_database_path']):
    #         # If update was successful, remove the key from session state
    #         del st.session_state['new_database_path']
    #         st.session_state['config'] = load_config()  # Reload config
    #     # No need to rerun() here, as update_config displays a success message


if __name__ == "__main__":
    main()
