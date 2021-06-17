from PIL import Image, ImageFont, ImageDraw, ImageOps
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageColor
import pandas as pd
from tqdm import tqdm
import numpy as np
import os
import glob
import random
from funcs import *
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
from stqdm import stqdm

clean_folder()
clean_folder("responses/*")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

TITLE = "Aplicación Correos y Certificados"
consolidado_generado = False

head1, head2 = st.beta_columns((3,15))

head1.markdown(
    f'<img src="https://media.giphy.com/media/jIRyzncqRWzM3GYaQm/giphy.gif"  width="100" height="100" alt="cat gif">',
    unsafe_allow_html=True,
)
head2.title(TITLE.title())

st.text("")
cert_name = st.text_input("¿Cuál es el nombre del certificado?", "🏆")

st.write("""
    Formato aceptado en el excel (.xslx) es [ NOMBRE | DNI | CORREO ]. Si no lo tienes lo puedes generar a partir de las asistencias (.xlsx). ¿Deseas generar el reporte a partir de las asistencias y la inscripción?: """)


if st.checkbox("Generar reporte de asistencia a partir de exceles", value=False):


    st.write("¿Cómo se llaman las columnas donde se encuentra el nombre y los apellidos, el DNI y el correo? (o usa los que se encuentran por defecto)")

    col1, col2, col3 = st.beta_columns(3)

    fullname_column = col1.text_input("Nombres y Apellidos", "Nombres y apellidos")
    dni_column = col2.text_input("Columna DNI", "DNI (Cedula o T.I)")
    mail_column = col3.text_input("Columna correo electrónico", "Dirección de correo electrónico")
    
    fullname_column = fullname_column.split(".")[0]
    dni_column = dni_column.split(".")[0]
    mail_column = mail_column.split(".")[0]


    exceles = st.file_uploader("Subir exceles para generar reporte", type=["xlsx"], accept_multiple_files=True)   

    if exceles:
        for i in exceles:

             if i.name.endswith("inscripción.xlsx"):
                df = pd.read_excel(i, engine='openpyxl')                
                def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
                def groupby_field(col):
                    parts = col.split('.')
                    return '{}'.format(parts[0])

                df = df.groupby(groupby_field, axis=1,).apply(lambda x: x.apply(sjoin, axis=1))

                df_final = df[[fullname_column, dni_column, mail_column]]
                df_final = df_final.rename(columns={'Nombres y apellidos': 'NOMBRES', 'DNI (Cedula o T': 'DNI', "Dirección de correo electrónico": "CORREO"})
                df_final["ASIS"] = 0

        cnt = 0
        for i in exceles: 

            
            if not i.name.endswith("inscripción.xlsx"):                

                def format_asistance(i):

                    df_asis = pd.read_excel(i)
                    df_asis = df_asis.rename(columns={'Nombre(s) y apellidos COMPLETOS.': "NOMBRES", "Dirección de correo electrónico": "CORREO"})
                    return df_asis

                df_asis = format_asistance(i)

                df_final["ASIS"]+=df_final.CORREO.isin(df_asis.CORREO).astype(int)
                cnt += 1
                
        st.write(f"¿Se encontraron {cnt} certificados de asistencia, cuantas asistencias mínimas deseas tomar para el consolidado?")

        asis_pts = st.slider("Número de asistencia", 0, 2, cnt//2, step=1, key='asis_pts')
        consolidado_generado = True



file = st.file_uploader("Subir imagen plantilla para generar certificados", type=["jpg", "png"])

if file is None:
    st.text("Por favor, sube una imagen...")

if file:
    
    try:
        os.mkdir("responses")
    except:
        pass
    imageLocation = st.empty()

    img = import_image(file)
    width, height = img.size
    img_cert = img.copy()
    imageLocation.image(img, use_column_width=True)

    st.sidebar.markdown("""### Parámetros a usar""")

    test_name = st.sidebar.text_input("Nombre de prueba", "Nombre Nombre Apellido Apellido")
    # name_pt1 = st.sidebar.slider(
    #     "Punto Nombre (x)", 0, img.size[0], 325, step=1, key='name_pt1')
    name_pt2 = st.sidebar.slider(
        "Altura vertical (texto centrado)", 0, img.size[1], 325, step=1, key='name_pt2')
    dni_pt1 = st.sidebar.slider(
        "Punto DNI (x)", 0, img.size[0], 740, step=1, key='dni_pt1')
    dni_pt2 = st.sidebar.slider(
        "Punto DNI (y)", 0, img.size[1], 390, step=1, key='dni_pt2')

    size_img = img.size

    name_size = st.sidebar.slider(
        "Tamaño Fuente Nombre", 0, 50, 28, step=1, key='name_fontsize')    
    dni_size = st.sidebar.slider(
        "Tamaño Fuente DNI", 0, 50, 20, step=1, key='dni_fontsize')

    color = st.sidebar.color_picker('Escoge un color para el texto', '#000000')
    

    font_selected = "alegreya.ttf"
    option_font = st.sidebar.selectbox("¿Qué fuente deseas usar?", ("Alegreya", "Computer Modern", "Comic Sans"))

    fonts_dict = {"Alegreya": "alegreya.ttf", "Computer Modern": "cmunorm.ttf", "Comic Sans": "comicsans.ttf"}

    font_selected = fonts_dict[option_font]


    if st.sidebar.checkbox("Dibuja Certificado de Prueba", value=False):
        test_img = ImageDraw.Draw(img)
        make_test(size_img, img, test_img, test_name , ptn1=100,
                  ptn2=name_pt2, ptd1=dni_pt1, ptd2=dni_pt2, font=font_selected, name_size=name_size, dni_size=dni_size, color=color)
        img2 = import_image("responses/test.png")
        imageLocation.image(img2,  use_column_width=True)


    try:
        os.mkdir("certificados")
    except:
        pass

    
    file_asis = st.file_uploader(label="Si ya generaste consolidado, este PASO no es necesario", type="xlsx")

    if file_asis or consolidado_generado == True:

        if consolidado_generado:            

            df_filtered = df_final[df_final['ASIS'] >= cnt]
 
            df_filtered = df_filtered.astype({"DNI": float})
            df_filtered = df_filtered.astype({"DNI": int})
    


        else:
            df_filtered = pd.read_excel(file_asis, engine='openpyxl')

        certs_generated = False

        st.table(df_filtered)

        if st.checkbox("Generar Certificados"):

            ls_mails, ls_names = generate_certs(size_img, img_cert,
                                      (100, name_pt2), (dni_pt1, dni_pt2), df_filtered, font_selected, name_size, dni_size, color=color)
            certs_generated = True

        if certs_generated:
            st.write("Los certificados se enviarán a los siguientes correos: ")
            st.write(ls_mails)
            user_input = st.text_input(
                "Correo", "@unal.edu.co")
            pword = st.text_input(
                "Type your password and press enter:", type="password")

            if st.button("Enviar correos"):

                st.write("Enviando Correos 🤹")    
                subject = f"Certificado {cert_name}"

                sender_email = user_input
                receiver_email = ls_mails
                password = pword

                try:
                    for i in stqdm(range(len(receiver_email))):
                        # Create a multipart message and set headers
                        body = f"Hola {ls_names[i]}, se te entrega el siguiente certificado por asistir al curso {cert_name}. Felicitaciones"
                        message = MIMEMultipart()
                        message["From"] = sender_email
                        message["To"] = receiver_email[i]
                        message["Subject"] = subject
                        message["Bcc"] = receiver_email[i]  # Recommended for mass emails

                        # Add body to email
                        message.attach(MIMEText(body, "plain"))

                        # In same directory as script
                        filename = "certificados/" + f"{ls_mails[i].split('@')[0]}-certificado.pdf"

                        # Open PDF file in binary mode
                        with open(filename, "rb") as attachment:
                            # Add file as application/octet-stream
                            # Email client can usually download this automatically as attachment
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())

                        # Encode file in ASCII characters to send by email
                        encoders.encode_base64(part)

                        # Add header as key/value pair to attachment part
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename.split('/')}",
                        )

                        # Add attachment to message and convert message to string
                        message.attach(part)
                        text = message.as_string()
                        #! IMPORTANT ENABLE LESS SECURE APPS
                        # Log in to server using secure context and send email
                        context = ssl.create_default_context()

                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(sender_email, receiver_email[i], text)

                    st.write(f"Correos enviados a {len(receiver_email)} personas")

                except Exception as e:

                    st.write(
                        "Tienes que habilitar las apps menos seguras para este procedimiento")
                    st.write(
                        "En: https://www.google.com/settings/security/lesssecureapps")
                    st.write(
                        "Si no te aparece esta opción en seguridad, deshabilita verificación en 2 pasos para realizar este proceso."
                    )
                    st.write(
                        "Por seguridad vuelve a deshabilitar esta opción cuando termines este proceso")
                    st.write(e)


blank, foot1, foot2, foot3= st.beta_columns((6,2,3,3))

st.text("")
st.text("")

st.write("\n")

st.markdown("""<br/>
               <br/>""",
    unsafe_allow_html=True)


foot1.markdown(
    f'<img src="https://avatars.githubusercontent.com/u/11964547?s=400&u=f6511da902a4d3374b9c46bf5c1d30642cd48b00&v=4"  width="75" height="75" alt="Me">',
    unsafe_allow_html=True,
)

foot2.markdown("""Programado por: <br/>
                    Iván E. Ferreira <br/>
                    UN-Bog Geología""",
    unsafe_allow_html=True)
foot3.markdown("""Mira más de mis proyectos <br/>
                [Github](https://github.com/ieferreira) <br/>
                [LinkedIn](https://www.linkedin.com/in/ieferreira/)""",
    unsafe_allow_html=True)