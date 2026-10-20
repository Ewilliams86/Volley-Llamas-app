import streamlit as st
import pandas as pd
import datetime

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Volley Llamas - Lineup & Match Hub",
    page_icon="🏐",
    layout="wide"
)

DEFAULT_ROSTER = ["Heidi", "Quinn", "Alivia", "Lillian", "Ellie", "Ella", "Emmalani", "Claire", "Brinley", "Khloe", "Lola"]

# --- INITIALIZE SESSION STATE ARCHIVE ---
if "matches" not in st.session_state:
    st.session_state.matches = {
        "Game 1 vs Velocity (10/07/2026)": {
            "date": "2026-10-07",
            "opponent": "Velocity",
            "active_players": DEFAULT_ROSTER,
            "lineup": {
                "Set 1": {
                    "Starters": ["Alivia", "Claire", "Heidi", "Brinley", "Lillian", "Ella"],
                    "Subs": ["Khloe", "Quinn", "Lola", "Ellie", "Emmalani", "Open / Continuous"]
                },
                "Set 2": {
                    "Starters": ["Khloe", "Quinn", "Lola", "Ellie", "Emmalani", "Ella"],
                    "Subs": ["Alivia", "Claire", "Heidi", "Brinley", "Lillian", "Open / Continuous"]
                },
                "Set 3": {
                    "Starters": ["Alivia", "Quinn", "Heidi", "Ellie", "Lillian", "Emmalani"],
                    "Subs": ["Khloe", "Claire", "Lola", "Brinley", "Emmalani", "Ella"]
                }
            },
            "stats": {p: {"Attempts": 0, "Makes": 0, "Aces": 0, "Points_Won": 0} for p in DEFAULT_ROSTER}
        }
    }

# --- GLOBAL MATCH SELECTOR (TOP BAR) ---
st.title("🏐 CBRC Volley Llamas - Lineup & Stat Hub")

col_m1, col_m2 = st.columns([2, 1])
with col_m1:
    match_list = list(st.session_state.matches.keys()) + ["➕ Create New Game"]
    selected_match_key = st.selectbox("Select Active Game / Match Archive:", match_list)

with col_m2:
    st.write("")
    if selected_match_key == "➕ Create New Game":
        st.info("Set up a new game below!")

# --- APP NAVIGATION TABS ---
tab_lineup, tab_stats, tab_history, tab_rules = st.tabs([
    "📋 Lineup Generator & Editor",
    "📊 Live Serve & Point Tracker",
    "📈 Season History & Trends",
    "⚙️ League Rules & Settings"
])

