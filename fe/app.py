import streamlit as st
from pages import AccountsPage, GalleryPage, MediaItemPage, HomePage, SettingsPage
from database import DatabaseConnection  # Import the DatabaseConnection class
import os


def initialize_database(db_connection):
    """Creates the accounts table if it doesn't exist and adds some initial accounts."""
    db_connection.create_accounts_table()
    if db_connection.get_number_of_accounts() == 0:
        print("No Accounts")


def load_config():
    """Loads configuration settings.  In a real app, this might read from a file."""
    config = {
        'database': {'path': 'database.db'},
        'media': {'base_path': './media'}  # Default media directory
    }
    return config


def save_config(config):
    """Saves configuration settings.  In a real app, this would write to a file."""
    # This is a placeholder. In a real application, you would save the config to a file (e.g., JSON, YAML).
    print("Saving config (placeholder):", config)


def header():
    """Creates the header banner with app name, logo, and navigation buttons."""
    st.markdown(
        """
        <style>
        .app-header {
            padding: 1rem 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .app-logo {
            margin-left: 1rem;
            height: 50px;  /* Adjust as needed */
        }
        .app-title {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .nav-buttons {
            margin-right: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="app-header">
            <img src="logo.png" class="app-logo">
            <div class="app-title">StitchSketch</div>
            <div class="nav-buttons">
                <a href="/" target="_self">
                  <button>Home</button>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    # Initialize session state
    if 'config' not in st.session_state:
        st.session_state['config'] = load_config()  # Load configuration

    # Initialize database connection
    if 'db_connection' not in st.session_state:
        st.session_state['db_connection'] = DatabaseConnection()

        # Initialize the database with accounts table and initial accounts.
        initialize_database(st.session_state['db_connection'])

    if 'accounts' not in st.session_state:
        st.session_state['accounts'] = []
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

    # Initialize page_name in session state
    if 'page_name' not in st.session_state:
        st.session_state.page_name = "Home"

    # React to setting changes.
    if 'new_database_path' in st.session_state:
        st.session_state['config']['database']['path'] = st.session_state['new_database_path']
        del st.session_state['new_database_path']
    if 'new_base_media_path' in st.session_state:
        st.session_state['config']['media']['base_path'] = st.session_state['new_base_media_path']
        del st.session_state['new_base_media_path']

        # Save config
        save_config(st.session_state['config'])

    # Sidebar to reload config
    if st.sidebar.button("Reload Config"):
        st.session_state['config'] = load_config()  # Reload configuration
        st.rerun()

    # **ADD HEADER HERE**
    header()

    page_name = st.session_state.page_name

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


if __name__ == "__main__":
    # Ensure the media directory exists.
    config = load_config()
    media_path = config.get('media', {}).get('base_path')
    if media_path:
        os.makedirs(media_path, exist_ok=True)

    main()
