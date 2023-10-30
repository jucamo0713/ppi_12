from io import BytesIO

import numpy as np
import requests
import skimage
import streamlit as st

from fake_useragent import UserAgent

ua = UserAgent()

MAX_SIZE_TEXT = 30


def book_card(book, key: str = None):
    user_agent = ua.random
    data_image = requests.get(book["image"], headers={
        "User-Agent": user_agent
    })
    if data_image.status_code == 200:
        # Se crea BytesIO object para que actúe como un archivo
        # falso
        img_file = BytesIO(data_image.content)
        try:
            # Read the image using 'skimage.io.imread'
            image = skimage.io.imread(img_file)
            desired_height = image.shape[1] * 3 / 2
            crop_top = int((image.shape[0] - desired_height) // 2)
            if crop_top >= 0:
                crop_bottom = int(image.shape[0] - crop_top)
                image = image[crop_top:crop_bottom, :]
            else:
                black_part = np.zeros((-crop_top, image.shape[
                    1], 3), dtype=np.uint8)
                image = np.vstack([black_part, image, black_part])
        except Exception:
            image = ("https://islandpress.org/sites/default/files"
                     "/default_book_cover_2015.jpg")
    else:
        image = ("https://islandpress.org/sites/default/files"
                 "/default_book_cover_2015.jpg")
    st.image(image,
             use_column_width=True, )

    if len(book["title"]) > MAX_SIZE_TEXT:
        book["title"] = book["title"][:MAX_SIZE_TEXT - 3] + "..."
    if len(book["author"]) > MAX_SIZE_TEXT:
        book["author"] = book["author"][:MAX_SIZE_TEXT - 3] + "..."
    st.write("**Título:**", book["title"])
    st.write("**Autor:**", book["author"])
    st.button('Detalle',
              key=book["_id"] if key is None else key + book["_id"],
              on_click=(lambda x: st.experimental_set_query_params(
                  book_id=x)), args=[book["_id"]])
