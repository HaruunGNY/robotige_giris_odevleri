# 🐢 Ödev 1: Turtlesim Konum Dinleyici ve Hareket Yönetimi (Python)

Bu paket, ROS (Robot Operating System) ortamındaki en temel iletişim desenleri olan **Publisher (Yayıncı)** ve **Subscriber (Abone)** kavramlarını öğrenmek amacıyla Turtlesim 2D simülasyon ortamında geliştirilmiştir.

---

## 💡 Başlangıç Seviyesi Teorik Anlatım

### 1. ROS Düğümü (Node) Nedir?
Robotun beyninde belirli bir görevi yerine getiren bağımsız, küçük programlara **Düğüm (Node)** denir. Örneğin; bu ödevde yazdığımız Python düğümü robotun konumunu takip etmekten ve motor hızını kontrol etmekten sorumludur.

### 2. Yayıncı (Publisher) ve Abone (Subscriber) Mantığı
ROS'ta düğümler birbirleriyle **Konular (Topics)** aracılığıyla haberleşirler. Bu yapıyı bir **posta/iletişim sistemine** benzetebiliriz:

*   **Konu (Topic):** Bir radyo frekansı veya mektup kutusudur (örn: `/turtle1/pose` veya `/turtle1/cmd_vel`).
*   **Yayıncı (Publisher):** Mektup kutusuna sürekli veri (mektup) bırakan taraftır. Robotun motorlarına "git" komutunu basan düğümümüz bir yayıncıdır.
*   **Abone (Subscriber):** Mektup kutusunu sürekli dinleyen ve yeni veri geldiğinde bunu okuyan taraftır. Kaplumbağanın o an nerede olduğunu ekrana yazdırmak için konum konusunu dinleyen düğümümüz bir abonedir.

---

## 🔍 Bu Ödevde Ne Yapılıyor?

Yazdığımız `kaplumbaga_takip_ve_hareket.py` betiği iki temel görevi eşzamanlı olarak yerine getirir:

1.  **Konum Okuma (Subscriber):** Kaplumbağanın o anki X, Y koordinatlarını ve dönüş açısını saniyede 1 kez `/turtle1/pose` konusundan okur ve terminal ekranına anlaşılır bir şekilde yazdırır.
2.  **Hareket Verme (Publisher):** `/turtle1/cmd_vel` konusuna saniyede 10 kez `geometry_msgs/Twist` mesaj tipinde doğrusal (linear) ve açısal (angular) hız göndererek kaplumbağayı sürekli dairesel hareket ettirir.

---

## 🚀 Nasıl Çalıştırılır?

Aşağıdaki komutları sırasıyla ayrı terminal sekmelerinde çalıştırın:

**1. ROS Çekirdeğini (Master) Başlatın:**
```bash
roscore
```

**2. Turtlesim Simülasyon Ekranını Açın:**
```bash
rosrun turtlesim turtlesim_node
```

**3. Yönetici Python Düğümünü Çalıştırın:**
```bash
rosrun odev_1_turtlesim kaplumbaga_takip_ve_hareket.py
```
