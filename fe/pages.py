import streamlit as st
from abc import ABC, abstractmethod
from models import Account  # Import the Account model


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
        st.write("Use the sidebar to navigate to different sections.")

    def required_state_keys(self):
        return []


class AccountsPage(Page):
    def render(self):
        st.header("Accounts Management")
        st.write("Manage user accounts here.")

        # Fetch accounts from the database
        accounts = Account.fetch_all()

        if accounts:
            for account in accounts:
                st.write(f"Account ID: {account.id}, Name: {account.name}")
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
