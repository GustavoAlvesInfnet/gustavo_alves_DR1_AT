import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch, Sbopen

parser = Sbopen()

def match_data(match_id):
    return parser.event(match_id)[0]

def get_match_label(matches, match_id):
    row = matches[matches["match_id"] == match_id].iloc[0]
    return f"{row['match_date']} - {row['home_team']} vs {row['away_team']}"

def plot_passes(match, player_name):
    player_filter = (match.type_name=="Pass") & (match.player_name==player_name)
    df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]

    pitch = Pitch(line_color="black", pitch_color="#799351", stripe_color="#799351", stripe=True)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, endnote_height=0.04, axis=False, title_space=0, endnote_space=0)

    pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, width=2, color="white", ax=ax["pitch"])
    pitch.kdeplot(x=df_pass.x, y=df_pass.y, ax=ax["pitch"], shade=True, alpha=0.5, cmap="plasma")

    return fig

def main():
    st.title("Gustavo Alves DR1 AT - Análises de Futebol")

    menu = ["Home", "Dados por competição", "Dados por jogador", "Análises"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Dados por competição":
        st.subheader("Explore os dados sobre as partidas e torneios")

        competitions = sb.competitions()
        competitions_names = competitions["competition_name"].unique()
        competition = st.selectbox("Selecione a competição", competitions_names)
        competition_id = competitions[competitions["competition_name"] == competition]["competition_id"].values[0]
        
        seasons = competitions[competitions["competition_name"] == competition]["season_name"].unique()
        season_name = st.selectbox("Selecione a Temporada", seasons)
        season_id = competitions[competitions["season_name"] == season_name]["season_id"].values[0]
        matches = sb.matches(competition_id=competition_id, season_id=season_id)

        game = st.selectbox("Selecione a partida", matches["match_id"], format_func=lambda idx:get_match_label(matches, idx))

        with st.container():
            st.title("Informações da Partida")

            date= matches[matches["match_id"] == game]["match_date"].values[0]
            st.markdown(f"<h2 style='text-align: center; color: red;'>{date}</h2>", unsafe_allow_html=True)

            referee = matches[matches["match_id"] == game]["referee"].values[0]
            st.markdown(f"<h6 style='text-align: center; color: white;'>Árbitro: {referee}</h6>", unsafe_allow_html=True)

        left_column, right_column = st.columns(2)
        with st.container():
            with left_column:
                st.write("Time da Casa")
                home_team = matches[matches["match_id"] == game]["home_team"].values[0]
                st.subheader(home_team)
                home_score = matches[matches["match_id"] == game]["home_score"].values[0]
                st.metric("Gols", home_score)

            with right_column:
                st.write("Time Visitante")
                away_team = matches[matches["match_id"] == game]["away_team"].values[0]
                st.subheader(away_team)
                away_score = matches[matches["match_id"] == game]["away_score"].values[0]
                st.metric("Gols", away_score)

        st.title("Dribles")
        dribbles = sb.events(match_id=game, split=True, flatten_attrs=False)["dribbles"]
        st.dataframe(dribbles)

        st.title("Passes")
        passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
        st.dataframe(passes)

        st.title("Competições")
        st.dataframe(competitions[competitions["competition_name"] == competition])

    elif choice == "Dados por jogador":
        st.subheader("Dados por jogador")
        fifa_world_cup_22 = sb.matches(competition_id=43, season_id=106)

        final_match_id = fifa_world_cup_22[(fifa_world_cup_22["home_team"] == "Argentina") & (fifa_world_cup_22["away_team"] == "France")].match_id.values[0]
        final_data = match_data(final_match_id)
        col_1, col_2 = st.columns(2)

        with col_1:
            st.subheader("Lionel Messi")

            fig_1 = plot_passes(final_data, "Lionel Andrés Messi Cuccittini")
            st.pyplot(fig_1)




        with col_2:
            st.subheader("Mbappé")

            fig_2 = plot_passes(final_data, "Kylian Mbappé Lottin") 
            st.pyplot(fig_2)




if __name__ == "__main__":
    main()