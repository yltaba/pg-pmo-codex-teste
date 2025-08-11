def get_options_dropdown_saude(df, column):
    """Versão simplificada da função get_options_dropdown para o app de saúde"""
    sorted_values = sorted(df[column].dropna().unique())
    return [{"label": x, "value": x} for x in sorted_values]