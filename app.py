import requests
import streamlit as st
import datetime
import pandas as pd
import os
from dotenv import load_dotenv
st.set_page_config(
    page_title="NBA Live Dashboard",  # Title shown on the browser tab
    page_icon="https://images.ctfassets.net/h8q6lxmb5akt/5qXnOINbPrHKXWa42m6NOa/421ab176b501f5bdae71290a8002545c/nba-logo_2x.png",  # Emoji or image URL
    layout="wide",  # Options: "centered" (default) or "wide"
    initial_sidebar_state="collapsed"  # Options: "auto", "expanded", "collapsed"
)

load_dotenv()
st.markdown("""
    <style>
        .title-container {
            display: flex;
            align-items: center;
            text-align: center;
            justify-content: center;
        }
        .title-container img {
            height: 70px;  /* Adjust size of the image */
            margin-right: 0px;  /* Space between image and title */
            text-align: center;

        }
        .title-container h1 {
            margin: 0;  /* Remove margin for the title */
            font-size: 2.5rem;  /* Adjust font size of the title */
            text-align: center;  /* Center the title */
        }
    </style>
    <div class="title-container">
        <img src="https://images.ctfassets.net/h8q6lxmb5akt/5qXnOINbPrHKXWa42m6NOa/421ab176b501f5bdae71290a8002545c/nba-logo_2x.png" alt="NBA Logo">
        <h1>NBA Live Dashboard</h1>
    </div>
""", unsafe_allow_html=True)
custom_css = """
<style>
    /* Style for all tabs */
    .stTabs [role="tab"] {
        background-color: #e8e8e8;
        color: #4f4f4f;
        font-family: 'Courier New', Courier, monospace;
        padding: 10px;
        border-radius: 5px;
        margin-right: 5px;
    }
    
    /* Active (selected) tab */
    .stTabs [aria-selected="true"] {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    h1, .stMarkdown h1 {
        color: #8110ad !important;
        text-align: center;
    }
     .basic-box {
            width: 100%;  /* Make the box take full width */
            padding: 10px;
            background-color: #f0f0f0;
            border: 2px solid #d1d1d1;
            border-radius: 10px;
            margin-bottom: 15px;
            color: #3498db;
            text-align: center;  /* This centers the text horizontally */
            display: flex;  /* Enables flexbox */
            justify-content: left;  /* Centers the content horizontally */
            align-items: center;  /* Centers the content vertically */
            height: 100px;  /* Adjust the height for vertical centering */
        }
        .basic-box div {
            display: flex;
            align-items: center;
            gap: 15px;  /* Space between image and team name */
    }   

        .basic-box img {
            max-width: 60px;  /* Adjust the image size */
            height: auto;  /* Maintain aspect ratio */
        }

        .basic-box span {
            font-weight: bold;
            font-size: 18px;  /* Increase font size for clarity */
        }
        </style>
        """
