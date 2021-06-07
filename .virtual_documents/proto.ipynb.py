import pandas as pd

df = pd.read_excel("CCDM-Formulario de inscripción.xlsx")
df.head()


#function to join columns if column is not null
def sjoin(x): return ';'.join(x[x.notnull()].astype(str))

#function to ignore the suffix on the column e.g. a.1, a.2 will be grouped together
def groupby_field(col):
    parts = col.split('.')
    return '{}'.format(parts[0])

df = df.groupby(groupby_field, axis=1,).apply(lambda x: x.apply(sjoin, axis=1))


df_final = df[["Nombres y apellidos", "DNI (Cedula o T", "Dirección de correo electrónico"]]
df_final = df_final.rename(columns={'Nombres y apellidos': 'NOMBRES', 'DNI (Cedula o T': 'DNI', "Dirección de correo electrónico": "CORREO"})
df_final



def format_asistance(i=1):
    df_asis = pd.read_excel(f"CCDM-Asistencia-{i}.xlsx")
    df_asis = df_asis.rename(columns={'Nombre(s) y apellidos COMPLETOS.': "NOMBRES", "Dirección de correo electrónico": "CORREO"})
    df_asis
    return df_asis

df_1 = format_asistance(i=1)
df_2 = format_asistance(i=2)





df_final = df_final.assign(ASIS=df_final.CORREO.isin(df_1.CORREO).astype(int)+df_final.CORREO.isin(df_2.CORREO).astype(int))

df_final





df_final





df_asis2 = pd.read_excel("CCDM-Asistencia-2.xlsx")
df_asis2


df_asis1 = pd.read_excel("CCDM-Asistencia-1.xlsx")
df_asis1



