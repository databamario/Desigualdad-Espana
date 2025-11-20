from pathlib import Path
import pandas as pd
project_root=Path('c:/Users/mario/Desktop/Projects/desigualdad_social_etl')
pickle_dir=project_root / 'outputs' / 'pickle_cache'
p=pickle_dir / 'df_arope_edad_sexo.pkl'
print('exists', p.exists())
if p.exists():
    da = pd.read_pickle(p)
    print('Initial columns:', list(da.columns))
    if 'Año' not in da.columns and 'Anio' in da.columns:
        da['Año'] = da['Anio']
    if 'Anio' not in da.columns and 'Año' in da.columns:
        da['Anio'] = da['Año']
    print('After alias columns:', list(da.columns))
    da_n = da[(da.get('Sexo') == 'Total') & (da.get('Edad') == 'Total') & (da.get('Indicador') == 'AROPE')]
    idx_col = 'Año' if 'Año' in da_n.columns else 'Anio' if 'Anio' in da_n.columns else None
    print('idx_col', idx_col)
    if idx_col is not None:
        da_n = da_n.groupby(idx_col)['Valor'].mean().reset_index()
        if 'Año' not in da_n.columns and 'Anio' in da_n.columns:
            da_n['Año'] = da_n['Anio']
    print('df_arope_anual columns:', list(da_n.columns))
    print('df_arope_anual head')
    print(da_n.head().to_string())
else:
    print('pickle not found')
