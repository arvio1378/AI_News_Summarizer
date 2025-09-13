import pandas as pd
import os
import csv

def history(url, title, content, content_lang, summary, summary_lang):
    # masukkan ke bagian history
    record = {
        "url": url,
        "title": title,
        "content": content,
        "content language": content_lang,
        "summary": summary,
        "summary language": summary_lang
    }

    df_history = pd.DataFrame([record])
    file_path = "./data/history.csv"

    # cek apakah file sudah ada dan tidak kosong
    write_header = not os.path.exists(file_path) or os.stat(file_path).st_size == 0

    # simpan
    df_history.to_csv(
        file_path,
        mode="a",
        index=False,
        header=write_header,
        sep=";",
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )
