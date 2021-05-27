import pandas as pd


def citySearch(city, csvPaths):
    # CARACTERÍSTICAS GERAIS DO ELEITORADO
    col_list_eleitorado = ["NM_MUNICIPIO", "DS_GENERO", "DS_GRAU_ESCOLARIDADE",
                           "QT_ELEITORES_INC_NM_SOCIAL", "DS_FAIXA_ETARIA", "DS_ESTADO_CIVIL"]

    iter_csv_eleitorado = pd.read_csv(csvPaths[0], usecols=col_list_eleitorado,
                                      delimiter=";", encoding='iso-8859-1',
                                      error_bad_lines=False)

    # Remove a coluna da cidade
    df_result = iter_csv_eleitorado.loc[iter_csv_eleitorado["NM_MUNICIPIO"] == city].drop(
        columns=["NM_MUNICIPIO"], axis=1)

    # Converte para json
    df_result.apply(pd.Series.value_counts, axis=1)

    # Alterações necessárias
    ds_genero_string = df_result["DS_GENERO"].value_counts().to_json()
    ds_grau_escolaridade_string = df_result["DS_GRAU_ESCOLARIDADE"].value_counts(
    ).to_json()
    ds_estado_civil_string = df_result["DS_ESTADO_CIVIL"].value_counts(
    ).to_json()

    ds_faixa_etaria_string = df_result["DS_FAIXA_ETARIA"].value_counts(
    ).to_json()
    ds_faixa_etaria_string = ds_faixa_etaria_string.replace("  ", "")

    cards_eleitorado = '{' + f'"DS_GENERO": {ds_genero_string}, "DS_GRAU_ESCOLARIDADE": {ds_grau_escolaridade_string}, "DS_ESTADO_CIVIL": {ds_estado_civil_string}, "DS_FAIXA_ETARIA": {ds_faixa_etaria_string}' + '}'
    eleitorado = cards_eleitorado.replace(
        '\n', ' ').replace('\r', '')

    # NOME SOCIAL
    total_eleitores_nomesocial = 0  # Iniciando a variável
    df_nomesocial = df_result.groupby('QT_ELEITORES_INC_NM_SOCIAL')[
        'QT_ELEITORES_INC_NM_SOCIAL'].sum()

    # Somando a quantidade de eleitores com nome social em cada grupo
    for index_nomesocial in range(len(df_nomesocial)):
        total_eleitores_nomesocial += df_nomesocial.index[index_nomesocial] * \
            df_nomesocial.values[index_nomesocial]

    qntString = str(total_eleitores_nomesocial)
    # Gerando string do nome social
    nomeSocial = f'"quantidade": {qntString}'

    # CANDIDATO ELEITO
    # Geração do CSV de candidato
    # col_list_candidato = ["NR_TURNO", "NM_UE", "DS_CARGO",
    #                       "NM_CANDIDATO", "SG_PARTIDO",
    #                       "DS_SIT_TOT_TURNO", "ST_REELEICAO"]

    # iter_csv_candidato = pd.read_csv(csvPaths[0], usecols=col_list_candidato,
    #                                  sep=';', encoding='iso-8859-1',
    #                                  error_bad_lines=False)

    # # Gerando string
    # candidato = iter_csv_candidato.query(
    #     'DS_CARGO == "PRESIDENTE" and DS_SIT_TOT_TURNO == "ELEITO"').to_json()

    # cards = '{ "cards": [' + eleitorado + '], "cardCandidato": [' + \
    #     candidato + '], "cardNomeSocial": [{' + nomeSocial + '}]}'

    cards = '{ "cards": [' + eleitorado + \
        '], "cardNomeSocial": [{' + nomeSocial + '}]}'

    print(cards)
    return cards