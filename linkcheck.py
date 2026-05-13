import tkinter as tk
from tkinter import scrolledtext
import requests
from urllib.parse import urlparse

def link_analiz_et():
   
    sonuc_alani.delete('1.0', tk.END)
    
    
    url = url_giris.get().strip()
    
    if not url:
        sonuc_alani.insert(tk.END, "Lütfen analiz etmek için bir link girin.\n")
        return

    sonuc_alani.insert(tk.END, f"--- {url} Analiz Ediliyor ---\n\n")
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        
        response = requests.get(url, allow_redirects=True, timeout=10)
        
        history = response.history
        redirect_count = len(history)
        
        sonuc_alani.insert(tk.END, f"[+] Toplam Yönlendirme Sayısı: {redirect_count}\n")
        for resp in history:
            sonuc_alani.insert(tk.END, f"    -> Yönlendirilen Adres: {resp.url} ({resp.status_code})\n")
        
        sonuc_alani.insert(tk.END, f"[+] Nihai Varış Adresi: {response.url}\n\n")

        suspicious_score = 0
        reasons = []

        if redirect_count > 2:
            suspicious_score += 1
            reasons.append("Çok fazla yönlendirme zinciri var.")

        if not response.url.startswith('https'):
            suspicious_score += 1
            reasons.append("Bağlantı güvenli değil (HTTPS kullanılmıyor).")

        shorteners = ['bit.ly', 't.co', 'tinyurl.com', 'is.gd', 'buff.ly']
        if any(s in url.lower() for s in shorteners):
            suspicious_score += 1
            reasons.append("URL kısaltma servisi tespit edildi.")

        sonuc_alani.insert(tk.END, "--- ANALİZ SONUCU ---\n")
        if suspicious_score == 0:
            sonuc_alani.insert(tk.END, "SONUÇ: Link temiz görünüyor.\n")
        elif suspicious_score == 1:
            sonuc_alani.insert(tk.END, "SONUÇ: Düşük riskli / Dikkatli olun.\n")
        else:
            sonuc_alani.insert(tk.END, "SONUÇ: !!! ŞÜPHELİ LİNK !!!\n")
        
        for reason in reasons:
            sonuc_alani.insert(tk.END, f"  - {reason}\n")

    except Exception as e:
        sonuc_alani.insert(tk.END, f"Hata: Linke ulaşılamadı veya geçersiz.\n")




root = tk.Tk()
root.title("URL Analiz Programı")
root.geometry("650x500")
root.configure(bg="#f0f0f0")


lbl = tk.Label(root, text="Analiz edilecek linki girin:", font=("Arial", 11, "bold"), bg="#f0f0f0")
lbl.pack(pady=(20, 5))

url_giris = tk.Entry(root, width=60, font=("Arial", 11))
url_giris.pack(pady=5)
url_giris.focus() 


btn = tk.Button(root, text="Analizi Başlat", command=link_analiz_et, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5)
btn.pack(pady=15)


sonuc_alani = scrolledtext.ScrolledText(root, width=75, height=18, font=("Consolas", 10), bg="#ffffff")
sonuc_alani.pack(pady=10, padx=15)


root.mainloop()