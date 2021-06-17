## Automatic Certificate generator and email Sender

An Automatic generator of certificates for my local university SEG Student Chapter, it generates a certificate with name and DNI given in an excel (test_prueba.xlsx is an example of the format that it uses, names and DNIs are fake or mine).

It also sends emails automatically to the recipients of the certificate.

### Demo

For a demo of how it works, please visit

[https://github.com/ieferreira/auto-certificate](https://github.com/ieferreira/auto-certificate)

### Heroku deployed app

If you want to see an online version of the app please go to:

#### [https://auto-certificate.herokuapp.com](https://auto-certificate.herokuapp.com/)

### Local use

Using streamlit as frontend, clone the repo and run it with the following command:

Requirements are:

```bash
streamlit
numpy
tqdm
stqdm
pandas
openpyxl
pillow==7.2.0
```

Alternatively run for installing the dependencies:

```bash
pip install -r requirements.txt
```

Clone the repo and run the following command:

```bash
streamlit run app.py
```

### To Do

- Ver como mejorar la calidad del pdf generado (se acepta jpg y png más sin embargo la calidad es similar)

## Author

Iván E. Ferreira - Unal Bogotá

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
