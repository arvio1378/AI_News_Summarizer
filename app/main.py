import streamlit as st
import pandas as pd
import os
from scraper import get_article
from summarizer import article_summarize
from translator import translate_long_text
from history import history
from topic import get_topics
from keywords import get_keywords

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="AI Summarizer",
    page_icon="📰",
    layout="wide"
)

# fungsi helper untuk load css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# panggil css eksternal
local_css("./style/style.css")

# Load Dataset
def load_data():
    file_path = "./data/history.csv"
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return pd.DataFrame(columns=["url", "title", "content", "content language", "summary", "summary language"])
    return pd.read_csv(file_path, sep=";", encoding="utf-8")

# navigasi halaman
pages = st.sidebar.selectbox("Menu : ", ["Summarizer", "History", "About"])

# Page Summarizer
if pages == "Summarizer":
    st.title("📰 AI Summarizer")
    st.subheader("This application is to summarize news to make it shorter")

    # Input URL
    url = st.text_input("Input URL :")
    lang_output = st.selectbox("Output Language : ", ["Indonesia", "English"], key="lang_output")

    if st.button("Summarize"):
        if url:
            try:
                # ambil artikelnya
                article = get_article(url)
                
                # bahasa artikel
                article_lang = article['lang']
                st.write(f"(Article Language : {article_lang})")

                # judul
                st.subheader("Title")
                title = article["title"]
                if lang_output == "Indonesia" and article_lang == "en":
                    title = translate_long_text(title, "id")
                elif lang_output == "English" and article_lang == "id":
                    title = translate_long_text(title, "en")  
                st.write(title)

                # isi artikel
                st.subheader("Content")
                content = article["text"]
                if lang_output == "Indonesia" and article_lang == "en":
                    content = translate_long_text(content, "id")
                elif lang_output == "English" and article_lang == "id":
                    content = translate_long_text(content, "en")
                st.write(content[:500] + "...")

                # ringkasan artikel
                st.subheader(f"Summary")
                summary = article_summarize(article["text"])
                if lang_output == "Indonesia" and article_lang == "en":
                    summary = translate_long_text(summary, "id")
                elif lang_output == "English" and article_lang == "id":
                    summary = translate_long_text(summary, "en")
                st.write(summary)

                # masukkan ke histori
                history(url=url, 
                        title=title, 
                        content=content, 
                        content_lang=lang_output, 
                        summary=summary, 
                        summary_lang=lang_output)

            except Exception as e:
                st.error(f"Error : {e}")

        else:
            st.warning("Please input the URL !!")

# Page History
elif pages == "History":
    st.title("📖 History, Topic, & Keywords")

    df = load_data()

    # Topic
    st.subheader("Topic")
    if not df.empty and "content" in df.columns and not df["content"].isnull().all():
        try:
            topic_results = get_topics(df)
            for t in topic_results:
                st.write(f"**🔑 Kata kunci:** {', '.join(t['keywords'])}")
                st.write("**📝 Contoh kalimat:**")
                for ex in t["examples"]:
                    st.write(f"- {ex[:200]}...")
        except Exception as e:
            st.warning(f"Failed to generate topics: {e}")
    else:
        st.info("No content available to generate topics.")

    # Keywords
    st.subheader("Most Keywords")
    if not df.empty and "content" in df.columns and not df["content"].isnull().all():
        try:
            keywords = get_keywords(df)
            for word, freq in keywords:
                st.write(f"- {word}: {freq}")
        except Exception as e:
            st.warning(f"Failed to generate keywords: {e}")
    else:
        st.info("No content available to generate keywords.")

    # tabel histori
    st.subheader("History Table")
    if df.empty:
        st.info("Belum ada data history.")
    else:
        st.dataframe(df)

