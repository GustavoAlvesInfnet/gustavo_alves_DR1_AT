import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch, Sbopen
import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_shots(match, player_name):
    player_filter = (match.type_name=="Shot") & (match.player_name==player_name)
    df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]

    pitch = Pitch(line_color="black", pitch_color="#799351", stripe_color="#799351", stripe=True)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, endnote_height=0.04, axis=False, title_space=0, endnote_space=0)

    pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, width=2, color="white", ax=ax["pitch"])
    pitch.kdeplot(x=df_pass.x, y=df_pass.y, ax=ax["pitch"], shade=True, alpha=0.5, cmap="plasma")

    return fig

def plot_shots_x_goals(matches, game, home_team, away_team):
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

            home_score = matches[matches["match_id"] == game]["home_score"].values[0]
            away_score = matches[matches["match_id"] == game]["away_score"].values[0]

            home_chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]["possession_team"] == home_team
            home_chutes = home_chutes.sum()

            away_chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]["possession_team"] == away_team
            away_chutes = away_chutes.sum()

            max_value = max(home_score, away_score, home_chutes, away_chutes)

            ax1.bar(["Gols", "Chutes"], [home_score, home_chutes])
            ax1.set_title('Comparação de Gols e Chutes - Time da Casa')
            ax1.set_xlabel('Tipo')
            ax1.set_ylabel('Número')
            ax1.set_ylim(0, max_value + 1)

            ax2.bar(["Gols", "Chutes"], [away_score, away_chutes])
            ax2.set_title('Comparação de Gols e Chutes - Time Visitante')
            ax2.set_xlabel('Tipo')
            ax2.set_ylabel('Número')
            ax2.set_ylim(0, max_value + 1)

            return fig

