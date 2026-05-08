"""
Modern UI Stil Tanımlamaları
LibraryOS v3.0 Professional Edition
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class Theme:
    """Tema yönetimi - Dark ve Light mod"""
    
    DARK = {
        "bg": "#0F172A",
        "sidebar": "#1E293B",
        "card": "#1E293B",
        "card_hover": "#334155",
        "border": "#334155",
        "accent": "#6366F1",
        "accent_hover": "#818CF8",
        "accent_light": "rgba(99, 102, 241, 0.1)",
        "success": "#10B981",
        "success_light": "rgba(16, 185, 129, 0.1)",
        "warning": "#F59E0B",
        "warning_light": "rgba(245, 158, 11, 0.1)",
        "danger": "#EF4444",
        "danger_light": "rgba(239, 68, 68, 0.1)",
        "info": "#3B82F6",
        "info_light": "rgba(59, 130, 246, 0.1)",
        "text": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_sub": "#64748B",
        "input_bg": "#0F172A",
        "input_border": "#334155",
        "input_focus": "#6366F1",
        "scrollbar_bg": "#1E293B",
        "scrollbar_handle": "#334155",
        "scrollbar_hover": "#6366F1"
    }
    
    LIGHT = {
        "bg": "#F8FAFC",
        "sidebar": "#FFFFFF",
        "card": "#FFFFFF",
        "card_hover": "#F1F5F9",
        "border": "#E2E8F0",
        "accent": "#4F46E5",
        "accent_hover": "#6366F1",
        "accent_light": "rgba(79, 70, 229, 0.05)",
        "success": "#059669",
        "success_light": "rgba(5, 150, 105, 0.05)",
        "warning": "#D97706",
        "warning_light": "rgba(217, 119, 6, 0.05)",
        "danger": "#DC2626",
        "danger_light": "rgba(220, 38, 38, 0.05)",
        "info": "#2563EB",
        "info_light": "rgba(37, 99, 235, 0.05)",
        "text": "#0F172A",
        "text_secondary": "#475569",
        "text_sub": "#94A3B8",
        "input_bg": "#FFFFFF",
        "input_border": "#CBD5E1",
        "input_focus": "#4F46E5",
        "scrollbar_bg": "#F8FAFC",
        "scrollbar_handle": "#CBD5E1",
        "scrollbar_hover": "#4F46E5"
    }
    
    @classmethod
    def get_theme(cls, dark_mode=True):
        """Tema seçimi"""
        return cls.DARK if dark_mode else cls.LIGHT


class Styles:
    """
    CSS Stil Üretici Sınıfı
    Tüm widget'lar için modern stil tanımlamaları
    """
    
    def __init__(self, theme=None):
        """
        Args:
            theme: Tema sözlüğü, None ise Dark tema kullanılır
        """
        self.theme = theme or Theme.get_theme()
    
    def set_theme(self, dark_mode=True):
        """Tema değiştir"""
        self.theme = Theme.get_theme(dark_mode)
    
    # ============================================================
    # ANA PENCERE VE SIDEBAR
    # ============================================================
    
    @property
    def main_window(self):
        """Ana pencere stili"""
        return f"""
            QMainWindow {{
                background-color: {self.theme['bg']};
                color: {self.theme['text']};
            }}
        """
    
    @property
    def sidebar(self):
        """Sidebar panel stili"""
        return f"""
            QFrame#sidebar {{
                background-color: {self.theme['sidebar']};
                border-right: 1px solid {self.theme['border']};
            }}
        """
    
    @property
    def topbar(self):
        """Üst bar stili"""
        return f"""
            QFrame#topbar {{
                background-color: {self.theme['bg']};
                border-bottom: 1px solid {self.theme['border']};
            }}
        """
    
    # ============================================================
    # BUTON STİLLERİ
    # ============================================================
    
    def button_primary(self, full_width=False, size="normal"):
        """
        Primary buton stili
        
        Args:
            full_width: Tam genişlik
            size: 'small', 'normal', 'large'
        """
        width_style = "width: 100%;" if full_width else ""
        
        sizes = {
            'small': 'padding: 6px 12px; font-size: 11px;',
            'normal': 'padding: 10px 20px; font-size: 13px;',
            'large': 'padding: 14px 28px; font-size: 15px;'
        }
        
        return f"""
            QPushButton {{
                background-color: {self.theme['accent']};
                color: white;
                border: none;
                border-radius: 8px;
                {sizes.get(size, sizes['normal'])}
                font-weight: 600;
                {width_style}
            }}
            QPushButton:hover {{
                background-color: {self.theme['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme['accent']};
            }}
            QPushButton:disabled {{
                background-color: {self.theme['border']};
                color: {self.theme['text_sub']};
            }}
        """
    
    def button_secondary(self, full_width=False):
        """İkincil buton stili"""
        width_style = "width: 100%;" if full_width else ""
        
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {self.theme['accent']};
                border: 2px solid {self.theme['accent']};
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
                {width_style}
            }}
            QPushButton:hover {{
                background-color: {self.theme['accent_light']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme['accent']};
                color: white;
            }}
        """
    
    def button_success(self, full_width=False):
        """Başarılı buton stili"""
        width_style = "width: 100%;" if full_width else ""
        
        return f"""
            QPushButton {{
                background-color: {self.theme['success']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                {width_style}
            }}
            QPushButton:hover {{
                background-color: #34D399;
            }}
            QPushButton:pressed {{
                background-color: {self.theme['success']};
            }}
        """
    
    def button_danger(self, full_width=False):
        """Tehlike buton stili"""
        width_style = "width: 100%;" if full_width else ""
        
        return f"""
            QPushButton {{
                background-color: {self.theme['danger']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                {width_style}
            }}
            QPushButton:hover {{
                background-color: #FCA5A5;
                color: #991B1B;
            }}
            QPushButton:pressed {{
                background-color: {self.theme['danger']};
            }}
        """
    
    def button_warning(self, full_width=False):
        """Uyarı buton stili"""
        width_style = "width: 100%;" if full_width else ""
        
        return f"""
            QPushButton {{
                background-color: {self.theme['warning']};
                color: #000;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                {width_style}
            }}
            QPushButton:hover {{
                background-color: #FBBF24;
            }}
        """
    
    def button_ghost(self):
        """Hayalet buton stili"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {self.theme['text_secondary']};
                border: none;
                padding: 8px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {self.theme['text']};
                background-color: {self.theme['card_hover']};
                border-radius: 6px;
            }}
        """
    
    def button_icon(self):
        """İkon buton stili"""
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 20px;
                padding: 8px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['card_hover']};
            }}
        """
    
    # ============================================================
    # INPUT STİLLERİ
    # ============================================================
    
    def input_field(self, width=None):
        """
        Input alanı stili
        
        Args:
            width: Sabit genişlik (örn: '300px')
        """
        width_style = f"width: {width};" if width else ""
        
        return f"""
            QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QDateTimeEdit {{
                background-color: {self.theme['input_bg']};
                color: {self.theme['text']};
                border: 2px solid {self.theme['input_border']};
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                {width_style}
            }}
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, 
            QDateEdit:focus, QDateTimeEdit:focus {{
                border-color: {self.theme['input_focus']};
                background-color: {self.theme['card']};
            }}
            QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled,
            QDateEdit:disabled, QDateTimeEdit:disabled {{
                background-color: {self.theme['border']};
                color: {self.theme['text_sub']};
            }}
        """
    
    def combo_box(self, width=None):
        """ComboBox stili"""
        width_style = f"width: {width};" if width else ""
        
        return f"""
            QComboBox {{
                background-color: {self.theme['input_bg']};
                color: {self.theme['text']};
                border: 2px solid {self.theme['input_border']};
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                {width_style}
            }}
            QComboBox:focus {{
                border-color: {self.theme['input_focus']};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 15px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.theme['card']};
                color: {self.theme['text']};
                border: 1px solid {self.theme['border']};
                border-radius: 8px;
                selection-background-color: {self.theme['accent_light']};
                selection-color: {self.theme['accent']};
                padding: 5px;
            }}
        """
    
    def text_edit(self):
        """Çok satırlı metin alanı stili"""
        return f"""
            QTextEdit, QPlainTextEdit {{
                background-color: {self.theme['input_bg']};
                color: {self.theme['text']};
                border: 2px solid {self.theme['input_border']};
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
            }}
            QTextEdit:focus, QPlainTextEdit:focus {{
                border-color: {self.theme['input_focus']};
            }}
        """
    
    # ============================================================
    # TABLO STİLLERİ
    # ============================================================
    
    @property
    def table(self):
        """Modern tablo stili"""
        return f"""
            QTableWidget {{
                background-color: {self.theme['card']};
                color: {self.theme['text']};
                border: none;
                border-radius: 12px;
                gridline-color: {self.theme['border']};
                font-size: 13px;
                selection-background-color: {self.theme['accent_light']};
                selection-color: {self.theme['accent']};
                alternate-background-color: {self.theme['card_hover']};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 12px 15px;
                border-bottom: 1px solid {self.theme['border']};
            }}
            QTableWidget::item:selected {{
                background-color: {self.theme['accent_light']};
                color: {self.theme['accent']};
                font-weight: 600;
            }}
            QTableWidget::item:hover {{
                background-color: {self.theme['card_hover']};
            }}
            QHeaderView::section {{
                background-color: {self.theme['sidebar']};
                color: {self.theme['accent']};
                padding: 14px 15px;
                border: none;
                border-bottom: 2px solid {self.theme['accent']};
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            QHeaderView::section:hover {{
                background-color: {self.theme['card_hover']};
            }}
            QScrollBar:vertical {{
                background: {self.theme['scrollbar_bg']};
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme['scrollbar_handle']};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme['scrollbar_hover']};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background: {self.theme['scrollbar_bg']};
                height: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.theme['scrollbar_handle']};
                border-radius: 4px;
                min-width: 30px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {self.theme['scrollbar_hover']};
            }}
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
    
    @property
    def table_compact(self):
        """Kompakt tablo stili"""
        return f"""
            QTableWidget {{
                background-color: {self.theme['card']};
                color: {self.theme['text']};
                border: none;
                border-radius: 8px;
                gridline-color: {self.theme['border']};
                font-size: 12px;
                selection-background-color: {self.theme['accent_light']};
                selection-color: {self.theme['accent']};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 8px 10px;
                border-bottom: 1px solid {self.theme['border']};
            }}
            QHeaderView::section {{
                background-color: {self.theme['sidebar']};
                color: {self.theme['accent']};
                padding: 10px;
                border: none;
                border-bottom: 2px solid {self.theme['accent']};
                font-size: 10px;
                font-weight: 700;
                text-transform: uppercase;
            }}
        """
    
    # ============================================================
    # KART STİLLERİ
    # ============================================================
    
    @property
    def card(self):
        """Standart kart stili"""
        return f"""
            QFrame#card {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['border']};
                border-radius: 16px;
                padding: 20px;
            }}
            QFrame#card:hover {{
                border-color: {self.theme['accent']};
            }}
        """
    
    @property
    def card_accent(self):
        """Vurgulu kart stili"""
        return f"""
            QFrame#card_accent {{
                background-color: {self.theme['card']};
                border: 2px solid {self.theme['accent']};
                border-radius: 16px;
                padding: 20px;
            }}
        """
    
    @property
    def card_success(self):
        """Başarı kartı stili"""
        return f"""
            QFrame#card_success {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['success']};
                border-radius: 16px;
                padding: 20px;
            }}
        """
    
    @property
    def card_danger(self):
        """Tehlike kartı stili"""
        return f"""
            QFrame#card_danger {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['danger']};
                border-radius: 16px;
                padding: 20px;
            }}
        """
    
    @property
    def card_warning(self):
        """Uyarı kartı stili"""
        return f"""
            QFrame#card_warning {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['warning']};
                border-radius: 16px;
                padding: 20px;
            }}
        """
    
    # ============================================================
    # ETİKET STİLLERİ
    # ============================================================
    
    @property
    def label_title(self):
        """Başlık etiketi"""
        return f"""
            color: {self.theme['text']};
            font-size: 24px;
            font-weight: 800;
        """
    
    @property
    def label_subtitle(self):
        """Alt başlık etiketi"""
        return f"""
            color: {self.theme['text_secondary']};
            font-size: 14px;
            font-weight: 400;
        """
    
    @property
    def label_small(self):
        """Küçük metin etiketi"""
        return f"""
            color: {self.theme['text_sub']};
            font-size: 11px;
            font-weight: 500;
        """
    
    def label_badge(self, color="accent"):
        """Rozet etiketi"""
        colors = {
            'accent': (self.theme['accent'], self.theme['accent_light']),
            'success': (self.theme['success'], self.theme['success_light']),
            'warning': (self.theme['warning'], self.theme['warning_light']),
            'danger': (self.theme['danger'], self.theme['danger_light']),
            'info': (self.theme['info'], self.theme['info_light']),
        }
        
        text_color, bg_color = colors.get(color, colors['accent'])
        
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 12px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
            }}
        """
    
    # ============================================================
    # CHECKBOX VE RADIO STİLLERİ
    # ============================================================
    
    @property
    def checkbox(self):
        """Checkbox stili"""
        return f"""
            QCheckBox {{
                color: {self.theme['text']};
                font-size: 13px;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {self.theme['border']};
                border-radius: 4px;
                background-color: {self.theme['input_bg']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.theme['accent']};
                border-color: {self.theme['accent']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {self.theme['accent']};
            }}
        """
    
    @property
    def radio_button(self):
        """Radio button stili"""
        return f"""
            QRadioButton {{
                color: {self.theme['text']};
                font-size: 13px;
                spacing: 10px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {self.theme['border']};
                border-radius: 10px;
                background-color: {self.theme['input_bg']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {self.theme['accent']};
                border-color: {self.theme['accent']};
            }}
            QRadioButton::indicator:hover {{
                border-color: {self.theme['accent']};
            }}
        """
    
    # ============================================================
    # PROGRESS BAR
    # ============================================================
    
    @property
    def progress_bar(self):
        """İlerleme çubuğu stili"""
        return f"""
            QProgressBar {{
                background-color: {self.theme['card']};
                border: none;
                border-radius: 8px;
                height: 10px;
                text-align: center;
                font-size: 10px;
                color: transparent;
            }}
            QProgressBar::chunk {{
                background-color: {self.theme['accent']};
                border-radius: 8px;
            }}
        """
    
    # ============================================================
    # TAB WIDGET
    # ============================================================
    
    @property
    def tab_widget(self):
        """Sekme widget stili"""
        return f"""
            QTabWidget::pane {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['border']};
                border-radius: 12px;
                padding: 15px;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {self.theme['text_secondary']};
                border: none;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                margin-right: 5px;
            }}
            QTabBar::tab:selected {{
                color: {self.theme['accent']};
                border-bottom: 3px solid {self.theme['accent']};
            }}
            QTabBar::tab:hover {{
                color: {self.theme['text']};
                background-color: {self.theme['card_hover']};
                border-radius: 8px;
            }}
        """
    
    # ============================================================
    # GROUP BOX
    # ============================================================
    
    @property
    def group_box(self):
        """Grup kutusu stili"""
        return f"""
            QGroupBox {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['border']};
                border-radius: 12px;
                margin-top: 20px;
                padding: 25px 15px 15px 15px;
                font-size: 14px;
                font-weight: 700;
                color: {self.theme['text']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: {self.theme['accent']};
            }}
        """
    
    # ============================================================
    # TOOLTIP
    # ============================================================
    
    @property
    def tooltip(self):
        """İpucu stili"""
        return f"""
            QToolTip {{
                background-color: {self.theme['card']};
                color: {self.theme['text']};
                border: 1px solid {self.theme['border']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
            }}
        """
    
    # ============================================================
    # MESSAGE BOX
    # ============================================================
    
    @property
    def notification_success(self):
        """Başarılı bildirim stili"""
        return f"""
            QMessageBox {{
                background-color: {self.theme['card']};
            }}
            QMessageBox QLabel {{
                color: {self.theme['text']};
                font-size: 13px;
                min-width: 300px;
            }}
            QMessageBox QPushButton {{
                background-color: {self.theme['success']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 12px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #34D399;
            }}
        """
    
    @property
    def notification_error(self):
        """Hata bildirimi stili"""
        return f"""
            QMessageBox {{
                background-color: {self.theme['card']};
            }}
            QMessageBox QLabel {{
                color: {self.theme['text']};
                font-size: 13px;
                min-width: 300px;
            }}
            QMessageBox QPushButton {{
                background-color: {self.theme['danger']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 12px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #FCA5A5;
                color: #991B1B;
            }}
        """
    
    @property
    def notification_warning(self):
        """Uyarı bildirimi stili"""
        return f"""
            QMessageBox {{
                background-color: {self.theme['card']};
            }}
            QMessageBox QLabel {{
                color: {self.theme['text']};
                font-size: 13px;
                min-width: 300px;
            }}
            QMessageBox QPushButton {{
                background-color: {self.theme['warning']};
                color: #000;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 12px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #FBBF24;
            }}
        """
    
    @property
    def notification_info(self):
        """Bilgi bildirimi stili"""
        return f"""
            QMessageBox {{
                background-color: {self.theme['card']};
            }}
            QMessageBox QLabel {{
                color: {self.theme['text']};
                font-size: 13px;
                min-width: 300px;
            }}
            QMessageBox QPushButton {{
                background-color: {self.theme['info']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 12px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #60A5FA;
            }}
        """
    
    # ============================================================
    # MENÜ
    # ============================================================
    
    @property
    def menu(self):
        """Menü stili"""
        return f"""
            QMenu {{
                background-color: {self.theme['card']};
                color: {self.theme['text']};
                border: 1px solid {self.theme['border']};
                border-radius: 8px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 30px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {self.theme['accent_light']};
                color: {self.theme['accent']};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {self.theme['border']};
                margin: 5px 10px;
            }}
        """
    
    # ============================================================
    # ÖZEL WIDGET STİLLERİ
    # ============================================================
    
    def search_bar(self, width="300px"):
        """Arama çubuğu stili"""
        return f"""
            QLineEdit {{
                background-color: {self.theme['card']};
                color: {self.theme['text']};
                border: 2px solid {self.theme['border']};
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 14px;
                width: {width};
            }}
            QLineEdit:focus {{
                border-color: {self.theme['accent']};
                background-color: {self.theme['bg']};
            }}
            QLineEdit::placeholder {{
                color: {self.theme['text_sub']};
            }}
        """
    
    def stat_card(self, accent_color=None):
        """İstatistik kartı stili"""
        color = accent_color or self.theme['accent']
        
        return f"""
            QFrame#stat_card {{
                background-color: {self.theme['card']};
                border: 1px solid {self.theme['border']};
                border-left: 4px solid {color};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame#stat_card:hover {{
                border-color: {color};
                background-color: {self.theme['card_hover']};
            }}
        """
    
    @property
    def scroll_area(self):
        """Kaydırma alanı stili"""
        return f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {self.theme['scrollbar_bg']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme['scrollbar_handle']};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme['scrollbar_hover']};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
    
    # ============================================================
    # ÖZEL EFEKTLER
    # ============================================================
    
    @staticmethod
    def shadow_effect(widget, blur=20, offset_y=4, color=(0, 0, 0, 80)):
        """
        Widget'a gölge efekti ekle
        
        Args:
            widget: Efekt eklenecek widget
            blur: Bulanıklık miktarı
            offset_y: Dikey kaydırma
            color: RGBA renk tuple
        """
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur)
        shadow.setColor(QColor(*color))
        shadow.setOffset(0, offset_y)
        widget.setGraphicsEffect(shadow)
        return shadow
    
    @staticmethod
    def fade_in_animation(widget, duration=500):
        """
        Widget'a fade-in animasyonu ekle
        
        Args:
            widget: Animasyon eklenecek widget
            duration: Süre (ms)
        """
        from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
        
        widget.setWindowOpacity(0)
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        return animation