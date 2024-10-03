import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch, Sbopen
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import spinners
import time
import plotly.express as px
import pandas as pd

from plots import plot_passes, plot_conversion, plot_shots_x_goals, plot_shots_team, plot_passes_team, plot_shots, plot_estatisticas_jogadores

parser = Sbopen()

def match_data(match_id):
    return parser.event(match_id)[0]

def get_match_label(matches, match_id):
    row = matches[matches["match_id"] == match_id].iloc[0]
    return f"{row['match_date']} - {row['home_team']} vs {row['away_team']}"



def main():


    st.title("DR1 AT - Análises de Futebol")

    menu = ["Home", "Dados por competição", "Final da Copa do Mundo de 2022"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.title("Bem vindo ao projeto de Análise de Futebol")

        st.subheader("Este projeto foi desenvolvido para auxiliar na compreensão da analise de dados de futebol")

        st.text("Escolha uma das opções no menu lateral para comecar")

        st.text("Desenvolvido por Gustavo Alves")

        st.text("https://github.com/GustavoAlvesInfnet/gustavo_alves_DR1_AT")

        st.image("./imgs/audience.jpg")

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

        # Botões de download
        data = sb.events(match_id=game)
        data.to_csv("dados_partida.csv", index=False)

        with open("dados_partida.csv", "rb") as f:
            dataDownload = f.read()

        st.download_button(
            label="Download dos dados da partida",
            data=dataDownload,
            file_name="dados_partida.csv",
            mime="text/csv",
        )


            
        tab1, tab2, tab3 = st.tabs(["Informações sobre a partida", "Formulário sobre os jogadores", "Tabelas"])

        with tab1:

            st.markdown(f"<font size='6'>Informações sobre a partida <font color='#F63366'>{get_match_label(matches, game)}</font> na competição <font color='#F63366'>{competition}</font> na Temporada <font color='#F63366'>{season_name}</font></font>", unsafe_allow_html=True)


            with st.container():
                left_column, right_column = st.columns(2)
                with left_column:
                    st.markdown("<div style='text-align: left; font-size: 32px; font-weight: bold'>Time da Casa</div>", unsafe_allow_html=True)
                    home_team = matches[matches["match_id"] == game]["home_team"].values[0]
                    st.markdown(f"<div style='text-align: left; font-size: 24px; color: #F63366'>{home_team}</div>", unsafe_allow_html=True)
                    home_score = matches[matches["match_id"] == game]["home_score"].values[0]
                    #st.metric("Gols", home_score, delta_color="normal")
                    st.markdown(f"<div style='font-size: 16px'>Gols:</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 36px; color: #F63366'>{home_score}</div>", unsafe_allow_html=True)


                    passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
                    passes_home_team = passes["possession_team"] == home_team
                    passes_home_team=passes_home_team.sum()
                    st.metric("Passes", passes_home_team)
                    #st.markdown(f"<div style='text-align: center; font-size: 18px'>Passes: {passes_home_team}</div>", unsafe_allow_html=True)

                    chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]
                    chutes_home_team = chutes["possession_team"] == home_team
                    chutes_home_team=chutes_home_team.sum()
                    st.metric("Chutes", chutes_home_team)
                    #st.markdown(f"<div style='text-align: center; font-size: 18px'>Chutes: {chutes_home_team}</div>", unsafe_allow_html=True)



                with right_column:
                    st.markdown("<div style='text-align: left; font-size: 32px; font-weight: bold'>Time Visitante</div>", unsafe_allow_html=True)
                    away_team = matches[matches["match_id"] == game]["away_team"].values[0]
                    st.markdown(f"<div style='text-align: left; font-size: 24px; color: #F63366'>{away_team}</div>", unsafe_allow_html=True)
                    away_score = matches[matches["match_id"] == game]["away_score"].values[0]
                    st.markdown(f"<div style='font-size: 18px'> Gols: </div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 36px; color: #F63366'>{away_score}</div>", unsafe_allow_html=True)
                    #st.metric(label="Gols", value=away_score)

                    passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
                    passes_away_team = passes["possession_team"] == away_team
                    passes_away_team=passes_away_team.sum()
                    #st.markdown(f"<div style='text-align: center; font-size: 18px'>Passes: {passes_away_team}</div>", unsafe_allow_html=True)
                    st.metric(label="Passes", value=passes_away_team)

                    chutes = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]
                    chutes_away_team = chutes["possession_team"] == away_team
                    chutes_away_team=chutes_away_team.sum()
                    #st.markdown(f"<div style='text-align: center; font-size: 18px'>Chutes: {chutes_away_team}</div>", unsafe_allow_html=True)
                    st.metric(label="Chutes", value=chutes_away_team)
                # arbitro
                st.write("")
                referee = matches[matches["match_id"] == game]["referee"].values[0]
                st.markdown(f"<h6 style='text-align: center; color: white;'>Árbitro: {referee}</h6>", unsafe_allow_html=True)
                st.write("")

                partida = sb.matches(competition_id=competition_id, season_id=season_id)
                final_match_id = partida[(partida["home_team"] == home_team) & (partida["away_team"] == away_team)].match_id.values[0]
                final_data = match_data(final_match_id)

                with st.spinner("Página está carregando..."):
                    st.subheader("Mapa de chutes")
                    left_column, right_column = st.columns(2)
                    with left_column:
                        st.write(plot_shots_team(final_data, home_team))
                    with right_column:
                        st.write(plot_shots_team(final_data, away_team))

                    st.subheader("Mapa de passes")
                    left_column, right_column = st.columns(2)
                    with left_column:
                        st.write(plot_passes_team(final_data, home_team))
                    with right_column:
                        st.write(plot_passes_team(final_data, away_team))

            st.title("Análises")    
            # Grafico de relação de chutes com gols
            st.write(plot_shots_x_goals(matches, game, home_team, away_team))

            # Grafico de % de conversao
            st.write(plot_conversion(matches, game, home_team, away_team))

            # Eventos
            st.title("Eventos")
            events = sb.events(match_id=game)
            st.write(events)






        with tab2:
            st.markdown(f"<font size='6'>Informações sobre a partida <font color='#F63366'>{get_match_label(matches, game)}</font> na competição <font color='#F63366'>{competition}</font> na Temporada <font color='#F63366'>{season_name}</font></font>", unsafe_allow_html=True)

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



            # Opções de estatísticas
            estatisticas_opcoes = st.multiselect("Selecione as estatísticas que deseja ver", ["Passes", "Chutes"])


            # Botão para atualizar os gráficos
            atualizar_graficos = st.button("Atualizar gráficos")

            if atualizar_graficos:
                partida = sb.matches(competition_id=competition_id, season_id=season_id)
                final_match_id = partida[(partida["home_team"] == home_team) & (partida["away_team"] == away_team)].match_id.values[0]
                final_data = match_data(final_match_id)
                col_1, col_2 = st.columns(2)

                with col_1:
                    if "Passes" in estatisticas_opcoes:
                        st.subheader(f"Passes de {jogador_casa.split()[0]}")
                        bar = st.progress(0)
                        fig_1 = plot_passes(final_data, jogador_casa)
                        for i in range(100):
                            bar.progress(i + 1)
                            time.sleep(0.01)
                        bar.empty()  # Limpa a barra de progresso
                        st.pyplot(fig_1)

                    if "Chutes" in estatisticas_opcoes:
                        st.subheader(f"Chutes de {jogador_casa.split()[0]}")
                        bar = st.progress(0)
                        fig_1 = plot_shots(final_data, jogador_casa)
                        for i in range(100):
                            bar.progress(i + 1)
                            time.sleep(0.01)
                        bar.empty()  # Limpa a barra de progresso
                        st.pyplot(fig_1)

                with col_2:
                    if "Passes" in estatisticas_opcoes:
                        st.subheader(f"Passes de {jogador_visit.split()[0]}")
                        bar = st.progress(0)
                        fig_2 = plot_passes(final_data, jogador_visit)
                        for i in range(100):
                            bar.progress(i + 1)
                            time.sleep(0.01)
                        bar.empty()  # Limpa a barra de progresso
                        st.pyplot(fig_2)

                    if "Chutes" in estatisticas_opcoes:
                        st.subheader(f"Chutes de {jogador_visit.split()[0]}")
                        bar = st.progress(0)
                        fig_2 = plot_shots(final_data, jogador_visit)
                        for i in range(100):
                            bar.progress(i + 1)
                            time.sleep(0.01)
                        bar.empty()  # Limpa a barra de progresso
                        st.pyplot(fig_2)


        with tab3:
            st.markdown(f"<font size='6'>Informações sobre a partida <font color='#F63366'>{get_match_label(matches, game)}</font> na competição <font color='#F63366'>{competition}</font> na Temporada <font color='#F63366'>{season_name}</font></font>", unsafe_allow_html=True)
            
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

            st.title("Matches")
            matches = sb.matches(competition_id=competition_id, season_id=season_id)
            matches = matches[matches["match_id"] == game]
            st.dataframe(matches)
            
            


    elif choice == "Final da Copa do Mundo de 2022":
        st.subheader("Quem foi o melhor jogador da final da copa do mundo de 2022?")
        st.image("https://images.mlssoccer.com/image/private/t_editorial_landscape_8_desktop_mobile/prd-league/ufp9p8wc4fqawmnx3ouf.jpg")
        fifa_world_cup_22 = sb.matches(competition_id=43, season_id=106)

        final_match_id = fifa_world_cup_22[(fifa_world_cup_22["home_team"] == "Argentina") & (fifa_world_cup_22["away_team"] == "France")].match_id.values[0]
        final_data = match_data(final_match_id)

        st.write("")

        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>MESSI</font></div>", unsafe_allow_html=True)
        
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Lionel-Messi-Argentina-2022-FIFA-World-Cup_sharpness.jpg/330px-Lionel-Messi-Argentina-2022-FIFA-World-Cup_sharpness.jpg", width=200, use_column_width=True)
        
        with col_2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            st.image("./imgs/x.png", width=200, use_column_width=True)
        
            
        with col_3:
            st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>MBAPPÉ</font></div>", unsafe_allow_html=True)
        
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/2019-07-17_SG_Dynamo_Dresden_vs._Paris_Saint-Germain_by_Sandro_Halank–129_%28cropped%29.jpg/330px-2019-07-17_SG_Dynamo_Dresden_vs._Paris_Saint-Germain_by_Sandro_Halank–129_%28cropped%29.jpg", width=200, use_column_width=True)


        st.write("")
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Estatísticas Básicas</font></div>", unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        with col_1:
            
            # número de chutes
            chutes = final_data[final_data["type_name"] == "Shot"]["player_name"]
            chutes_messi = chutes[chutes == "Lionel Andrés Messi Cuccittini"].count()
            #numero de passes
            passes = final_data[final_data["type_name"] == "Pass"]["player_name"]
            passes_messi = passes[passes == "Lionel Andrés Messi Cuccittini"].count()
            #numero de dribles
            dribles = final_data[final_data["type_name"] == "Dribble"]["player_name"]
            dribles_messi = dribles[dribles == "Lionel Andrés Messi Cuccittini"].count()

            # Número de gols
            goals_messi = final_data[final_data["type_name"] == "Shot"]
            goals_messi = goals_messi[goals_messi["outcome_name"] == "Goal"]
            goals_messi = goals_messi[goals_messi["player_name"] == "Lionel Andrés Messi Cuccittini"]

            goals_messi_open = goals_messi["sub_type_name"] == "Open Play"
            goals_messi_open = goals_messi_open.sum()

            goals_messi_penalty = goals_messi["sub_type_name"] == "Penalty"
            goals_messi_penalty = goals_messi_penalty.sum()

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Gols com bola rolando</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{goals_messi_open}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Gols de penalti</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{goals_messi_penalty}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Chutes</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{chutes_messi}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Passes</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{passes_messi}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Dribles</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{dribles_messi}</div>", unsafe_allow_html=True)


        with col_2:

            #numero de chutes
            chutes = final_data[final_data["type_name"] == "Shot"]["player_name"]
            chutes_mbappe = chutes[chutes == "Kylian Mbappé Lottin"].count()
            #numero de passes
            passes = final_data[final_data["type_name"] == "Pass"]["player_name"]
            passes_mbappe = passes[passes == "Kylian Mbappé Lottin"].count()
            #numero de dribles
            dribles = final_data[final_data["type_name"] == "Dribble"]["player_name"]
            dribles_mbappe = dribles[dribles == "Kylian Mbappé Lottin"].count()
            #numero de gols
            goals_mbappe = final_data[final_data["type_name"] == "Shot"]
            goals_mbappe = goals_mbappe[goals_mbappe["outcome_name"] == "Goal"]
            goals_mbappe = goals_mbappe[goals_mbappe["player_name"] == "Kylian Mbappé Lottin"]

            goals_mbappe_open = goals_mbappe["sub_type_name"]=="Open Play"
            goals_mbappe_open = goals_mbappe_open.sum()

            goals_mbappe_penalty = goals_mbappe["sub_type_name"]=="Penalty"
            goals_mbappe_penalty = goals_mbappe_penalty.sum()

            
            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Gols com bola rolando</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{goals_mbappe_open}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Gols de penalti</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{goals_mbappe_penalty}</div>", unsafe_allow_html=True)


            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Chutes</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{chutes_mbappe}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Passes</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{passes_mbappe}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size: 30px; color: white; text-align: center;'>Dribles</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: #F63366; text-align: center;'>{dribles_mbappe}</div>", unsafe_allow_html=True)

        # mapa de gols
        st.write("")
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Mapa de Gols</font></div>", unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("<h3 style='text-align: center;'>Messi</h3>", unsafe_allow_html=True)

            fig_1 = plot_shots(goals_messi, "Lionel Andrés Messi Cuccittini")
            st.pyplot(fig_1)

        with col_2:
            st.markdown("<h3 style='text-align: center;'>Mbappé</h3>", unsafe_allow_html=True)

            fig_2 = plot_shots(goals_mbappe, "Kylian Mbappé Lottin") 
            st.pyplot(fig_2)

                

        st.write("")
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Mapa de Chutes</font></div>", unsafe_allow_html=True)
        
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("<h3 style='text-align: center;'>Messi</h3>", unsafe_allow_html=True)

            fig_3 = plot_shots(final_data, "Lionel Andrés Messi Cuccittini")
            st.pyplot(fig_3)

        with col_2:
            st.markdown("<h3 style='text-align: center;'>Mbappé</h3>", unsafe_allow_html=True)

            fig_4 = plot_shots(final_data, "Kylian Mbappé Lottin")
            st.pyplot(fig_4)


        st.write("")   
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Mapa de Passes</font></div>", unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("<h3 style='text-align: center;'>Messi</h3>", unsafe_allow_html=True)

            fig_1 = plot_passes(final_data, "Lionel Andrés Messi Cuccittini")
            st.pyplot(fig_1)

        with col_2:
            st.markdown("<h3 style='text-align: center;'>Mbappé</h3>", unsafe_allow_html=True)

            fig_2 = plot_passes(final_data, "Kylian Mbappé Lottin") 
            st.pyplot(fig_2)


        st.write("")  
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Estatísticas</font></div>", unsafe_allow_html=True)
        soma_gols = goals_mbappe_open + goals_messi_open
        soma_chutes = chutes_mbappe + chutes_messi
        soma_passes = passes_mbappe + passes_messi
        soma_gols_parados = goals_messi_penalty + goals_mbappe_penalty
        soma_dribles = dribles_mbappe + dribles_messi

        porcentagem_goals_messi_open = (goals_messi_open / soma_gols)
        porcentagem_goals_mbappe_open = (goals_mbappe_open / soma_gols)
        porcentagem_goals_messi_penalty = (goals_messi_penalty / soma_gols_parados)
        porcentagem_goals_mbappe_penalty = (goals_mbappe_penalty / soma_gols_parados)
        porcentagem_chutes_mbappe = (chutes_mbappe / soma_chutes)
        porcentagem_chutes_messi = (chutes_messi / soma_chutes)
        porcentagem_passes_mbappe = (passes_mbappe / soma_passes)
        porcentagem_passes_messi = (passes_messi / soma_passes)
        porcentagem_dribles_mbappe = (dribles_mbappe / soma_dribles)
        porcentagem_dribles_messi = (dribles_messi / soma_dribles)



        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("<h3 style='text-align: center;'>Messi</h3>", unsafe_allow_html=True)
            fig_1 = plot_estatisticas_jogadores(porcentagem_goals_messi_open, porcentagem_goals_messi_penalty, porcentagem_chutes_messi, porcentagem_passes_messi, porcentagem_dribles_messi)
            st.plotly_chart(fig_1)

        with col_2:
            st.markdown("<h3 style='text-align: center;'>Mbappé</h3>", unsafe_allow_html=True)
            fig_2 = plot_estatisticas_jogadores(porcentagem_goals_mbappe_open, porcentagem_goals_mbappe_penalty, porcentagem_chutes_mbappe, porcentagem_passes_mbappe, porcentagem_dribles_mbappe)
            st.plotly_chart(fig_2)



        # pontuação final
        st.write("")
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Pontuação Final</font></div>", unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("<h3 style='text-align: center;'>Messi</h3>", unsafe_allow_html=True)

            pont_messi = porcentagem_goals_messi_open + porcentagem_goals_messi_penalty + porcentagem_chutes_messi + porcentagem_passes_messi + porcentagem_dribles_messi
            st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>{pont_messi:.2f}</font></div>", unsafe_allow_html=True)

        with col_2:
            st.markdown("<h3 style='text-align: center;'>Mbappé</h3>", unsafe_allow_html=True)

            pont_mbappe = porcentagem_goals_mbappe_open + porcentagem_goals_mbappe_penalty + porcentagem_chutes_mbappe + porcentagem_passes_mbappe + porcentagem_dribles_mbappe
            st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>{pont_mbappe:.2f}</font></div>", unsafe_allow_html=True)
        

        # conclusões
        st.write("")
        st.markdown(f"<div style='text-align: center; font-size: 42px;'><font color='#F63366'>Conclusões</font></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Ambos possuem estilos diferentes, mas o Mbappé tem uma pontuação mais alta.</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>O Messi possui muito mais passes enquanto o Mbappé possui mais chutes, dribles e gols.</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()