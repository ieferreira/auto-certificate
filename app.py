from PIL import Image, ImageFont, ImageDraw, ImageOps
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


TITLE = "Aplicación Correos y Certificados"

st.title(TITLE.title())
file = st.file_uploader("", type=["jpg"])

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

    st.sidebar.title("Puntos y parámetros")

    name_pt1 = st.sidebar.number_input(
        "Punto Nombre (x)", 0, img.size[0], 285, step=1, key='name_pt1')
    name_pt2 = st.sidebar.number_input(
        "Punto Nombre (y)", 0, img.size[1], 325, step=1, key='name_pt2')
    dni_pt1 = st.sidebar.number_input(
        "Punto DNI (x)", 0, img.size[0], 740, step=1, key='dni_pt1')
    dni_pt2 = st.sidebar.number_input(
        "Punto DNI (y)", 0, img.size[1], 390, step=1, key='dni_pt2')

    if st.sidebar.checkbox("Dibuja Puntos", value=False):
        test_img = ImageDraw.Draw(img)
        make_test(img, test_img, ptn1=name_pt1,
                  ptn2=name_pt2, ptd1=dni_pt1, ptd2=dni_pt2)
        img2 = import_image("responses/test.jpg")
        imageLocation.image(img2,  use_column_width=True)


    try:
        os.mkdir("certificados")
    except:
        pass

    file_asis = st.file_uploader(label="", type="xlsx")

    if file_asis:

        df = pd.read_excel(file_asis, engine='openpyxl')
        certs_generated = False
        st.table(df)
        if st.checkbox("Generar Certificados"):
            ls_mails = generate_certs(img_cert,
                                      (name_pt1, name_pt2), (dni_pt1, dni_pt2), df)
            certs_generated = True

        if certs_generated:
            st.write("Los certificados se enviarán a los siguientes correos: ")
            st.write(ls_mails)
            user_input = st.text_input(
                "Correo", "@unal.edu.co")
            pword = st.text_input(
                "Type your password and press enter:", type="password")

            if st.button("Enviar correos"):

                subject = "Certificado SEG"
                body = "Se te entrega el siguiente certificado"
                sender_email = user_input
                receiver_email = ls_mails
                password = pword

                try:
                    for i in stqdm(range(len(receiver_email))):
                        # Create a multipart message and set headers
                        message = MIMEMultipart()
                        message["From"] = sender_email
                        message["To"] = receiver_email[i]
                        message["Subject"] = subject
                        message["Bcc"] = receiver_email[i]  # Recommended for mass emails

                        # Add body to email
                        message.attach(MIMEText(body, "plain"))

                        # In same directory as script
                        filename = "certificados/" + \
                            f"{ls_mails[i].split('@')[0]}-certificado.pdf"

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
                            f"attachment; filename= {filename}",
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
