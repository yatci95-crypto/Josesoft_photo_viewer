
"""
Windows 7 Fotoğraf Görüntüleyicisi v6 - ICON FIX
- Simgeler duzeltildi: Win7 Aero seffaf ikonlar
- Klasor tarama + ortalanmis alt bar korundu
- Animasyonlu ikonlar + seffaf PNG

ikon dosyaları: icon_zoom.png, icon_actual.png, icon_prev.png, icon_next.png,
icon_center.png, icon_rotleft.png, icon_rotright.png, icon_delete.png
ve program ikonu icon.png ayni klasorde olmali
"""

import sys
import os
import locale
import math
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout,
    QVBoxLayout, QPushButton, QFileDialog, QScrollArea, QFrame, QMessageBox,
    QDialog, QTabWidget, QCheckBox, QSpinBox, QFontComboBox, QGroupBox,
    QFormLayout, QColorDialog, QListWidget, QListWidgetItem, QDialogButtonBox
)
from PyQt6.QtGui import (
    QPixmap, QTransform, QAction, QDesktopServices, QPainter, QIcon,
    QPen, QColor, QFont
)
from PyQt6.QtCore import (
    QEvent,
    Qt, QTimer, QUrl, QSettings, QSize, QPropertyAnimation,
    QEasingCurve
)
import json
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

try:
    import winreg
    HAS_WINREG = True
except ImportError:
    HAS_WINREG = False

# Genisletilmis format listesi - modern ve RAW dahil
IMAGE_EXTS = [
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tiff", ".tif", ".ico",
    ".jfif", ".jpe", ".jxr", ".hdp", ".wdp",
    ".heic", ".heif", ".avif", ".jxl", ".svg", ".svgz",
    ".psd", ".psb",
    ".raw", ".cr2", ".cr3", ".nef", ".nrw", ".arw", ".srf", ".sr2",
    ".raf", ".rw2", ".rwl", ".dng", ".orf", ".pef", ".srw", ".x3f", ".3fr", ".ari", ".bay", ".crw", ".cap", ".data", ".dcs", ".dcr", ".drf", ".eip", ".erf", ".fff", ".iiq", ".k25", ".kdc", ".mdc", ".mef", ".mos", ".mrw", ".obm", ".ptx", ".pxn", ".r3d", ".raf", ".raw", ".rwz", ".sr2", ".srf", ".x3f"
]
# Tekil hale getir ve kucuk harf
IMAGE_EXTS = sorted(list(set([e.lower() for e in IMAGE_EXTS])))

PROG_ID = "Win7PhotoViewerFile"

LANGUAGES = {
    "tr": "Türkçe",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "pl": "Polski",
}