team_logos = {
    "Atlanta Hawks": "https://loodibee.com/wp-content/uploads/nba-atlanta-hawks-logo.png",
    "Boston Celtics": "https://loodibee.com/wp-content/uploads/nba-boston-celtics-logo.png",
    "Brooklyn Nets": "https://loodibee.com/wp-content/uploads/brooklyn-nets-logo-symbol.png",
    "Charlotte Hornets": "https://loodibee.com/wp-content/uploads/nba-charlotte-hornets-logo.png",
    "Chicago Bulls": "https://loodibee.com/wp-content/uploads/nba-chicago-bulls-logo.png",
    "Cleveland Cavaliers": "https://loodibee.com/wp-content/uploads/nba-cleveland-cavaliers-logo.png",
    "Dallas Mavericks": "https://loodibee.com/wp-content/uploads/nba-dallas-mavericks-logo.png",
    "Denver Nuggets": "https://content.sportslogos.net/logos/6/229/full/8926_denver_nuggets-primary-2019.png",
    "Detroit Pistons": "https://loodibee.com/wp-content/uploads/nba-detroit-pistons-logo.png",
    "Golden State Warriors": "https://loodibee.com/wp-content/uploads/nba-golden-state-warriors-logo.png",
    "Houston Rockets": "https://loodibee.com/wp-content/uploads/nba-houston-rockets-logo.png",
    "Indiana Pacers": "https://loodibee.com/wp-content/uploads/nba-indiana-pacers-logo.png",
    "Los Angeles Clippers": "https://content.sportslogos.net/logos/6/236/full/los_angeles_clippers_logo_primary_2025_sportslogosnet-5542.png",
    "Los Angeles Lakers": "https://loodibee.com/wp-content/uploads/nba-los-angeles-lakers-logo.png",
    "Memphis Grizzlies": "https://loodibee.com/wp-content/uploads/nba-memphis-grizzlies-logo.png",
    "Miami Heat": "https://loodibee.com/wp-content/uploads/nba-miami-heat-logo.png",
    "Milwaukee Bucks": "https://loodibee.com/wp-content/uploads/nba-milwaukee-bucks-logo.png",
    "Minnesota Timberwolves": "https://loodibee.com/wp-content/uploads/nba-minnesota-timberwolves-logo.png",
    "New Orleans Pelicans": "https://loodibee.com/wp-content/uploads/nba-new-orleans-pelicans-logo.png",
    "New York Knicks": "https://loodibee.com/wp-content/uploads/nba-new-york-knicks-logo.png",
    "Oklahoma City Thunder": "https://loodibee.com/wp-content/uploads/nba-oklahoma-city-thunder-logo.png",
    "Orlando Magic": "https://loodibee.com/wp-content/uploads/nba-orlando-magic-logo.png",
    "Philadelphia 76ers": "https://loodibee.com/wp-content/uploads/nba-philadelphia-76ers-logo.png",
    "Phoenix Suns": "https://loodibee.com/wp-content/uploads/nba-phoenix-suns-logo.png",
    "Portland Trail Blazers": "https://loodibee.com/wp-content/uploads/nba-portland-trail-blazers-logo.png",
    "Sacramento Kings": "https://loodibee.com/wp-content/uploads/nba-sacramento-kings-logo.png",
    "San Antonio Spurs": "https://loodibee.com/wp-content/uploads/nba-san-antonio-spurs-logo.png",
    "Toronto Raptors": "https://content.sportslogos.net/logos/6/227/full/7024_toronto_raptors-primary-2021.png",
    "Utah Jazz": "https://loodibee.com/wp-content/uploads/nba-utah-jazz-logo.png",
    "Washington Wizards": "https://loodibee.com/wp-content/uploads/nba-washington-wizards-logo.png"
    }
team_shortcut_logos = {
    "Hawks": "https://loodibee.com/wp-content/uploads/nba-atlanta-hawks-logo.png",
    "Celtics": "https://loodibee.com/wp-content/uploads/nba-boston-celtics-logo.png",
    "Nets": "https://loodibee.com/wp-content/uploads/brooklyn-nets-logo-symbol.png",
    "Hornets": "https://loodibee.com/wp-content/uploads/nba-charlotte-hornets-logo.png",
    "Bulls": "https://loodibee.com/wp-content/uploads/nba-chicago-bulls-logo.png",
    "Cavaliers": "https://loodibee.com/wp-content/uploads/nba-cleveland-cavaliers-logo.png",
    "Mavericks": "https://loodibee.com/wp-content/uploads/nba-dallas-mavericks-logo.png",
    "Nuggets": "https://content.sportslogos.net/logos/6/229/full/8926_denver_nuggets-primary-2019.png",
    "Pistons": "https://loodibee.com/wp-content/uploads/nba-detroit-pistons-logo.png",
    "Warriors": "https://loodibee.com/wp-content/uploads/nba-golden-state-warriors-logo.png",
    "Rockets": "https://loodibee.com/wp-content/uploads/nba-houston-rockets-logo.png",
    "Pacers": "https://loodibee.com/wp-content/uploads/nba-indiana-pacers-logo.png",
    "Clippers": "https://content.sportslogos.net/logos/6/236/full/los_angeles_clippers_logo_primary_2025_sportslogosnet-5542.png",
    "Lakers": "https://loodibee.com/wp-content/uploads/nba-los-angeles-lakers-logo.png",
    "Grizzlies": "https://loodibee.com/wp-content/uploads/nba-memphis-grizzlies-logo.png",
    "Heat": "https://loodibee.com/wp-content/uploads/nba-miami-heat-logo.png",
    "Bucks": "https://loodibee.com/wp-content/uploads/nba-milwaukee-bucks-logo.png",
    "Timberwolves": "https://loodibee.com/wp-content/uploads/nba-minnesota-timberwolves-logo.png",
    "Pelicans": "https://loodibee.com/wp-content/uploads/nba-new-orleans-pelicans-logo.png",
    "Knicks": "https://loodibee.com/wp-content/uploads/nba-new-york-knicks-logo.png",
    "Thunder": "https://loodibee.com/wp-content/uploads/nba-oklahoma-city-thunder-logo.png",
    "Magic": "https://loodibee.com/wp-content/uploads/nba-orlando-magic-logo.png",
    "76ers": "https://loodibee.com/wp-content/uploads/nba-philadelphia-76ers-logo.png",
    "Suns": "https://loodibee.com/wp-content/uploads/nba-phoenix-suns-logo.png",
    "Trail Blazers": "https://loodibee.com/wp-content/uploads/nba-portland-trail-blazers-logo.png",
    "Kings": "https://loodibee.com/wp-content/uploads/nba-sacramento-kings-logo.png",
    "Spurs": "https://loodibee.com/wp-content/uploads/nba-san-antonio-spurs-logo.png",
    "Raptors": "https://content.sportslogos.net/logos/6/227/full/7024_toronto_raptors-primary-2021.png",
    "Jazz": "https://loodibee.com/wp-content/uploads/nba-utah-jazz-logo.png",
    "Wizards": "https://loodibee.com/wp-content/uploads/nba-washington-wizards-logo.png"
}
    
