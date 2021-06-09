from PIL import Image, ImageFont, ImageDraw
import pandas as pd
from tqdm import tqdm
import numpy as np
import os
import glob
from stqdm import stqdm


def make_cert(file, text: str, dni: str, fname: str, ptn1: int = 100, ptn2: int = 100, ptd1: int = 100, ptd2: int = 200, font="alegreya.ttf", name_size=28, dni_size=20):
    file = file.copy()
    folder="certificados"
    image_editable = ImageDraw.Draw(file)
    title_font = ImageFont.truetype(f"fonts/{font}", name_size)
    dni_font = ImageFont.truetype(f"fonts/{font}", dni_size)
    if len(text.split()) == 2:
        name_text = text.center(80)
    elif len(text.split()) == 3:
        name_text = text.center(70)
    else:
        name_text = text.center(55)
    name_text = name_text.upper()
    dni_text = dni
    image_editable.text((ptn1, ptn2), name_text, (0, 0, 0), font=title_font)
    image_editable.text((ptd1, ptd2), dni_text, (0, 0, 0), font=dni_font)
    file.save(folder+"/"+f"{fname}-certificado.pdf")


def make_test(file, image_editable, text: str = "TextoNombre PruebaNombre PruebaApellido Texto", dni: str = "100001000", ptn1: int = 100, ptn2: int = 100, ptd1: int = 100, ptd2: int = 200, folder="responses", font="alegreya.ttf", name_size=28, dni_size=20):

    title_font = ImageFont.truetype(f"fonts/{str(font)}", name_size)
    dni_font = ImageFont.truetype(f"fonts/{str(font)}", dni_size)
    name_text = text
    name_text = name_text.title()
    dni_text = dni
    image_editable.text((ptn1, ptn2), name_text, (255, 0, 0), font=title_font)
    image_editable.text((ptd1, ptd2), dni_text, (255, 0, 0), font=dni_font)
    file.save(folder+"/test.jpg")


def generate_certs(img_cert, coords1, coords2, df, font, name_size, dni_size):

    ls_names = []
    ls_dni = []
    ls_mails = []

    for i in range(len(df)):

        ls_names.append(df.iloc[i]["NOMBRES"])
        ls_dni.append(df.iloc[i]["DNI"])
        ls_mails.append(df.iloc[i]["CORREO"])

    for i in range(len(ls_names)):
        make_cert(img_cert, str(ls_names[i]), str(
            ls_dni[i]), str(ls_mails[i].split("@")[0]), coords1[0], coords1[1], coords2[0], coords2[1], font, name_size, dni_size)

    return ls_mails, ls_names


def import_image(file):
    img = Image.open(file)
    return img


def clean_folder(folder="certificados/*"):
    files = glob.glob(folder)
    for f in files:
        os.remove(f)