TRANSLATIONS = {
    "tr": {
        "window_title": "Fotoğraf Görüntüleyici",
        "menu_file": "Dosya",
        "menu_view": "Görünüm",
        "menu_settings": "Ayarlar",
        "menu_help": "Yardım",
        "file_open": "Aç...",
        "file_open_folder": "Klasör aç...",
        "file_print": "Yazdır...",
        "file_email": "E-posta ile gönder",
        "file_burn": "Diske yaz",
        "file_open_location": "Dosya konumunu aç",
        "file_open_with": "Birlikte aç...",
        "file_exit": "Çıkış",
        "view_prev": "Önceki",
        "view_next": "Sonraki",
        "view_zoom_in": "Yakınlaştır",
        "view_zoom_out": "Uzaklaştır",
        "view_actual": "Gerçek boyut",
        "view_rot_left": "Sola döndür",
        "view_rot_right": "Sağa döndür",
        "view_delete": "Sil",
        "view_slideshow": "Slayt gösterisi",
        "settings_set_default": "Varsayılan görüntüleyici yap",
        "settings_language": "Dil / Language",
        "settings_auto_detect": "Sistem dilini otomatik algıla",
        "settings_current": "Mevcut dil",
        "settings_auto_failed": "Otomatik dil algılanamadı",
        "settings_auto_failed_msg": "Windows dili otomatik algılanamadı.",
        "help_about": "Hakkında",
        "about_text": "Josesoft tarafından tasarlandı",
        "no_photo": "Hiç fotoğraf bulunamadı\nDosya > Aç veya klasör sürükle",
        "btn_prev_tip": "Önceki",
        "btn_next_tip": "Sonraki",
        "btn_zoom_tip": "Yakınlaştır",
        "btn_actual_tip": "Gerçek boyut (Esc)",
        "btn_rot_left_tip": "Sola döndür",
        "btn_rot_right_tip": "Sağa döndür",
        "btn_delete_tip": "Sil (Del)",
        "btn_slideshow_tip": "Slayt gösterisi (Ortadaki)",
        "status_count": "{} / {}",
        "default_check_title": "Varsayılan",
        "default_success": "Başarılı! {} tür bağlandı",
        "default_fail": "Başarısız",
        "print_no_img": "Resim yok!",
        "slideshow_title": "Slayt Gösterisi",
        "slideshow_interval_label": "Resimler arası geçiş süresi:",
        "slideshow_fullscreen_label": "Tam ekranda göster",
        "slideshow_esc_hint": "ESC ile durdurabilirsiniz",
        "slideshow_running": "Slayt Gösterisi {}sn - ESC durdur",
        "slideshow_stop_tip": "Slayt gösterisini durdur",
        "theme_settings_title": "Tema Ayarları",
        "theme_tab": "Tema",
        "lang_tab": "Dil / Language",
        "ext_tab": "Dosya Türleri",
        "theme_auto_accent": "Windows tema rengini otomatik kullan (önerilen)",
        "theme_top_color": "Üst çubuk - Top bar:",
        "theme_bottom_color": "Alt çubuk - Bottom bar:",
        "theme_bg_color": "Arka plan - Background:",
        "theme_font": "Yazı Tipi - Font",
        "theme_font_label": "Font:",
        "theme_size_label": "Boyut - Size:",
        "theme_text_auto": "Yazı rengini otomatik belirle (kontrasta göre)",

        "btn_ok": "Tamam",
        "btn_cancel": "İptal",
        "btn_close": "Kapat",
        "btn_select_all": "Tümünü seç",
        "btn_select_none": "Hiçbirini seçme",
        "theme_colors_group": "Renkler",
        "theme_font_group": "Yazı Tipi",
        "lang_select_label": "Dil seçin:",
        "ext_select_label": "Varsayılan yapılacak dosya türleri:",    },
    "en": {
        "window_title": "Photo Viewer",
        "menu_file": "File",
        "menu_view": "View",
        "menu_settings": "Settings",
        "menu_help": "Help",
        "file_open": "Open...",
        "file_open_folder": "Open folder...",
        "file_print": "Print...",
        "file_email": "Email",
        "file_burn": "Burn",
        "file_open_location": "Open location",
        "file_open_with": "Open with...",
        "file_exit": "Exit",
        "view_prev": "Previous",
        "view_next": "Next",
        "view_zoom_in": "Zoom in",
        "view_zoom_out": "Zoom out",
        "view_actual": "Actual size",
        "view_rot_left": "Rotate left",
        "view_rot_right": "Rotate right",
        "view_delete": "Delete",
        "view_slideshow": "Slideshow",
        "settings_set_default": "Set as default",
        "settings_language": "Language",
        "settings_auto_detect": "Auto-detect language",
        "settings_current": "Current",
        "settings_auto_failed": "Failed",
        "settings_auto_failed_msg": "Not detected",
        "help_about": "About",
        "about_text": "Designed by Josesoft",
        "no_photo": "No photos",
        "btn_prev_tip": "Previous",
        "btn_next_tip": "Next",
        "btn_zoom_tip": "Zoom",
        "btn_actual_tip": "Actual size",
        "btn_rot_left_tip": "Rotate left",
        "btn_rot_right_tip": "Rotate right",
        "btn_delete_tip": "Delete",
        "btn_slideshow_tip": "Slideshow",
        "status_count": "{} / {}",
        "default_check_title": "Check",
        "default_success": "Success! {} types",
        "default_fail": "Failed",
        "print_no_img": "No image!",
        "slideshow_title": "Slideshow",
        "slideshow_interval_label": "Interval between images:",
        "slideshow_fullscreen_label": "Show in fullscreen",
        "slideshow_esc_hint": "Press ESC to stop",
        "slideshow_running": "Slideshow {}s - ESC to stop",
        "slideshow_stop_tip": "Stop slideshow",
        "theme_settings_title": "Theme Settings",
        "theme_tab": "Theme",
        "lang_tab": "Language",
        "ext_tab": "File Types",
        "theme_auto_accent": "Use Windows accent color automatically (recommended)",
        "theme_top_color": "Top bar:",
        "theme_bottom_color": "Bottom bar:",
        "theme_bg_color": "Background:",
        "theme_font": "Font",
        "theme_font_label": "Font:",
        "theme_size_label": "Size:",
        "theme_text_auto": "Auto-detect text color (based on contrast)",

        "btn_ok": "OK",
        "btn_cancel": "Cancel",
        "btn_close": "Close",
        "btn_select_all": "Select all",
        "btn_select_none": "Select none",
        "theme_colors_group": "Colors",
        "theme_font_group": "Font",
        "lang_select_label": "Select language:",
        "ext_select_label": "File types to set as default:",    },
    "de": {
        "window_title": "Fotoanzeige",
        "menu_file": "Datei",
        "menu_view": "Ansicht",
        "menu_settings": "Einstellungen",
        "menu_help": "Hilfe",
        "file_open": "Oeffnen...",
        "file_open_folder": "Ordner oeffnen...",
        "file_print": "Drucken...",
        "file_email": "Per E-Mail senden",
        "file_burn": "Auf Datentraeger brennen",
        "file_open_location": "Dateispeicherort oeffnen",
        "file_open_with": "Oeffnen mit...",
        "file_exit": "Beenden",
        "view_prev": "Zurueck",
        "view_next": "Weiter",
        "view_zoom_in": "Vergroessern",
        "view_zoom_out": "Verkleinern",
        "view_actual": "Echte Groesse",
        "view_rot_left": "Nach links drehen",
        "view_rot_right": "Nach rechts drehen",
        "view_delete": "Loeschen",
        "view_slideshow": "Diashow",
        "settings_set_default": "Als Standard festlegen",
        "settings_language": "Sprache",
        "settings_auto_detect": "Sprache automatisch erkennen",
        "settings_current": "Aktuell",
        "settings_auto_failed": "Automatische Erkennung fehlgeschlagen",
        "settings_auto_failed_msg": "Windows-Sprache konnte nicht erkannt werden.",
        "help_about": "Ueber",
        "about_text": "Entworfen von Josesoft",
        "no_photo": "Keine Fotos gefunden",
        "btn_prev_tip": "Zurueck",
        "btn_next_tip": "Weiter",
        "btn_zoom_tip": "Vergroessern",
        "btn_actual_tip": "Echte Groesse (Esc)",
        "btn_rot_left_tip": "Nach links drehen",
        "btn_rot_right_tip": "Nach rechts drehen",
        "btn_delete_tip": "Loeschen (Entf)",
        "btn_slideshow_tip": "Diashow",
        "status_count": "{} / {}",
        "default_check_title": "Standard",
        "default_success": "Erfolg! {} Typen verbunden",
        "default_fail": "Fehlgeschlagen",
        "print_no_img": "Kein Bild!",
        "slideshow_title": "Diashow",
        "slideshow_interval_label": "Intervall zwischen Bildern:",
        "slideshow_fullscreen_label": "Im Vollbild anzeigen",
        "slideshow_esc_hint": "Mit ESC beenden",
        "slideshow_running": "Diashow {}s - ESC zum Stoppen",
        "slideshow_stop_tip": "Diashow stoppen",
        "theme_settings_title": "Design-Einstellungen",
        "theme_tab": "Design",
        "lang_tab": "Sprache",
        "ext_tab": "Dateitypen",
        "theme_auto_accent": "Windows-Akzentfarbe automatisch verwenden (empfohlen)",
        "theme_top_color": "Obere Leiste:",
        "theme_bottom_color": "Untere Leiste:",
        "theme_bg_color": "Hintergrund:",
        "theme_font": "Schriftart",
        "theme_font_label": "Schrift:",
        "theme_size_label": "Groesse:",
        "theme_text_auto": "Textfarbe automatisch bestimmen (Kontrast)",

        "btn_ok": "OK",
        "btn_cancel": "Abbrechen",
        "btn_close": "Schließen",
        "btn_select_all": "Alle auswählen",
        "btn_select_none": "Keine auswählen",
        "theme_colors_group": "Farben",
        "theme_font_group": "Schriftart",
        "lang_select_label": "Sprache auswählen:",
        "ext_select_label": "Dateitypen als Standard festlegen:",    },
    "fr": {
        "window_title": "Visionneuse de photos",
        "menu_file": "Fichier",
        "menu_view": "Affichage",
        "menu_settings": "Parametres",
        "menu_help": "Aide",
        "file_open": "Ouvrir...",
        "file_open_folder": "Ouvrir dossier...",
        "file_print": "Imprimer...",
        "file_email": "Envoyer par e-mail",
        "file_burn": "Graver sur disque",
        "file_open_location": "Ouvrir l'emplacement",
        "file_open_with": "Ouvrir avec...",
        "file_exit": "Quitter",
        "view_prev": "Precedent",
        "view_next": "Suivant",
        "view_zoom_in": "Zoom avant",
        "view_zoom_out": "Zoom arriere",
        "view_actual": "Taille reelle",
        "view_rot_left": "Pivoter a gauche",
        "view_rot_right": "Pivoter a droite",
        "view_delete": "Supprimer",
        "view_slideshow": "Diaporama",
        "settings_set_default": "Definir par defaut",
        "settings_language": "Langue",
        "settings_auto_detect": "Detection auto de la langue",
        "settings_current": "Actuelle",
        "settings_auto_failed": "Echec detection",
        "settings_auto_failed_msg": "Langue Windows non detectee.",
        "help_about": "A propos",
        "about_text": "Conçu par Josesoft",
        "no_photo": "Aucune photo trouvee",
        "btn_prev_tip": "Precedent",
        "btn_next_tip": "Suivant",
        "btn_zoom_tip": "Zoom",
        "btn_actual_tip": "Taille reelle (Echap)",
        "btn_rot_left_tip": "Gauche",
        "btn_rot_right_tip": "Droite",
        "btn_delete_tip": "Supprimer (Suppr)",
        "btn_slideshow_tip": "Diaporama",
        "status_count": "{} / {}",
        "default_check_title": "Verifier",
        "default_success": "Succes! {} types lies",
        "default_fail": "Echec",
        "print_no_img": "Pas d'image!",
        "slideshow_title": "Diaporama",
        "slideshow_interval_label": "Intervalle entre les images:",
        "slideshow_fullscreen_label": "Afficher en plein ecran",
        "slideshow_esc_hint": "Echap pour arreter",
        "slideshow_running": "Diaporama {}s - Echap pour arreter",
        "slideshow_stop_tip": "Arreter diaporama",
        "theme_settings_title": "Parametres du theme",
        "theme_tab": "Theme",
        "lang_tab": "Langue",
        "ext_tab": "Types de fichiers",
        "theme_auto_accent": "Utiliser couleur d'accent Windows auto (recommande)",
        "theme_top_color": "Barre du haut:",
        "theme_bottom_color": "Barre du bas:",
        "theme_bg_color": "Arriere-plan:",
        "theme_font": "Police",
        "theme_font_label": "Police:",
        "theme_size_label": "Taille:",
        "theme_text_auto": "Detecter couleur texte auto (contraste)",

        "btn_ok": "OK",
        "btn_cancel": "Annuler",
        "btn_close": "Fermer",
        "btn_select_all": "Tout sélectionner",
        "btn_select_none": "Tout désélectionner",
        "theme_colors_group": "Couleurs",
        "theme_font_group": "Police",
        "lang_select_label": "Choisir la langue:",
        "ext_select_label": "Types de fichiers par défaut:",    },
    "es": {
        "window_title": "Visor de fotos",
        "menu_file": "Archivo",
        "menu_view": "Ver",
        "menu_settings": "Configuracion",
        "menu_help": "Ayuda",
        "file_open": "Abrir...",
        "file_open_folder": "Abrir carpeta...",
        "file_print": "Imprimir...",
        "file_email": "Enviar por correo",
        "file_burn": "Grabar en disco",
        "file_open_location": "Abrir ubicacion",
        "file_open_with": "Abrir con...",
        "file_exit": "Salir",
        "view_prev": "Anterior",
        "view_next": "Siguiente",
        "view_zoom_in": "Acercar",
        "view_zoom_out": "Alejar",
        "view_actual": "Tamano real",
        "view_rot_left": "Girar izquierda",
        "view_rot_right": "Girar derecha",
        "view_delete": "Eliminar",
        "view_slideshow": "Presentacion",
        "settings_set_default": "Establecer por defecto",
        "settings_language": "Idioma",
        "settings_auto_detect": "Detectar idioma automaticamente",
        "settings_current": "Actual",
        "settings_auto_failed": "Fallo en deteccion",
        "settings_auto_failed_msg": "No se detecto idioma de Windows.",
        "help_about": "Acerca de",
        "about_text": "Diseñado por Josesoft",
        "no_photo": "No se encontraron fotos",
        "btn_prev_tip": "Anterior",
        "btn_next_tip": "Siguiente",
        "btn_zoom_tip": "Acercar",
        "btn_actual_tip": "Tamano real (Esc)",
        "btn_rot_left_tip": "Girar izq.",
        "btn_rot_right_tip": "Girar der.",
        "btn_delete_tip": "Eliminar (Supr)",
        "btn_slideshow_tip": "Presentacion",
        "status_count": "{} / {}",
        "default_check_title": "Verificar",
        "default_success": "Exito! {} tipos vinculados",
        "default_fail": "Error",
        "print_no_img": "Sin imagen!",
        "slideshow_title": "Presentacion",
        "slideshow_interval_label": "Intervalo entre imagenes:",
        "slideshow_fullscreen_label": "Mostrar en pantalla completa",
        "slideshow_esc_hint": "ESC para detener",
        "slideshow_running": "Presentacion {}s - ESC para detener",
        "slideshow_stop_tip": "Detener presentacion",
        "theme_settings_title": "Ajustes de tema",
        "theme_tab": "Tema",
        "lang_tab": "Idioma",
        "ext_tab": "Tipos de archivo",
        "theme_auto_accent": "Usar color de acento de Windows auto (recomendado)",
        "theme_top_color": "Barra superior:",
        "theme_bottom_color": "Barra inferior:",
        "theme_bg_color": "Fondo:",
        "theme_font": "Fuente",
        "theme_font_label": "Fuente:",
        "theme_size_label": "Tamano:",
        "theme_text_auto": "Detectar color de texto auto (contraste)",

        "btn_ok": "Aceptar",
        "btn_cancel": "Cancelar",
        "btn_close": "Cerrar",
        "btn_select_all": "Seleccionar todo",
        "btn_select_none": "Deseleccionar todo",
        "theme_colors_group": "Colores",
        "theme_font_group": "Fuente",
        "lang_select_label": "Seleccionar idioma:",
        "ext_select_label": "Tipos de archivo por defecto:",    },
    "it": {
        "window_title": "Visualizzatore foto",
        "menu_file": "File",
        "menu_view": "Visualizza",
        "menu_settings": "Impostazioni",
        "menu_help": "Guida",
        "file_open": "Apri...",
        "file_open_folder": "Apri cartella...",
        "file_print": "Stampa...",
        "file_email": "Invia per email",
        "file_burn": "Masterizza su disco",
        "file_open_location": "Apri percorso",
        "file_open_with": "Apri con...",
        "file_exit": "Esci",
        "view_prev": "Precedente",
        "view_next": "Successivo",
        "view_zoom_in": "Ingrandisci",
        "view_zoom_out": "Riduci",
        "view_actual": "Dimensione effettiva",
        "view_rot_left": "Ruota a sinistra",
        "view_rot_right": "Ruota a destra",
        "view_delete": "Elimina",
        "view_slideshow": "Presentazione",
        "settings_set_default": "Imposta come predefinito",
        "settings_language": "Lingua",
        "settings_auto_detect": "Rileva lingua automaticamente",
        "settings_current": "Attuale",
        "settings_auto_failed": "Rilevamento fallito",
        "settings_auto_failed_msg": "Lingua Windows non rilevata.",
        "help_about": "Informazioni",
        "about_text": "Progettato da Josesoft",
        "no_photo": "Nessuna foto trovata",
        "btn_prev_tip": "Precedente",
        "btn_next_tip": "Successivo",
        "btn_zoom_tip": "Zoom",
        "btn_actual_tip": "Effettiva (Esc)",
        "btn_rot_left_tip": "Sinistra",
        "btn_rot_right_tip": "Destra",
        "btn_delete_tip": "Elimina (Canc)",
        "btn_slideshow_tip": "Presentazione",
        "status_count": "{} / {}",
        "default_check_title": "Verifica",
        "default_success": "Successo! {} tipi collegati",
        "default_fail": "Fallito",
        "print_no_img": "Nessuna immagine!",
        "slideshow_title": "Presentazione",
        "slideshow_interval_label": "Intervallo tra immagini:",
        "slideshow_fullscreen_label": "Mostra a schermo intero",
        "slideshow_esc_hint": "ESC per fermare",
        "slideshow_running": "Presentazione {}s - ESC per fermare",
        "slideshow_stop_tip": "Ferma presentazione",
        "theme_settings_title": "Impostazioni tema",
        "theme_tab": "Tema",
        "lang_tab": "Lingua",
        "ext_tab": "Tipi di file",
        "theme_auto_accent": "Usa colore accento Windows auto (consigliato)",
        "theme_top_color": "Barra superiore:",
        "theme_bottom_color": "Barra inferiore:",
        "theme_bg_color": "Sfondo:",
        "theme_font": "Carattere",
        "theme_font_label": "Font:",
        "theme_size_label": "Dimensione:",
        "theme_text_auto": "Rileva colore testo auto (contrasto)",

        "btn_ok": "OK",
        "btn_cancel": "Annulla",
        "btn_close": "Chiudi",
        "btn_select_all": "Seleziona tutto",
        "btn_select_none": "Deseleziona tutto",
        "theme_colors_group": "Colori",
        "theme_font_group": "Carattere",
        "lang_select_label": "Seleziona lingua:",
        "ext_select_label": "Tipi di file predefiniti:",    },
    "pt": {
        "window_title": "Visualizador de fotos",
        "menu_file": "Arquivo",
        "menu_view": "Exibir",
        "menu_settings": "Configuracoes",
        "menu_help": "Ajuda",
        "file_open": "Abrir...",
        "file_open_folder": "Abrir pasta...",
        "file_print": "Imprimir...",
        "file_email": "Enviar por e-mail",
        "file_burn": "Gravar em disco",
        "file_open_location": "Abrir local",
        "file_open_with": "Abrir com...",
        "file_exit": "Sair",
        "view_prev": "Anterior",
        "view_next": "Proximo",
        "view_zoom_in": "Ampliar",
        "view_zoom_out": "Reduzir",
        "view_actual": "Tamanho real",
        "view_rot_left": "Girar a esquerda",
        "view_rot_right": "Girar a direita",
        "view_delete": "Excluir",
        "view_slideshow": "Apresentacao",
        "settings_set_default": "Definir como padrao",
        "settings_language": "Idioma",
        "settings_auto_detect": "Detectar idioma automaticamente",
        "settings_current": "Atual",
        "settings_auto_failed": "Falha na deteccao",
        "settings_auto_failed_msg": "Idioma do Windows nao detectado.",
        "help_about": "Sobre",
        "about_text": "Desenvolvido por Josesoft",
        "no_photo": "Nenhuma foto encontrada",
        "btn_prev_tip": "Anterior",
        "btn_next_tip": "Proximo",
        "btn_zoom_tip": "Ampliar",
        "btn_actual_tip": "Real (Esc)",
        "btn_rot_left_tip": "Esquerda",
        "btn_rot_right_tip": "Direita",
        "btn_delete_tip": "Excluir (Del)",
        "btn_slideshow_tip": "Apresentacao",
        "status_count": "{} / {}",
        "default_check_title": "Verificar",
        "default_success": "Sucesso! {} tipos vinculados",
        "default_fail": "Falha",
        "print_no_img": "Sem imagem!",
        "slideshow_title": "Apresentacao",
        "slideshow_interval_label": "Intervalo entre imagens:",
        "slideshow_fullscreen_label": "Mostrar em tela cheia",
        "slideshow_esc_hint": "ESC para parar",
        "slideshow_running": "Apresentacao {}s - ESC para parar",
        "slideshow_stop_tip": "Parar apresentacao",
        "theme_settings_title": "Configuracoes de tema",
        "theme_tab": "Tema",
        "lang_tab": "Idioma",
        "ext_tab": "Tipos de arquivo",
        "theme_auto_accent": "Usar cor de destaque do Windows auto (recomendado)",
        "theme_top_color": "Barra superior:",
        "theme_bottom_color": "Barra inferior:",
        "theme_bg_color": "Fundo:",
        "theme_font": "Fonte",
        "theme_font_label": "Fonte:",
        "theme_size_label": "Tamanho:",
        "theme_text_auto": "Detectar cor do texto auto (contraste)",

        "btn_ok": "OK",
        "btn_cancel": "Cancelar",
        "btn_close": "Fechar",
        "btn_select_all": "Selecionar tudo",
        "btn_select_none": "Desmarcar tudo",
        "theme_colors_group": "Cores",
        "theme_font_group": "Fonte",
        "lang_select_label": "Selecionar idioma:",
        "ext_select_label": "Tipos de arquivo padrão:",    },
    "pl": {
        "window_title": "Przegladarka zdjec",
        "menu_file": "Plik",
        "menu_view": "Widok",
        "menu_settings": "Ustawienia",
        "menu_help": "Pomoc",
        "file_open": "Otworz...",
        "file_open_folder": "Otworz folder...",
        "file_print": "Drukuj...",
        "file_email": "Wyslij e-mailem",
        "file_burn": "Nagraj na dysk",
        "file_open_location": "Otworz lokalizacje",
        "file_open_with": "Otworz za pomoca...",
        "file_exit": "Zakoncz",
        "view_prev": "Poprzedni",
        "view_next": "Nastepny",
        "view_zoom_in": "Powieksz",
        "view_zoom_out": "Pomniejsz",
        "view_actual": "Rzeczywisty rozmiar",
        "view_rot_left": "Obroc w lewo",
        "view_rot_right": "Obroc w prawo",
        "view_delete": "Usun",
        "view_slideshow": "Pokaz slajdow",
        "settings_set_default": "Ustaw jako domyslna",
        "settings_language": "Jezyk",
        "settings_auto_detect": "Wykryj jezyk automatycznie",
        "settings_current": "Biezacy",
        "settings_auto_failed": "Wykrywanie nie powiodlo sie",
        "settings_auto_failed_msg": "Nie wykryto jezyka Windows.",
        "help_about": "O programie",
        "about_text": "Zaprojektowane przez Josesoft",
        "no_photo": "Nie znaleziono zdjec",
        "btn_prev_tip": "Poprzedni",
        "btn_next_tip": "Nastepny",
        "btn_zoom_tip": "Powieksz",
        "btn_actual_tip": "Rzeczywisty (Esc)",
        "btn_rot_left_tip": "W lewo",
        "btn_rot_right_tip": "W prawo",
        "btn_delete_tip": "Usun (Del)",
        "btn_slideshow_tip": "Pokaz slajdow",
        "status_count": "{} / {}",
        "default_check_title": "Sprawdz",
        "default_success": "Sukces! Polaczono {} typow",
        "default_fail": "Niepowodzenie",
        "print_no_img": "Brak obrazu!",
        "slideshow_title": "Pokaz slajdow",
        "slideshow_interval_label": "Interwal miedzy obrazami:",
        "slideshow_fullscreen_label": "Pokaz na pelnym ekranie",
        "slideshow_esc_hint": "ESC aby zatrzymac",
        "slideshow_running": "Pokaz {}s - ESC aby zatrzymac",
        "slideshow_stop_tip": "Zatrzymaj pokaz",
        "theme_settings_title": "Ustawienia motywu",
        "theme_tab": "Motyw",
        "lang_tab": "Jezyk",
        "ext_tab": "Typy plikow",
        "theme_auto_accent": "Uzyj koloru akcentu Windows auto (zalecane)",
        "theme_top_color": "Gorny pasek:",
        "theme_bottom_color": "Dolny pasek:",
        "theme_bg_color": "Tlo:",
        "theme_font": "Czcionka",
        "theme_font_label": "Czcionka:",
        "theme_size_label": "Rozmiar:",
        "theme_text_auto": "Auto-wykrywanie koloru tekstu (kontrast)",

        "btn_ok": "OK",
        "btn_cancel": "Anuluj",
        "btn_close": "Zamknij",
        "btn_select_all": "Zaznacz wszystko",
        "btn_select_none": "Odznacz wszystko",
        "theme_colors_group": "Kolory",
        "theme_font_group": "Czcionka",
        "lang_select_label": "Wybierz język:",
        "ext_select_label": "Domyślne typy plików:",    },
}


