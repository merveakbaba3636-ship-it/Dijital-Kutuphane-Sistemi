"""
Ana Pencere - Sidebar Navigasyon
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QFrame, QLabel, QPushButton, QStackedWidget,
                             QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from gui.styles import Theme, Styles
from gui.dashboard import DashboardPage
from gui.islemler import IslemPage
from gui.gecmis import GecmisPage


class SidebarButton(QPushButton):
    def __init__(self, icon, text, parent=None):
        super().__init__(f"  {icon}   {text}", parent)
        self.setCheckable(True)
        self.setFixedHeight(52)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._style(False)
    
    def setChecked(self, checked):
        super().setChecked(checked)
        self._style(checked)
    
    def _style(self, active):
        if active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Theme.DARK['accent_light']};
                    color: {Theme.DARK['accent']};
                    border: none;
                    border-left: 4px solid {Theme.DARK['accent']};
                    text-align: left;
                    padding-left: 22px;
                    font-size: 14px;
                    font-weight: 700;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Theme.DARK['text_secondary']};
                    border: none;
                    border-left: 4px solid transparent;
                    text-align: left;
                    padding-left: 22px;
                    font-size: 14px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: rgba(255,255,255,0.05);
                    color: {Theme.DARK['text']};
                }}
            """)


class MainWindow(QMainWindow):
    def __init__(self, sistem, admin):
        super().__init__()
        self.sistem = sistem
        self.admin = admin
        self.styles = Styles()
        self.setWindowTitle("LibraryOS v3.0")
        self.setMinimumSize(1400, 850)
        self.setStyleSheet(f"QMainWindow{{background-color:{Theme.DARK['bg']};}}")
        
        central = QWidget()
        self.setCentralWidget(central)
        ml = QHBoxLayout(central)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)
        
        # === SIDEBAR ===
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(270)
        sidebar.setStyleSheet(f"QFrame#sidebar{{background:{Theme.DARK['sidebar']};border-right:1px solid {Theme.DARK['border']};}}")
        
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(0, 0, 0, 10)
        sl.setSpacing(0)
        
        # Logo
        logo = QFrame()
        logo.setFixedHeight(100)
        logo.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {Theme.DARK['accent']},stop:1 {Theme.DARK['accent_hover']});")
        ll = QVBoxLayout(logo)
        ll.setContentsMargins(25, 20, 25, 20)
        t1 = QLabel("📚 LibraryOS")
        t1.setStyleSheet("color:white;font-size:20px;font-weight:900;")
        t2 = QLabel("v3.0 Professional")
        t2.setStyleSheet("color:rgba(255,255,255,0.8);font-size:11px;font-weight:600;")
        ll.addWidget(t1)
        ll.addWidget(t2)
        sl.addWidget(logo)
        sl.addSpacing(15)
        
        # Navigasyon
        self.nav_buttons = []
        for icon, text in [("📊","Dashboard"),("📚","Kitap Yönetimi"),("👥","Üye Yönetimi"),("🔄","Ödünç İşlemleri"),("📝","İşlem Geçmişi")]:
            btn = SidebarButton(icon, text)
            btn.clicked.connect(lambda checked, t=text: self._navigate(t))
            sl.addWidget(btn)
            self.nav_buttons.append(btn)
        
        sl.addStretch()
        
        # Kullanıcı bilgisi
        uf = QFrame()
        uf.setStyleSheet(f"background:{Theme.DARK['card']};border-radius:10px;margin:10px;padding:12px;")
        ul = QVBoxLayout(uf)
        ul.setContentsMargins(12, 10, 12, 10)
        ul.setSpacing(3)
        ul.addWidget(QLabel(f"👤 {self.admin.get_ad()}"))
        ul.addWidget(QLabel(f"🔑 {self.admin.get_rol().title()}"))
        sl.addWidget(uf)
        
        # Çıkış
        cikis = QPushButton("🚪  Çıkış Yap")
        cikis.setStyleSheet(f"background:transparent;color:{Theme.DARK['text_secondary']};border:none;text-align:left;padding:10px 25px;font-size:13px;")
        cikis.clicked.connect(self.close)
        cikis.setCursor(Qt.PointingHandCursor)
        sl.addWidget(cikis)
        
        # Saat
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignCenter)
        self.clock.setStyleSheet(f"color:{Theme.DARK['text_sub']};font-size:11px;padding:10px;")
        sl.addWidget(self.clock)
        
        ml.addWidget(sidebar)
        
        # === İÇERİK ===
        icerik = QWidget()
        il = QVBoxLayout(icerik)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(0)
        
        # Topbar
        topbar = QFrame()
        topbar.setFixedHeight(65)
        topbar.setStyleSheet(f"background:{Theme.DARK['bg']};border-bottom:1px solid {Theme.DARK['border']};")
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(30, 0, 30, 0)
        
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet(f"color:{Theme.DARK['text']};font-size:20px;font-weight:800;")
        tl.addWidget(self.page_title)
        tl.addStretch()
        
        yenile = QPushButton("🔄 Yenile")
        yenile.setStyleSheet(f"background:{Theme.DARK['card']};color:{Theme.DARK['text']};border:1px solid {Theme.DARK['border']};border-radius:6px;padding:8px 15px;font-size:12px;")
        yenile.clicked.connect(self._refresh)
        yenile.setCursor(Qt.PointingHandCursor)
        tl.addWidget(yenile)
        il.addWidget(topbar)
        
        # Stack
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.sistem)
        self.islem_page = IslemPage(self.sistem)
        self.gecmis_page = GecmisPage(self.sistem)
        
        self.stack.addWidget(self.dashboard_page)  # 0
        self.stack.addWidget(self.islem_page)      # 1
        self.stack.addWidget(self.gecmis_page)     # 2
        
        il.addWidget(self.stack)
        ml.addWidget(icerik)
        
        self._navigate("Dashboard")
        self._clock_update()
        t = QTimer(self)
        t.timeout.connect(self._clock_update)
        t.start(1000)
    
    def _navigate(self, page_name):
        page_map = {
            "Dashboard": 0,
            "Kitap Yönetimi": 1,
            "Üye Yönetimi": 1,
            "Ödünç İşlemleri": 1,
            "İşlem Geçmişi": 2,
        }
        
        index = page_map.get(page_name, 0)
        self.stack.setCurrentIndex(index)
        self.page_title.setText(page_name)
        
        # Buton güncelle
        names = ["Dashboard", "Kitap Yönetimi", "Üye Yönetimi", "Ödünç İşlemleri", "İşlem Geçmişi"]
        for i, btn in enumerate(self.nav_buttons):
            if i < len(names):
                btn.setChecked(names[i] == page_name)
        
        # Sekme geçişi
        if index == 1:
            if page_name == "Kitap Yönetimi":
                self.islem_page.tab_widget.setCurrentIndex(0)
            elif page_name == "Üye Yönetimi":
                self.islem_page.tab_widget.setCurrentIndex(1)
            elif page_name == "Ödünç İşlemleri":
                self.islem_page.tab_widget.setCurrentIndex(2)
            self.islem_page._load_data()
        elif index == 0:
            self.dashboard_page.refresh()
        elif index == 2:
            self.gecmis_page._load_data()
    
    def _refresh(self):
        i = self.stack.currentIndex()
        if i == 0:
            self.dashboard_page.refresh()
        elif i == 1:
            self.islem_page._load_data()
        elif i == 2:
            self.gecmis_page._load_data()
    
    def _clock_update(self):
        self.clock.setText(datetime.now().strftime("%d.%m.%Y\n%H:%M:%S"))