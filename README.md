# 🍕 SiparişBotu - Yapay Zeka Destekli Pizza Sipariş Asistanı

SiparişBotu, müşterilerin bir pizza restoranından tamamen doğal dil kullanarak sipariş vermesini sağlayan, OpenAI'ın `gpt-4o-mini` modeli ile güçlendirilmiş akıllı bir chatbot uygulamasıdır. Proje, modern ve dinamik bir arayüz sunmak adına **Streamlit** kullanılarak web ortamına taşınmıştır.

---

## 🚀 Özellikler

* **Akıllı Sipariş Yönetimi:** Menüdeki pizzaları (Pepperoni, Peynirli, Patlıcanlı), ekstraları, salataları ve içecekleri boyut seçenekleriyle birlikte akıllıca analiz eder.
* **Dinamik Kural Takibi:** Sipariş tamamlanana kadar müşteri adımlarını (teslimat türü, adres bilgisi, ödeme yöntemi) mantıksal bir sıra ile takip eder.
* **Hafıza Yönetimi:** `st.session_state` kullanarak konuşma geçmişini kaybetmez, bağlamı (context) akıcı bir şekilde korur.
* **Esnek Menü Entegrasyonu:** Müşteri menü dışı bir ürün istediğinde (örneğin hamburger), kibar bir şekilde menüye yönlendirir.

---

## 🛠️ Kullanılan Teknolojiler

* **Python 3.14+**
* **Streamlit:** Hızlı ve modern web arayüzü yönetimi.
* **OpenAI API (GPT-4o-Mini):** Doğal dil işleme ve akıllı asistan motoru.
* **Python-Dotenv:** Çevresel değişkenlerin ve konfigürasyonların yönetimi.

---

## 📦 Kurulum ve Yerel Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak isterseniz aşağıdaki adımları takip edebilirsiniz:

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/muhendistunahan/pizza_bot.git](https://github.com/muhendistunahan/pizza_bot.git)
    cd pizza_bot
    ```

2.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ortam Değişkenlerini Ayarlayın:**
    Proje ana dizininde bir `.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
    ```env
    OPENAI_API_KEY="sk-proj-sizin-api-anahtariniz"
    ```

4.  **Uygulamayı Başlatın:**
    ```bash
    streamlit run app.py
    ```

---

## ☁️ Canlı Yayın (Deployment)

Bu proje **Streamlit Community Cloud** üzerinde canlı olarak barındırılmaktadır. Canlı versiyonda güvenlik amacıyla API anahtarı kod içerisine gömülmemiş, Streamlit'in kriptolu **Secrets Management** (Kasa) altyapısı kullanılarak tamamen güvenli hale getirilmiştir.

---

## 📝 Menü İçeriği

Asistan aşağıdaki menü kurallarına göre müşterileri yönlendirir:

| Ürün Sınıfı | Seçenekler | Fiyatlar |
| :--- | :--- | :--- |
| **Pizzalar** | Pepperoni, Peynirli, Patlıcanlı | Boyuta göre (Küçük, Orta, Büyük) |
| **Yan Ürünler** | Patates Kızartması, Grek Salatası | 3.50 - 7.25 |
| **Ekstralar** | Peynir, Mantar, Sosis, Jambon, AI Sos, Biber | 1.00 - 3.50 |
| **İçecekler** | Kola, Sprite, Şişe Su | Boyuta göre |

---
👨‍💻 **Geliştirici:** [@muhendistunahan](https://github.com/muhendistunahan)
