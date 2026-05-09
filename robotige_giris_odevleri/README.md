# Robotiğe Giriş ROS Ödevleri

Bu depo (repository), Robotiğe Giriş dersi kapsamında verilen 3 farklı ROS (Robot Operating System) ödevini içermektedir. Her bir ödev bağımsız bir ROS paketi olarak tasarlanmıştır.

## İçerik

1. **[odev_1_turtlesim](./odev_1_turtlesim/)**
   Turtlesim simülasyon ortamında yayıncı (publisher) ve abone (subscriber) kavramlarının pratiği. Turtle'ın konumunu dinleyip, ona hareket komutları gönderme.

2. **[odev_2_service](./odev_2_service/)**
   ROS Servis ve İstemci (Service / Client) mimarisi kullanılarak dikdörtgenin alanını hesaplayan otonom hesaplayıcı. Özel bir `.srv` mesaj türü barındırır.

3. **[odev_3_navigation](./odev_3_navigation/)**
   Gazebo ve TurtleBot3 kullanarak otonom navigasyon (navigation stack) ve haritalama. Belirlenen 5 farklı noktaya sırayla Action Client (`move_base`) kullanarak gitme.

## 🛠️ Nasıl İndirilir ve Kurulur? (Download & Installation)

Bu paketteki uygulamaların çalışabilmesi için öncelikle repoyu bilgisayarınıza indirmeniz ve ROS çalışma alanınızda (catkin workspace) derlemeniz gerekmektedir.

**1. Depoyu İndirin (Clone):**
Çalışma alanınızın `src` dizinine gidin ve bu projeyi bilgisayarınıza klonlayın:
```bash
cd ~/catkin_ws/src
git clone https://github.com/KULLANICI_ADINIZ/robotige_giris_odevleri.git
```
*(Not: Yukarıdaki linkteki `KULLANICI_ADINIZ` kısmını kendi GitHub kullanıcı adınızla değiştirmeyi unutmayın veya deponun asıl linkini yapıştırın.)*

**2. Çalışma alanınızın kök dizinine gidin ve derleyin:**
```bash
cd ~/catkin_ws
catkin_make
```

**3. Çalışma alanını source edin:**
```bash
source devel/setup.bash
```

**4. (ÖNEMLİ): Python betiklerine çalıştırma yetkisi verin:**
Python düğümlerini hatasız çalıştırabilmeniz için executable izinlerinin (`chmod +x`) verildiğinden emin olun.
```bash
chmod +x ~/catkin_ws/src/odev_1_turtlesim/scripts/*.py
chmod +x ~/catkin_ws/src/odev_2_service/scripts/*.py
chmod +x ~/catkin_ws/src/odev_3_navigation/scripts/*.py
```

*Detaylı çalıştırma talimatları için ilgili ödev klasörünün içindeki `README.md` dosyasını inceleyebilirsiniz.*
