import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


@st.cache_data
def plot_passes(match, player_name):
    player_filter = (match.type_name=="Pass") & (match.player_name==player_name)
    df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]

    pitch = Pitch(line_color="black", pitch_color="#799351", stripe_color="#799351", stripe=True)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, endnote_height=0.04, axis=False, title_space=0, endnote_space=0)

    pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, width=2, color="white", ax=ax["pitch"])
    pitch.kdeplot(x=df_pass.x, y=df_pass.y, ax=ax["pitch"], shade=True, alpha=0.5, cmap="plasma")

    return fig

@st.cache_data
def plot_passes_team(match, team):
    player_filter = (match.type_name=="Pass") & (match.team_name==team)
    df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]

    pitch = Pitch(line_color="black", pitch_color="#799351", stripe_color="#799351", stripe=True)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, endnote_height=0.04, axis=False, title_space=0, endnote_space=0)

    #pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, width=2, color="white", ax=ax["pitch"])
    pitch.kdeplot(x=df_pass.x, y=df_pass.y, ax=ax["pitch"], shade=True, alpha=0.5, cmap="plasma")

    return fig

@st.cache_data
def plot_shots(match, player_name):
    player_filter = (match.type_name=="Shot") & (match.player_name==player_name)
    df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]

    pitch = Pitch(line_color="black", pitch_color="#799351", stripe_color="#799351", stripe=True)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, endnote_height=0.04, axis=False, title_space=0, endnote_space=0)

    pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, width=2, color="white", ax=ax["pitch"])
    pitch.kdeplot(x=df_pass.x, y=df_pass.y, ax=ax["pitch"], shade=True, alpha=0.5, cmap="plasma")

    return fig

@st.cache_data
def plot_shots_team(match, team):
    player_filter = (match.type_name=="Shot") & (match.team_name==team)
    df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]

    pitch = Pitch(line_color="black", pitch_color="#799351", stripe_color="#799351", stripe=True)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, endnote_height=0.04, axis=False, title_space=0, endnote_space=0)

    pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, width=2, color="white", ax=ax["pitch"])
    pitch.kdeplot(x=df_pass.x, y=df_pass.y, ax=ax["pitch"], shade=True, alpha=0.5, cmap="plasma")

    return fig

@st.cache_data
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

@st.cache_data
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


@st.cache_data
def plot_estatisticas_jogadores(goals_open, goals_penalty, chutes, passes, dribles):
    df = pd.DataFrame(dict(
        r=[goals_open, goals_penalty, chutes, passes, dribles],
        theta=['Gols abertos', 'Gols parados', 'Chutes','Passes','Dribles']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    return fig