def get_windows_accent_color():
    """Windows tema baslat/accent rengini al - Win7/10/11 uyumlu - coklu yontem"""
    from PyQt6.QtGui import QColor
    default = QColor(42, 111, 199)
    if sys.platform != "win32":
        return default
    try:
        import ctypes
        dwmapi = ctypes.windll.dwmapi
        color = ctypes.c_uint()
        opaque = ctypes.c_bool()
        hr = dwmapi.DwmGetColorizationColor(ctypes.byref(color), ctypes.byref(opaque))
        if hr == 0:
            val = color.value
            r = (val >> 16) & 0xFF
            g = (val >> 8) & 0xFF
            b = val & 0xFF
            if not (r==0 and g==0 and b==0):
                return QColor(r, g, b)
    except:
        pass
    if HAS_WINREG:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM") as key:
                try:
                    val, _ = winreg.QueryValueEx(key, "AccentColor")
                    r = val & 0xFF
                    g = (val >> 8) & 0xFF
                    b = (val >> 16) & 0xFF
                    if not (r==0 and g==0 and b==0):
                        return QColor(r, g, b)
                except:
                    pass
                try:
                    val, _ = winreg.QueryValueEx(key, "ColorizationColor")
                    r = (val >> 16) & 0xFF
                    g = (val >> 8) & 0xFF
                    b = val & 0xFF
                    if not (r==0 and g==0 and b==0):
                        return QColor(r, g, b)
                except:
                    pass
        except:
            pass
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent") as key:
                try:
                    val, _ = winreg.QueryValueEx(key, "AccentColorMenu")
                    r = val & 0xFF
                    g = (val >> 8) & 0xFF
                    b = (val >> 16) & 0xFF
                    if not (r==0 and g==0 and b==0):
                        return QColor(r, g, b)
                except:
                    pass
                try:
                    val, _ = winreg.QueryValueEx(key, "StartColorMenu")
                    r = val & 0xFF
                    g = (val >> 8) & 0xFF
                    b = (val >> 16) & 0xFF
                    if not (r==0 and g==0 and b==0):
                        return QColor(r, g, b)
                except:
                    pass
        except:
            pass
    return default

def get_windows_font_info():
    info = {"family": "Segoe UI", "size": 9}
    if sys.platform != "win32" or not HAS_WINREG:
        return info
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics") as key:
            try:
                val, _ = winreg.QueryValueEx(key, "MenuFont")
                import struct
                if len(val) >= 4:
                    height = struct.unpack_from("l", val, 0)[0]
                    size = int(abs(height) * 72 / 96)
                    if 6 <= size <= 20:
                        info["size"] = size
            except:
                pass
    except:
        pass
    return info


def get_settings_path():
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        settings_dir = os.path.join(base, "Win7PhotoViewer")
    else:
        settings_dir = os.path.join(os.path.expanduser("~"), ".win7photoviewer")
    os.makedirs(settings_dir, exist_ok=True)
    return os.path.join(settings_dir, "settings.json")

def load_json_settings():
    default = {
        "language": "tr",
        "theme": {
            "use_windows_accent": True,
            "top_color": "#2A6FC7",
            "bottom_color": "#2A6FC7",
            "background_color": "#E5E5E5",
            "font_family": "Segoe UI",
            "font_size": 9,
            "text_color_auto": True
        },
        "viewer": {
            "smart_zoom": True,
            "animation_reduced": True
        },
        "extensions": IMAGE_EXTS
    }
    path = get_settings_path()
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # merge with default
                for k, v in default.items():
                    if k not in data:
                        data[k] = v
                    elif isinstance(v, dict):
                        for kk, vv in v.items():
                            if kk not in data[k]:
                                data[k][kk] = vv
                return data
    except Exception as e:
        print(f"settings load fail {e}")
    return default

def save_json_settings(data):
    path = get_settings_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"settings save fail {e}")
        return False