# Inject CSS
st.markdown(custom_css, unsafe_allow_html=True)

API_KEY = os.getenv("API_KEY")

def get_injury_report():
    url = f"https://api.sportradar.com/nba/trial/v8/en/league/injuries.json?api_key={API_KEY}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    return None

def get_daily_matches(selected_date):
    formatted_date = selected_date.strftime('%Y/%m/%d')

    url =f"https://api.sportradar.com/nba/trial/v8/en/games/{formatted_date}/schedule.json?api_key={API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_standings(season):
    
    url = f"https://api.sportradar.com/nba/trial/v8/en/seasons/{season}/REG/standings.json?api_key={API_KEY}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None




if 'show_games' not in st.session_state:
    st.session_state.show_games = False

# Callback function to toggle the display of upcoming games
def toggle_games():
    st.session_state.show_games = not st.session_state.show_games

# Example usage of tabs
tab1, tab2, tab3= st.tabs(["📅 Games Schedule", "🏆 Standings", "🩹 Injury Report"])

left_column,median_column, right_column = st.columns([1, 1, 1])
with tab1:
    # Select Date
    selected_date = st.date_input("Select a date")
    st.write("")
    
    # Button to show games
    if st.button("View upcoming games"):
        toggle_games()

    if st.session_state.show_games:
        data = get_daily_matches(selected_date)  # Fetch data once
        if not data or "games" not in data:
            st.write("No games available.")
        else:
            # Create three columns layout
            left_column, median_column, right_column = st.columns([1, 1, 1])
            
            # Ended Games (Left Column)
            with left_column:
                st.write("### Ended Games:")
                ended_games = [game for game in data["games"] if game["status"] == "closed" or game["status"] == "complete"]
                if not ended_games:
                    st.write("No finished games.")
                for game in ended_games:
                    home_team = game["home"]["name"]
                    away_team = game["away"]["name"]
                    home_logo = team_logos.get(home_team, "")
                    away_logo = team_logos.get(away_team, "")
                    home_points = game["home_points"]
                    away_points = game["away_points"]
                    st.markdown(f"""
                        <div class="basic-box">
                            <div>
                                <img src="{home_logo}" alt="{home_team} logo" />
                                <span>{home_team}</span>
                            </div>
                            <span style="margin: 0 40px; color: black;">vs</span>
                            <div>
                                <img src="{away_logo}" alt="{away_team} logo" />
                                <span>{away_team}</span>
                            </div>
                            <span style="margin: 0 40px; color: black;">{home_points} - {away_points}</span>
                        </div>
                        """, unsafe_allow_html=True)

            # Upcoming Games (Middle Column)
            with median_column:
                st.write("### Upcoming Games:")
                upcoming_games = [game for game in data["games"] if game["status"] == "scheduled"]
                if not upcoming_games:
                    st.write("No scheduled games.")
                for game in upcoming_games:
                    home_team = game["home"]["name"]
                    away_team = game["away"]["name"]
                    home_logo = team_logos.get(home_team, "")
                    away_logo = team_logos.get(away_team, "")
                    hour = (game["scheduled"][11:16])  # Convert time to Greek time
                    st.markdown(f"""
                        <div class="basic-box">
                            <div>
                                <img src="{home_logo}" alt="{home_team} logo" />
                                <span>{home_team}</span>
                            </div>
                            <span style="margin: 0 40px; color: black;">vs</span>
                            <div>
                                <img src="{away_logo}" alt="{away_team} logo" />
                                <span>{away_team}</span>
                            </div>
                            <span style="margin: 0 40px; color: black;">⏱️ {hour}</span>
                        </div>
                        """, unsafe_allow_html=True)

            # Live Games (Right Column)
            with right_column:
                st.write("### Live Games:")
                live_games = [game for game in data["games"] if game["status"] == "inprogress"]
                if not live_games:
                    st.write("No games in progress.")
                for game in live_games:
                    home_team = game["home"]["name"]
                    away_team = game["away"]["name"]
                    home_logo = team_logos.get(home_team, "")
                    away_logo = team_logos.get(away_team, "")
                    #home_points = game["home_points"]
                    #away_points = game["away_points"]
                    st.markdown(f"""
                        <div class="basic-box">
                            <div>
                                <img src="{home_logo}" alt="{home_team} logo" />
                                <span>{home_team}</span>
                            </div>
                            <span style="margin: 0 40px; color: black;">vs</span>
                            <div>
                                <img src="{away_logo}" alt="{away_team} logo" />
                                <span>{away_team}</span>
                            </div>
                            
                        </div>
                        """, unsafe_allow_html=True)

            st.write("All times are in UTC time (UTC).")

