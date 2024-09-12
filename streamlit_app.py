import streamlit as st
import pandas as pd
import re



uploaded_file = st.sidebar.file_uploader("Upload your event data (CSV only)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    total_unique_users = df['user_pseudo_id'].nunique()
    st.sidebar.header('Total Users')
    st.sidebar.write(f"Total Users: {total_unique_users}")

    # Step 2: Convert 'event_time_UTC' to datetime with the correct format
    df['timestamp'] = pd.to_datetime(df['event_time_UTC'], format='%Y-%m-%d %H:%M:%S.%f %Z', errors='coerce')

    # Step 3: Check if there are any invalid timestamps
    if df['timestamp'].isnull().any():
        st.warning("Some timestamps couldn't be converted. Please check the format.")

    # Step 4: Sort the data by user_id and timestamp
    df = df.sort_values(by=['user_pseudo_id', 'timestamp'])

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
    df_filtered = df[~df['event_name'].isin(events_to_skip)]

    # Step 7: Create event sequences for each user with filtered events
    df_filtered['event_sequence'] = df_filtered.groupby('user_pseudo_id')['event_name'].transform(lambda x: ' -> '.join(x))

    # Step 8: Drop duplicates to keep only unique sequences per user
    unique_sequences = df_filtered[['user_pseudo_id', 'event_sequence']].drop_duplicates()

    path_user_counts = unique_sequences.groupby('event_sequence')['user_pseudo_id'].nunique().reset_index()
    path_user_counts.columns = ['event_sequence', 'user_count']
    path_user_counts = path_user_counts.sort_values(by='user_count', ascending=False)

    # Step 10: Display the results
    st.write("Unique User Event Flows and User Counts (Filtered):")
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

    st.write("App removed Users and their Last 5 Events:")
    st.dataframe(users_last_5_events)

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

    st.write("Churn Users and their Last 5 Events:")
    st.dataframe(users_last_5_events)


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



