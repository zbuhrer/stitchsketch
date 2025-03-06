import streamlit as st
from pages import AccountsPage, GalleryPage, MediaItemPage, HomePage, SettingsPage
from database import MariaDBConnection, SQLiteConnection  # Import connection classes
from config_manager import ConfigManager
import os


def initialize_database(db_connection):
    """Creates the accounts table if it doesn't exist and adds some initial accounts."""
    try:
        with db_connection:  # Use context manager
            cursor = db_connection.conn.cursor()
            if isinstance(db_connection, MariaDBConnection):
                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS accounts (
                            id VARCHAR(255) PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            date_entered DATETIME,
                            date_modified DATETIME,
                            modified_user_id VARCHAR(255),
                            created_by VARCHAR(255),
                            description TEXT,
                            deleted BOOLEAN,
                            assigned_user_id VARCHAR(255)
                        );
                    """)
                    db_connection.conn.commit()  # Commit the changes
                except Exception as e:
                    st.error(f"Error creating table: {type(e).__name__}: {e}")
                    st.stop()

                # Check if accounts exist
                try:
                    cursor.execute("SELECT COUNT(*) FROM accounts")
                    result = cursor.fetchone()
                    if result is None:
                        count = 0  # Handle the case where fetchone() returns None
                    else:
                        # Access the count using the column name.  Handle cases where the column is named "COUNT(*)" or "count".
                        count = result.get(
                            'COUNT(*)') or result.get('count') or 0

                    if count == 0:
                        print("No Accounts")

                except Exception as e:
                    st.error(
                        f"Error checking if accounts exist: {type(e).__name__}: {e}")
                    st.stop()

            elif isinstance(db_connection, SQLiteConnection):
                # This is the config DB, *not* the accounts DB
                return  # Don't do anything for SQLite connection

    except Exception as e:
        st.error(f"Error initializing database: {type(e).__name__}: {e}")
        st.stop()  # Stop execution if database initialization fails


def initialize_config(config_manager):
    """Initializes default configuration values if they don't exist."""
    default_config = {
        'database_type': 'mariadb',  # Default to MariaDB
        'database_path': 'database.db',
        'media_base_path': './media'
    }

    for key, default_value in default_config.items():
        if config_manager.get_config(key) is None:
            config_manager.set_config(key, default_value)
            print(f"Initialized {key} to default value: {default_value}")


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
    # Initialize SQLite database for configuration
    config_manager = ConfigManager("config.db")
    initialize_config(config_manager)

    # Get database credentials from environment
    db_host = os.getenv("DB_HOST")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    # Create MariaDB connection - this is now *always* MariaDB, pass values explicitly
    mariadb_connection = MariaDBConnection(
        db_host=db_host, db_port=db_port, db_name=db_name, db_user=db_user, db_password=db_password)

    # Initialize the database - creates the account table in MariaDB.
    initialize_database(mariadb_connection)

    # Ensure the media directory exists.
    media_path = config_manager.get_config('media_base_path')
    if media_path:
        os.makedirs(media_path, exist_ok=True)

    # Define initial session state
    initial_state = {
        'config_manager': config_manager,  # Store the config manager
        'db_connection': mariadb_connection,  # Store the MariaDB connection instance
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

    # React to setting changes.
    if 'new_database_type' in st.session_state:
        st.session_state['config_manager'].set_config(
            'database_type', st.session_state['new_database_type'])
        del st.session_state['new_database_type']
        st.rerun()
    if 'new_database_path' in st.session_state:
        st.session_state['config_manager'].set_config(
            'database_path', st.session_state['new_database_path'])
        del st.session_state['new_database_path']
        st.rerun()
    if 'new_base_media_path' in st.session_state:
        st.session_state['config_manager'].set_config(
            'media_base_path', st.session_state['new_base_media_path'])
        del st.session_state['new_base_media_path']
        st.rerun()

    # Sidebar to reload config - not really needed, but kept for consistency
    if st.sidebar.button("Reload Config"):
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
    main()
