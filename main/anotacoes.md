        '''

        st.title("Comparações individuais - Chutes")
        # time da casa
        lineups = sb.lineups(match_id=game)
        jogadores = lineups[home_team].values
        list_jogadores = []
        for i in jogadores:
            list_jogadores.append(i[1])

        jogador_casa_2 = st.selectbox("Selecione um Jogador do time da casa", list_jogadores, key="selectbox_jogador_casa_chute")

        # time visitante
        lineups = sb.lineups(match_id=game)
        jogadores = lineups[away_team].values
        list_jogadores = []
        for i in jogadores:
            list_jogadores.append(i[1])

        jogador_visit_2 = st.selectbox("Selecione um Jogador do time visitante", list_jogadores, key="selectbox_jogador_visitante_chute")

        partida = sb.matches(competition_id=competition_id, season_id=season_id)
        final_match_id = partida[(partida["home_team"] == home_team) & (partida["away_team"] == away_team)].match_id.values[0]
        final_data = match_data(final_match_id)
        col_1, col_2 = st.columns(2)
        '''