APP_STYLESHEET = """
QMainWindow { background: #E5E5E5; }
QMenuBar {
    background-color: #F0F0F0;
    color: #000000;
    border-bottom: 1px solid #CCCCCC;
    padding: 2px;
}
QMenuBar::item {
    background: transparent;
    color: #000000;
    padding: 6px 12px;
    border: 1px solid transparent;
}
QMenuBar::item:selected {
    background-color: #0078D7;
    color: #FFFFFF;
}
QMenu {
    background-color: #FFFFFF;
    color: #000000;
    border: 1px solid #A0A0A0;
    padding: 4px;
}
QMenu::item {
    background: transparent;
    color: #000000;
    padding: 7px 30px 7px 32px;
    border: 1px solid transparent;
}
QMenu::item:selected {
    background-color: #0078D7;
    color: #FFFFFF;
}
QMenu::item:disabled { color: #8A8A8A; }
QMenu::separator { height: 1px; background: #D0D0D0; margin: 5px 8px; }

#OldBlueBar {
    /* Yarim kesilme fix - yeterli yukseklik ve padding */

    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A8DDE, stop:0.5 #2A6FC7, stop:1 #1A4FA0);
    border-top: 1px solid #5AA0E6;
}
#PillBar {
    /* Tam merkezde ve kesilmemesi icin */
    margin: 2px;

    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F8FBFF, stop:0.5 #E2F0FF, stop:1 #C8DFF6);
    border: 1px solid #8AB4E0;
    border-radius: 15px;
    padding: 3px;
}
QPushButton#PillBtn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    padding: 2px;
    min-width: 36px;
    min-height: 36px;
}
QPushButton#PillBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #A8D0F0);
    border: 1px solid transparent;
}
QPushButton#PillBtn:pressed {
    background: #8ABBE8;
    border: 1px solid transparent;
}
QPushButton#CenterBtn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 22px;
    padding: 0px;
    min-width: 42px;
    min-height: 42px;
}
QPushButton#CenterBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #A8D0F0);
    border: 1px solid transparent;
    border-radius: 22px;
}
QPushButton#CenterBtn:pressed {
    background: #8ABBE8;
    border: 1px solid transparent;
    border-radius: 22px;
}
QScrollArea { background: #E5E5E5; border: none; }
QLabel#ImageLabel { background: transparent; color: #666; }
"""

def detect_system_language():
    lang_code = None
    if sys.platform == "win32":
        try:
            import ctypes
            try:
                buf = ctypes.create_unicode_buffer(85)
                ctypes.windll.kernel32.GetUserDefaultLocaleName(buf, 85)
                locale_name = buf.value
                if locale_name:
                    lang_code = locale_name.split("-")[0].split("_")[0].lower()
                    if lang_code in LANGUAGES:
                        return lang_code
            except: pass
            try:
                lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
                lcid_map = {0x041F:"tr",0x001F:"tr",0x0409:"en",0x0009:"en",0x0407:"de",0x0007:"de",0x040C:"fr",0x000C:"fr",0x040A:"es",0x000A:"es",0x0C0A:"es",0x0410:"it",0x0010:"it",0x0416:"pt",0x0016:"pt",0x0816:"pt",0x0415:"pl",0x0015:"pl"}
                if lcid in lcid_map:
                    return lcid_map[lcid]
                primary = lcid & 0x3FF
                primary_map = {9:"en",7:"de",12:"fr",10:"es",16:"it",22:"pt",21:"pl",31:"tr"}
                if primary in primary_map:
                    return primary_map[primary]
            except: pass
        except: pass
    try:
        loc = locale.getdefaultlocale()[0]
        if loc:
            code = loc.split("_")[0].split("-")[0].lower()
            if code in LANGUAGES:
                return code
    except: pass
    try:
        for env in ["LANG","LANGUAGE","LC_ALL"]:
            val = os.environ.get(env,"")
            if val:
                code = val.split("_")[0].split("-")[0].split(".")[0].lower()
                if code in LANGUAGES:
                    return code
    except: pass
    return None

def get_exe_command():
    if getattr(sys, 'frozen', False):
        return f'"{sys.executable}" "%1"'
    else:
        return f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1"'

def is_default_viewer():
    if not HAS_WINREG or sys.platform != "win32":
        return False
    try:
        for ext in [".jpg",".png"]:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{ext}") as key:
                    val,_ = winreg.QueryValueEx(key,"")
                    if val != PROG_ID:
                        return False
            except FileNotFoundError:
                pass
        return True
    except:
        return False

def set_as_default_viewer(extensions=None):
    if not HAS_WINREG:
        return False, "winreg bulunamadi"
    if sys.platform != "win32":
        return False, "Sadece Windows"
    if extensions is None:
        try:
            js = load_json_settings()
            extensions = js.get("extensions", IMAGE_EXTS)
        except:
            extensions = IMAGE_EXTS
    try:
        cmd = get_exe_command()
        exe_icon = sys.executable if getattr(sys,'frozen',False) else sys.executable
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\Classes\{PROG_ID}") as key:
            winreg.SetValueEx(key,"",0,winreg.REG_SZ,"Windows Fotoğraf Görüntüleyicisi Resmi")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\Classes\{PROG_ID}\DefaultIcon") as key:
            winreg.SetValueEx(key,"",0,winreg.REG_SZ,f'"{exe_icon}",0')
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\Classes\{PROG_ID}\shell\open\command") as key:
            winreg.SetValueEx(key,"",0,winreg.REG_SZ,cmd)
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\Classes\{PROG_ID}\shell\open") as key:
            winreg.SetValueEx(key,"",0,winreg.REG_SZ,"Onizle")
        for ext in extensions:
            ext = ext.lower()
            if not ext.startswith("."):
                ext = "." + ext
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\Classes\{ext}") as key:
                winreg.SetValueEx(key,"",0,winreg.REG_SZ,PROG_ID)
        try:
            from ctypes import windll
            windll.shell32.SHChangeNotify(0x08000000,0,None,None)
        except: pass
        return True, f"{len(extensions)} dosya turu"
    except Exception as e:
        return False, str(e)

def scan_images_in_folder(folder_path):
    try:
        if not os.path.isdir(folder_path):
            return []
        files = []
        for f in os.listdir(folder_path):
            if f.lower().endswith(tuple(IMAGE_EXTS)):
                full = os.path.join(folder_path, f)
                if os.path.isfile(full):
                    files.append(full)
        files.sort(key=lambda x: os.path.basename(x).lower())
        return files
    except:
        return []

# === ICON YUKLEME ===
def find_icon_file(kind):
    names = {
        "zoom": ["icon_zoom.png","zoom.png"],
        "actual": ["icon_actual.png","actual.png"],
        "prev": ["icon_prev.png","prev.png"],
        "next": ["icon_next.png","next.png"],
        "center": ["icon_center.png","center.png","icon_slideshow.png"],
        "rot_left": ["icon_rotleft.png","rotleft.png","icon_rot_left.png"],
        "rot_right": ["icon_rotright.png","rotright.png","icon_rot_right.png"],
        "delete": ["icon_delete.png","delete.png","icon_x.png"],
    }
    search_dirs = [
        os.path.dirname(os.path.abspath(__file__)),
        os.getcwd(),
        "/mnt/data",
        "."
    ]
    for d in search_dirs:
        for fname in names.get(kind, []):
            p = os.path.join(d, fname)
            if os.path.exists(p):
                return p
    return None

def load_qicon(kind, fallback_size=32):
    path = find_icon_file(kind)
    if path and os.path.exists(path):
        return QIcon(path)
    pm = QPixmap(fallback_size, fallback_size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor("#1A3A5A"))
    pen.setWidth(2)
    p.setPen(pen)
    c = fallback_size//2
    if kind=="zoom":
        p.drawEllipse(4,4,fallback_size-14,fallback_size-14)
        p.drawLine(fallback_size-10,fallback_size-10,fallback_size-4,fallback_size-4)
    elif kind=="actual":
        p.drawRect(6,6,fallback_size-12,fallback_size-12)
    elif kind=="prev":
        p.drawLine(c+6,6,c-2,c); p.drawLine(c-2,c,c+6,fallback_size-6)
    elif kind=="next":
        p.drawLine(c-6,6,c+2,c); p.drawLine(c+2,c,c-6,fallback_size-6)
    elif kind=="center":
        p.drawRect(4,6,fallback_size-8,fallback_size-12)
    elif kind in ("rot_left","rot_right"):
        p.drawArc(4,4,fallback_size-8,fallback_size-8,0,270*16)
    elif kind=="delete":
        p.drawLine(8,8,fallback_size-8,fallback_size-8)
        p.drawLine(fallback_size-8,8,8,fallback_size-8)
    p.end()
    return QIcon(pm)