# Page About
elif pages == "About":
    # Judul aplikasi
    st.title("Arvio Abe Suhendar")
    # Subheader
    st.subheader("Career Shifter | From Network to AI | Designing Intelligent Futures | Ready to Make an Impact in AI | Python Developer | Machine Learning Engineer | Data Scientist")
    st.markdown("---")

    # About me
    st.write("### 📝 About Me")
    st.write("👨‍💻 I'm a tech enthusiast with a strong foundation in Informatics Engineering from Universitas Gunadarma, where I developed solid analytical thinking, programming, and problem-solving skills.")
    st.write("🔧 After graduating, I began my professional journey as a Junior Network Engineer, managing enterprise network services like VPNIP, Astinet, and SIP Trunk on Huawei and Cisco platforms—handling configurations, service activations, and troubleshooting.")
    st.write("🤖 Over time, my curiosity led me to explore the world of Artificial Intelligence & Machine Learning. I've been actively upskilling through bootcamps and self-learning—covering data preprocessing, supervised & unsupervised learning, and deep learning using Python.")
    st.write("🎯 I'm now transitioning my career into AI/ML, combining my network infrastructure background with my growing expertise in data and intelligent systems. I'm particularly interested in how AI can improve systems, automate operations, and drive smarter decision-making.")
    st.write("🤝 Open to collaborations, mentorship, and new opportunities in the AI/ML space.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Education", "Experience", "Skills"])
    with tab1:
        # Pendidikan
        st.write("### 🎓 Education")
        st.write("""
        - **Bachelor of Informatics Engineering**   
        Universitas Gunadarma, 2019 - 2023, GPA 3.82/4.00
            - Built multiple applications (web & desktop) using Java, Python, and PHP in individual and team projects.
            - Built and optimized database systems
            - Learn techniques for solving mathematical problems using programming, numerical integration, and solving equations.
        - **Bootcamp AI/ML**    
        Dibimbing.id Academy, 2025 - Present
            - Mastered core concepts of Python programming including variables, data types, control structures, and functions.
            - Understanding the fundamentals of Artificial Intelligence and Machine Learning, key concepts, and applications.
            - Techniques to clean, transform, and prepare data for analysis, including handling missing data and feature scaling.
        """)
    with tab2:
        # Pengalaman
        st.write("### 💼 Experience")
        st.write("""
        - **Junior Network Engineer**   
        PT. Infomedia Nusantara, 2023 - Present
            - Astinet & VPNIP Service Management (Huawei Routers) : 
                 Handled service activation, disconnection,isolation, modification, and resumption for enterprise clients.
            - Wifi.id Service Provisioning (Cisco & WPgen) :    
                 Performed end-to-end activation and troubleshooting for public Wi-Fi services.
            - SIP Trunk International Access Control :  
                 Managed blocking and unblocking processes for international SIP trunk services to ensure secure and compliant voice connectivity
        """)
    with tab3:
        # Keterampilan
        st.write("### 🛠️ Skills")
        st.write("""
        - **Programming Languages**: Python
        - **Machine Learning**: Scikit-learn, TensorFlow, Keras
        - **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
        - **Database Management**: MySQL, PostgreSQL
        - **Networking**: Huawei Routers, Cisco Routers, WPgen
        - **Tools & Technologies**: Git, Docker, Jupyter Notebook
        - **Soft Skills**: Attention to Detail, Team Collaboration, Adaptability
        """)
    
    st.markdown("---")
    # Kontak
    st.write("### 📞 Contact Information")
    st.write("I'm currently studying and building a career in AI/ML. This project is my practice in building a simple Python application. I want to further develop my skills in this field through existing projects.")
    st.write("Feel free to contact me if you have any questions or suggestions regarding this project.")
    st.write("Email: 4rv10suhendar@gmail.com")
    st.write("LinkedIn: [Arvio Abe Suhendar](https://www.linkedin.com/in/arvio-abe-suhendar/)")
    st.write("Location: Depok, Indonesia")
    st.write("GitHub: [Arvio1378](https://github.com/arvio1378)")