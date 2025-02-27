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
        background-color: #f0f2f6; /* Add a background color */
        position: sticky; /* Make it sticky */
        top: 0; /* Stick to the top */
        z-index: 1000; /* Ensure it stays on top of other elements */
        }
        .app-logo {
            margin-left: 1rem;
            height: 50px;  /* Adjust as needed */
        }
        .app-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 1rem;
            margin-left: auto;  /* Push title to the center */
            margin-right: auto; /* Ensure it stays centered */
        }
        .nav-buttons {
            margin-right: 1rem;
            display: flex;  /* Use flexbox for button layout */
            gap: 0.5rem;    /* Add some spacing between buttons */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create columns for layout
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed

    with col1:
        with st.container():
            st.markdown('<div class="nav-buttons">',
                        unsafe_allow_html=True)  # Open nav-buttons div
            if st.button(label="Home", key="home_button"):  # Unique key is important!
                st.session_state.page_name = "Home"
            # Close nav-buttons div
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="app-title"></div>',
                    unsafe_allow_html=True)

    # You can add more buttons in col3 if needed.
    with col3:
        with st.container():
            st.markdown('<div class="nav-buttons">',
                        unsafe_allow_html=True)  # Open nav-buttons div
            if st.button(label="Settings", key="settings_button"):
                st.session_state.page_name = "Settings"
            # Close nav-buttons div
            st.markdown('</div>', unsafe_allow_html=True)


def main():
    # Define initial session state
    initial_state = {
        'config': load_config(),
        'db_connection': DatabaseConnection(),
        'accounts': [],
        'selected_account_id': None,
        'media_items': [
            {"id": 101, "name": "Image 1", "account_id": 1},
            {"id": 102, "name": "Video 1", "account_id": 2},
            {"id": 103, "name": "Model 1", "account_id": 1},
        ],
        'selected_media_item_id': None,
        'page_name': "Home"
    }

    # Initialize session state
    for key, value in initial_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Initialize the database with accounts table and initial accounts.
    initialize_database(st.session_state['db_connection'])

    # React to setting changes.  Consider making this a function.
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
