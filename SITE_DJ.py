from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import io
import requests
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Путь к папке с изображениями
UPLOAD_FOLDER = 'static/images'

# Список текстовых документов
documents = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?",
]

# Создание TF-IDF матрицы
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверка, был ли загружен файл
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Сохранение файла
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))

                # Поиск по изображению
                image_search_results = search_by_image(os.path.join(UPLOAD_FOLDER, file.filename))

                # Поиск по тексту
                text_search_results = search_by_text(request.form['search_text'])

                return render_template('index.html', image_search_results=image_search_results,
                                       text_search_results=text_search_results)

    return render_template('index.html')


def search_by_image(image_path):
    # Реализация поиска по изображению
    # (в данном примере будет возвращаться список изображений из папки static/images)
    image_files = os.listdir(UPLOAD_FOLDER)
    return image_files


def search_by_text(search_text):
    # Реализация поиска по тексту
    query_vector = tfidf_vectorizer.transform([search_text])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    indices = (-similarities).argsort()[:3]

    result = []
    for i in indices:
        result.append(documents[i])

    return result


if __name__ == '__main__':
    app.run(debug=True)

