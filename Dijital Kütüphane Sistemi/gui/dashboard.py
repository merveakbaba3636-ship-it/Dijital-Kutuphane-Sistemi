"""
Dashboard - KPI kartları ve kitap listesi
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QTableWidget, QTableWidgetItem, QLineEdit,
                             QHeaderView, QAbstractItemView, QGraphicsDropShadowEffect,
                             QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from gui.styles import Theme, Styles


class KPICard(QFrame):
    """Modern KPI kartı"""
    
    def __init__(self, title, value, icon, color=None):
        super().__init__()
        self.setObjectName("card")
        self.setFixedHeight(130)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Stil
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {Theme.DARK['card']};
                border: 1px solid {Theme.DARK['border']};
                border-radius: 16px;
                padding: 20px;
            }}
            QFrame#card:hover {{
                border-color: {color or Theme.DARK['accent']};
                background-color: {Theme.DARK['card_hover']};
            }}
        """)
        
        # Gölge efekti
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Sol taraf - bilgiler
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        
        title_label = QLabel(title.upper())
        title_label.setStyleSheet(f"color: {Theme.DARK['text_sub']}; font-size: 11px; font-weight: 700; letter-spacing: 1px;")
        
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"color: {Theme.DARK['text']}; font-size: 36px; font-weight: 800;")
        
        left_layout.addWidget(title_label)
        left_layout.addWidget(self.value_label)
        
        layout.addLayout(left_layout)
        layout.addStretch()
        
        # Sağ taraf - ikon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 48px; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
    
    def update_value(self, new_value):
        """Değeri güncelle"""
        self.value_label.setText(str(new_value))


class SearchBar(QLineEdit):
    """Modern arama çubuğu"""
    
    def __init__(self, placeholder="Ara..."):
        super().__init__()
        self.setPlaceholderText(f"🔍  {placeholder}")
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Theme.DARK['card']};
                color: {Theme.DARK['text']};
                border: 2px solid {Theme.DARK['border']};
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 14px;
                min-width: 300px;
            }}
            QLineEdit:focus {{
                border-color: {Theme.DARK['accent']};
                background-color: {Theme.DARK['bg']};
            }}
        """)


class DashboardPage(QWidget):
    """Dashboard ana sayfası"""
    
    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self.styles = Styles()
        self._init_ui()
        
        # Otomatik yenileme timer'ı
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(30000)  # 30 saniyede bir yenile
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # === KPI KARTLARI ===
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(20)
        
        self.kpi_toplam_kitap = KPICard("Toplam Kitap", "0", "📚", Theme.DARK['info'])
        self.kpi_mevcut_kitap = KPICard("Mevcut Kitap", "0", "✅", Theme.DARK['success'])
        self.kpi_odunc_kitap = KPICard("Ödünçteki Kitap", "0", "🔄", Theme.DARK['warning'])
        self.kpi_toplam_uye = KPICard("Kayıtlı Üye", "0", "👥", Theme.DARK['accent'])
        self.kpi_gecikmis = KPICard("Gecikmiş İade", "0", "⚠️", Theme.DARK['danger'])
        self.kpi_toplam_ceza = KPICard("Toplam Ceza", "0 TL", "💰", Theme.DARK['danger'])
        
        kpi_layout.addWidget(self.kpi_toplam_kitap)
        kpi_layout.addWidget(self.kpi_mevcut_kitap)
        kpi_layout.addWidget(self.kpi_odunc_kitap)
        kpi_layout.addWidget(self.kpi_toplam_uye)
        kpi_layout.addWidget(self.kpi_gecikmis)
        kpi_layout.addWidget(self.kpi_toplam_ceza)
        
        layout.addLayout(kpi_layout)
        
        # === KİTAP LİSTESİ ===
        list_frame = QFrame()
        list_frame.setObjectName("card")
        list_frame.setStyleSheet(self.styles.card)
        
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(25, 25, 25, 25)
        list_layout.setSpacing(20)
        
        # Başlık ve arama
        header_layout = QHBoxLayout()
        
        list_title = QLabel("📋 Kütüphane Envanteri")
        list_title.setStyleSheet(self.styles.label_title + "font-size: 20px;")
        
        self.search_bar = SearchBar("Kitap adı, yazar veya kategori ara...")
        self.search_bar.textChanged.connect(self._filter_table)
        
        header_layout.addWidget(list_title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_bar)
        
        list_layout.addLayout(header_layout)
        
        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "KİTAP ADI", "YAZAR", "KATEGORİ", "ISBN", "STOK", "DURUM"
        ])
        
        # Tablo ayarları
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 60)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(self.styles.table)
        self.table.setSortingEnabled(True)
        
        list_layout.addWidget(self.table)
        layout.addWidget(list_frame)
        
        # İlk yükleme
        self.refresh()
    
    def refresh(self):
        """Dashboard'ı güncelle"""
        stats = self.sistem.db.get_stats()
        
        # KPI'ları güncelle
        self.kpi_toplam_kitap.update_value(stats['toplam_kitap'])
        self.kpi_mevcut_kitap.update_value(stats['toplam_kitap'] - stats['odunc_kitap'])
        self.kpi_odunc_kitap.update_value(stats['odunc_kitap'])
        self.kpi_toplam_uye.update_value(stats['toplam_uye'])
        self.kpi_gecikmis.update_value(stats['gecikmis_islem'])
        self.kpi_toplam_ceza.update_value(f"{stats['toplam_ceza']:.2f} TL")
        
        # Tabloyu güncelle
        self._load_table_data()
    
    def _load_table_data(self):
        """Kitap listesini yükle"""
        kitaplar = self.sistem.db.execute_query(
            "SELECT * FROM kitaplar ORDER BY ad"
        )
        
        self.table.setRowCount(len(kitaplar))
        
        for row, kitap in enumerate(kitaplar):
            mevcut = kitap['toplam_adet'] - kitap['odunc_adet']
            durum = "Tümü Mevcut" if mevcut == kitap['toplam_adet'] else \
                   "Tümü Ödünçte" if mevcut == 0 else f"{mevcut}/{kitap['toplam_adet']} Mevcut"
            
            items = [
                QTableWidgetItem(str(kitap['id'])),
                QTableWidgetItem(kitap['ad']),
                QTableWidgetItem(kitap['yazar']),
                QTableWidgetItem(kitap['kategori']),
                QTableWidgetItem(kitap['isbn'] or "-"),
                QTableWidgetItem(str(kitap['toplam_adet'])),
                QTableWidgetItem(durum)
            ]
            
            # Durum renklendirme
            durum_lower = durum.lower()
            if "tümü mevcut" in durum_lower:
                items[6].setForeground(QColor(Theme.DARK['success']))
            elif "tümü ödünçte" in durum_lower:
                items[6].setForeground(QColor(Theme.DARK['danger']))
            else:
                items[6].setForeground(QColor(Theme.DARK['warning']))
            
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
    
    def _filter_table(self):
        """Tabloyu filtrele"""
        search_text = self.search_bar.text().lower()
        
        for row in range(self.table.rowCount()):
            show = False
            if not search_text:
                show = True
            else:
                # Ad, yazar, kategori, ISBN sütunlarını kontrol et
                for col in [1, 2, 3, 4]:
                    item = self.table.item(row, col)
                    if item and search_text in item.text().lower():
                        show = True
                        break
            
            self.table.setRowHidden(row, not show)