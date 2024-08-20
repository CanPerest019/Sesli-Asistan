import tkinter as tk
from tkinter import scrolledtext
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from gtts import gTTS
from io import BytesIO
import pandas as pd
import uvicorn
import time
import pygame
import threading
import speech_recognition as sr

app = FastAPI()

# Global variables
model = None
vectorizer = None
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Pydantic model for handling command requests
class CommandRequest(BaseModel):
    command: str

# Konuşma motoru
def konus(metin):
    tts = gTTS(text=metin, lang='tr')
    ses_dosyasi = BytesIO()
    tts.write_to_fp(ses_dosyasi)
    ses_dosyasi.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(ses_dosyasi)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Model ve vectorizer'ı eğit
def model_egitimi(komutlar, yanitlar):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(komutlar)
    model = MultinomialNB()
    model.fit(X, yanitlar)
    return model, vectorizer

# Sabit veri setini oluştur
def veri_seti_olustur():
    veri = {
        "komut": [
        "Merhaba", 
        "Nasılsın?", 
        "Adın ne?", 
        "Bugün hava nasıl?", 
        "Saat kaç?", 
        "Teşekkür ederim", 
        "Hoşça kal", 
        "Müzik çal", 
        "Haberleri göster", 
        "Alarm kur", 
        "Bugün hangi gün?", 
        "Beni hatırlıyor musun?", 
        "Ne yapıyorsun?", 
        "Beni seviyor musun?", 
        "En sevdiğin renk ne?", 
        "En iyi arkadaşın kim?", 
        "Hangi yemekleri seversin?"
        ],

        "yanit": [
        "Merhaba! Size nasıl yardımcı olabilirim?", 
        "Teşekkür ederim, siz nasılsınız?", 
        "Benim adım Asistan. Sizin adınız nedir?", 
        "Havanın güzel olduğunu duyuyorum!", 
        "Şu anda saat 3:30.", 
        "Rica ederim, her zaman buradayım!", 
        "Hoşça kalın, iyi günler dilerim!", 
        "Hangi müziği çalmak istersiniz?", 
        "Bugünün haberlerini getiriyorum.", 
        "Hangi saatte alarm kurmamı istersiniz?", 
        "Bugün Salı.", 
        "Tabii ki! Sizi tanıdığım için mutluyum.", 
        "Ben bir sesli asistansım, her zaman yardıma hazırım.", 
        "Benim için önemlisiniz!", 
        "Renkleri çok seviyorum ama mavi gözde farklı bir güzellik var!", 
        "Benim en iyi arkadaşım sizsiniz!", 
        "Pizza, pasta ve salatayı çok seviyorum!"
        ]
    }

    df = pd.DataFrame(veri)
    return df

# Veri setini yükle ve modeli eğit
def veri_seti_ve_model_yukle():
    global model, vectorizer
    
    veri = veri_seti_olustur()
    
    if 'komut' in veri.columns and 'yanit' in veri.columns:
        komutlar = veri['komut'].tolist()
        yanitlar = veri['yanit'].tolist()
        model, vectorizer = model_egitimi(komutlar, yanitlar)
        konus("Veri seti başarıyla yüklendi ve model eğitildi.")
    else:
        konus("Veri setinde gerekli sütunlar bulunamadı. Lütfen veri setinizi kontrol edin.")

# Komutları işleme
def komut_isle(komut):
    if model and vectorizer:
        X = vectorizer.transform([komut])
        tahmin = model.predict(X)[0]
        konus(tahmin)
        return tahmin
    else:
        konus("Model yüklenmedi. Lütfen veri setini kontrol edin ve tekrar deneyin.")
        return "Model yüklenmedi."

@app.post("/upload-dataset/")
async def upload_dataset(file: UploadFile = File(...)):
    global model, vectorizer
    
    try:
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        
        if 'komut' in df.columns and 'yanit' in df.columns:
            komutlar = df['komut'].tolist()
            yanitlar = df['yanit'].tolist()
            model, vectorizer = model_egitimi(komutlar, yanitlar)
            konus("Veri seti başarıyla yüklendi ve model eğitildi.")
            return JSONResponse(content={"message": "Veri seti başarıyla yüklendi ve model eğitildi."})
        else:
            konus("Veri setinde gerekli sütunlar bulunamadı. Lütfen veri setinizi kontrol edin.")
            raise HTTPException(status_code=400, detail="Veri setinde gerekli sütunlar bulunamadı.")
    
    except pd.errors.ParserError as e:
        konus(f"Veri seti okunurken hata oluştu: {str(e)}")
        raise HTTPException(status_code=400, detail="Veri seti okunurken hata oluştu.")
    except Exception as e:
        konus(f"Bilinmeyen bir hata oluştu: {str(e)}")
        raise HTTPException(status_code=500, detail="Bilinmeyen bir hata oluştu.")

@app.post("/process-command/")
async def process_command(request: CommandRequest):
    komut = request.command
    tahmin = komut_isle(komut)
    return JSONResponse(content={"response": tahmin})

# Tkinter Arayüzü
class SesliAsistanArayuz(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sesli Asistan")
        self.geometry("400x300")
        
        # Komutları ve cevapları göstermek için metin alanı
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, width=50)
        self.text_area.pack(pady=10)
        
        # Konuş butonu
        self.konus_button = tk.Button(self, text="Konuş", command=self.konus_baslat)
        self.konus_button.pack(side=tk.LEFT, padx=10)
        
        # Konuşmayı Bitir butonu
        self.bitir_button = tk.Button(self, text="Konuşmayı Bitir", command=self.konus_bitir)
        self.bitir_button.pack(side=tk.RIGHT, padx=10)

        # Mikrofon dinleme durumu
        self.dinleme = False

    def konus_baslat(self):
        self.dinleme = True
        self.text_area.insert(tk.END, "Mikrofon dinlenmeye başladı...\n")
        self.dinleme_thread = threading.Thread(target=self.mikrofon_dinle)
        self.dinleme_thread.start()

    def mikrofon_dinle(self):
        global recognizer, microphone
        
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            while self.dinleme:
                try:
                    ses = recognizer.listen(source)
                    komut = recognizer.recognize_google(ses, language='tr')
                    self.text_area.insert(tk.END, f"Kullanıcı: {komut}\n")
                    self.after(1000, lambda: self.konus_cevapla(komut))
                except sr.UnknownValueError:
                    self.text_area.insert(tk.END, "Mikrofon sesi anlayamadı.\n")
                except sr.RequestError as e:
                    self.text_area.insert(tk.END, f"Google API hatası: {str(e)}\n")

    def konus_cevapla(self, komut):
        tahmin = komut_isle(komut)
        self.text_area.insert(tk.END, f"Asistan: {tahmin}\n")

    def konus_bitir(self):
        self.dinleme = False
        self.text_area.insert(tk.END, "Mikrofon dinlenmesi durduruldu.\n")

# FastAPI ve Tkinter'i paralel çalıştır
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=4554)

if __name__ == "__main__":
    veri_seti_ve_model_yukle()  # Veri setini yükle ve modeli eğit
    threading.Thread(target=run_fastapi).start()
    arayuz = SesliAsistanArayuz()
    arayuz.mainloop()
