from deep_translator import GoogleTranslator
from langdetect import detect
import pycountry
from pydantic import BaseModel

class processed_text(BaseModel):
    translated: str
    language: str
    

def detect_language(text):
    language=pycountry.languages.get(alpha_2=detect(text))
    return language    
    
def translate_language(text,language):
    translated = GoogleTranslator(source=detect(text), target=language).translate(text)
    language=pycountry.languages.get(alpha_2=detect(text))
    return processed_text(translated=translated,language=language.name)