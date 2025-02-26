import streamlit as st
from abc import ABC, abstractmethod


class Page(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def required_state_keys(self):
        pass


class HomePage(Page):
    def render(self):
        st.header("Welcome to the Application")
        st.write("Use the buttons below to navigate to different sections.")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Accounts"):
                st.session_state.page_name = "Accounts"
                st.rerun()
        with col2:
            if st.button("Gallery"):
                st.session_state.page_name = "Gallery"
                st.rerun()
        with col3:
            if st.button("Settings"):
                st.session_state.page_name = "Settings"
                st.rerun()

    def required_state_keys(self):
        return []


class AccountsPage(Page):
    def render(self):
        st.header("Accounts Management")
        st.write("Manage user accounts here.")

        db_connection = st.session_state.get('db_connection')

        if not db_connection or not db_connection.is_connected():
            st.error("Not connected to the database.")
            return  # Exit if no connection

        # Database Information
        db_name = db_connection.get_database_name()
        is_connected = db_connection.is_connected()
        num_accounts = db_connection.get_number_of_accounts()

        st.subheader("Database Information")
        st.write(f"Database Name: {db_name}")
        st.write(f"Connection Status: {
                 'Connected' if is_connected else 'Disconnected'}")
        st.write(f"Number of Accounts: {num_accounts}")

        # Account Listing
        st.subheader("Accounts List")
        accounts = db_connection.fetch_all_accounts()  # Fetch from database
        if accounts:
            for account in accounts:
                st.write(f"Account ID: {account[0]}, Name: {account[1]}")
        else:
            st.write("No accounts found.")

    def required_state_keys(self):
        return []  # No session state keys are required anymore


class GalleryPage(Page):
    def render(self):
        st.header("Gallery")
        st.write("View and manage media items here.")

    def required_state_keys(self):
        return ['media_items', 'accounts']


class MediaItemPage(Page):
    def render(self):
        st.header("Media Item Details")
        st.write("Manage individual photos, videos, or 3D models.")

    def required_state_keys(self):
        return ['media_items', 'accounts', 'selected_media_item_id']


class SettingsPage(Page):
    def render(self):
        st.header("Settings")

        with st.form("settings_form"):
            # Get the current database path from the config
            current_database_path = st.session_state.get(
                'config', {}).get('database', {}).get('path', '')

            new_database_path = st.text_input(
                "Database Path", value=current_database_path)
            submitted = st.form_submit_button("Save Changes")

            if submitted:
                # Validation
                if not new_database_path:
                    st.error("Database path cannot be empty.")
                elif not isinstance(new_database_path, str):
                    st.error("Database path must be a string.")
                # Removed file exists test, as it might not exist on the server
                else:
                    # Update the session state (the actual writing to the config will happen in app.py)
                    st.session_state['new_database_path'] = new_database_path
                    st.success(
                        "Settings saved!  Click the 'Reload Config' button in the sidebar to apply changes.")

    def required_state_keys(self):
        return ['config']  # Ensure the config is loaded before rendering
