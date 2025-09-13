import textwrap
from transformers import pipeline

translator_model_en_id = "Helsinki-NLP/opus-mt-en-id"
translator_model_id_en = "Helsinki-NLP/opus-mt-id-en"

# Inggris to Indonesia
engtoid = pipeline("translation", model=translator_model_en_id)
# Indonesia to Inggris
idtoeng = pipeline("translation", model=translator_model_id_en)

def translate(content, lang_content):
    if lang_content == "id":
        return engtoid(content)[0]["translation_text"]
    elif lang_content == "en":
        return idtoeng(content)[0]["translation_text"]
    return content

def translate_long_text(content, lang_content, max_chars=400):
    chunks = textwrap.wrap(content, max_chars, break_long_words=False, replace_whitespace=False)
    translated_chunks = [translate(chunk, lang_content) for chunk in chunks]
    return "\n".join(translated_chunks)