class ThemeSettingsDialog(QDialog):
    def __init__(self, parent, current_settings):
        super().__init__(parent)
        self.current_settings = current_settings
        self.setWindowTitle(self.parent().t("theme_settings_title") if self.parent() else "Tema Ayarları")
        self.setMinimumSize(520, 480)
        self.resize(580, 560)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # TAB 1 - TEMA
        theme_tab = QWidget()
        theme_layout = QVBoxLayout(theme_tab)

        # Windows accent checkbox
        self.chk_accent = QCheckBox("Windows tema rengini otomatik kullan (önerilen)")
        self.chk_accent.setChecked(self.current_settings["theme"].get("use_windows_accent", True))
        self.chk_accent.toggled.connect(self.on_accent_toggled)
        theme_layout.addWidget(self.chk_accent)

        # Renkler
        color_group = QGroupBox("Renkler - Colors")
        color_form = QFormLayout(color_group)

        self.btn_top_color = QPushButton()
        self.btn_top_color.setFixedSize(80, 28)
        self.top_color = QColor(self.current_settings["theme"].get("top_color", "#2A6FC7"))
        self.update_color_btn(self.btn_top_color, self.top_color)
        self.btn_top_color.clicked.connect(lambda: self.pick_color("top"))
        color_form.addRow("Üst çubuk - Top bar:", self.btn_top_color)

        self.btn_bottom_color = QPushButton()
        self.btn_bottom_color.setFixedSize(80, 28)
        self.bottom_color = QColor(self.current_settings["theme"].get("bottom_color", "#2A6FC7"))
        self.update_color_btn(self.btn_bottom_color, self.bottom_color)
        self.btn_bottom_color.clicked.connect(lambda: self.pick_color("bottom"))
        color_form.addRow("Alt çubuk - Bottom bar:", self.btn_bottom_color)

        self.btn_bg_color = QPushButton()
        self.btn_bg_color.setFixedSize(80, 28)
        self.bg_color = QColor(self.current_settings["theme"].get("background_color", "#E5E5E5"))
        self.update_color_btn(self.btn_bg_color, self.bg_color)
        self.btn_bg_color.clicked.connect(lambda: self.pick_color("bg"))
        color_form.addRow("Arka plan - Background:", self.btn_bg_color)

        theme_layout.addWidget(color_group)

        # Font
        font_group = QGroupBox("Yazı Tipi - Font")
        font_form = QFormLayout(font_group)

        self.combo_font = QFontComboBox()
        fam = self.current_settings["theme"].get("font_family", "Segoe UI")
        self.combo_font.setCurrentFont(QFont(fam))
        font_form.addRow("Font:", self.combo_font)

        self.spin_size = QSpinBox()
        self.spin_size.setRange(6, 24)
        self.spin_size.setValue(self.current_settings["theme"].get("font_size", 9))
        font_form.addRow("Boyut - Size:", self.spin_size)

        self.chk_text_auto = QCheckBox("Yazı rengini otomatik belirle (kontrasta göre)")
        self.chk_text_auto.setChecked(self.current_settings["theme"].get("text_color_auto", True))
        font_form.addRow(self.chk_text_auto)

        theme_layout.addWidget(font_group)
        theme_layout.addStretch()

        tabs.addTab(theme_tab, "Tema")

        # TAB 2 - DIL
        lang_tab = QWidget()
        lang_layout = QVBoxLayout(lang_tab)
        lang_layout.addWidget(QLabel("Dil seçin / Select language:"))
        self.list_lang = QListWidget()
        for code, name in LANGUAGES.items():
            item = QListWidgetItem(f"{name} ({code.upper()})")
            item.setData(Qt.ItemDataRole.UserRole, code)
            self.list_lang.addItem(item)
            if code == self.current_settings.get("language", "tr"):
                self.list_lang.setCurrentItem(item)
        lang_layout.addWidget(self.list_lang)
        tabs.addTab(lang_tab, "Dil / Language")

        # TAB 3 - DOSYA TURleri
        ext_tab = QWidget()
        ext_layout = QVBoxLayout(ext_tab)
        ext_layout.addWidget(QLabel("Varsayılan yapılacak dosya türleri:"))
        self.list_ext = QListWidget()
        self.list_ext.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        current_exts = set(self.current_settings.get("extensions", IMAGE_EXTS))
        for ext in sorted(IMAGE_EXTS):
            item = QListWidgetItem(ext)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if ext in current_exts else Qt.CheckState.Unchecked)
            self.list_ext.addItem(item)
        ext_layout.addWidget(self.list_ext)
        btn_all = QPushButton("Tümünü seç")
        btn_all.clicked.connect(self.select_all_ext)
        btn_none = QPushButton("Hiçbirini seçme")
        btn_none.clicked.connect(self.select_none_ext)
        h = QHBoxLayout()
        h.addWidget(btn_all)
        h.addWidget(btn_none)
        ext_layout.addLayout(h)
        tabs.addTab(ext_tab, "Dosya Türleri")

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        try:
            ok_btn = buttons.button(QDialogButtonBox.StandardButton.Ok)
            cancel_btn = buttons.button(QDialogButtonBox.StandardButton.Cancel)
            if ok_btn:
                ok_btn.setText(self.parent().t("btn_ok") if self.parent() else "Tamam")
            if cancel_btn:
                cancel_btn.setText(self.parent().t("btn_cancel") if self.parent() else "Iptal")
        except:
            pass
        layout.addWidget(buttons)

        self.on_accent_toggled(self.chk_accent.isChecked())

    def on_accent_toggled(self, checked):
        self.btn_top_color.setEnabled(not checked)
        self.btn_bottom_color.setEnabled(not checked)

    def update_color_btn(self, btn, color):
        btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #888; border-radius: 4px;")

    def pick_color(self, which):
        current = {"top": self.top_color, "bottom": self.bottom_color, "bg": self.bg_color}[which]
        col = QColorDialog.getColor(current, self, f"Renk seç - {which}")
        if col.isValid():
            if which == "top":
                self.top_color = col
                self.update_color_btn(self.btn_top_color, col)
            elif which == "bottom":
                self.bottom_color = col
                self.update_color_btn(self.btn_bottom_color, col)
            else:
                self.bg_color = col
                self.update_color_btn(self.btn_bg_color, col)

    def select_all_ext(self):
        for i in range(self.list_ext.count()):
            self.list_ext.item(i).setCheckState(Qt.CheckState.Checked)

    def select_none_ext(self):
        for i in range(self.list_ext.count()):
            self.list_ext.item(i).setCheckState(Qt.CheckState.Unchecked)

    def get_settings(self):
        new_settings = {
            "language": self.current_settings.get("language", "tr"),
            "theme": {
                "use_windows_accent": self.chk_accent.isChecked(),
                "top_color": self.top_color.name(),
                "bottom_color": self.bottom_color.name(),
                "background_color": self.bg_color.name(),
                "font_family": self.combo_font.currentFont().family(),
                "font_size": self.spin_size.value(),
                "text_color_auto": self.chk_text_auto.isChecked()
            },
            "viewer": self.current_settings.get("viewer", {"smart_zoom": True, "animation_reduced": True}),
            "extensions": []
        }
        # dil
        cur_item = self.list_lang.currentItem()
        if cur_item:
            new_settings["language"] = cur_item.data(Qt.ItemDataRole.UserRole)
        # ext
        exts = []
        for i in range(self.list_ext.count()):
            item = self.list_ext.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                exts.append(item.text())
        new_settings["extensions"] = exts if exts else IMAGE_EXTS
        return new_settings


class AnimatedToolButton(QPushButton):
    """Animasyonlu buton - eksenleri milimetrik ortali"""
    def __init__(self, kind, tooltip, is_center=False, is_nav_big=False):
        super().__init__()
        self.kind = kind
        self.is_center = is_center
        self.is_nav_big = is_nav_big
        self.setObjectName("CenterBtn" if is_center else "PillBtn")
        self.setToolTip(tooltip)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Boyut hiyerarsisi - %80 azaltildi, goz yormasin
        if is_center:
            base = 48
            hover = 50
            btn_size = 68
        elif is_nav_big:
            base = 30
            hover = 32
            btn_size = 46
        else:
            base = 30
            hover = 32
            btn_size = 46

        self._base = QSize(base, base)
        self._hover = QSize(hover, hover)
        self.setIcon(load_qicon(kind, base))
        self.setIconSize(self._base)
        self.setFixedSize(btn_size, btn_size)
        # Eksenleri tam ortala
        self.setStyleSheet(self.styleSheet() + " QPushButton { qproperty-iconSize: %dpx %dpx; }" % (base, base))
        
        self.anim_in = QPropertyAnimation(self, b"iconSize")
        self.anim_in.setDuration(120)
        self.anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_in.setStartValue(self._base)
        self.anim_in.setEndValue(self._hover)
        
        self.anim_out = QPropertyAnimation(self, b"iconSize")
        self.anim_out.setDuration(150)
        self.anim_out.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_out.setStartValue(self._hover)
        self.anim_out.setEndValue(self._base)
    
    def enterEvent(self, e):
        self.anim_out.stop()
        self.anim_in.start()
        super().enterEvent(e)
    
    def leaveEvent(self, e):
        self.anim_in.stop()
        self.anim_out.start()
        super().leaveEvent(e)

