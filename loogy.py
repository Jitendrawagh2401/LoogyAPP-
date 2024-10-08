import streamlit as st
import pandas as pd
import re

def main():
    #st.title("Analysis of Tripeaks Events Data 📉")
    global df, uploaded_file
    st.markdown(
            """
            <style>
            .stApp {
                background-image: url('data:image/jpeg;base64,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');            
                background-size: cover; /* Adjusts the size to cover the entire container */
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    st.sidebar.markdown(
            """
            <div style="text-align: center; padding: 10px;">
                <img src="data:image/jpeg;base64,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" alt="Sidebar Image" style="max-width: 100%; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )

    uploaded_file = st.sidebar.file_uploader("Upload your event data (CSV only)", type=["csv"])
    if uploaded_file is None:
        st.title("Analysis of Tripeaks Events Data 📉")
    else:
        # Show a different title after data is uploaded
        st.title("Analysis of User Removal and Churn Events in the Tripeaks App 🐶")




    #if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        total_unique_users = df['user_pseudo_id'].nunique()
        st.sidebar.header('Total Users')
        st.sidebar.write(f"Total Users: {total_unique_users}")
        #st.title("Analysis of User Removal and Churn Events in the Tripeaks App🐶")
        with st.spinner('Please wait, results are being processed...'):

            # Step 2: Convert 'event_time_UTC' to datetime with the correct format
            df['timestamp'] = pd.to_datetime(df['event_time_UTC'], format='%Y-%m-%d %H:%M:%S.%f %Z', errors='coerce')

        # Step 3: Check if there are any invalid timestamps
            #if df['timestamp'].isnull().any():
                #st.warning("Some timestamps couldn't be converted. Please check the format.")

            # Step 4: Sort the data by user_id and timestamp
            df = df.sort_values(by=['user_pseudo_id', 'timestamp'])
            st.success('Results are ready😀!')

        # Step 5: Define the list of events to consider
            events_to_skip  = [
                "NewSessionEvent", "UpdateAPI_Started", "UpdateAPI_Success", "MaxNonMatchCard",
                "InitMETA_Completed", "LevelAPI_Started", "LevelAPI_Success", "DogFeedAPI_Started",
                "DogFeedAPI_Success", "BankEventAPI_Started", "EarnFreeRewardAPI_Started",
                "EarnFreeRewardAPI_Success", "BankEventAPI_Success", "DesertChampStatusAPI_Started",
                "DesertChampStatusAPI_Success", "QuestAPI_Started", "QuestAPI_Success",
                "RoyalPassAPI_Started", "RoyalPassAPI_Success", "ProgressionAPI_Started",
                "ProgressionAPI_Success", "user_engagement", "EndlessTreasureAPI_Started",
                "EndlessTreasureAPI_Success", "CreditCoinAPI_Fail", "DocTournamentAPI_Success",
                "EnergyRushStatusAPI_Started", "EnergyRushStatusAPI_Success", "RA_NotAvailable",
                "session_start", "LoadAdTimeOut", "On_move_mistake_in_gameplay", "FR_Read_Default_Started",
                "DocLeaderboardAPI_Started", "DocLeaderboardAPI_Success", "LoginAPI_Started",
                "FR_DD_Started", "FR_DD_Added", "FR_RC_Init_Completed", "LoginAPI_Success",
                "FR_RC_Fetch_Completed", "ExtraAdStart", "NewSessionFailed", "DocJoinMatchAPI_Started",
                "ExtraAdComplete", "On_Splash_PlayNow_Clicked", "DocJoinMatchAPI_Success",
                "DesertChampMatchAPI_Started", "DesertChampMatchAPI_Success", "NewUsersTimeOutUpdate",
                "level_up", "firebase_campaign", "Send_Server_Request", "FR_Read_Default_Completed",
                "Data_Collection_Started", "On_ThemeStore_Server_Request", "HandleGameData",
                "FR_GameStart_Wait", "RA_LevelWin_ExtraCoins_Visible", "On_ThemeStore_Response_Received",
                "Firebase_game_start", "Bundle_Downloaded", "AutoCatchEvent_Found", "AutoCatchEvent_ReadyToGO",
                "AutoCatchEvent_Invoke", "FR_GameStarted", "Level_01_Data_Fetched", "Server_Request_Return_Success",
                "EnergyRushChampMatchAPI_Success", "EnergyRushChampMatchAPI_Started", "FR_Init_Started",
                "UpdateAPI_Fail", "FR_Init_Completed", "FR_Fetch_Started", "On_Level_Completed_01_Animation_Started",
                "Level_02_Data_Fetched", "InstantRequestAds", "On_Level_Completed_02_Animation_Started",
                "Level_03_Data_Fetched", "On_Level_Completed_03_Animation_Started", "On_Asset_Bundle_Downloaded",
                "DesertChampStatusAPI_Fail", "Level_04_Data_Fetched", "Firebase_Data_received",
                "On_Level_Completed_04_Animation_Started", "On_Level_Completed_05_Animation_Started",
                "Level_05_Data_Fetched", "On_Level_Completed_01_Animation_Skipped", "InstantRequestComplete",
                "On_Level_Completed_02_Animation_Skipped", "On_Level_Completed_03_Animation_Skipped",
                "Level_06_Data_Fetched", "On_Level_Completed_06_Animation_Started", "Quest_First_Time_Enabled",
                "Level_07_Data_Fetched", "On_Level_Completed_07_Animation_Started", "BankEventAPI_Fail",
                "On_Level_Completed_04_Animation_Skipped", "Level_08_Data_Fetched",
                "On_Level_Completed_08_Animation_Started", "On_Level_Completed_05_Animation_Skipped",
                "Level_09_Data_Fetched", "On_Level_Completed_09_Animation_Started", "EnergyRushStatusAPI_Fail",
                "ExtraAdFail", "RoyalPassAPI_Fail", "EarnFreeRewardAPI_Fail", "Level_10_Data_Fetched",
                "On_Level_Completed_10_Animation_Started", "LoginAPI_Fail", "NewUsersTimeOut",
                "InstantRequestTimeout", "On_Level_Completed_11_Animation_Started", "Level_11_Data_Fetched",
                "On_Level_Completed_06_Animation_Skipped", "OnInviteShareClick", "DocTournamentAPI_Fail",
                "Level_12_Data_Fetched", "On_Level_Completed_12_Animation_Started", "QuestAPI_Fail",
                "Level_13_Data_Fetched", "On_Level_Completed_07_Animation_Skipped", "On_Level_Completed_13_Animation_Started",
                "On_Level_Completed_08_Animation_Skipped", "On_Level_Completed_09_Animation_Skipped",
                "Level_14_Data_Fetched", "On_Level_Completed_14_Animation_Started", "On_Level_Completed_15_Animation_Started",
                "Level_15_Data_Fetched", "On_Level_Completed_16_Animation_Started", "Level_16_Data_Fetched",
                "EndlessTreasureAPI_Fail", "Level_17_Data_Fetched", "On_Level_Completed_17_Animation_Started",
                "On_Level_Completed_10_Animation_Skipped", "On_Level_Completed_11_Animation_Skipped",
                "FR_Fetch_TimedOut", "Level_18_Data_Fetched", "On_Level_Completed_18_Animation_Started",
                "On_Rate_Now_Clicked", "Level_19_Data_Fetched", "On_Level_Completed_19_Animation_Started",
                "On_Level_Completed_14_Animation_Skipped", "On_Level_Completed_13_Animation_Skipped",
                "Level_20_Data_Fetched", "On_Level_Completed_20_Animation_Started", "On_Level_Completed_12_Animation_Skipped",
                "Continue_With_Local_Data", "On_Level_Completed_21_Animation_Started", "Level_21_Data_Fetched",
                "On_Level_Completed_16_Animation_Skipped", "On_Level_Completed_15_Animation_Skipped",
                "Level_22_Data_Fetched", "On_Level_Completed_22_Animation_Started", "On_Level_Completed_23_Animation_Started",
                "EventAPI_Fail", "Level_23_Data_Fetched", "On_Level_Completed_17_Animation_Skipped",
                "On_Level_Completed_19_Animation_Skipped", "On_Level_Completed_18_Animation_Skipped",
                "On_Settings_Sound_OFF", "On_Level_Completed_24_Animation_Started", "Level_24_Data_Fetched",
                "On_Level_Completed_25_Animation_Started", "Level_25_Data_Fetched", "On_Level_Completed_26_Animation_Started",
                "On_Level_Completed_21_Animation_Skipped", "Level_26_Data_Fetched", "On_Level_Completed_20_Animation_Skipped",
                "Level_28_Data_Fetched", "On_Level_Completed_28_Animation_Started", "On_Level_Completed_27_Animation_Started",
                "Level_29_Data_Fetched", "Level_27_Data_Fetched", "On_Level_Completed_22_Animation_Skipped",
                "On_Level_Completed_23_Animation_Skipped", "On_Level_Completed_29_Animation_Started",
                "Bundle_Downloading_failed", "Level_30_Data_Fetched", "DocJoinMatchAPI_Fail",
                "Server_Request_Return_Failed", "On_Settings_Music_OFF", "On_Level_Completed_30_Animation_Started",
                "On_Level_Completed_26_Animation_Skipped", "On_Level_Completed_24_Animation_Skipped",
                "On_Level_Completed_25_Animation_Skipped", "On_Level_Completed_27_Animation_Skipped",
                "On_Level_Completed_29_Animation_Skipped", "On_Level_Completed_28_Animation_Skipped",
                "Level_31_Data_Fetched", "On_Level_Completed_30_Animation_Skipped", "app_exception",
                "On_Level_Completed_31_Animation_Started", "DesertChampMatchAPI_Fail", "Level_32_Data_Fetched",
                "On_Level_Completed_32_Animation_Started", "In_DoIt_Button_Clicked", "On_Settings_Sound_ON",
                "PurchaseAPI_Started", "On_Level_Completed_31_Animation_Skipped", "On_Level_Completed_33_Animation_Started",
                "Level_33_Data_Fetched", "Quest_Restart_For_2_Time", "On_Level_Completed_34_Animation_Started",
                "DeleteAPI_Success", "app_clear_data", "Level_34_Data_Fetched", "On_sound_OFF_gameplay",
                "ReferAPI_Success", "ReferAPI_Started", "On_Level_Completed_33_Animation_Skipped",
                "On_Level_Completed_34_Animation_Skipped", "Level_35_Data_Fetched", "DeleteAPI_Fail",
                "On_Main_Screen_Tripeaks_Loading", "On_Main_Screen_Data_Received", "On_Main_Screen_Event_Invoked",
                "On_Level_Completed_32_Animation_Skipped", "On_Level_Completed_35_Animation_Skipped",
                "On_Level_Completed_35_Animation_Started", "DocLeaderboardAPI_Fail", "Firebase_Data_update_found",
                "DocTournamentAPI_Started","FR_Fetch_Completed"


            ]

        # Step 6: Filter to keep only the events to consider
            df['date'] = df['timestamp'].dt.date

        # Step 4: Filter the dataframe for 'first_open' event
            first_open_df = df[df['event_name'] == 'first_open']

            # Step 5: Get unique dates where 'first_open' event occurred
            first_open_dates = first_open_df['date'].dropna().unique()

            # Step 6: Add a sidebar selectbox for the user to pick a date from 'first_open' event dates
            selected_date = st.sidebar.selectbox('Select Date (first_open users)', sorted(first_open_dates, reverse=False))

            # Step 7: Filter the entire dataset based on the selected date
            df_filtered = df[df['date'] == selected_date]

            #st.write(f"Displaying data for the selected date: {selected_date}")

            ### Step 1: First Pivot Table - Date-wise Unique Users (filtered by selected_date)
            #datewise_users = df_filtered.groupby('date')['user_pseudo_id'].nunique().reset_index()
            #datewise_users.columns = ['Date', 'Unique Users']

            # Calculate the percentage of users for each date
            #datewise_users['Percentage'] = (datewise_users['Unique Users'] / datewise_users['Unique Users'].sum()) * 100

            #st.write("Date-wise Unique Users and Percentage (Filtered by Selected Date):")
            #st.write(datewise_users.style.format({'Percentage': "{:.2f}%"}))

            ### Step 2: Retention and Churn Percentage Calculation

            # Filter for 'app_remove' event in the dataset
            app_remove_df = df[df['event_name'] == 'app_remove']

            # Count unique 'app_remove' users on the selected date
            app_remove_users_count = app_remove_df[app_remove_df['date'] == selected_date]['user_pseudo_id'].nunique()

            # Count unique 'first_open' users on the selected date
            first_open_users_count = first_open_df[first_open_df['date'] == selected_date]['user_pseudo_id'].nunique()

            ### NEW LOGIC FOR RETENTION:
            # Find users who had 'first_open' on the selected date and came back the next day
            next_day = pd.to_datetime(selected_date) + pd.Timedelta(days=1)
            next_day_users = df[(df['date'] == next_day.date()) & (df['user_pseudo_id'].isin(first_open_df['user_pseudo_id']))]

            # Count unique users who came back on the next day
            next_day_users_count = next_day_users['user_pseudo_id'].nunique()

            # Calculate retention and churn percentage
            if first_open_users_count > 0:
                Churn_percentage = (next_day_users_count / first_open_users_count) * 100
                App_Remove_percentage = (app_remove_users_count / first_open_users_count) * 100
            else:
                Churn_percentage = 0
                App_Remove_percentage = 0

            ### Display Retention and Churn Percentage in Card Format

            st.markdown(f"""
                <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                    <div style="
                        padding: 10px; 
                        background-color: #e0f7fa; 
                        border-radius: 10px; 
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        text-align: center;
                        width: 40%;
                    ">
                        <h3 style="margin: 0;">Churn percentage</h3>
                        <h2 style="margin: 0; color: #00796b;">{Churn_percentage:.2f}%</h2>
                    </div>
                    <div style="
                        padding: 10px; 
                        background-color: #ffebee; 
                        border-radius: 10px; 
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        text-align: center;
                        width: 40%;
                    ">
                        <h3 style="margin: 0;">AppRemove percentage</h3>
                        <h2 style="margin: 0; color: #d32f2f;">{App_Remove_percentage:.2f}%</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            ### Step 3: Event sequence table (Filtered by Selected Date)
            df_filtered['event_sequence'] = df_filtered.groupby('user_pseudo_id')['event_name'].transform(lambda x: ' -> '.join(x))

            # Drop duplicates to keep only unique sequences per user
            unique_sequences = df_filtered[['user_pseudo_id', 'event_sequence']].drop_duplicates()

            # Group by event sequences and count users
            path_user_counts = unique_sequences.groupby('event_sequence')['user_pseudo_id'].nunique().reset_index()
            path_user_counts.columns = ['event_sequence', 'Total Users']
            path_user_counts = path_user_counts.sort_values(by='Total Users', ascending=False)

            # Display the event sequences and user counts
            st.write("Unique User Event Flows and User Counts (Filtered by Selected Date):")
            st.dataframe(path_user_counts)


            # Step 9: Display the results: User IDs and their event sequences
            st.write("User IDs and Their Event Sequences (Filtered):")
            st.dataframe(unique_sequences)

        # Step 7: Identify users whose last event is 'app_remove'
            df_last_event = df.groupby('user_pseudo_id').tail(1)
            app_remove_users = df_last_event[df_last_event['event_name'] == 'app_remove']
            non_app_remove_users = df_last_event[df_last_event['event_name'] != 'app_remove']

            # Step 8: Merge to get event sequences for users with 'app_remove' as the last event
            app_remove_sequences = unique_sequences[unique_sequences['user_pseudo_id'].isin(app_remove_users['user_pseudo_id'])]

            # Step 9: Merge to get event sequences for users without 'app_remove' as the last event
            non_app_remove_sequences = unique_sequences[unique_sequences['user_pseudo_id'].isin(non_app_remove_users['user_pseudo_id'])]

            # Display the results
            st.write("Users Whose Last Event is 'app_remove':")
            st.dataframe(app_remove_sequences)

            total_app_remove_users = len(app_remove_sequences)

            path_user_counts = app_remove_sequences.groupby('event_sequence')['user_pseudo_id'].nunique().reset_index()
            path_user_counts.columns = ['event_sequence', 'user_count']
            path_user_counts['Percentage'] = (path_user_counts['user_count'] / total_app_remove_users) * 100
            path_user_counts = path_user_counts.sort_values(by='user_count', ascending=False)
            st.write("App removed Users event flow:")
            st.dataframe(path_user_counts.style.format({'Percentage': "{:.2f}%"}))

            st.write("Users Whose Last Event is Not 'app_remove':")
            st.dataframe(non_app_remove_sequences)

            total_non_app_remove_users = len(non_app_remove_sequences)

            path_user_counts_non_remove = non_app_remove_sequences.groupby('event_sequence')['user_pseudo_id'].nunique().reset_index()
            path_user_counts_non_remove.columns = ['event_sequence', 'user_count']
            path_user_counts_non_remove['Percentage'] = (path_user_counts_non_remove['user_count'] / total_non_app_remove_users) * 100
            path_user_counts_non_remove = path_user_counts_non_remove.sort_values(by='user_count', ascending=False)
            st.write("Churn Users event flow:")
            st.dataframe(path_user_counts_non_remove.style.format({'Percentage': "{:.2f}%"}))

            total_users = len(unique_sequences)

            # Step 11: Create the user counts table with percentages
            user_counts = {
                "Category": ["App Removed", "Churn"],
                "User Count": [len(app_remove_sequences), len(non_app_remove_sequences)],
            }
            user_counts_df = pd.DataFrame(user_counts)
            user_counts_df["Percentage"] = (user_counts_df["User Count"] / total_users) * 100
            user_counts_df = user_counts_df.set_index("Category")

            # Step 12: Display the vertical summary table with percentages formatted
            st.write("Summary of User Counts (Vertical with Percentage):")
            st.dataframe(user_counts_df.style.format({"Percentage": "{:.2f}%"}))


            app_remove_sequences['last_5_events'] = app_remove_sequences['event_sequence'].apply(lambda x: ' -> '.join(x.split(' -> ')[-5:]))

            # Calculate the total number of users whose last event is 'app_remove'
            total_app_remove_users = len(app_remove_sequences)

            # Group by the last 5 events and count the number of users, then calculate the percentage
            path_user_counts_last_5_1 = app_remove_sequences.groupby('last_5_events')['user_pseudo_id'].nunique().reset_index()
            path_user_counts_last_5_1.columns = ['last_5_events', 'user_count']
            path_user_counts_last_5_1['Percentage'] = (path_user_counts_last_5_1['user_count'] / total_app_remove_users) * 100
            path_user_counts_last_5_1 = path_user_counts_last_5_1.sort_values(by='user_count', ascending=False)
            users_last_5_events = app_remove_sequences[['user_pseudo_id', 'last_5_events']].drop_duplicates()
            # Display the results
            st.write("App removed Users event flow (Last 5 Events):")
            st.dataframe(path_user_counts_last_5_1.style.format({'Percentage': "{:.2f}%"}))

            #st.write("App removed Users and their Last 5 Events:")
            #st.dataframe(users_last_5_events)

            non_app_remove_sequences['last_5_events'] = non_app_remove_sequences['event_sequence'].apply(lambda x: ' -> '.join(x.split(' -> ')[-5:]))

            # Calculate the total number of users whose last event is 'app_remove'
            total_app_remove_users = len(non_app_remove_sequences)

            # Group by the last 5 events and count the number of users, then calculate the percentage
            path_user_counts_last_5_2 = non_app_remove_sequences.groupby('last_5_events')['user_pseudo_id'].nunique().reset_index()
            path_user_counts_last_5_2.columns = ['last_5_events', 'user_count']
            path_user_counts_last_5_2['Percentage'] = (path_user_counts_last_5_2['user_count'] / total_non_app_remove_users) * 100
            path_user_counts_last_5_2 = path_user_counts_last_5_2.sort_values(by='user_count', ascending=False)
            users_last_5_events = non_app_remove_sequences[['user_pseudo_id', 'last_5_events']].drop_duplicates()
            # Display the results
            st.write("Churn Users event flow (Last 5 Events):")
            st.dataframe(path_user_counts_last_5_2.style.format({'Percentage': "{:.2f}%"}))

            #st.write("Churn Users and their Last 5 Events:")
            #st.dataframe(users_last_5_events)


           # Step 2: Aggregate events based on 'On_Level_Successful' and its variations
            def contains_on_level_successful(sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('On_Level_Successful' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_level_successful_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_on_level_successful)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_level_successful_count = on_level_successful_sequences['user_pseudo_id'].nunique()

            # Create a new table for users who had 'On_Level_Successful' or its variations
            def contains_on_level_loaded(sequence):
                # Check if the sequence contains any 'loaded' event variants
                loaded_events = ['On_Level_easy_loaded', 'On_Level_easymedium_loaded', 'On_Level_medium_loaded', 'On_Level_superhard_loaded', 'On_Level_hard_loaded']
                return any(event in sequence.split(' -> ') for event in loaded_events)

            # Filter sequences containing any of the 'loaded' events
            on_level_loaded_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_on_level_loaded)]

            # Total count of users with 'loaded' events in their last 5 events
            on_level_loaded_count = on_level_loaded_sequences['user_pseudo_id'].nunique()

            def contains_rm_mapcard_events(sequence):
            # Regex patterns for events with variations
                rm_mapcard_events_variations = [
                    r'RM_Scenario_with_MC_Created.*',    # Matches any variant of RM_Scenario_with_MC_Created
                    r'MapCard.*_Clicked',                # Matches any variant of MapCard_Clicked
                    r'RM_Scenario_with_MC_EndGame_Clicked.*'  # Matches any variant of RM_Scenario_with_MC_EndGame_Clicked
                ]

                # Exact event names without variations
                exact_events = [
                    'WildCard_Clicked',
                    'Booster_Remove_Cards_Used',
                    'MaxNonMatchCard',
                    'DeckCard_00_Clicked'
                ]

                # Check for variations using regex
                sequence_events = sequence.split(' -> ')
                for event in sequence_events:
                    if any(re.match(pattern, event) for pattern in rm_mapcard_events_variations):
                        return True
                    if event in exact_events:  # Check for exact matches for non-variant events
                        return True
                return False

            # Filter sequences containing any of the 'RM_Scenario_with_MC_Created', 'MapCard_Clicked', or exact matches
            rm_mapcard_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_rm_mapcard_events)]

            # Total count of users with these events in their last 5 events
            rm_mapcard_count = rm_mapcard_sequences['user_pseudo_id'].nunique()


            # Step 5: Aggregate events based on 'Level_CardOpened' and its variants
            def contains_level_card_opened(sequence):
                # Use a regular expression to match any event that includes 'Level' followed by '_CardOpened'
                return any(re.search(r'Level_\d*_CardOpened', event) for event in sequence.split(' -> '))

            # Filter sequences containing 'Level_CardOpened' or its variants
            level_card_opened_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_level_card_opened)]

            # Total count of users with 'Level_CardOpened' in their last 5 events
            level_card_opened_count = level_card_opened_sequences['user_pseudo_id'].nunique()

            def contains_on_level_adwatch(sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('On_Level_Success_Ad_Watched' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_level_adwatch_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_on_level_adwatch)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_level_adwatch_count = on_level_adwatch_sequences['user_pseudo_id'].nunique()

            def contains_result_popup(sequence):
                # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
                result_popup_events = ['On_Level_Completed_Result_Opened', 'On_Level_Completed_Result_Continue']
                #return any(event.startswith('RM_Scenario_with_MC_Created') and event.startswith('MapCard_Clicked') and event.startswith('DeckCard_00_Clicked') and event.startswith('MaxNonMatchCard') and event.startswith('Booster_Remove_Cards_Used') and event.startswith('WildCard_Clicked') and event.startswith('RM_Scenario_with_MC_EndGame_Clicked')for event in sequence.split(' -> '))
                return any(event in sequence.split(' -> ') for event in result_popup_events)

            # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            result_popup_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_result_popup)]

            # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            result_popup_count = rm_mapcard_sequences['user_pseudo_id'].nunique()


            def contains_on_main_screen(sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('On_Main_Screen_Open' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_main_screen_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_on_main_screen)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_main_screen_count = on_main_screen_sequences['user_pseudo_id'].nunique()

            def contains_level_popup(sequence):
                # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
               return any(re.search(r'On_Level\d*_Popup_closed', event) for event in sequence.split(' -> '))

            # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            level_popup_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_level_popup)]

            # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            level_popup_count = level_popup_sequences['user_pseudo_id'].nunique()

            def contains_on_firstopen (sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('first_open' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_firstopen_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_on_firstopen)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_firstopen_count = on_firstopen_sequences['user_pseudo_id'].nunique()

            def contains_level_fail(sequence):
                    # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
                    level_fail_events = ['On_Level_Failed']
                    #return any(event.startswith('RM_Scenario_with_MC_Created') and event.startswith('MapCard_Clicked') and event.startswith('DeckCard_00_Clicked') and event.startswith('MaxNonMatchCard') and event.startswith('Booster_Remove_Cards_Used') and event.startswith('WildCard_Clicked') and event.startswith('RM_Scenario_with_MC_EndGame_Clicked')for event in sequence.split(' -> '))
                    return any(event in sequence.split(' -> ') for event in level_fail_events)

                # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            level_fail_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_level_fail)]

                # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            level_fail_count = level_fail_sequences['user_pseudo_id'].nunique()


            def is_second_to_last_event_level_started(sequence):
                # Split the event sequence into a list of events
                events = sequence.split(' -> ')
                # Ensure there are at least 2 events and the last one is 'app_remove'
                if len(events) >= 2 and events[-1] == 'app_remove':
                    # Check if the second-to-last event starts with 'On_Level_Started'
                    return events[-2].startswith('On_Level_Started_1')
                return False

            # Filter sequences where the second-to-last event is a variation of 'On_Level_Started'
            level_started_before_remove_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(is_second_to_last_event_level_started)]

            # Total count of users whose second-to-last event is 'On_Level_Started' before 'app_remove'
            level_started_count = level_started_before_remove_sequences['user_pseudo_id'].nunique()


            def contains_dailybonus_collect(sequence):
                    # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
                    contains_dailybonus_collect_events = ['On_Level_Failed']
                    return any(event in sequence.split(' -> ') for event in contains_dailybonus_collect_events)

                # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            dailybonus_collect_sequences = app_remove_sequences[app_remove_sequences['last_5_events'].apply(contains_dailybonus_collect)]

                # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            dailybonus_collect_count = dailybonus_collect_sequences['user_pseudo_id'].nunique()


            # Create a new table for all event groups (On_Level_Successful, Loaded Events, RM/MapCard Events, Level_CardOpened)
            event_summary_table = pd.DataFrame({
                'Event Group': [
                    'users successfully completed a level',
                    'users started the next level and loaded level ease',
                    'users started a level and left the game (map card collected)',
                    'users started a level and opened a card',
                    'users achieved level success and watched an advertisement',
                    'users saw the level completion result popup',
                    'users opened the app for the first time and viewed the main screen',
                    'users encountered the next level popup',
                    'users opened the app for the first time',
                    'users experienced a level failure',
                    'users started a level',
                    'users started a level and collected the daily bonus'
                ],
                'Total Users': [on_level_successful_count, on_level_loaded_count, rm_mapcard_count, level_card_opened_count, on_level_adwatch_count,result_popup_count,
                                on_main_screen_count,level_popup_count,on_firstopen_count,level_fail_count,level_started_count,dailybonus_collect_count]
            })
            total_users = event_summary_table['Total Users'].sum()

            # Add a percentage column
            event_summary_table['Percentage'] = (event_summary_table['Total Users'] / total_users) * 100
            event_summary_table = event_summary_table.sort_values(by='Total Users', ascending=False)
            # Display the new table summarizing all four event groups
            st.write("senerio of App Removed Users:")
            st.dataframe(event_summary_table.style.format({'Percentage': "{:.2f}%"}))


            def contains_on_level_successful(sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('On_Level_Successful' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_level_successful_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_on_level_successful)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_level_successful_count = on_level_successful_sequences['user_pseudo_id'].nunique()

            # Create a new table for users who had 'On_Level_Successful' or its variations
            def contains_on_level_loaded(sequence):
                # Check if the sequence contains any 'loaded' event variants
                loaded_events = ['On_Level_easy_loaded', 'On_Level_easymedium_loaded', 'On_Level_medium_loaded', 'On_Level_superhard_loaded', 'On_Level_hard_loaded']
                return any(event in sequence.split(' -> ') for event in loaded_events)

            # Filter sequences containing any of the 'loaded' events
            on_level_loaded_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_on_level_loaded)]

            # Total count of users with 'loaded' events in their last 5 events
            on_level_loaded_count = on_level_loaded_sequences['user_pseudo_id'].nunique()

            def contains_rm_mapcard_events(sequence):
            # Regex patterns for events with variations
                rm_mapcard_events_variations = [
                    r'RM_Scenario_with_MC_Created.*',    # Matches any variant of RM_Scenario_with_MC_Created
                    r'MapCard.*_Clicked',                # Matches any variant of MapCard_Clicked
                    r'RM_Scenario_with_MC_EndGame_Clicked.*'  # Matches any variant of RM_Scenario_with_MC_EndGame_Clicked
                ]

                # Exact event names without variations
                exact_events = [
                    'WildCard_Clicked',
                    'Booster_Remove_Cards_Used',
                    'MaxNonMatchCard',
                    'DeckCard_00_Clicked'
                ]

                # Check for variations using regex
                sequence_events = sequence.split(' -> ')
                for event in sequence_events:
                    if any(re.match(pattern, event) for pattern in rm_mapcard_events_variations):
                        return True
                    if event in exact_events:  # Check for exact matches for non-variant events
                        return True
                return False

            # Filter sequences containing any of the 'RM_Scenario_with_MC_Created', 'MapCard_Clicked', or exact matches
            rm_mapcard_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_rm_mapcard_events)]

            # Total count of users with these events in their last 5 events
            rm_mapcard_count = rm_mapcard_sequences['user_pseudo_id'].nunique()


            # Step 5: Aggregate events based on 'Level_CardOpened' and its variants
            def contains_level_card_opened(sequence):
                # Use a regular expression to match any event that includes 'Level' followed by '_CardOpened'
                return any(re.search(r'Level_\d*_CardOpened', event) for event in sequence.split(' -> '))

            # Filter sequences containing 'Level_CardOpened' or its variants
            level_card_opened_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_level_card_opened)]

            # Total count of users with 'Level_CardOpened' in their last 5 events
            level_card_opened_count = level_card_opened_sequences['user_pseudo_id'].nunique()

            def contains_on_level_adwatch(sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('On_Level_Success_Ad_Watched' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_level_adwatch_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_on_level_adwatch)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_level_adwatch_count = on_level_adwatch_sequences['user_pseudo_id'].nunique()

            def contains_result_popup(sequence):
                # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
                result_popup_events = ['On_Level_Completed_Result_Opened', 'On_Level_Completed_Result_Continue']
                #return any(event.startswith('RM_Scenario_with_MC_Created') and event.startswith('MapCard_Clicked') and event.startswith('DeckCard_00_Clicked') and event.startswith('MaxNonMatchCard') and event.startswith('Booster_Remove_Cards_Used') and event.startswith('WildCard_Clicked') and event.startswith('RM_Scenario_with_MC_EndGame_Clicked')for event in sequence.split(' -> '))
                return any(event in sequence.split(' -> ') for event in result_popup_events)

            # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            result_popup_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_result_popup)]

            # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            result_popup_count = rm_mapcard_sequences['user_pseudo_id'].nunique()


            def contains_on_main_screen(sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('On_Main_Screen_Open' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_main_screen_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_on_main_screen)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_main_screen_count = on_main_screen_sequences['user_pseudo_id'].nunique()

            def contains_level_popup(sequence):
                # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
               return any(re.search(r'On_Level\d*_Popup_closed', event) for event in sequence.split(' -> '))

            # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            level_popup_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_level_popup)]

            # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            level_popup_count = level_popup_sequences['user_pseudo_id'].nunique()

            def contains_on_firstopen (sequence):
                # Check if any part of the event sequence contains 'On_Level_Successful'
                return any('first_open' in event for event in sequence.split(' -> '))

            # Filter sequences containing 'On_Level_Successful'
            on_firstopen_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_on_firstopen)]

            # Total count of users with 'On_Level_Successful' in their last 5 events
            on_firstopen_count = on_firstopen_sequences['user_pseudo_id'].nunique()

            def contains_level_fail(sequence):
                    # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
                    level_fail_events = ['On_Level_Failed']
                    #return any(event.startswith('RM_Scenario_with_MC_Created') and event.startswith('MapCard_Clicked') and event.startswith('DeckCard_00_Clicked') and event.startswith('MaxNonMatchCard') and event.startswith('Booster_Remove_Cards_Used') and event.startswith('WildCard_Clicked') and event.startswith('RM_Scenario_with_MC_EndGame_Clicked')for event in sequence.split(' -> '))
                    return any(event in sequence.split(' -> ') for event in level_fail_events)

                # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            level_fail_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_level_fail)]

                # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            level_fail_count = level_fail_sequences['user_pseudo_id'].nunique()


            def is_last_event_level_started(sequence):
            # Get the last event from the sequence
                last_event = sequence.split(' -> ')[-1]  # Extract the last event in the sequence
                # Check if the last event starts with 'On_Level_Started'
                return last_event.startswith('On_Level_Started')

            # Filter sequences where the last event in the last 5 events starts with 'On_Level_Started'
            level_started_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(is_last_event_level_started)]

            # Total count of users with 'On_Level_Started' as the last event in their last 5 events
            level_started_count = level_started_sequences['user_pseudo_id'].nunique()


            def contains_dailybonus_collect(sequence):
                    # Check if the sequence contains any 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' event variants
                    contains_dailybonus_collect_events = ['On_Level_Failed']
                    return any(event in sequence.split(' -> ') for event in contains_dailybonus_collect_events)

                # Filter sequences containing any of the 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' variants
            dailybonus_collect_sequences = non_app_remove_sequences[non_app_remove_sequences['last_5_events'].apply(contains_dailybonus_collect)]

                # Total count of users with 'RM_Scenario_with_MC_Created' or 'MapCard_Clicked' events in their last 5 events
            dailybonus_collect_count = dailybonus_collect_sequences['user_pseudo_id'].nunique()




            # Create a new table for all event groups (On_Level_Successful, Loaded Events, RM/MapCard Events, Level_CardOpened)
            event_summary_table = pd.DataFrame({
                'Event Group': [
                    'users successfully completed a level',
                    'users started the next level and loaded level ease',
                    'users started a level and left the game (map card collected)',
                    'users started a level and opened a card',
                    'users achieved level success and watched an advertisement',
                    'users saw the level completion result popup',
                    'users opened the app for the first time and viewed the main screen',
                    'users encountered the next level popup',
                    'users opened the app for the first time',
                    'users experienced a level failure',
                    'users started a level',
                    'users started a level and collected the daily bonus'
                ],
                'Total Users': [on_level_successful_count, on_level_loaded_count, rm_mapcard_count, level_card_opened_count, on_level_adwatch_count,result_popup_count,
                                on_main_screen_count,level_popup_count,on_firstopen_count,level_fail_count,level_started_count,dailybonus_collect_count]
            })
            total_users = event_summary_table['Total Users'].sum()

            # Add a percentage column
            event_summary_table['Percentage'] = (event_summary_table['Total Users'] / total_users) * 100
            event_summary_table = event_summary_table.sort_values(by='Total Users', ascending=False)
            # Display the updated table with the percentage column
            st.write("Scenario of Churn Users:")
            st.dataframe(event_summary_table.style.format({'Percentage': "{:.2f}%"}))



if __name__ == "__main__":
    main()
