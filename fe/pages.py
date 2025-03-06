import streamlit as st
import os
import glob
from abc import ABC, abstractmethod
import io  # For working with BytesIO objects
from models import Account  # Import the Account model
from database import DBConnection, MariaDBConnection  # Import MariaDBConnection
from typing import List, Optional


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
        st.write("Select an account to view its gallery.")

        db_connection: DBConnection = st.session_state.get('db_connection')

        if not db_connection or not db_connection.is_connected():
            st.error("Not connected to the database.")
            return

        # Database Information
        db_name = db_connection.get_database_name()
        is_connected = db_connection.is_connected()

        st.subheader("Database Information")
        st.write(f"Database Name: {db_name}")
        status = "Connected" if is_connected else "Disconnected"
        st.write(f"Connection Status: {status}")

        # Account Listing
        st.subheader("Accounts List")

        try:
            if not isinstance(db_connection, MariaDBConnection):
                st.error(
                    "Accounts must be fetched from a MariaDB connection.")
                return

            # Fetch accounts using the model
            accounts: List[Account] = Account.fetch_all(db_connection)
            if accounts:
                for account in accounts:
                    # Use account.id
                    with st.form(key=f'account_form_{account.id}'):
                        st.write(f"Account Name: {account.name}")
                        submit_button = st.form_submit_button(label='Select')
                        if submit_button:
                            st.session_state['selected_account_id'] = account.id
                            st.session_state.page_name = "Gallery"
                            st.rerun()
            else:
                st.write("No accounts found.")
        except Exception as e:
            st.error(f"Error fetching accounts: {e}")

    def required_state_keys(self):
        return ['db_connection']  # Ensure the database connection is available


class GalleryPage(Page):
    def render(self):
        st.header("Gallery")

        config_manager = st.session_state.get('config_manager')
        base_media_dir = config_manager.get_config('media_base_path')
        selected_account_id = st.session_state.get('selected_account_id')
        db_connection: DBConnection = st.session_state.get('db_connection')

        if not base_media_dir:
            st.error(
                "Base media directory not configured. Please set it in Settings.")
            return

        # Determine the account name for the tab title
        selected_account_name = "Select Account"  # Default value
        if selected_account_id:
            try:
                account: Optional[Account] = Account.get_account_by_id(
                    db_connection, selected_account_id)
                if account:
                    selected_account_name = account.name
                else:
                    st.warning(
                        f"Account with ID {selected_account_id} not found.")
            except Exception as e:
                st.error(f"Error fetching account: {e}")

        # Create tabs
        all_tab, account_tab = st.tabs(["All", selected_account_name])

        with all_tab:
            st.subheader("All Media")
            all_media_files = glob.glob(os.path.join(
                base_media_dir, "**/*.*"), recursive=True)

            if not all_media_files:
                st.info("No media files found in any account directories.")
            else:
                for file_path in all_media_files:
                    if not isinstance(file_path, str):
                        st.warning(
                            f"Skipping non-string file path: {file_path}")
                        continue
                    try:
                        file_extension = os.path.splitext(file_path)[1].lower()

                        if file_extension in ['.jpg', '.jpeg', '.png']:
                            st.image(file_path, caption=os.path.basename(
                                file_path), use_column_width=True)
                        elif file_extension in ['.mp4', '.avi', '.mov']:
                            st.video(file_path, start_time=0)
                        else:
                            filename = os.path.basename(file_path)
                            st.warning(
                                f"Unsupported media type: {file_extension} for file {filename}")
                    except Exception as e:
                        filename = os.path.basename(file_path)
                        st.error(f"Error displaying {filename}: {e}")

        with account_tab:
            if selected_account_id:
                # Ensure account_id is a string
                account_media_dir = os.path.join(
                    base_media_dir, str(selected_account_id))

                # Ensure the account directory exists
                if not os.path.exists(account_media_dir):
                    try:
                        os.makedirs(account_media_dir)
                        st.info(f"Created directory: {account_media_dir}")
                    except Exception as e:
                        st.error(f"Error creating directory: {e}")
                        return  # Stop further processing if directory creation fails

                # File Upload Section
                uploaded_file = st.file_uploader(
                    "Upload Media", type=['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov'])

                if uploaded_file is not None:
                    try:
                        # Determine the file size
                        file_size = len(uploaded_file.getvalue())
                        # Save the uploaded file to the account's directory
                        file_path = os.path.join(
                            account_media_dir, uploaded_file.name)

                        # Create a placeholder for the progress bar
                        progress_bar_placeholder = st.empty()

                        bytes_written = 0

                        with open(file_path, "wb") as f:
                            # Read the file in chunks
                            for chunk in iter(lambda: uploaded_file.read(4096), b""):  # 4KB chunks
                                f.write(chunk)
                                bytes_written += len(chunk)
                                progress = int(
                                    (bytes_written / file_size) * 100)
                                # Update the progress bar in the placeholder
                                progress_bar_placeholder.progress(progress)

                        # Set progress bar to 100%
                        progress_bar_placeholder.progress(100)

                        st.success(
                            f"File '{uploaded_file.name}' uploaded successfully!")
                        # Rerun to refresh the gallery
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error uploading file: {e}")

                # Display Media Files
                media_files = glob.glob(os.path.join(account_media_dir, "*"))

                if not media_files:
                    st.info("No media files found for this account.")
                else:
                    st.subheader(f"Media for Account ID: {selected_account_id}"
                                 )
                    for file_path in media_files:
                        try:
                            file_extension = os.path.splitext(file_path)[
                                1].lower()

                            if file_extension in ['.jpg', '.jpeg', '.png']:
                                st.image(file_path, caption=os.path.basename(
                                    file_path), use_column_width=True)
                            elif file_extension in ['.mp4', '.avi', '.mov']:
                                st.video(file_path, start_time=0)
                            else:
                                filename = os.path.basename(file_path)
                                st.warning(
                                    f"Unsupported media type: {file_extension} for file {filename}")
                        except Exception as e:
                            filename = os.path.basename(file_path)
                            st.error(f"Error displaying {filename}: {e}")

            else:
                st.info("Please select an account from the Accounts page.")

    def required_state_keys(self):
        return ['config_manager', 'selected_account_id', 'db_connection']