with tab3:
    if st.button("Get Injury Report"):
        injury_data = get_injury_report()  # Make sure to pass the selected date
        
        # Check if injury_data is a valid structure
        if injury_data:
            # Flatten the data: We'll create a list of dictionaries, each for a player
            injury_list = []
            if "teams" in injury_data:
                for team in injury_data["teams"]:
                        for player in team.get("players", []):
                            injury_description = player.get("injuries", [{}])[0].get('comment', 'No description available')
                            injury_list.append({
                                "Player Name": player["full_name"],
                                "Position": player.get("position", "N/A"),
                                "Injury Description": injury_description,
                                "Status": player.get("injuries", [{}])[0].get("status", "N/A"),
                                "Team": team["name"]
                            })
                
                if injury_list:
                    injury_df = pd.DataFrame(injury_list)
                    st.dataframe(injury_df)
                else:
                    st.write(f"No injuries found.")
            else:
                st.write("No 'teams' data in the injury report.")
        else:
            st.write("No injury report available.")
with tab2:
    st.write("Standings")
    year = st.selectbox("Select a year", options=list(range(2013, 2025)))
    standings = get_standings(year)
    if standings:
        for conf in standings["conferences"]:
            if conf["name"] == "WESTERN CONFERENCE":
                teams_west = []
                st.write("### Western Conference")
                for division in conf["divisions"]:
                    for team in division["teams"]:
                        team_name = team["name"]
                        team_logo = team_shortcut_logos.get(team_name, "")
                        team_wins = team["wins"]
                        team_losses = team["losses"]
                        team_rank = team["calc_rank"]["conf_rank"]
                        teams_west.append({
                            "Team": team_name,
                            "Wins": team_wins,
                            "Losses": team_losses,
                            "Rank": team_rank,
                            "Logo": team_logo
                        })
                teams_west = sorted(teams_west, key=lambda x: x["Rank"])
                for team in teams_west:
                        st.markdown(f"""
                                <div class="basic-box">
                                    <div>
                                        <img src="{team["Logo"]}" alt="{team["Logo"]} logo" />
                                        <span>{team['Team']}</span>
                                    </div>
                                    <span style="margin: 0 40px; color: black;">{team['Wins']} - {team['Losses']}</span>
                                </div>
                                """, unsafe_allow_html = True)
            else:
                teams_east = []
                st.write("### Eastern Conference")
                for division in conf["divisions"]:
                    for team in division["teams"]:
                        team_name = team["name"]
                        team_logo = team_shortcut_logos.get(team_name, "")
                        team_wins = team["wins"]
                        team_losses = team["losses"]
                        team_rank = team["calc_rank"]["conf_rank"]
                        teams_east.append({
                            "Team": team_name,
                            "Wins": team_wins,
                            "Losses": team_losses,
                            "Rank": team_rank,
                            "Logo": team_logo
                        })
                teams_east = sorted(teams_east, key=lambda x: x["Rank"])
                for team in teams_east:
                    st.markdown(f"""
                                <div class="basic-box">
                                    <div>
                                        <img src="{team["Logo"]}" alt="{team["Logo"]} logo" />
                                        <span>{team['Team']}</span>
                                    </div>
                                    <span style="margin: 0 40px; color: black;">{team['Wins']} - {team['Losses']}</span>
                                </div>
                                """, unsafe_allow_html = True)
                
    else:
        st.write("No standings available.")
