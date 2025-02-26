import streamlit as st
from pages import AccountsPage, GalleryPage, MediaItemPage, HomePage, SettingsPage
from database import DatabaseConnection  # Import the DatabaseConnection class


def initialize_database(db_connection):
    """Creates the accounts table if it doesn't exist and adds some initial accounts."""
    db_connection.create_accounts_table()
    if db_connection.get_number_of_accounts() == 0:
        print("No Accounts")


def main():
    st.title("Application Dashboard")

    # Initialize database connection
    if 'db_connection' not in st.session_state:
        st.session_state['db_connection'] = DatabaseConnection()

        # Initialize the database with accounts table and initial accounts.
        initialize_database(st.session_state['db_connection'])

    # Initialize session state
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

    # st.sidebar.title("Navigation")
    # page_name = st.sidebar.radio(
    #     "Go to",
    #     ["Home", "Accounts", "Gallery", "Media Item", "Settings"]
    # )

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
