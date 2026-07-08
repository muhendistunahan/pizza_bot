import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import panel as pn
from IPython.display import display, HTML

# =====================================================================
# 1. ORTAM DEĞİŞKENLERİ VE API AYARLARI
# =====================================================================
_ = load_dotenv(find_dotenv(), override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Güncel OpenAI istemcisini (client) başlatıyoruz
client = OpenAI()

# Panel arayüz uzantısını aktifleştiriyoruz
pn.extension()

# =====================================================================
# 2. YAPAY ZEKA CORE (ÇEKİRDEK) FONKSİYONLARI
# =====================================================================
def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    """Gelen mesaj geçmişini kullanarak OpenAI'dan yanıt döner."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message.content

# =====================================================================
# 3. SENİN EKLEDİĞİN: JSON SİPARİŞ ÖZETİ ÇIKARAN FONKSİYON
# =====================================================================
def get_order_summary_json():
    """Konuşma geçmişini analiz eder ve mutfak/kasa için JSON özet üretir."""
    # Mevcut sohbet geçmişinin bir kopyasını alıyoruz
    messages = context.copy()
    
    # Modelin tam olarak bir JSON objesi üretmesi için talimatı ekliyoruz
    messages.append({
        'role': 'system', 
        'content': """Sohbetteki pizza siparişinin JSON formatında bir özetini çıkar. 
Her bir ürünün fiyatını ayrı ayrı belirt. 
JSON yapısı tam olarak şu alanları içermelidir:
1) pizza (boyutu dahil et)
2) list of toppings (ekstra malzemelerin listesi)
3) list of drinks (içecekler ve boyutları)
4) list of sides (yan ürünler/patates vb. ve boyutları)
5) total price (toplam fiyat)

Yalnızca geçerli bir JSON objesi döndür, başında veya sonunda açıklama yazma."""
    })
    
    # JSON çıktısı alırken tam kesinlik için temperature=0 kalmalıdır
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"} # OpenAI'ın JSON modu (Hata payını sıfıra indirir)
    )
    return response.choices[0].message.content

# =====================================================================
# 4. GÖRSEL GÖSTERİM FONKSİYONLARI (HTML & JSON GEÇMİŞİ)
# =====================================================================
def get_html_conversation(messages):
    """Konuşma geçmişini estetik bir HTML chat ekranına dönüştürür."""
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #1a1a1a; color: #f0f0f0; padding: 20px; }
            .chat-container { max-width: 600px; margin: 0 auto; background: #242424; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            .message { padding: 12px 16px; margin: 10px 0; border-radius: 10px; max-width: 75%; line-height: 1.4; font-size: 0.95em; }
            .user { background-color: #1e88e5; color: white; margin-left: auto; text-align: left; border-bottom-right-radius: 2px; }
            .assistant { background-color: #3a3a3a; color: #e0e0e0; margin-right: auto; border-bottom-left-radius: 2px; }
            .system { background-color: #444; color: #aaa; max-width: 100%; text-align: center; font-size: 0.85em; border-radius: 5px; }
            .sender { font-weight: bold; font-size: 0.8em; margin-bottom: 4px; display: block; opacity: 0.8; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h2 style="text-align: center; color: #4caf50; margin-bottom: 20px;">🍕 SiparişBotu Rapor Ekranı</h2>
    """
    for msg in messages:
        role = msg['role']
        content = msg['content'].replace('\n', '<br>')
        if role == 'system':
            html_content += '<div class="message system"><strong>Sistem Hafızası:</strong> Menü ve Kurallar Yüklendi.</div>'
        elif role == 'user':
            html_content += f'<div class="message user"><span class="sender">Siz</span>{content}</div>'
        elif role == 'assistant':
            html_content += f'<div class="message assistant"><span class="sender">SiparişBotu</span>{content}</div>'
            
    html_content += "</div></body></html>"
    return html_content

def print_pretty_json(messages):
    """Tüm konuşma geçmişini ham JSON olarak formatlar."""
    clean_history = [msg for msg in messages if msg['role'] != 'system']
    return json.dumps(clean_history, indent=4, ensure_ascii=False)

# =====================================================================
# 5. ARAYÜZ MOTORU VE TETİKLEYİCİLER (UI MOTORU)
# =====================================================================
def collect_messages(_):
    prompt = inp.value_input
    if not prompt: 
        return pn.Column(*panels)
        
    inp.value = ''
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role': 'assistant', 'content': f"{response}"})
    
    user_box = pn.pane.Markdown(f"**Siz:** {prompt}", styles={
        'background': '#1E88E5', 'color': 'white', 'padding': '12px 16px', 
        'border-radius': '12px', 'margin': '5px', 'max-width': '450px'
    })
    
    assistant_box = pn.pane.Markdown(f"**SiparişBotu:** {response}", styles={
        'background': '#2C2C2C', 'color': '#E0E0E0', 'padding': '12px 16px', 
        'border-radius': '12px', 'margin': '5px', 'max-width': '450px'
    })
    
    panels.append(pn.Row(user_box, align='end'))
    panels.append(pn.Row(assistant_box, align='start'))
 
    return pn.Column(*panels, styles={'background': '#121212', 'padding': '15px', 'border-radius': '10px'})

# =====================================================================
# 6. BOT HAFIZASI VE SİSTEM TALİMATLARI (CONTEXT)
# =====================================================================
panels = [] 
context = [ {'role':'system', 'content':"""
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
"""} ]

initial_welcome = pn.pane.Markdown("**SiparişBotu:** Merhaba! Pizza restoranımıza hoş geldiniz! Bugün ne sipariş etmek istersiniz? Menüdeki pizzalarımız, salatalarımız ve içeceklerimiz var. Hadi başlayalım! 🍕", styles={
    'background': '#2C2C2C', 'color': '#E0E0E0', 'padding': '12px 16px', 'border-radius': '12px', 'margin': '5px'
})
panels.append(pn.Row(initial_welcome))

# =====================================================================
# 7. GÖRSEL PANEL BİLEŞENLERİ VE DASHBOARD BAŞLATMA (TAM EKRAN GÜNCELLEMESİ)
# =====================================================================
# Genişlikleri sabit (width=450) yapmak yerine esnek (%90) yapıyoruz
inp = pn.widgets.TextInput(
    placeholder="Mesajınızı buraya yazın ve Gönder'e basın...", 
    sizing_mode='stretch_width'
)
button_conversation = pn.widgets.Button(name="Gönder!", button_type='primary', width=120)

interactive_conversation = pn.bind(collect_messages, button_conversation)

# height'ı 400 yerine tarayıcı yüksekliğine uydurması için esnek yapıyoruz
chat_window = pn.panel(
    interactive_conversation, 
    loading_indicator=True, 
    sizing_mode='stretch_both', # Hem eni hem boyu ekrana yayar
    styles={'background': '#121212', 'border-radius': '10px', 'overflow-y': 'auto'}
)

input_row = pn.Row(inp, button_conversation, sizing_mode='stretch_width', align='center')

# Tüm ekranı kaplayacak ana dashboard yapısı
dashboard = pn.Column(
    chat_window,
    pn.Spacer(height=15),
    input_row,
    sizing_mode='stretch_both', # Tarayıcı sayfasının tamamını doldurur
    styles={'padding': '20px', 'background': '#1A1A1A', 'height': '95vh'} # vh: ekran yüksekliği yüzdesi
)

# Tarayıcıda tam ekran başlatır
# dashboard.show() -> Bu satırı silip yerine altındakini yazıyoruz:
dashboard.servable()