# --- TAB 1: LINEUP GENERATOR & EDITABLE OVERRIDE ---
with tab_lineup:
    st.header("📋 Lineup Generator & Manual Swap Editor")
   
    if selected_match_key == "➕ Create New Game":
        c1, c2, c3 = st.columns(3)
        with c1:
            game_num = st.text_input("Game Number/Name", "Game 2")
        with c2:
            opp_name = st.text_input("Opponent Name", "Blazers")
        with c3:
            game_date = st.date_input("Match Date", datetime.date.today())
       
        match_title = f"{game_num} vs {opp_name} ({game_date.strftime('%m/%d/%Y')})"
        active_list = st.multiselect("Active Roster Today:", DEFAULT_ROSTER, default=DEFAULT_ROSTER)
       
        rot_style = st.selectbox("Rotation Mode:", ["Buddy System (Equal Play / Rec)", "Fixed Core Positions (Competitive)"])
       
        if st.button("🚀 Generate & Save Match Lineup"):
            st.session_state.matches[match_title] = {
                "date": str(game_date),
                "opponent": opp_name,
                "active_players": active_list,
                "lineup": {
                    "Set 1": {
                        "Starters": ["Alivia", "Claire", "Heidi", "Brinley", "Lillian", "Ella"],
                        "Subs": ["Khloe", "Quinn", "Lola", "Ellie", "Emmalani", "Open / Continuous"]
                    },
                    "Set 2": {
                        "Starters": ["Khloe", "Quinn", "Lola", "Ellie", "Emmalani", "Ella"],
                        "Subs": ["Alivia", "Claire", "Heidi", "Brinley", "Lillian", "Open / Continuous"]
                    },
                    "Set 3": {
                        "Starters": ["Alivia", "Quinn", "Heidi", "Ellie", "Lillian", "Emmalani"],
                        "Subs": ["Khloe", "Claire", "Lola", "Brinley", "Emmalani", "Ella"]
                    }
                },
                "stats": {p: {"Attempts": 0, "Makes": 0, "Aces": 0, "Points_Won": 0} for p in active_list}
            }
            st.success(f"Created {match_title}! Select it in the top dropdown to view, edit, or track stats.")
            st.rerun()
           
    else:
        current_data = st.session_state.matches[selected_match_key]
        st.subheader(f"Active Match: {selected_match_key}")
        st.info("💡 **Coaching Tip:** You or Coach Ashley can manually edit or swap any starter or sub position using the drop-down selectors below!")
       
        s1, s2, s3 = st.tabs(["Set 1 Lineup", "Set 2 Lineup", "Set 3 Lineup"])
        for set_num, set_tab in zip(["Set 1", "Set 2", "Set 3"], [s1, s2, s3]):
            with set_tab:
                col_st, col_su = st.columns(2)
               
                # Editable Starting 6
                with col_st:
                    st.markdown("### 🏐 Starting 6 (Editable)")
                    new_starters = []
                    for idx in range(6):
                        current_player = current_data["lineup"][set_num]["Starters"][idx] if idx < len(current_data["lineup"][set_num]["Starters"]) else DEFAULT_ROSTER[0]
                        selected_player = st.selectbox(
                            f"Serve Order {idx+1}:",
                            DEFAULT_ROSTER,
                            index=DEFAULT_ROSTER.index(current_player) if current_player in DEFAULT_ROSTER else 0,
                            key=f"{selected_match_key}_{set_num}_starter_{idx}"
                        )
                        new_starters.append(selected_player)
                    current_data["lineup"][set_num]["Starters"] = new_starters

                # Editable Subs
                with col_su:
                    st.markdown("### 🔄 Bench Substitutes (Editable)")
                    sub_options = DEFAULT_ROSTER + ["Open / Continuous"]
                    new_subs = []
                    for idx in range(6):
                        current_sub = current_data["lineup"][set_num]["Subs"][idx] if idx < len(current_data["lineup"][set_num]["Subs"]) else "Open / Continuous"
                        selected_sub = st.selectbox(
                            f"Sub Line {idx+1}:",
                            sub_options,
                            index=sub_options.index(current_sub) if current_sub in sub_options else 0,
                            key=f"{selected_match_key}_{set_num}_sub_{idx}"
                        )
                        new_subs.append(selected_sub)
                    current_data["lineup"][set_num]["Subs"] = new_subs

