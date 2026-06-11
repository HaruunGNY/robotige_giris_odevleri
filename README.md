# 🤖 Robotiğe Giriş ROS Ödevleri (TurtleBot3 & Turtlesim)

Bu depo (repository), **Robotiğe Giriş** dersi kapsamında hazırlanan, 2D simülasyon ortamından (Turtlesim) başlayıp 3D Gazebo ortamında otonom mobil robot kontrolüne (TurtleBot3) kadar uzanan **5 farklı ROS (Robot Operating System) ödevini ve 1 kapsamlı Final Uygulama Projesini** içermektedir.

Her bir ödev ve final projesi, bağımsız birer ROS paketi olarak tasarlanmış olup başlangıç seviyesindeki öğrencilerin ve meraklıların robotik sistemleri, sensör veri işlemeyi ve klasik kontrol algoritmalarını pratik ederek öğrenmesi için kapsamlı dokümantasyonlar barındırır.

---

## 📁 Depo İçeriği ve Özetler

Her bir klasörün içerisinde, ilgili ödevin çalışması için gereken teorik altyapıyı (Publisher/Subscriber, Service/Client, Lidar sensörleri, Move-Stop-Rotate algoritması, PID teorisi, AMCL Navigasyon vb.) anlatan detaylı rehberler yer almaktadır.

### 1. 🐢 [Ödev 1: Turtlesim Konum Dinleyici ve Hareket](./odev_1_turtlesim/)
*   **Açıklama:** Turtlesim simülasyonundaki kaplumbağanın konumunu saniyede bir okuyup ekrana yazarken, aynı anda robota sürekli dairesel hareket komutları yayınlar.
*   **Kazanım:** ROS Publisher (Yayıncı) ve Subscriber (Abone) mimarisi.

### 📐 [Ödev 2: Dikdörtgen Alanı Hesaplayan Servis](./odev_2_service/)
*   **Açıklama:** İstemciden (Client) gelen en ve boy değerlerini alıp alanı hesaplayarak istemciye dönen bir ROS Servis düğümüdür. Özel bir `.srv` dosya yapısı kullanır.
*   **Kazanım:** ROS Service ve Client (İstek-Cevap) mimarisi.

### 🗺️ [Ödev 3: Gazebo ile Otonom Navigasyon](./odev_3_navigation/)
*   **Açıklama:** Gazebo simülasyonunda TurtleBot3 robotunun harita üzerinden belirlenen 5 farklı X, Y koordinat noktasına engellerden kaçarak otonom sırayla gitmesini sağlar.
*   **Kazanım:** Action Client (`move_base`), Harita Okuma ve Otonom Navigasyon.

### 🛑 [Ödev 4: Lidar ile Otonom Engelden Kaçma](./odev_4_engel_kacma/)
*   **Açıklama:** Robotun Lidar (LaserScan) sensörünü kullanarak önündeki engelleri algılamasını ve reaktif bir durum makinesiyle (**Move-Stop-Rotate**) çarpmadan hareket etmesini sağlar.
*   **Kazanım:** Lidar Verisi İşleme, Durum Makinesi (State Machine) Mantığı.

### 📊 [Ödev 5: PID Denetleyicisi ile Duvara Yaklaşma](./odev_5_pid_kontrol/)
*   **Açıklama:** Robotun Lidar sensörüyle önündeki duvarı ölçüp, tam belirlenen hedef mesafede (0.35m) sarsıntısız, salınım yapmadan ve pürüzsüz durması için PID algoritmasını çalıştırır.
*   **Kazanım:** Klasik Kontrol Teorisi (P, I, D Katsayıları) ve Satürasyon/Tolerans Sınırları.

### 🏁 [Final Projesi: Çoklu Görev QR Doğrulama Servis Robotu](./final_odev/)
*   **Açıklama:** Robotun bir kitapçı/kütüphane ortamında (`AWS Bookstore World`) 4 farklı görev noktasına otonom navigasyon yapmasını, hedeflerdeki QR kodları kamerasıyla okuyup doğrulamasını ve görev raporu hazırlamasını sağlar.
*   **Kazanım:** Kompleks Durum Makineleri, Move-Base Hedef Yönetimi, OpenCV Kamerayla QR Kod Çözme, Hata ve Zaman Aşımı Yönetimi.

---

## 🛠️ Kurulum ve Derleme (Installation & Setup)

Uygulamaların çalışabilmesi için öncelikle bu depoyu bilgisayarınıza indirmeniz ve ROS çalışma alanınızda (catkin workspace) derlemeniz gerekmektedir.

**1. Çalışma Alanının (Workspace) Oluşturulması ve Klonlama:**
Eğer mevcut bir çalışma alanınız yoksa yeni bir tane oluşturup `src` dizinine gidin ve projeyi klonlayın:
```bash
# Workspace oluşturma ve src klasörüne geçiş
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src

# Depoyu klonlayın
git clone https://github.com/HaruunGNY/robotige_giris_odevleri.git
```

**2. Derleme Adımı:**
Çalışma alanınızın kök dizinine gidip projeyi derleyin:
```bash
cd ~/catkin_ws
catkin_make
```

**3. Çalışma Alanını Çevreye Ekleme (Source):**
```bash
source devel/setup.bash
```

**4. Çalıştırma Yetkisi Verme:**
Python düğümlerinin sorunsuz çalışabilmesi için dosyalara çalıştırma izni (`chmod +x`) verildiğinden emin olun:
```bash
chmod +x ~/catkin_ws/src/robotige_giris_odevleri/odev_1_turtlesim/scripts/*.py
chmod +x ~/catkin_ws/src/robotige_giris_odevleri/odev_2_service/scripts/*.py
chmod +x ~/catkin_ws/src/robotige_giris_odevleri/odev_3_navigation/scripts/*.py
chmod +x ~/catkin_ws/src/robotige_giris_odevleri/odev_4_engel_kacma/scripts/*.py
chmod +x ~/catkin_ws/src/robotige_giris_odevleri/odev_5_pid_kontrol/scripts/*.py
chmod +x ~/catkin_ws/src/robotige_giris_odevleri/final_odev/src/*.py
```

*Detaylı teorik anlatımlar ve özgün komutlar için çalışmak istediğiniz ödev klasörünün içindeki `README.md` dosyasını inceleyin.*