def plot_conversion(matches, game, home_team, away_team):
            fig, ax = plt.subplots(figsize=(8, 6))

            home_score = matches[matches["match_id"] == game]["home_score"].values[0]
            away_score = matches[matches["match_id"] == game]["away_score"].values[0]

            home_chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]["possession_team"] == home_team
            home_chutes = home_chutes.sum()

            away_chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]["possession_team"] == away_team
            away_chutes = away_chutes.sum()

            home_conversao = (home_score / home_chutes) * 100
            away_conversao = (away_score / away_chutes) * 100

            ax.bar(["Time da Casa", "Time Visitante"], [home_conversao, away_conversao])
            ax.set_title('Conversão de Chutes em Gols')
            ax.set_xlabel('Time')
            ax.set_ylabel('Conversão (%)')
            ax.set_ylim(0, 100)

            return(fig)

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

        
        tab1, tab2, tab3 = st.tabs(["Informações sobre a partida", "Informações sobre os jogadores", "Tabelas"])

        with tab1:
            with st.container():
                st.markdown(f"<font size='6'>Informações sobre a partida <font color='#F63366'>{get_match_label(matches, game)}</font> na competição <font color='#F63366'>{competition}</font> na Temporada <font color='#F63366'>{season_name}</font></font>", unsafe_allow_html=True)



            left_column, right_column = st.columns(2)
            with st.container():
                with left_column:
                    st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold'>Time da Casa</div>", unsafe_allow_html=True)
                    home_team = matches[matches["match_id"] == game]["home_team"].values[0]
                    st.markdown(f"<div style='text-align: center; font-size: 24px; color: #F63366'>{home_team}</div>", unsafe_allow_html=True)
                    home_score = matches[matches["match_id"] == game]["home_score"].values[0]
                    st.markdown(f"<div style='text-align: center; font-size: 18px'>Gols: {home_score}</div>", unsafe_allow_html=True)

                    passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
                    passes_home_team = passes["possession_team"] == home_team
                    passes_home_team=passes_home_team.sum()
                    st.markdown(f"<div style='text-align: center; font-size: 18px'>Passes: {passes_home_team}</div>", unsafe_allow_html=True)

                    chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]
                    chutes_home_team = chutes["possession_team"] == home_team
                    chutes_home_team=chutes_home_team.sum()
                    st.markdown(f"<div style='text-align: center; font-size: 18px'>Chutes: {chutes_home_team}</div>", unsafe_allow_html=True)


                with right_column:
                    st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold'>Time Visitante</div>", unsafe_allow_html=True)
                    away_team = matches[matches["match_id"] == game]["away_team"].values[0]
                    st.markdown(f"<div style='text-align: center; font-size: 24px; color: #F63366'>{away_team}</div>", unsafe_allow_html=True)
                    away_score = matches[matches["match_id"] == game]["away_score"].values[0]
                    st.markdown(f"<div style='text-align: center; font-size: 18px'>Gols: {away_score}</div>", unsafe_allow_html=True)

                    passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
                    passes_away_team = passes["possession_team"] == away_team
                    passes_away_team=passes_away_team.sum()
                    st.markdown(f"<div style='text-align: center; font-size: 18px'>Passes: {passes_away_team}</div>", unsafe_allow_html=True)


                    chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]
                    chutes_away_team = chutes["possession_team"] == away_team
                    chutes_away_team=chutes_away_team.sum()
                    st.markdown(f"<div style='text-align: center; font-size: 18px'>Chutes: {chutes_away_team}</div>", unsafe_allow_html=True)


            st.write("")
            st.write("")
            referee = matches[matches["match_id"] == game]["referee"].values[0]
            st.markdown(f"<h6 style='text-align: center; color: white;'>Árbitro: {referee}</h6>", unsafe_allow_html=True)

            # Grafico de relação de chutes com gols
            st.write(plot_shots_x_goals(matches, game, home_team, away_team))

            # Grafico de % de conversao
            st.write(plot_conversion(matches, game, home_team, away_team))






        with tab2:
            st.markdown(f"<font size='6'>Eventos da partida <font color='#F63366'>{get_match_label(matches, game)}</font> na competição <font color='#F63366'>{competition}</font> na Temporada <font color='#F63366'>{season_name}</font></font>", unsafe_allow_html=True)
            
            st.title("Comparações individuais")
            # time da casa
            lineups = sb.lineups(match_id=game)
            jogadores = lineups[home_team].values
            list_jogadores = []
            for i in jogadores:
                list_jogadores.append(i[1])

            jogador_casa = st.selectbox("Selecione um Jogador do time da casa", list_jogadores)

            # time visitante
            lineups = sb.lineups(match_id=game)
            jogadores = lineups[away_team].values
            list_jogadores = []
            for i in jogadores:
                list_jogadores.append(i[1])

            jogador_visit = st.selectbox("Selecione um Jogador do time visitante", list_jogadores)

            partida = sb.matches(competition_id=competition_id, season_id=season_id)
            final_match_id = partida[(partida["home_team"] == home_team) & (partida["away_team"] == away_team)].match_id.values[0]
            final_data = match_data(final_match_id)
            col_1, col_2 = st.columns(2)

            with col_1:
                st.subheader(f"Passes de {jogador_casa.split()[0]}")
                fig_1 = plot_passes(final_data, jogador_casa)
                st.pyplot(fig_1)

                st.subheader(f"Chutes de {jogador_casa.split()[0]}")
                fig_1 = plot_shots(final_data, jogador_casa)
                st.pyplot(fig_1)


            with col_2:
                st.subheader(f"Passes de {jogador_visit.split()[0]}")
                fig_2 = plot_passes(final_data, jogador_visit)
                st.pyplot(fig_2)

                st.subheader(f"Chutes de {jogador_visit.split()[0]}")
                fig_2 = plot_shots(final_data, jogador_visit)
                st.pyplot(fig_2)


        with tab3:
            st.markdown(f"<font size='6'>Eventos da partida <font color='#F63366'>{get_match_label(matches, game)}</font> na competição <font color='#F63366'>{competition}</font> na Temporada <font color='#F63366'>{season_name}</font></font>", unsafe_allow_html=True)
            
            st.title("Eventos")
            events = sb.events(match_id=game)
            st.dataframe(events)

            st.title("Gols")
            game_id = game
            events = sb.events(match_id=game_id)
            gols = events[(events['type'] == 'Shot') & (events['shot_outcome'] == 'Goal')]
            gols = gols.dropna(axis=1, how='all')
            st.dataframe(gols)

            st.title("Chutes")
            shots = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]
            st.dataframe(shots)

            st.title("Passes")
            passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
            st.dataframe(passes)

            st.title("Dribles")
            dribbles = sb.events(match_id=game, split=True, flatten_attrs=False)["dribbles"]
            st.dataframe(dribbles)

            st.title("Faltas")
            fouls = sb.events(match_id=game, split=True, flatten_attrs=False)["fouls"]
            st.dataframe(fouls)

            st.title("Cartões")
            cards = sb.events(match_id=game, split=True, flatten_attrs=False)["cards"]
            st.dataframe(cards)

            
            


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