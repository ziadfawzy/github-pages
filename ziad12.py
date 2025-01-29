import pyttsx3
import pytesseract
from PIL import Image
import cv2
import os
import mimetypes
from tkinter import Tk, filedialog, simpledialog, messagebox

def text_to_speech(text, language):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if not voices:
        print("No voices available. Using default settings.")
        return
    for voice in voices:
        if voice.id.startswith(language) or language in voice.id:
            engine.setProperty('voice', voice.id)
            break
    
    rate = simpledialog.askinteger("Set Speed", "Enter speech rate (default 150):", minvalue=50, maxvalue=300)
    if rate:
        engine.setProperty('rate', rate)
    else:
        engine.setProperty('rate', 150)
    
    engine.say(text)
    engine.runAndWait()

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image. Please select a valid image file.")
        return ""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Check if the required languages are installed in Tesseract
    available_languages = pytesseract.get_languages(config='')
    lang = 'ara+eng'
    for l in lang.split('+'):
        if l not in available_languages:
            print(f"Warning: Language '{l}' is not installed in Tesseract. Using default 'eng'.")
            lang = 'eng'
            break
    
    text = pytesseract.image_to_string(thresh, lang=lang)
    return text.strip()

def select_image():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title='Select an image', filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in ["image/png", "image/jpeg"]:
            messagebox.showerror("Invalid File", "Please select a valid image file (PNG, JPG, JPEG).")
            return None
    return file_path

def select_language():
    Tk().withdraw()
    languages = {'Arabic': 'ar', 'English': 'en', 'French': 'fr'}
    selected_lang = simpledialog.askstring("Select Language", "Choose a language: Arabic, English, French")
    if selected_lang and selected_lang.strip().capitalize() in languages:
        return languages[selected_lang.strip().capitalize()]
    else:
        messagebox.showwarning("Invalid Input", "Invalid language selection. Defaulting to Arabic.")
        return 'ar'

if __name__ == "__main__":
    image_path = select_image()
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        if extracted_text:
            print("Extracted Text:", extracted_text)
            user_language = select_language()
            text_to_speech(extracted_text, language=user_language)
