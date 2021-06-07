from PIL import Image, ImageFont, ImageDraw
import pandas as pd
from tqdm import tqdm
import numpy as np
import os
import glob


def make_cert(file, text: str, dni: str, fname: str, ptn1: int = 100, ptn2: int = 100, ptd1: int = 100, ptd2: int = 200, folder="certificados", font="alegreya.ttf"):
    file = file.copy()
    image_editable = ImageDraw.Draw(file)
    title_font = ImageFont.truetype("fonts"+"/"+font, 28)
    dni_font = ImageFont.truetype("fonts"+"/"+font, 20)
    if len(text.split()) == 2:
        name_text = text.center(105)
    elif len(text.split()) == 3:
        name_text = text.center(90)
    else:
        name_text = text.center(75)
    name_text = name_text.upper()
    dni_text = dni
    image_editable.text((ptn1, ptn2), name_text, (0, 0, 0), font=title_font)
    image_editable.text((ptd1, ptd2), dni_text, (0, 0, 0), font=dni_font)
    file.save(folder+"/"+f"{fname}-certificado.pdf")


def make_test(file, image_editable, text: str = "TextoNombre PruebaNombre PruebaApellido Texto", dni: str = "100001000", ptn1: int = 100, ptn2: int = 100, ptd1: int = 100, ptd2: int = 200, folder="responses", font="/alegreya.ttf"):

    title_font = ImageFont.truetype("fonts"+"/"+font, 30)
    dni_font = ImageFont.truetype("fonts"+"/"+font, 20)
    name_text = text
    name_text = name_text.title()
    dni_text = dni
    image_editable.text((ptn1, ptn2), name_text, (255, 0, 0), font=title_font)
    image_editable.text((ptd1, ptd2), dni_text, (255, 0, 0), font=dni_font)
    file.save(folder+"/test.jpg")


def generate_certs(img_cert, coords1, coords2, df):

    ls_names = []
    ls_dni = []
    ls_mail = []

    for i in range(len(df)):

        ls_names.append(df.iloc[i]["NOMBRES"])
        ls_dni.append(df.iloc[i]["DNI"])
        ls_mail.append(df.iloc[i]["CORREO"])

    for i in range(len(ls_names)):
        print("print making cert cert", str(ls_names[i]), str(
            ls_dni[i]), str(ls_mail[i].split("@")[0]),)
        make_cert(img_cert, str(ls_names[i]), str(
            ls_dni[i]), str(ls_mail[i].split("@")[0]), coords1[0], coords1[1], coords2[0], coords2[1])

    return ls_mail


def import_image(file):
    img = Image.open(file)
    return img


def clean_folder(folder="certificados/*"):
    files = glob.glob(folder)
    for f in files:
        os.remove(f)