class Win7Viewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_settings = load_json_settings()
        self.qsettings = QSettings("Win7PhotoViewer","PhotoViewerV6")
        self.detected_lang = detect_system_language()
        # JSON oncelikli, sonra QSettings
        saved_lang = self.json_settings.get("language") or self.qsettings.value("language",None)
        if saved_lang and saved_lang in LANGUAGES:
            self.current_lang = saved_lang
        elif self.detected_lang and self.detected_lang in LANGUAGES:
            self.current_lang = self.detected_lang
        else:
            self.current_lang = "en"
        self.auto_detect_failed = self.detected_lang is None
        self.files=[]; self.index=0; self.zoom=1.0; self.angle=0; self.orig_pixmap=None; self.current_path=None
        self.set_program_icon()
        self.setGeometry(200,100,1020,720)
        self.setMinimumSize(800,600)
        self.setAcceptDrops(True)
        self.init_ui()
        self.retranslate_ui()
        self.load_initial_images()
    
    def set_program_icon(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        possible=[
            "app_icon.ico",
            "icon.ico",
            "app_icon.png",
            "icon.png",
            os.path.join(base_dir, "app_icon.ico"),
            os.path.join(base_dir, "icon.ico"),
            os.path.join(base_dir, "app_icon.png"),
            os.path.join(base_dir, "icon.png"),
            os.path.join(os.getcwd(), "app_icon.ico"),
            os.path.join(os.getcwd(), "icon.ico"),
            "/mnt/data/app_icon.ico",
            "/mnt/data/icon.ico",
            "/mnt/data/app_icon.png",
            "/mnt/data/icon.png",
        ]
        for p in possible:
            if os.path.exists(p):
                self.setWindowIcon(QIcon(p))
                try:
                    from PyQt6.QtWidgets import QApplication
                    QApplication.instance().setWindowIcon(QIcon(p))
                except:
                    pass
                return
    
    def t(self,key):
        return TRANSLATIONS.get(self.current_lang,TRANSLATIONS["en"]).get(key,TRANSLATIONS["en"].get(key,key))
    
    def init_ui(self):
        central=QWidget()
        self.setCentralWidget(central)
        main_layout=QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        self.scroll=QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label=QLabel()
        self.img_label.setObjectName("ImageLabel")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll.setWidget(self.img_label)
        main_layout.addWidget(self.scroll,1)
        self.bottom_bar=QFrame()
        self.bottom_bar.setObjectName("OldBlueBar")
        self.bottom_bar.setFixedHeight(90)  # Kesilme fix icin yukseklik artirildi
        bottom_layout=QHBoxLayout(self.bottom_bar)
        bottom_layout.setContentsMargins(0,0,0,0)
        bottom_layout.setSpacing(0)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pill_bar=QFrame()
        self.pill_bar.setObjectName("PillBar")
        # Tam merkezde ve eksenleri duzgun
        self.pill_bar.setFixedHeight(62)
        pill_layout=QHBoxLayout(self.pill_bar)
        pill_layout.setContentsMargins(14, 6, 14, 6)
        pill_layout.setSpacing(8)
        pill_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_zoom=AnimatedToolButton("zoom",self.t("btn_zoom_tip"))
        self.btn_actual=AnimatedToolButton("actual",self.t("btn_actual_tip"))
        self.btn_prev=AnimatedToolButton("prev",self.t("btn_prev_tip"), is_nav_big=True)
        self.btn_center=AnimatedToolButton("center",self.t("btn_slideshow_tip"), is_center=True)
        self.btn_next=AnimatedToolButton("next",self.t("btn_next_tip"), is_nav_big=True)
        self.btn_rot_left=AnimatedToolButton("rot_left",self.t("btn_rot_left_tip"))
        self.btn_rot_right=AnimatedToolButton("rot_right",self.t("btn_rot_right_tip"))
        self.btn_zoom.clicked.connect(self.toggle_zoom)
        self.btn_actual.clicked.connect(self.actual)
        self.btn_prev.clicked.connect(self.prev_img)
        self.btn_next.clicked.connect(self.next_img)
        self.btn_center.clicked.connect(self.start_slideshow_dialog)
        self.btn_rot_left.clicked.connect(self.rot_left)
        self.btn_rot_right.clicked.connect(self.rot_right)
        def make_sep():
            sep=QFrame(); sep.setFrameShape(QFrame.Shape.VLine); sep.setFixedWidth(1); sep.setStyleSheet("background:#8AB4E0;margin:6px 4px;"); return sep
        pill_layout.addWidget(self.btn_zoom)
        pill_layout.addWidget(self.btn_actual)
        pill_layout.addWidget(make_sep())
        pill_layout.addWidget(self.btn_prev)
        pill_layout.addWidget(self.btn_center)
        pill_layout.addWidget(self.btn_next)
        pill_layout.addWidget(make_sep())
        pill_layout.addWidget(self.btn_rot_left)
        pill_layout.addWidget(self.btn_rot_right)
        # Tam merkez - stretchler esit
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.pill_bar, 0, Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addStretch(1)
        main_layout.addWidget(self.bottom_bar)
        self.menubar=self.menuBar()
        self.file_menu=self.menubar.addMenu("Dosya")
        self.view_menu=self.menubar.addMenu("Görünüm")
        self.settings_menu=self.menubar.addMenu("Ayarlar")
        self.help_menu=self.menubar.addMenu("Yardım")
        self.act_open=QAction("Aç...",self); self.act_open.setShortcut("Ctrl+O"); self.act_open.triggered.connect(self.open_file)
        self.act_open_folder=QAction("Klasör aç...",self); self.act_open_folder.setShortcut("Ctrl+Shift+O"); self.act_open_folder.triggered.connect(self.open_folder)
        self.act_print=QAction("Yazdır...",self); self.act_print.triggered.connect(self.print_image)
        self.act_email=QAction("E-posta",self); self.act_email.triggered.connect(self.email_image)
        self.act_burn=QAction("Diske yaz",self); self.act_burn.triggered.connect(self.burn_image)
        self.act_open_loc=QAction("Dosya konumunu aç",self); self.act_open_loc.triggered.connect(self.open_location)
        self.act_open_default=QAction("Birlikte aç...",self); self.act_open_default.triggered.connect(self.open_default)
        self.act_exit=QAction("Çıkış",self); self.act_exit.triggered.connect(self.close)
        self.file_menu.addAction(self.act_open); self.file_menu.addAction(self.act_open_folder); self.file_menu.addSeparator()
        self.file_menu.addAction(self.act_print); self.file_menu.addAction(self.act_email); self.file_menu.addAction(self.act_burn); self.file_menu.addSeparator()
        self.file_menu.addAction(self.act_open_loc); self.file_menu.addAction(self.act_open_default); self.file_menu.addSeparator(); self.file_menu.addAction(self.act_exit)
        self.act_prev=QAction("Önceki",self); self.act_prev.triggered.connect(self.prev_img)
        self.act_next=QAction("Sonraki",self); self.act_next.triggered.connect(self.next_img)
        self.act_zoom_in=QAction("Yakınlaştır",self); self.act_zoom_in.triggered.connect(self.zoom_in)
        self.act_zoom_out=QAction("Uzaklaştır",self); self.act_zoom_out.triggered.connect(self.zoom_out)
        self.act_actual=QAction("Gerçek boyut",self); self.act_actual.triggered.connect(self.actual)
        self.act_rot_left=QAction("Sola döndür",self); self.act_rot_left.triggered.connect(self.rot_left)
        self.act_rot_right=QAction("Sağa döndür",self); self.act_rot_right.triggered.connect(self.rot_right)
        self.act_delete=QAction("Sil",self); self.act_delete.triggered.connect(self.delete_img)
        self.view_menu.addAction(self.act_prev); self.view_menu.addAction(self.act_next); self.view_menu.addSeparator()
        self.view_menu.addAction(self.act_zoom_in); self.view_menu.addAction(self.act_zoom_out); self.view_menu.addAction(self.act_actual); self.view_menu.addSeparator()
        self.view_menu.addAction(self.act_rot_left); self.view_menu.addAction(self.act_rot_right); self.view_menu.addSeparator(); self.view_menu.addAction(self.act_delete)
        self.act_set_default=QAction("Varsayılan yap",self); self.act_set_default.triggered.connect(self.action_set_default)
        self.act_auto_detect=QAction("Otomatik dil algıla",self); self.act_auto_detect.triggered.connect(self.action_auto_detect_lang)
        self.act_theme = QAction("Tema Ayarları...",self); self.act_theme.triggered.connect(self.open_theme_settings)
        self.settings_menu.addAction(self.act_set_default); self.settings_menu.addAction(self.act_theme); self.settings_menu.addSeparator(); self.settings_menu.addAction(self.act_auto_detect)
        self.lang_menu=self.settings_menu.addMenu("Dil / Language")
        self.lang_actions={}
        for code,native in LANGUAGES.items():
            act=QAction(f"{native} ({code.upper()})",self); act.setCheckable(True); act.setData(code); act.triggered.connect(lambda checked,c=code: self.change_language(c)); self.lang_menu.addAction(act); self.lang_actions[code]=act
        if self.auto_detect_failed:
            self.settings_menu.addSeparator()
            self.act_auto_failed=QAction(f"⚠ {self.t('settings_auto_failed')}",self); self.act_auto_failed.setEnabled(False); self.settings_menu.addAction(self.act_auto_failed)
        self.act_about=QAction("Hakkında",self); self.act_about.triggered.connect(self.show_about); self.help_menu.addAction(self.act_about)
        self._last_accent = None
        self.apply_accent_color()
        self.scroll.viewport().installEventFilter(self)
        self.accent_timer=QTimer(self)
        self.accent_timer.timeout.connect(self.check_accent_change)
        self.accent_timer.start(2000)
        # Slideshow
        self.slideshow_timer=QTimer(self)
        self.is_slideshow=False
        self.slideshow_interval=3
        # Panning
        self._panning=False
        self._pan_start=None
        self._h_start=0
        self._v_start=0

    def apply_accent_color(self):
        try:
            # JSON ayarlarindan oku
            theme_set = self.json_settings.get("theme", {})
            use_accent = theme_set.get("use_windows_accent", True)
            if use_accent:
                accent=get_windows_accent_color()
            else:
                # custom renk
                custom = theme_set.get("bottom_color", "#2A6FC7")
                from PyQt6.QtGui import QColor as QC
                accent=QC(custom)
            self._last_accent=accent
            light=accent.lighter(135)
            dark=accent.darker(125)
            border=accent.lighter(150)
            light2=accent.lighter(160)
            lum = (0.299*accent.red() + 0.587*accent.green() + 0.114*accent.blue())/255
            text_color = "#FFFFFF" if lum < 0.5 else "#000000"
            font_info=get_windows_font_info()
            # JSON font override
            if "font_family" in theme_set:
                font_info["family"]=theme_set.get("font_family", font_info["family"])
            if "font_size" in theme_set:
                font_info["size"]=theme_set.get("font_size", font_info["size"])
            try:
                from PyQt6.QtWidgets import QApplication
                app_font = QApplication.font()
                # eger json'da windows accent kapali degilse sistem fontunu kullan ama boyut json'dan gelsin
                if use_accent:
                    sys_size = app_font.pointSize()
                    if sys_size>0 and theme_set.get("font_family","")==app_font.family():
                        # sadece family ayni ise size sistemden al
                        pass
            except:
                pass
            # arka plan rengi
            bg_color = theme_set.get("background_color", "#E5E5E5")
            try:
                self.scroll.setStyleSheet(f"QScrollArea {{ background: {bg_color}; border: none; }}")
            except:
                pass
            # top color custom ise
            if not use_accent:
                top_custom = theme_set.get("top_color", theme_set.get("bottom_color", "#2A6FC7"))
                from PyQt6.QtGui import QColor as QC2
                top_accent = QC2(top_custom)
                light_top = top_accent.lighter(160)
                dark_top = top_accent.darker(125)
                bottom_style = "#OldBlueBar { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 " + light.name() + ", stop:0.5 " + accent.name() + ", stop:1 " + dark.name() + "); border-top: 1px solid " + border.name() + "; }"
                menubar_style = "QMenuBar { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 " + light_top.name() + ", stop:1 " + top_accent.name() + "); color: " + text_color + "; border-bottom: 1px solid " + dark_top.name() + "; font-family: \"" + font_info["family"] + "\"; font-size: " + str(font_info["size"]) + "pt; } QMenuBar::item { background: transparent; color: " + text_color + "; font-family: \"" + font_info["family"] + "\"; font-size: " + str(font_info["size"]) + "pt; } QMenuBar::item:selected { background-color: " + light.name() + "; color: " + text_color + "; }"
            else:
                bottom_style = "#OldBlueBar { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 " + light.name() + ", stop:0.5 " + accent.name() + ", stop:1 " + dark.name() + "); border-top: 1px solid " + border.name() + "; }"
                menubar_style = "QMenuBar { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 " + light2.name() + ", stop:1 " + accent.name() + "); color: " + text_color + "; border-bottom: 1px solid " + dark.name() + "; font-family: \"" + font_info["family"] + "\"; font-size: " + str(font_info["size"]) + "pt; } QMenuBar::item { background: transparent; color: " + text_color + "; font-family: \"" + font_info["family"] + "\"; font-size: " + str(font_info["size"]) + "pt; } QMenuBar::item:selected { background-color: " + light.name() + "; color: " + text_color + "; }"
            self.bottom_bar.setStyleSheet(bottom_style)
            self.bottom_bar.style().unpolish(self.bottom_bar)
            self.bottom_bar.style().polish(self.bottom_bar)
            self.menubar.setStyleSheet(menubar_style)
            self.menubar.style().unpolish(self.menubar)
            self.menubar.style().polish(self.menubar)
            try:
                from PyQt6.QtGui import QFont
                f = QFont(font_info["family"], font_info["size"])
                self.menubar.setFont(f)
                for menu in [self.file_menu, self.view_menu, self.settings_menu, self.help_menu]:
                    menu.setFont(f)
            except:
                pass
        except Exception as e:
            print(f"accent apply fail {e}")
            import traceback
            traceback.print_exc()


    def check_accent_change(self):
        try:
            cur=get_windows_accent_color()
            if self._last_accent is None or cur.name()!=self._last_accent.name():
                self.apply_accent_color()
        except:
            pass

    def eventFilter(self, obj, event):
        vp = self.scroll.viewport()
        if obj==vp:
            if event.type()==QEvent.Type.Wheel:
                self.handle_wheel_zoom(event)
                return True
            elif event.type()==QEvent.Type.MouseButtonPress:
                # Orta tus veya zoomluyken sol tus ile surukle
                if event.button()==Qt.MouseButton.MiddleButton or (event.button()==Qt.MouseButton.LeftButton and self.zoom!=1.0):
                    self._panning=True
                    self._pan_start=event.pos()
                    self._h_start=self.scroll.horizontalScrollBar().value()
                    self._v_start=self.scroll.verticalScrollBar().value()
                    vp.setCursor(Qt.CursorShape.ClosedHandCursor)
                    return True
            elif event.type()==QEvent.Type.MouseMove:
                if self._panning:
                    delta=event.pos() - self._pan_start
                    self.scroll.horizontalScrollBar().setValue(self._h_start - delta.x())
                    self.scroll.verticalScrollBar().setValue(self._v_start - delta.y())
                    return True
            elif event.type()==QEvent.Type.MouseButtonRelease:
                if self._panning and event.button() in (Qt.MouseButton.MiddleButton, Qt.MouseButton.LeftButton):
                    self._panning=False
                    vp.setCursor(Qt.CursorShape.ArrowCursor)
                    return True
        return super().eventFilter(obj, event)

    def handle_wheel_zoom(self, event):
        if not self.orig_pixmap:
            return
        delta=event.angleDelta().y()
        if delta==0:
            return
        mp=self.get_megapixels()
        if mp>8: step=1.08
        elif mp>4: step=1.12
        elif mp>1: step=1.18
        else: step=1.22
        notches=delta/120.0
        factor=math.pow(step, abs(notches))
        fit=self.get_fit_scale()
        if fit==0: fit=1.0
        if notches>0:
            self.zoom=factor if self.zoom==1.0 else self.zoom*factor
        else:
            self.zoom=(1.0/factor) if self.zoom==1.0 else self.zoom/factor
        max_abs=12.0 if mp<1 else 8.0 if mp<4 else 5.0
        min_abs=0.05
        max_rel=max_abs/fit if fit!=0 else max_abs
        min_rel=min_abs/fit if fit!=0 else 0.05
        self.zoom=max(min_rel, min(self.zoom, max_rel))
        if abs(self.zoom-1.0)<0.10:
            self.zoom=1.0
        self.render()

    def wheelEvent(self, event):
        if self.orig_pixmap and self.scroll.underMouse():
            self.handle_wheel_zoom(event)
            event.accept()
        else:
            super().wheelEvent(event)

    def start_slideshow_dialog(self):
        if not self.files:
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(self.t('slideshow_title'))
        dlg.setMinimumWidth(340)
        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel(self.t('slideshow_interval_label')))
        spin = QSpinBox()
        spin.setRange(1, 60)
        last_interval = self.json_settings.get("slideshow", {}).get("interval", 3)
        spin.setValue(last_interval)
        spin.setSuffix(" sn" if self.current_lang=="tr" else " s")
        lay.addWidget(spin)
        chk_full = QCheckBox(self.t('slideshow_fullscreen_label'))
        chk_full.setChecked(True)
        lay.addWidget(chk_full)
        lay.addWidget(QLabel(self.t('slideshow_esc_hint')))
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        try:
            ok_btn = btns.button(QDialogButtonBox.StandardButton.Ok)
            cancel_btn = btns.button(QDialogButtonBox.StandardButton.Cancel)
            if ok_btn:
                ok_btn.setText(self.t("btn_ok"))
            if cancel_btn:
                cancel_btn.setText(self.t("btn_cancel"))
        except:
            pass
        lay.addWidget(btns)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            interval = spin.value()
            if "slideshow" not in self.json_settings:
                self.json_settings["slideshow"] = {}
            self.json_settings["slideshow"]["interval"] = interval
            save_json_settings(self.json_settings)
            self.start_slideshow(interval, fullscreen=chk_full.isChecked())

    def start_slideshow(self, interval_sec=3, fullscreen=False):
        if self.is_slideshow:
            self.stop_slideshow()
            return
        self.is_slideshow=True
        self.slideshow_interval=interval_sec
        try:
            self.slideshow_timer.timeout.disconnect()
        except:
            pass
        self.slideshow_timer.timeout.connect(self.next_img)
        self.slideshow_timer.start(interval_sec*1000)
        self.btn_center.setToolTip(self.t('slideshow_stop_tip') + f" ({interval_sec}sn)")
        # Tam ekran - gercek tam ekran, butun masaustunu kaplar
        if fullscreen:
            # Menubar ve alt bari gizle, arka plani siyah yap
            self._pre_fullscreen_bg = self.scroll.styleSheet()
            self.menubar.hide()
            self.bottom_bar.hide()
            self.scroll.setStyleSheet("QScrollArea { background: black; border: none; }")
            self.showFullScreen()
        self.setWindowTitle(self.t('slideshow_running').format(interval_sec))

    def stop_slideshow(self):
        if self.slideshow_timer.isActive():
            self.slideshow_timer.stop()
        try:
            self.slideshow_timer.timeout.disconnect()
        except:
            pass
        self.is_slideshow=False
        self.btn_center.setToolTip(self.t('btn_slideshow_tip'))
        # Tam ekrandan cik ve UI'i geri getir
        if self.isFullScreen():
            self.showNormal()
        # UI'i geri goster
        self.menubar.show()
        self.bottom_bar.show()
        # Arka plani geri al
        try:
            if hasattr(self, '_pre_fullscreen_bg'):
                self.scroll.setStyleSheet(self._pre_fullscreen_bg)
            else:
                bg = self.json_settings.get("theme", {}).get("background_color", "#E5E5E5")
                self.scroll.setStyleSheet(f"QScrollArea {{ background: {bg}; border: none; }}")
        except:
            pass
        if self.current_path:
            base=os.path.basename(self.current_path)
            self.setWindowTitle(f"{base} - {self.t('window_title')} ({self.index+1}/{len(self.files)})")
        else:
            self.setWindowTitle(self.t('window_title'))


    
    def retranslate_ui(self):
        if self.current_path:
            base=os.path.basename(self.current_path)
            self.setWindowTitle(f"{base} - {self.t('window_title')} ({self.index+1}/{len(self.files)})")
        else:
            self.setWindowTitle(self.t('window_title'))
        self.file_menu.setTitle(self.t('menu_file')); self.view_menu.setTitle(self.t('menu_view')); self.settings_menu.setTitle(self.t('menu_settings')); self.help_menu.setTitle(self.t('menu_help'))
        self.act_open.setText(self.t('file_open')); self.act_open_folder.setText(self.t('file_open_folder')); self.act_print.setText(self.t('file_print')); self.act_email.setText(self.t('file_email')); self.act_burn.setText(self.t('file_burn'))
        self.act_open_loc.setText(self.t('file_open_location')); self.act_open_default.setText(self.t('file_open_with')); self.act_exit.setText(self.t('file_exit'))
        self.act_prev.setText(self.t('view_prev')); self.act_next.setText(self.t('view_next')); self.act_zoom_in.setText(self.t('view_zoom_in')); self.act_zoom_out.setText(self.t('view_zoom_out'))
        self.act_actual.setText(self.t('view_actual')); self.act_rot_left.setText(self.t('view_rot_left')); self.act_rot_right.setText(self.t('view_rot_right')); self.act_delete.setText(self.t('view_delete'))
        self.act_set_default.setText(self.t('settings_set_default')); self.act_theme.setText('Tema Ayarları...' if self.current_lang=='tr' else 'Theme Settings...'); self.act_auto_detect.setText(self.t('settings_auto_detect')); self.lang_menu.setTitle(self.t('settings_language')); self.act_about.setText(self.t('help_about'))
        for code,act in self.lang_actions.items(): act.setChecked(code==self.current_lang)
        self.btn_prev.setToolTip(self.t('btn_prev_tip')); self.btn_next.setToolTip(self.t('btn_next_tip')); self.btn_zoom.setToolTip(self.t('btn_zoom_tip')); self.btn_actual.setToolTip(self.t('btn_actual_tip'))
        self.btn_rot_left.setToolTip(self.t('btn_rot_left_tip')); self.btn_rot_right.setToolTip(self.t('btn_rot_right_tip')); self.btn_center.setToolTip(self.t('btn_slideshow_tip'))
        if not self.orig_pixmap and not self.files:
            self.img_label.setText(self.t('no_photo'))
    
    def change_language(self,lang_code):
        if lang_code not in LANGUAGES: return
        self.current_lang=lang_code
        self.qsettings.setValue("language",lang_code)
        self.json_settings["language"]=lang_code
        save_json_settings(self.json_settings)
        self.retranslate_ui()

    def open_theme_settings(self):
        dlg = ThemeSettingsDialog(self, self.json_settings)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_set = dlg.get_settings()
            self.json_settings = new_set
            save_json_settings(self.json_settings)
            self.current_lang = new_set.get("language", self.current_lang)
            self.qsettings.setValue("language", self.current_lang)
            self.retranslate_ui()
            self.apply_accent_color()
            QMessageBox.information(self, "Ayarlar", f"Ayarlar kaydedildi!\nSettings saved to:\n{get_settings_path()}")
    def action_auto_detect_lang(self):
        detected=detect_system_language()
        if detected and detected in LANGUAGES:
            self.change_language(detected)
            QMessageBox.information(self,self.t('settings_current'),f"{self.t('settings_current')}: {LANGUAGES[detected]}")
        else:
            QMessageBox.warning(self,self.t('settings_auto_failed'),self.t('settings_auto_failed_msg'))
    def action_set_default(self):
        ok,msg=set_as_default_viewer()
        if ok:
            QMessageBox.information(self,self.t('default_check_title'),self.t('default_success').format(len(IMAGE_EXTS)))
        else:
            QMessageBox.warning(self,self.t('default_fail'),msg)
    def show_about(self):
        QMessageBox.about(self,self.t('help_about'),f"{self.t('about_text')}\n{LANGUAGES[self.current_lang]}")
    def load_initial_images(self):
        args=sys.argv[1:]
        if args:
            first=args[0]
            if os.path.isdir(first):
                files=scan_images_in_folder(first)
                if files:
                    self.files=files; self.index=0; self.show_img(files[0]); return
            elif os.path.isfile(first) and first.lower().endswith(tuple(IMAGE_EXTS)):
                folder=os.path.dirname(os.path.abspath(first))
                files=scan_images_in_folder(folder)
                if files:
                    try:
                        idx=[os.path.abspath(f) for f in files].index(os.path.abspath(first))
                    except: idx=0
                    self.files=files; self.index=idx; self.show_img(files[idx]); return
        try:
            cwd=os.getcwd()
            files=scan_images_in_folder(cwd)
            if files:
                self.files=files; self.index=0; self.show_img(files[0]); return
            exe_dir=os.path.dirname(os.path.abspath(sys.argv[0]))
            if exe_dir!=cwd:
                files=scan_images_in_folder(exe_dir)
                if files:
                    self.files=files; self.index=0; self.show_img(files[0]); return
        except: pass
        self.img_label.setText(self.t('no_photo'))
    def show_img(self,path):
        pix=QPixmap(path)
        if pix.isNull(): return
        self.orig_pixmap=pix; self.current_path=path; self.zoom=1.0; self.angle=0; self.render()
        base=os.path.basename(path)
        self.setWindowTitle(f"{base} - {self.t('window_title')} ({self.index+1}/{len(self.files)})")
    def get_fit_scale(self):
        if not self.orig_pixmap:
            return 1.0
        vw=self.scroll.viewport().width()-30
        vh=self.scroll.viewport().height()-30
        if vw<50: vw=800
        if vh<50: vh=550
        pix = self.orig_pixmap
        if self.angle!=0:
            tr=QTransform(); tr.rotate(self.angle)
            pix=pix.transformed(tr,Qt.TransformationMode.SmoothTransformation)
        if pix.width()==0 or pix.height()==0:
            return 1.0
        fit = min(vw/pix.width(), vh/pix.height())
        if fit>1.0:
            fit=1.0
        return fit

    def get_megapixels(self):
        if not self.orig_pixmap:
            return 0
        return self.orig_pixmap.width()*self.orig_pixmap.height()/1e6

    def render(self):
        if not self.orig_pixmap:
            return
        pix=self.orig_pixmap
        if self.angle!=0:
            tr=QTransform(); tr.rotate(self.angle); pix=pix.transformed(tr,Qt.TransformationMode.SmoothTransformation)
        vw=self.scroll.viewport().width()-30
        vh=self.scroll.viewport().height()-30
        if vw<50: vw=800
        if vh<50: vh=550
        fit_scale = min(vw/pix.width(), vh/pix.height()) if pix.width() and pix.height() else 1.0
        if fit_scale>1.0:
            fit_scale=1.0
        self._last_fit_scale = fit_scale
        if self.zoom==1.0:
            final_scale = fit_scale
        else:
            final_scale = fit_scale * self.zoom
        mp = self.get_megapixels()
        max_abs = 12.0 if mp<1 else 8.0 if mp<4 else 5.0
        min_abs = 0.05
        final_scale = max(min_abs, min(final_scale, max_abs))
        w=int(pix.width()*final_scale)
        h=int(pix.height()*final_scale)
        if w>0 and h>0:
            if abs(final_scale-1.0)>0.001 or fit_scale<1.0 or self.zoom!=1.0:
                pix=pix.scaled(w,h,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.img_label.setPixmap(pix)
        self.img_label.setText("")
    def print_image(self):
        if not self.orig_pixmap or not self.current_path:
            QMessageBox.warning(self,self.t('file_print'),self.t('print_no_img')); return
        printer=QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog=QPrintDialog(printer,self)
        dialog.setWindowTitle(self.t('file_print'))
        if dialog.exec()==QPrintDialog.DialogCode.Accepted:
            painter=QPainter(); painter.begin(printer)
            rect=painter.viewport(); size=self.orig_pixmap.size()
            size.scale(rect.size(),Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(),rect.y(),size.width(),size.height())
            painter.setWindow(self.orig_pixmap.rect())
            painter.drawPixmap(0,0,self.orig_pixmap)
            painter.end()
    def email_image(self):
        """E-posta ile gönder - Outlook'a baglan ve acik resmi ekle"""
        if not self.current_path:
            QMessageBox.information(self, self.t('file_email'), self.t('print_no_img'))
            return
        img_path = os.path.abspath(self.current_path)
        if not os.path.exists(img_path):
            QMessageBox.warning(self, self.t('file_email'), f"Dosya bulunamadi:\n{img_path}")
            return
        try:
            import win32com.client
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.Subject = os.path.basename(img_path)
            mail.Body = f"{os.path.basename(img_path)} - Windows Fotoğraf Görüntüleyicisi ile gonderildi.\n\n"
            mail.Attachments.Add(img_path)
            mail.Display(True)
            return
        except Exception as e:
            print(f"Outlook COM denemesi basarisiz: {e}")
        try:
            if sys.platform == "win32":
                import subprocess
                outlook_paths = [
                    r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
                ]
                try:
                    import winreg
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\OUTLOOK.EXE") as k:
                        reg_path = winreg.QueryValue(k, None)
                        if reg_path:
                            outlook_paths.insert(0, reg_path)
                except:
                    pass
                outlook_exe = None
                for p in outlook_paths:
                    if os.path.exists(p):
                        outlook_exe = p
                        break
                if outlook_exe:
                    subprocess.Popen([outlook_exe, "/a", img_path])
                    return
                else:
                    try:
                        subprocess.Popen(["outlook", "/a", img_path])
                        return
                    except:
                        pass
        except Exception as e:
            print(f"Outlook.exe /a denemesi basarisiz: {e}")
        try:
            import urllib.parse
            subject = urllib.parse.quote(f"Fotograf: {os.path.basename(img_path)}")
            body = urllib.parse.quote(f"Fotograf ektedir: {img_path}\n\nWindows Fotoğraf Görüntüleyicisi ile gonderildi.")
            mailto = f"mailto:?subject={subject}&body={body}"
            QDesktopServices.openUrl(QUrl(mailto))
            QTimer.singleShot(1000, lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(img_path))))
            QMessageBox.information(self, self.t('file_email'), f"Outlook bulunamadi.\nVarsayılan e-posta uygulamasi acildi.\n\nDosya:\n{img_path}\n\nLutfen dosyayi maile surukleyip ekleyin.")
        except Exception as e:
            QMessageBox.warning(self, self.t('file_email'), f"E-posta gonderilemedi:\n{e}\n\nDosya:\n{img_path}")
    def burn_image(self):
        if not self.current_path: return
        try:
            if sys.platform=="win32":
                burn_folder=os.path.join(os.environ.get('LOCALAPPDATA',''),r'Microsoft\Windows\Burn\Burn')
                os.makedirs(burn_folder,exist_ok=True)
                import shutil
                dest=os.path.join(burn_folder,os.path.basename(self.current_path))
                shutil.copy2(self.current_path,dest)
                QDesktopServices.openUrl(QUrl.fromLocalFile(burn_folder))
        except Exception as e:
            QMessageBox.warning(self,self.t('file_burn'),f"{e}")
    def open_location(self):
        if self.current_path: QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(self.current_path)))
    def open_default(self):
        if self.current_path: QDesktopServices.openUrl(QUrl.fromLocalFile(self.current_path))
    def open_file(self):
        path,_=QFileDialog.getOpenFileName(self,self.t('file_open'),"","Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff)")
        if not path: return
        folder=os.path.dirname(path)
        files=scan_images_in_folder(folder)
        if not files: files=[path]
        self.files=files
        try: self.index=[os.path.abspath(f) for f in files].index(os.path.abspath(path))
        except: self.index=0
        self.show_img(self.files[self.index])
    def open_folder(self):
        folder=QFileDialog.getExistingDirectory(self,self.t('file_open_folder'),os.getcwd())
        if not folder: return
        files=scan_images_in_folder(folder)
        if not files:
            QMessageBox.information(self,self.t('file_open_folder'),self.t('no_photo')); return
        self.files=files; self.index=0; self.show_img(files[0])
    def prev_img(self):
        if not self.files: return
        self.index=(self.index-1)%len(self.files); self.show_img(self.files[self.index])
    def next_img(self):
        if not self.files: return
        self.index=(self.index+1)%len(self.files); self.show_img(self.files[self.index])
    def zoom_in(self):
        if not self.orig_pixmap:
            return
        mp=self.get_megapixels()
        if mp>8: step=1.08
        elif mp>4: step=1.12
        elif mp>1: step=1.18
        else: step=1.25
        fit=self.get_fit_scale()
        if self.zoom==1.0:
            self.zoom=step
        else:
            self.zoom*=step
        max_abs=12.0 if mp<1 else 8.0 if mp<4 else 5.0
        max_rel=max_abs/fit if fit!=0 else max_abs
        if self.zoom>max_rel:
            self.zoom=max_rel
        self.render()

    def zoom_out(self):
        if not self.orig_pixmap:
            return
        mp=self.get_megapixels()
        if mp>8: step=1.08
        elif mp>4: step=1.12
        elif mp>1: step=1.18
        else: step=1.25
        fit=self.get_fit_scale()
        if self.zoom==1.0:
            self.zoom=1.0/step
        else:
            self.zoom/=step
        min_abs=0.05
        min_rel=min_abs/fit if fit!=0 else 0.05
        if self.zoom<min_rel:
            self.zoom=min_rel
        if abs(self.zoom-1.0)<0.12:
            self.zoom=1.0
        self.render()

    def toggle_zoom(self):
        if not self.orig_pixmap:
            return
        mp=self.get_megapixels()
        fit=self.get_fit_scale()
        if fit==0: fit=1.0
        if self.zoom==1.0:
            if mp>8:
                self.zoom=1.25
            elif mp>2:
                self.zoom=1.45
            else:
                self.zoom=1.70
        else:
            if mp>8: step=1.18
            elif mp>2: step=1.28
            else: step=1.45
            self.zoom*=step
            max_abs=12.0 if mp<1 else 8.0 if mp<4 else 5.0
            max_rel=max_abs/fit if fit!=0 else max_abs
            if self.zoom>max_rel or (fit*self.zoom)>max_abs:
                self.zoom=1.0
        self.render()

    def actual(self):
        # Tam sigdirma - goruntuleyici icine sigdir
        if not self.orig_pixmap:
            return
        self.zoom=1.0
        self.render()

    def actual_size(self):
        # Gerçek boyut %100 - ihtiyac olursa
        if not self.orig_pixmap:
            return
        fit=self.get_fit_scale()
        if fit==0: fit=1.0
        if fit<1.0:
            self.zoom=1.0/fit
        else:
            self.zoom=1.0
        self.render()
    def rot_left(self): self.angle=(self.angle-90)%360; self.render()
    def rot_right(self): self.angle=(self.angle+90)%360; self.render()
    def delete_img(self):
        if len(self.files)<=1: return
        del self.files[self.index]
        if self.index>=len(self.files): self.index=0
        self.show_img(self.files[self.index])
    def keyPressEvent(self,e):
        k=e.key()
        if k==Qt.Key.Key_Left:
            self.prev_img()
        elif k==Qt.Key.Key_Right:
            self.next_img()
        elif k==Qt.Key.Key_Delete:
            self.delete_img()
        elif k==Qt.Key.Key_Escape:
            if self.is_slideshow:
                self.stop_slideshow()
            else:
                self.actual()
        elif k==Qt.Key.Key_Space:
            # Space ile slayt durdur/baslat
            if self.is_slideshow:
                self.stop_slideshow()
            else:
                self.start_slideshow_dialog()
        else:
            super().keyPressEvent(e)
    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()
    def dropEvent(self,e):
        url=e.mimeData().urls()[0].toLocalFile()
        if os.path.isdir(url):
            files=scan_images_in_folder(url)
            if files:
                self.files=files; self.index=0; self.show_img(files[0])
        elif url.lower().endswith(tuple(IMAGE_EXTS)):
            folder=os.path.dirname(url)
            files=scan_images_in_folder(folder)
            if not files: files=[url]
            self.files=files
            try: self.index=[os.path.abspath(f) for f in files].index(os.path.abspath(url))
            except: self.index=0
            self.show_img(self.files[self.index])
    def mouseDoubleClickEvent(self, e):
        if self.orig_pixmap:
            # Cift tiklama gercek boyut / sigdir toggle
            if self.zoom==1.0:
                self.actual_size()
            else:
                self.actual()
        super().mouseDoubleClickEvent(e)

    def resizeEvent(self,e):
        super().resizeEvent(e)
        if self.orig_pixmap and self.zoom==1.0:
            QTimer.singleShot(30,self.render)

if __name__=="__main__":
    app=QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)
    w=Win7Viewer()
    w.show()
    sys.exit(app.exec())