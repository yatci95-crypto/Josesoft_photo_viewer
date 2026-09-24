# Josesoft Photo Viewer 🖼️

An advanced photo viewer designed to bring back the highly acclaimed, simple, stable, and lightning-fast classic habits of the **Windows 7 Photo Viewer** to modern operating systems. Specially crafted by **Josesoft** for those who are tired of the bloated and sluggish photo applications of modern Windows versions.

---

### ✨ Key Features & Windows 7 Behaviors

The application replicates the traditional Windows 7 Photo Viewer behaviors out of the box while introducing modern customization options:

*   **Familiar Classic Experience:** Smooth zooming/unzooming via mouse wheel (Scroll) and lag-free, lightning-fast navigation between photos in a folder using the keyboard arrow keys.
*   **Advanced Slideshow:** Enjoy your photos in full-screen mode with a smooth and fully customizable slideshow experience.
*   **Customizable Themes:** Change and personalize the interface colors and themes to suit your style.
*   **System Font Adaptive:** Automatically detects the active Windows text size and font style, rendering the UI seamlessly and in perfect harmony with your OS configuration.

---

### 🌐 Language Support

Featuring the official Josesoft signature, the app includes native support for **8 different languages** that automatically adapt to your system language or can be selected manually:

| Language Code | Native Name | English Name |
| :---: | :--- | :--- |
| **tr** | Türkçe | Turkish |
| **en** | English | English |
| **de** | Deutsch | German |
| **fr** | Français | French |
| **es** | Español | Spanish |
| **it** | Italiano | Italian |
| **pt** | Português | Portuguese |
| **pl** | Polski | Polish |

---

### 🚀 Versions

*   **Normal Version (`Photo_Viewer.py`)** 
    *   Compiled Asset: `JosesoftPhotoViewer.exe`
    *   Feature: Automatically sets itself as the default system photo viewer directly via `regedit` (Windows Registry).
*   **Store Version (`Photo_Viewer_Store.py`)** 
    *   Compiled Asset: `JosesoftPhotoViewer_Store.msix`
    *   Feature: Fully compliant with Microsoft Store policies. Registry writing is moved to the Store app manifest; it triggers `ms-settings:defaultapps` (Default Apps) to let users set the preference safely. Registry reading remains fully functional.

---

### 🛠️ Installation

*   **EXE (Normal Version):** Download the latest release from the [Releases](https://github.com) tab and run it directly.
*   **MSIX (Store Version):** Double-click the installer package to securely deploy it onto your system.

---

### 💻 Developer Compilation

To run the project locally or build the executable yourself, follow the instructions below:

```bash
# Install the required dependencies
pip install PyQt6 pyinstaller Pillow

# Compile into a standalone EXE via PyInstaller
pyinstaller --onefile --windowed --icon=app_icon.ico --name=Win7PhotoViewer Photo_Viewer.py
```

---

### 📄 License

This project is licensed under the **MIT** License. Proudly carrying the Josesoft signature.



# Josesoft Photo Viewer 🖼️

**Windows 7 Fotoğraf Görüntüleyicisi**'nin o çok sevilen, sade, kararlı ve yıldırım hızındaki klasik alışkanlıklarını modern sistemlere geri getiren gelişmiş bir fotoğraf görüntüleyici. Modern Windows sürümlerinin hantal uygulamalarından sıkılanlar için **Josesoft** tarafından özel olarak tasarlandı.

---

### ✨ Öne Çıkan Özellikler ve Windows 7 Davranışları

Uygulama, alışılagelmiş klasik Windows 7 Fotoğraf Görüntüleyicisi davranışlarını birebir yansıtır ve üzerine modern özelleştirmeler ekler:

*   **Alışılmış Klasik Deneyim:** Fare tekerleği (Scroll) ile yakınlaştırma/uzaklaştırma ve klavye yön tuşlarıyla klasördeki fotoğraflar arasında gecikmesiz, yıldırım hızında geçiş.
*   **Gelişmiş Slayt Gösterisi:** Fotoğraflarınızı tam ekran modunda, akıcı ve özelleştirilebilir bir slayt gösterisi eşliğinde keyifle inceleyin.
*   **Özelleştirilebilir Temalar:** Keyfinize göre arayüz renklerini ve temalarını değiştirebilir, kişiselleştirebilirsiniz.
*   **Sistem Font Uyumu:** Windows'un aktif yazı boyutunu ve yazı tipi stilini otomatik olarak algılar; arayüzü işletim sisteminizle tamamen pürüzsüz ve uyumlu hale getirir.

---

### 🌐 Dil Desteği (Language Support)

Josesoft imzasıyla uygulama, sistem dilinize otomatik uyum sağlayan veya içerisinden seçebileceğiniz **8 farklı dil** desteğine sahiptir:

| Dil Kodu | Dil Adı (Yerel) | Dil Adı (Türkçe) |
| :---: | :--- | :--- |
| **tr** | Türkçe | Türkçe |
| **en** | English | İngilizce |
| **de** | Deutsch | Almanca |
| **fr** | Français | Fransızca |
| **es** | Español | İspanyolca |
| **it** | Italiano | İtalyanca |
| **pt** | Português | Portekizce |
| **pl** | Polski | Lehçe |

---

### 🚀 Versiyonlar

*   **Normal Sürüm (`Photo_Viewer.py`)** 
    *   Derlenmiş Hali: `JosesoftPhotoViewer.exe`
    *   Özellik: Doğrudan `regedit` (Kayıt Defteri) üzerinden kendisini sisteme varsayılan fotoğraf görüntüleyici olarak atar.
*   **Store Sürümü (`Photo_Viewer_Store.py`)** 
    *   Derlenmiş Hali: `JosesoftPhotoViewer_Store.msix`
    *   Özellik: Microsoft Store politikalarına tam uyumludur. Registry yazma işlemi Store için manifest dosyasına taşınmıştır; varsayılan yapmak için doğrudan `ms-settings:defaultapps` (Varsayılan Uygulamalar) sayfasını açar. Registry okuma serbesttir.

---

### 🛠️ Kurulum

*   **EXE (Normal Sürüm):** [Releases](https://github.com) sekmesinden güncel sürümü indirin ve doğrudan çalıştırın.
*   **MSIX (Store Sürümü):** Mağaza paketine çift tıklayarak güvenle sisteminize kurun.

---

### 💻 Geliştiriciler İçin Derleme

Projeyi yerel ortamınızda çalıştırmak veya yeniden derlemek için aşağıdaki adımları takip edebilirsiniz:

```bash
# Gerekli kütüphanelerin yüklenmesi
pip install PyQt6 pyinstaller Pillow

# PyInstaller ile EXE haline getirme
pyinstaller --onefile --windowed --icon=app_icon.ico --name=Win7PhotoViewer Photo_Viewer.py
```


### 📄 Lisans

Bu proje **MIT** lisansı altında korunmaktadır. Josesoft imzası taşımaktadır.
