# AI News Summarizer

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
git https://github.com/arvio1378/Apple-QA-RAG.git](https://github.com/arvio1378/AI_News_Summarizer.git
cd AI_News_Summarizer
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Jalankan Program
```bash
streamlit run app/main.py
```

## 📈 Hasil
Berikut ini adalah contoh hasil dari berita dan ringkasannya :
- Berita :
  - The Middle East Donald Trump See all topics Follow Qatar’s prime minister excoriated Israeli Prime Minister Benjamin Netanyahu in an exclusive interview with CNN on Wednesday, calling Israel’s attempted assassination of Hamas leaders in Doha “barbaric.”
“We were thinking that we are dealing with civilized people,” Qatari Prime Minister Sheikh Mohammed bin Abdulrahman bin Jassim Al-Thani told CNN’s Becky Anderson. “That’s the way we are dealing with others. And the action that (Netanyahu) took ...
-Ringkasan :
  - This is a full transcript of the attacks on Hamas in the Middle East. The prime minister says he is “betrayed” by Israel’s attack on the group, amid concerns over the deaths of five of its members. Here's what happened to those who were hostage in Gaza during the Israeli strike in Doha on Tuesday evening. Why? Following reports that Qatar has been accused of trying to assassinate their leaders.

## 🏗️ Kontribusi
- Bisa memilih ringkasan singkat, sedang, atau panjang.
- Ringkasan dari teks + video berita + podcast/audio.
- Membuat desain streamlit menjadi lebih bagus

## 🧑‍💻 Tentang Saya
Saya sedang belajar dan membangun karir di bidang AI/ML. Projek ini adalah latihan saya untuk membangun aplikasi python sederhana. Saya ingin lebih untuk mengembangkan skill saya di bidang ini melalui projek-projek yang ada.

📫 Terhubung dengan saya di:
- Linkedin : https://www.linkedin.com/in/arvio-abe-suhendar/
- Github : https://github.com/arvio1378
