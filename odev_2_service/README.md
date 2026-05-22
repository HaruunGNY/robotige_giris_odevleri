# 📐 Ödev 2: Dikdörtgen Alanı Hesaplama Servisi (Python)

Bu paket, ROS'ta anlık veya sürekli veri akışı yerine, "Soru-Cevap" (İstek-Yanıt) şeklinde çalışan **Service & Client** mimarisini öğretmek amacıyla geliştirilmiştir.

---

## 💡 Başlangıç Seviyesi Teorik Anlatım

### 1. ROS Servis (Service / Client) Nedir?
Publisher/Subscriber yapısında, radyo yayını gibi sürekli bir veri akışı vardır. Ancak bazen sadece **belirli bir anda bir iş yaptırmak ve sonucunu almak** isteriz. 

Bunu bir **restorandaki garson ve müşteri ilişkisine** benzetebiliriz:
*   **İstemci (Client - Müşteri):** Menüden bir yemek seçip sipariş verir (İstek / Request).
*   **Servis (Service/Server - Garson/Mutfak):** Siparişi alır, yemeği hazırlar ve müşteriye servis eder (Cevap / Response).

### 2. Özel `.srv` Mesaj Türü Nedir?
ROS'ta servisler, istek ve yanıt verilerini tanımlamak için özel `.srv` dosyaları kullanır. Bu dosyalarda istek ve yanıt kısımları üç kesikli çizgi (`---`) ile birbirinden ayrılır:

```txt
# İSTEK KISMI (Request) - Client'tan Server'a gidenler
float64 en
float64 boy
---
# CEVAP KISMI (Response) - Server'dan Client'a dönenler
float64 alan
```

---

## 🔍 Bu Ödevde Ne Yapılıyor?

1.  **Alan Sunucusu (`alan_sunucu.py`):** Arka planda çalışır ve bir istek gelmesini bekler. Bir istek geldiğinde kenar uzunluklarını alır, çarpar ($en \times boy$) ve sonucu yanıt olarak gönderir.
2.  **Alan İstemcisi (`alan_istemci.py`):** Kullanıcının terminalden girdiği iki sayıyı sunucuya istek olarak gönderir, sunucudan dönen cevabı ekrana yazdırır ve kapanır.

---

## 🚀 Nasıl Çalıştırılır ve Test Edilir?

Aşağıdaki komutları sırasıyla ayrı terminal sekmelerinde çalıştırın:

**1. ROS Çekirdeğini (Master) Başlatın:**
```bash
roscore
```

**2. Alan Hesaplayıcı Sunucuyu (Server) Başlatın:**
```bash
rosrun odev_2_service alan_sunucu.py
```

**3. İstemciyi (Client) Çalıştırıp Değer Gönderin (Örnek: En=5.2, Boy=10.0):**
```bash
rosrun odev_2_service alan_istemci.py 5.2 10.0
```

**4. Alternatif Test (Terminalden doğrudan servis çağırmak):**
```bash
rosservice call /dikdortgen_alani_hesapla "en: 5.2
boy: 10.0"
```