# --- TAB 2: LIVE SERVE & POINT TRACKER ---
with tab_stats:
    st.header("📊 Live Courtside Serve & Point Tracker")
   
    if selected_match_key == "➕ Create New Game":
        st.warning("Please select or create an active game in the top dropdown to start tracking stats.")
    else:
        active_match = st.session_state.matches[selected_match_key]
        p_list = active_match["active_players"]
       
        col_ctrl, col_view = st.columns([1, 2])
       
        with col_ctrl:
            st.subheader("Record Action")
            server = st.selectbox("Select Current Server:", p_list)
           
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✅ Serve IN"):
                    active_match["stats"][server]["Attempts"] += 1
                    active_match["stats"][server]["Makes"] += 1
                    st.toast(f"Logged Serve IN for {server}")
                if st.button("🔥 ACE!"):
                    active_match["stats"][server]["Attempts"] += 1
                    active_match["stats"][server]["Makes"] += 1
                    active_match["stats"][server]["Aces"] += 1
                    active_match["stats"][server]["Points_Won"] += 1
                    st.toast(f"Logged ACE for {server}!")
            with b2:
                if st.button("❌ Serve Out / Net"):
                    active_match["stats"][server]["Attempts"] += 1
                    st.toast(f"Logged Serve Out for {server}")
                if st.button("🏆 Point Scored on Serve"):
                    active_match["stats"][server]["Points_Won"] += 1
                    st.toast(f"Logged Point Won on {server}'s serve!")

        with col_view:
            st.subheader(f"Match Box Score - {selected_match_key}")
            stats_rows = []
            for player_name in p_list:
                p_stat = active_match["stats"].get(player_name, {"Attempts": 0, "Makes": 0, "Aces": 0, "Points_Won": 0})
                att = p_stat["Attempts"]
                mks = p_stat["Makes"]
                pct = (mks / att * 100) if att > 0 else 0.0
                stats_rows.append({
                    "Player": player_name,
                    "Attempts": att,
                    "Serves In": mks,
                    "Serve %": f"{pct:.1f}%",
                    "Aces": p_stat["Aces"],
                    "Points Won on Serve": p_stat["Points_Won"]
                })
           
            df_match_stats = pd.DataFrame(stats_rows)
            st.dataframe(df_match_stats, use_container_width=True)

# --- TAB 3: SEASON HISTORY & TRENDS ---
with tab_history:
    st.header("📈 Season History & Cumulative Trends")
    st.caption("Aggregated performance across all logged matches.")
   
    season_totals = {p: {"Attempts": 0, "Makes": 0, "Aces": 0, "Points_Won": 0} for p in DEFAULT_ROSTER}
   
    for g_key, g_data in st.session_state.matches.items():
        for p_name, p_stat in g_data["stats"].items():
            if p_name not in season_totals:
                season_totals[p_name] = {"Attempts": 0, "Makes": 0, "Aces": 0, "Points_Won": 0}
            season_totals[p_name]["Attempts"] += p_stat["Attempts"]
            season_totals[p_name]["Makes"] += p_stat["Makes"]
            season_totals[p_name]["Aces"] += p_stat["Aces"]
            season_totals[p_name]["Points_Won"] += p_stat["Points_Won"]
           
    season_rows = []
    for p_name, s_stat in season_totals.items():
        att = s_stat["Attempts"]
        mks = s_stat["Makes"]
        pct = (mks / att * 100) if att > 0 else 0.0
        season_rows.append({
            "Player": p_name,
            "Total Serve Attempts": att,
            "Total Serves In": mks,
            "Season Serve %": f"{pct:.1f}%",
            "Total Aces": s_stat["Aces"],
            "Total Points Scored on Serve": s_stat["Points_Won"]
        })
       
    df_season = pd.DataFrame(season_rows)
    st.dataframe(df_season, use_container_width=True)

# --- TAB 4: LEAGUE RULES & SETTINGS ---
with tab_rules:
    st.header("⚙️ CBRC League Rules & Settings Engine")
   
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.subheader("Substitution Limits")
        st.slider("Max Subs Per Stoppage", 1, 6, 3)
        st.number_input("Mandatory Sub Credits Per Match", 1, 10, 4)
        st.selectbox("Match Format", ["3 Fixed Sets (CBRC Standard)", "Best 2 out of 3", "Best 3 out of 5"])
   
    with col_r2:
        st.subheader("Participation Rules")
        st.selectbox("Set Starting Requirement", ["Must start Set 1 or Set 2 (CBRC)", "Must start at least 1 set", "Open / Coach Choice"])
        st.checkbox("Enforce Set 3 Participation for All Active Players", value=True)
        st.checkbox("Enable Libero / Position Tracking", value=False)