class MediaItemPage(Page):
    def render(self):
        st.header("Media Item Details")
        st.write("Manage individual photos, videos, or 3D models.")

    def required_state_keys(self):
        return ['media_items', 'accounts', 'selected_media_item_id']


class SettingsPage(Page):
    def render(self):
        st.header("Settings")

        config_manager = st.session_state.get('config_manager')

        with st.form("settings_form"):
            # Database settings
            db_type = st.selectbox("Database Type", options=[
                'sqlite', 'mariadb'], index=['sqlite', 'mariadb'].index(config_manager.get_config('database_type', 'sqlite')))
            new_database_path = st.text_input(
                "Database Path", value=config_manager.get_config('database_path', 'database.db'))

            # Media settings
            new_base_media_path = st.text_input(
                "Base Media Path", value=config_manager.get_config('media_base_path', './media'))

            submitted = st.form_submit_button("Save Changes")

            if submitted:
                # Validation
                if not new_database_path:
                    st.error("Database path cannot be empty.")
                elif not isinstance(new_database_path, str):
                    st.error("Database path must be a string.")
                elif not new_base_media_path:
                    st.error("Base media path cannot be empty.")
                elif not isinstance(new_base_media_path, str):
                    st.error("Database path must be a string.")
                else:
                    # Update the session state
                    st.session_state['new_database_type'] = db_type
                    st.session_state['new_database_path'] = new_database_path
                    st.session_state['new_base_media_path'] = new_base_media_path

                    st.success(
                        "Settings saved!  Click the 'Reload Config' button in the sidebar to apply changes.")

    def required_state_keys(self):
        # Ensure the config manager is loaded before rendering
        return ['config_manager']
