# AI_News_Summarizer

## 📋 Deskripsi
AI News Summarizer adalah aplikasi yang memanfaatkan Natural Language Processing (NLP) untuk meringkas berita panjang menjadi ringkas, informatif, dan mudah dipahami. Proyek ini ditujukan untuk membantu pembaca mendapatkan inti berita dengan cepat, baik dalam bahasa Indonesia maupun Inggris.

## 🚀 Fitur
- Ringkasan otomatis dari artikel berita.
- Mendukung dua bahasa (Indonesia & Inggris).
- Antarmuka sederhana menggunakan Streamlit

## 🧠 Tools & Library
- Python
- Streamlit
- Pandas
- Newspaper
- Transformers
- NLTK
- Bertopic
- Langdetect

## 📁 Struktur Folder
- AI News Summarizer/
  - data
      - history.csv -> Tempat histori
  - app
      - history.py -> Memasukkan data ke histori
      - keywords.py -> Mencari keywords dari berita
      - main.py -> File utama untuk menjalankan program
      - scraper.py -> Mengambil isi berita dari url
      - summarizer.py -> Meringkas berita
      - topic.py -> Mendapatkan topik dari berita
      - translator.py -> Menterjemahkan berita
  -models -> Tempat model
      - embedding -> Model embedding untuk topik
      - summarizer -> Model Summarizer
      - translator -> Model Translator
  - notebooks
      - test.ipynb -> Eksperimen program
  - style
      style.css -> Desain tampilan 
  - requirements.txt -> Library program
  - README.md -> Desripsi pada program

## 🛠️ Arsitektur
- Preprocessing artikel berita (hapus noise, stopwords, dan lainnya)
- Translate ke bahasa antara Inggris dan Indonesia
- Summarization, Translate, dan Embedding dengan model huggingface
- Output ringkasan singkat dalam bahasa sesuai input

## 🖥️ Cara Menjalankan Program
1. Clone repositori
```bash
git clone https://github.com/arvio1378/Apple-QA-RAG.git
cd Apple QA RA
```
