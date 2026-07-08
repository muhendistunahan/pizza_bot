import os
import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import streamlit as st

# =====================================================================
# 1. ORTAM DEĞİŞKENLERİ VE API AYARLARI
# =====================================================================
_ = load_dotenv(find_dotenv(), override=True)

# Streamlit Cloud üzerindeki Secrets'tan veya yerelden API anahtarını alır
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Sayfa başlığı ve tasarımı
st.set_page_config(page_title="Sipariş Ekranına Hoşgeldin
🤗", page_icon="🍕", layout="centered")
st.title("🍕 Sipariş Vermek İçin Benimle İletişim Kurabilirsin")
st.write("---")

# =====================================================================
# 2. BOT HAFIZASI VE SİSTEM TALİMATLARI (CONTEXT)
# =====================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'system', 'content': """
Sen SiparişBotu'sun, bir pizza restoranı için sipariş toplayan otomatik bir robotsun.
Önce müşteriyi selamla, sonra siparişi topla ve ardından gelip alacaklar mı yoksa adrese teslim mi istediklerini sor.
Tüm siparişi toplayana kadar bekle, sonra siparişi özetle ve son bir kez eklemek istedikleri bir şey olup olmadığını kontrol et.
Eğer adrese teslimat ise, mutlaka açık adres iste.
Son olarak ödemeyi al (nakit/kart).
Menüdeki ürünleri netleştirmek için tüm seçenekleri, ekstraları ve boyutları (büyük, orta, küçük) net bir şekilde sor.
Çok kısa, samimi ve konuşkan bir tarzda yanıt ver.

Menü aşağıdadır:
Pepperoni Pizza: 12.95 (Büyük), 10.00 (Orta), 7.00 (Küçük)
Peynirli Pizza: 10.95 (Büyük), 9.25 (Orta), 6.50 (Küçük)
Patlıcanlı Pizza: 11.95 (Büyük), 9.75 (Orta), 6.75 (Küçük)
Patates Kızartması: 4.50 (Büyük), 3.50 (Küçük)
Grek Salatası: 7.25

Malzemeler (Ekstralar):
Ekstra peynir: 2.00
Mantar: 1.50
Sosis: 3.00
Dana Jambon: 3.50
Özel Yapay Zeka Sosu: 1.50
Biber: 1.00

İçecekler:
Kola: 3.00 (Büyük), 2.00 (Orta), 1.00 (Küçük)
Sprite: 3.00 (Büyük), 2.00 (Orta), 1.00 (Küçük)
Şişe Su: 5.00
"""}
    ]

# =====================================================================
# 3. CHAT EKRANI GÖSTERİMİ
# =====================================================================
# Hafızadaki eski mesajları ekrana bas (Sistem mesajı hariç)
for msg in st.session_state.messages:
    if msg['role'] != 'system':
        with st.chat_message(msg['role']):
            st.write(msg['content'])

# Kullanıcıdan girdi alma alanı
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Kullanıcı mesajını ekrana bas ve hafızaya ekle
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    # OpenAI'dan yanıt üret
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyor..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.5
            )
            answer = response.choices[0].message.content
            st.write(answer)
            
    # Asistanın yanıtını hafızaya ekle
    st.session_state.messages.append({'role': 'assistant', 'content': answer})
