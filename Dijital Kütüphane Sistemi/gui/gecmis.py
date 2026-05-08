"""
İşlem Geçmişi ve Raporlama Sayfası
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QComboBox, QDateEdit, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from datetime import date
from gui.styles import Theme, Styles
from backend.utils import ExportManager


class GecmisPage(QWidget):
    
    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self.styles = Styles()  # ← Bu satır mutlaka olsun!
        self._all_data = []
        self._init_ui()
        self._load_data()
    
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # === BAŞLIK ===
        baslik = QLabel("📝 Ödünç ve İade İşlem Geçmişi")
        baslik.setStyleSheet(f"color: {Theme.DARK['text']}; font-size: 22px; font-weight: 800;")
        layout.addWidget(baslik)
        
        # === FİLTRE PANELİ ===
        filtre_panel = QFrame()
        filtre_panel.setObjectName("card")
        filtre_panel.setStyleSheet(self.styles.card)
        
        filtre_layout = QHBoxLayout(filtre_panel)
        filtre_layout.setContentsMargins(20, 15, 20, 15)
        filtre_layout.setSpacing(15)
        
        # Durum filtresi
        filtre_layout.addWidget(QLabel("Durum:"))
        self.filtre_durum = QComboBox()
        self.filtre_durum.addItems(["Tümü", "Devam Eden", "İade Edilen", "Gecikmiş"])
        self.filtre_durum.setStyleSheet(self.styles.combo_box("150px"))
        self.filtre_durum.currentTextChanged.connect(self._filtrele)
        filtre_layout.addWidget(self.filtre_durum)
        
        # Tarih aralığı
        filtre_layout.addWidget(QLabel("Başlangıç:"))
        self.filtre_baslangic = QDateEdit()
        self.filtre_baslangic.setDate(QDate.currentDate().addMonths(-1))
        self.filtre_baslangic.setCalendarPopup(True)
        self.filtre_baslangic.setStyleSheet(self.styles.input_field("130px"))
        self.filtre_baslangic.dateChanged.connect(self._filtrele)
        filtre_layout.addWidget(self.filtre_baslangic)
        
        filtre_layout.addWidget(QLabel("Bitiş:"))
        self.filtre_bitis = QDateEdit()
        self.filtre_bitis.setDate(QDate.currentDate())
        self.filtre_bitis.setCalendarPopup(True)
        self.filtre_bitis.setStyleSheet(self.styles.input_field("130px"))
        self.filtre_bitis.dateChanged.connect(self._filtrele)
        filtre_layout.addWidget(self.filtre_bitis)
        
        filtre_layout.addStretch()
        
        # Arama
        self.arama = QLineEdit()
        self.arama.setPlaceholderText("🔍 Kitap veya üye ara...")
        self.arama.setStyleSheet(self.styles.search_bar("250px"))
        self.arama.textChanged.connect(self._filtrele)
        filtre_layout.addWidget(self.arama)
        
        layout.addWidget(filtre_panel)
        
        # === BUTONLAR ===
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.export_csv_btn = QPushButton("📊 CSV'ye Aktar")
        self.export_csv_btn.setStyleSheet(self.styles.button_secondary())
        self.export_csv_btn.clicked.connect(self._export_csv)
        
        self.export_pdf_btn = QPushButton("📄 PDF Rapor")
        self.export_pdf_btn.setStyleSheet(self.styles.button_secondary())
        self.export_pdf_btn.clicked.connect(self._export_pdf)
        
        self.yenile_btn = QPushButton("🔄 Yenile")
        self.yenile_btn.setStyleSheet(self.styles.button_primary())
        self.yenile_btn.clicked.connect(self._load_data)
        
        btn_layout.addWidget(self.export_csv_btn)
        btn_layout.addWidget(self.export_pdf_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.yenile_btn)
        
        layout.addLayout(btn_layout)
        
        # === İSTATİSTİK KARTLARI ===
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.stat_toplam = self._stat_card("Toplam İşlem", "0", "📋")
        self.stat_aktif = self._stat_card("Aktif Ödünç", "0", "📖")
        self.stat_iade = self._stat_card("İade Edilen", "0", "✅")
        self.stat_gecikmis = self._stat_card("Gecikmiş", "0", "⚠️")
        self.stat_ceza = self._stat_card("Toplam Ceza", "0 TL", "💰")
        
        stats_layout.addWidget(self.stat_toplam)
        stats_layout.addWidget(self.stat_aktif)
        stats_layout.addWidget(self.stat_iade)
        stats_layout.addWidget(self.stat_gecikmis)
        stats_layout.addWidget(self.stat_ceza)
        
        layout.addLayout(stats_layout)
        
        # === TABLO ===
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(9)
        self.tablo.setHorizontalHeaderLabels([
            "İŞLEM ID", "KİTAP ADI", "ÜYE ADI", "VERİLİŞ",
            "BEKLENEN İADE", "İADE TARİHİ", "GECİKME",
            "CEZA (TL)", "DURUM"
        ])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tablo.setColumnWidth(0, 70)
        self.tablo.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.tablo.setColumnWidth(6, 80)
        self.tablo.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)
        self.tablo.setColumnWidth(7, 80)
        self.tablo.horizontalHeader().setSectionResizeMode(8, QHeaderView.Fixed)
        self.tablo.setColumnWidth(8, 130)
        
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setShowGrid(False)
        self.tablo.setStyleSheet(self.styles.table)
        self.tablo.setSortingEnabled(True)
        
        layout.addWidget(self.tablo)
    
    def _stat_card(self, baslik, deger, ikon):
        """İstatistik kartı oluştur"""
        frame = QFrame()
        frame.setObjectName("stat_card")
        frame.setStyleSheet(f"""
            QFrame#stat_card {{
                background-color: {Theme.DARK['card']};
                border: 1px solid {Theme.DARK['border']};
                border-radius: 12px;
                padding: 15px;
            }}
            QFrame#stat_card:hover {{
                border-color: {Theme.DARK['accent']};
            }}
        """)
        
        flayout = QVBoxLayout(frame)
        flayout.setContentsMargins(15, 12, 15, 12)
        flayout.setSpacing(5)
        
        baslik_label = QLabel(f"{ikon} {baslik}")
        baslik_label.setStyleSheet(f"color: {Theme.DARK['text_sub']}; font-size: 10px; font-weight: 700;")
        
        deger_label = QLabel(deger)
        deger_label.setStyleSheet(f"color: {Theme.DARK['text']}; font-size: 18px; font-weight: 800;")
        deger_label.setObjectName("stat_value")
        
        flayout.addWidget(baslik_label)
        flayout.addWidget(deger_label)
        
        return frame
    
    def _load_data(self):
        """Tüm verileri yükle"""
        self._all_data = self.sistem.db.execute_query("""
            SELECT o.*, k.ad as kitap_ad, u.ad as uye_ad 
            FROM oduncler o
            JOIN kitaplar k ON o.kitap_id = k.id
            JOIN uyeler u ON o.uye_id = u.id
            ORDER BY o.id DESC
        """)
        
        # İstatistikleri güncelle
        bugun = date.today()
        toplam = len(self._all_data)
        aktif = sum(1 for o in self._all_data if o['iade_tarihi'] is None)
        iade_edilen = toplam - aktif
        toplam_ceza = sum(o['ceza_tutari'] for o in self._all_data)
        
        gecikmis = sum(
            1 for o in self._all_data
            if o['iade_tarihi'] is None and bugun > date.fromisoformat(o['beklenen_iade'])
        )
        
        # Kartları güncelle
        self._update_stat_card(self.stat_toplam, str(toplam))
        self._update_stat_card(self.stat_aktif, str(aktif))
        self._update_stat_card(self.stat_iade, str(iade_edilen))
        self._update_stat_card(self.stat_gecikmis, str(gecikmis))
        self._update_stat_card(self.stat_ceza, f"{toplam_ceza:.2f} TL")
        
        self._filtrele()
    
    def _update_stat_card(self, card, value):
        """İstatistik kartı değerini güncelle"""
        for child in card.findChildren(QLabel):
            if child.objectName() == "stat_value":
                child.setText(value)
                break
    
    def _filtrele(self):
        """Filtreleme uygula"""
        durum_filtre = self.filtre_durum.currentText()
        baslangic = self.filtre_baslangic.date().toPyDate()
        bitis = self.filtre_bitis.date().toPyDate()
        arama = self.arama.text().lower()
        
        filtrelenmis = []
        bugun = date.today()
        
        for odunc in self._all_data:
            # Tarih filtresi
            odunc_tarih = date.fromisoformat(odunc['odunc_tarihi'])
            if not (baslangic <= odunc_tarih <= bitis):
                continue
            
            # Durum filtresi
            if durum_filtre == "Devam Eden" and odunc['iade_tarihi'] is not None:
                continue
            elif durum_filtre == "İade Edilen" and odunc['iade_tarihi'] is None:
                continue
            elif durum_filtre == "Gecikmiş":
                if odunc['iade_tarihi'] is not None:
                    continue
                beklenen = date.fromisoformat(odunc['beklenen_iade'])
                if bugun <= beklenen:
                    continue
            
            # Arama filtresi
            if arama:
                if arama not in odunc['kitap_ad'].lower() and arama not in odunc['uye_ad'].lower():
                    continue
            
            filtrelenmis.append(odunc)
        
        self._tabloyu_doldur(filtrelenmis)
    
    def _tabloyu_doldur(self, oduncler):
        """Tabloyu verilerle doldur"""
        self.tablo.setRowCount(len(oduncler))
        bugun = date.today()
        
        for row, odunc in enumerate(oduncler):
            # İade tarihi
            iade_tarihi = odunc['iade_tarihi'] if odunc['iade_tarihi'] else "-"
            
            # Gecikme ve durum
            if odunc['iade_tarihi']:
                beklenen = date.fromisoformat(odunc['beklenen_iade'])
                iade = date.fromisoformat(odunc['iade_tarihi'])
                gecikme_gun = max(0, (iade - beklenen).days)
                
                if gecikme_gun > 0:
                    durum = f"⚠️ Gecikmeli ({gecikme_gun}g)"
                    durum_color = Theme.DARK['danger']
                else:
                    durum = "✅ İade Edildi"
                    durum_color = Theme.DARK['success']
            else:
                beklenen = date.fromisoformat(odunc['beklenen_iade'])
                gecikme_gun = max(0, (bugun - beklenen).days)
                
                if gecikme_gun > 0:
                    durum = f"❌ Gecikti ({gecikme_gun}g)"
                    durum_color = Theme.DARK['danger']
                else:
                    kalan = (beklenen - bugun).days
                    durum = f"📖 Okumada ({kalan}g kaldı)"
                    durum_color = Theme.DARK['warning']
            
            items = [
                QTableWidgetItem(str(odunc['id'])),
                QTableWidgetItem(odunc['kitap_ad']),
                QTableWidgetItem(odunc['uye_ad']),
                QTableWidgetItem(odunc['odunc_tarihi']),
                QTableWidgetItem(odunc['beklenen_iade']),
                QTableWidgetItem(iade_tarihi),
                QTableWidgetItem(f"{gecikme_gun} gün"),
                QTableWidgetItem(f"{odunc['ceza_tutari']:.2f}"),
                QTableWidgetItem(durum)
            ]
            
            # Renklendirme
            items[8].setForeground(QColor(durum_color))
            
            if odunc['ceza_tutari'] > 0:
                items[7].setForeground(QColor(Theme.DARK['danger']))
            else:
                items[7].setForeground(QColor(Theme.DARK['success']))
            
            if gecikme_gun > 0:
                items[6].setForeground(QColor(Theme.DARK['danger']))
            
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.tablo.setItem(row, col, item)
    
    # ============================================================
    # EXPORT İŞLEMLERİ
    # ============================================================
    
    def _export_csv(self):
        """CSV'ye aktar"""
        if not self._all_data:
            self._msg("Aktarılacak veri yok!", "warning")
            return
        
        filename = f"odunc_gecmisi_{date.today().strftime('%Y%m%d')}.csv"
        filepath = ExportManager.to_csv(self._all_data, filename)
        
        if filepath:
            self._msg(f"✅ CSV dosyası oluşturuldu:\n{filepath}", "success")
    
    def _export_pdf(self):
        """PDF'e aktar"""
        if not self._all_data:
            self._msg("Aktarılacak veri yok!", "warning")
            return
        
        filename = f"odunc_raporu_{date.today().strftime('%Y%m%d')}.pdf"
        filepath = ExportManager.to_pdf(self._all_data, "Ödünç İşlemleri Raporu", filename)
        
        if filepath:
            self._msg(f"✅ PDF raporu oluşturuldu:\n{filepath}", "success")
        else:
            self._msg("⚠️ PDF için reportlab yükleyin:\npip install reportlab", "warning")
    
    def _msg(self, mesaj, tip="info"):
        """Mesaj göster"""
        msg = QMessageBox(self)
        msg.setWindowTitle({
            "success": "✅ Başarılı",
            "error": "❌ Hata",
            "warning": "⚠️ Uyarı",
            "info": "ℹ️ Bilgi"
        }.get(tip, "Bilgi"))
        
        msg.setText(mesaj)
        
        if tip == "success":
            msg.setStyleSheet(self.styles.notification_success)
        elif tip == "error":
            msg.setStyleSheet(self.styles.notification_error)
        elif tip == "warning":
            msg.setStyleSheet(self.styles.notification_warning)
        else:
            msg.setStyleSheet(self.styles.notification_info)
        
        msg.exec_()