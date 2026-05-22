# 📊 Ödev 5: PID Denetleyici ile Mesafe Kontrolü (Distance Control)

Bu paket, kontrol mühendisliğinde ve robotikte en çok kullanılan klasik kontrol algoritması olan **PID (Proportional-Integral-Derivative)** teorisini öğrenmek ve uygulamak amacıyla geliştirilmiştir.

---

## 💡 Başlangıç Seviyesi Teorik Anlatım

### 1. PID Denetleyici Nedir?
PID, robotun bir hedef değere (örneğin duvara olan mesafeye) ulaşırken sarsılmadan, aşırı hızlanmadan ve hedefin etrafında çılgınca sallanmadan (salınım yapmadan) tam o noktada pürüzsüzce durmasını sağlayan bir **geri bildirim (feedback)** algoritmasıdır.

Günlük hayattan **kırmızı ışıkta duran araba** benzetmesini yapalım:
*   Işığa çok uzaktayken gaza hızlıca basarsınız.
*   Işığa yaklaştıkça frene basarak yavaşlarsınız.
*   Tam çizginin üstünde sarsıntısız bir şekilde durursunuz.

İşte robotun da önündeki duvara yaklaşırken duvara çarpmadan, tam hedef mesafesinde durmasını bu algoritma sağlar.

---

### 2. PID Bileşenleri Nelerdir? (Basit Formül Anlatımı)

Algoritma, anlık hata miktarını (yani **mevcut mesafe - hedef mesafe**) alır ve üç farklı matematiksel süzgeçten geçirerek robota verilecek hızı hesaplar:

$$\text{Hesaplanan Hız} = \underbrace{K_p \times \text{Hata}}_{P} + \underbrace{K_i \times \text{Hata Toplamı}}_{I} + \underbrace{K_d \times \text{Hata Değişimi}}_{D}$$

#### 🔴 P (Proportional - Oransal Bileşen) ── *"Şu anki Durum"*
*   **Mantık:** Hata miktarı ile doğru orantılı bir güç verir.
*   **Açıklama:** Robot duvardan çok uzaktaysa hata büyüktür, hızlı gider. Duvara yaklaştıkça hata küçülür, hız da orantılı olarak yavaşlar.
*   **Sınırı:** Tek başına P katsayısı sürtünme gibi engeller yüzünden robotu tam hedefte durduramaz; hedefe yaklaşıldığında hız sıfırlanacağı için robot hedefin biraz gerisinde kalır (Kalıcı Hata).

#### 🟡 I (Integral - Bütünsel Bileşen) ── *"Geçmişin Değerlendirilmesi"*
*   **Mantık:** Zaman içinde biriken tüm küçük hataları toplar.
*   **Açıklama:** Robot hedefe çok yaklaştı ama motorların son 2 cm'yi aşacak gücü yetmiyor. Zaman geçtikçe I bileşeni bu aşamadığı 2 cm'yi üst üste toplar (entegre eder). Sonunda motorlara o son adımı attıracak ekstra torku vererek kalıcı hatayı sıfırlar.

#### 🔵 D (Derivative - Türevsel Bileşen) ── *"Geleceğin Tahmini / Frenleme"*
*   **Mantık:** Hatanın değişim hızına bakarak tepki verir.
*   **Açıklama:** Robot duvara çok hızlı yaklaşıyorsa, D bileşeni "Çok hızlı yaklaşıyoruz, çarpmak üzereyiz!" uyarısı yapar ve motorlara ters yönde fren etkisi (damperleme) uygular. Robotun hedefi aşmasını ve salınım yapmasını önler.

---

## 🔍 Bu Ödevde Ne Yapılıyor?

1.  **Düğüm (`mesafe_pid_kontrol.py`):** Lidar verileriyle önündeki duvarın anlık mesafesini dinler ve robota tam **0.35 metre** önünde durma görevi verir.
2.  **PID Döngüsü (10 Hz):** Her 0.1 saniyede bir PID formülünü işleterek motorlara hız yayınlar.
3.  **Tolerans (Deadband) ve Kilitleme:** Motorlardaki mikro titreşimleri ve salınımları engellemek için +-2 cm'lik bir hata toleransı tanımlanmıştır. Robot bu aralığa girdiğinde hızı sıfırlayıp sistemi kilitler ve görevi başarıyla tamamlar.

---

## 🚀 Nasıl Çalıştırılır?

Aşağıdaki komutları sırasıyla farklı terminallerde çalıştırın:

**1. Gazebo Simülasyon Dünyasını Başlatın:**
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

**2. PID Kontrolcü Düğümünü Çalıştırın:**
```bash
rosrun odev_5_pid_kontrol mesafe_pid_kontrol.py
```

*Not: Ödevin çalışmasını gösteren demo videosunu [videos/gorev2.mp4](./videos/gorev2.mp4) dosyasından izleyebilirsiniz.*
