from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading,sys,os,time,datetime,shutil,winutils,subprocess,pyautogui,webbrowser
from themeParser import parse
import urllib.request
from mimetypes import MimeTypes
from hurry.filesize import size
import pythoncom,requests,bs4
import pyperclip
from send2trash import send2trash

DEFAULT_SETTINGS="PROMPT:True;2\nDEVELOPER_MODE:False\nDOUBLE-CLICK_OPEN:False\nDC_INSIDE:True\nAUTO_REPLACE:False"
SETTING_NAMES = "PROMPT:;DEVELOPER_MODE:;DOUBLE-CLICK_OPEN:;DC_INSIDE:;AUTO_REPLACE:".split(";")
VERSION = "1.0"

class SettingsWindow(QWidget):
    def __init__(self,THEME,parent=None):
        super(SettingsWindow,self).__init__(parent)
        self.setGeometry(100,100,10,100)
        self.setStyleSheet(parse("settingsBody",THEME).getStyle())
        self.setWindowOpacity(0.0)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(r"Icons\settings.png"))

        cover = QPushButton(self)
        cover.setIcon(QIcon(r"Icons\settingsCover.png"))
        cover.setStyleSheet("background-color:none;border:0;")
        cover.setIconSize(QSize(500,300))
        cover.move(0,-70)

        self.prompt = QCheckBox(self)
        self.prompt.setStyleSheet(parse("checkBox",THEME).getStyle())
        self.prompt.move(30,190)
        self.prompt.stateChanged.connect(self.promptStateChange)

        self.prompt_list = "1 2 3 4 5 6 8 10 15".split(" ")

        self.prompt_no = QComboBox(self)
        self.prompt_no.addItem("1")
        self.prompt_no.addItem("2")
        self.prompt_no.addItem("3")
        self.prompt_no.addItem("4")
        self.prompt_no.addItem("5")
        self.prompt_no.addItem("6")
        self.prompt_no.addItem("8")
        self.prompt_no.addItem("10")
        self.prompt_no.addItem("15")
        self.prompt_no.setGeometry(530,204,50,23)
        self.prompt_no.setStyleSheet(parse("settingComboBox",THEME).getStyle())

        self.developer_mode = QCheckBox(self)
        self.developer_mode.setStyleSheet(parse("checkBox",THEME).getStyle())
        self.developer_mode.move(30,233)

        self.label = QLabel(self)
        self.label.setStyleSheet(parse("setingsLabel",THEME).getStyle())
        self.label.move(85,204)
        self.label.setText("Prompt for confirmation when copying/moving item more than : <br><br>Developer Mode<span style = 'color:grey;font-size:14px;'>  Will automatically launch BM 2 next time</span>")

        self.dblclk_setting = QRadioButton(self)
        self.dblclk_setting.setStyleSheet(parse("radioButton",THEME).getStyle())
        self.dblclk_setting.move(30,277)
       
        self.dblclk_setting2 = QRadioButton(self)
        self.dblclk_setting2.setStyleSheet(parse("radioButton",THEME).getStyle())
        self.dblclk_setting2.move(30,322)

        self.label2 = QLabel(self)
        self.label2.setStyleSheet(parse("setingsLabel",THEME).getStyle())
        self.label2.move(85,290)
        self.label2.setText("Double Clicking an item will open the selected file/folder.")
        
        self.label2 = QLabel(self)
        self.label2.setStyleSheet(parse("setingsLabel",THEME).getStyle())
        self.label2.move(85,335)
        self.label2.setText("Double Clicking an item will open the selected folder/directory inside B.M.")
        
        self.replace_checkBox = QCheckBox(self)
        self.replace_checkBox.setStyleSheet(parse("checkBox",THEME).getStyle())
        self.replace_checkBox.move(30,355+15)

        self.label2 = QLabel(self)
        self.label2.setStyleSheet(parse("setingsLabel",THEME).getStyle())
        self.label2.move(85,335+49)
        self.label2.setText("Automatically replace file if the same exists in other directory")

        self.next_btn = ""

        note = QLabel(self)
        note.setStyleSheet(parse("setingsLabel_NOTE",THEME).getStyle())
        note.move(10,570)
        note.setText("<b> Note: </b> You may need to restart Backup Manager 2 in order to apply some settings")

        save=QPushButton(self)
        save.setGeometry(450,504,120,50)
        save.setStyleSheet(parse("setingsSaveBtn",THEME).getStyle())
        save.setIcon(QIcon(r"Icons\save.png"))
        save.setCursor(Qt.PointingHandCursor)
        save.setIconSize(QSize(70,70))
        save.clicked.connect(self.save)
            
    def promptStateChange(self):
        if self.prompt.isChecked():
            self.prompt_no.setDisabled(False)
            self.label.setText("Prompt for confirmation when copying/moving item more than : <br><br>Developer Mode<span style = 'color:grey;font-size:14px;'>  Will automatically launch BM 2 next time</span>")
        else:
            self.prompt_no.setDisabled(True)
            self.label.setText("<span style = 'color:grey;'>Prompt for confirmation when copying/moving item more than : </span><br><br>Developer Mode<span style = 'color:grey;font-size:14px;'>  Will automatically launch BM 2 next time</span>")
    def win(self,stdio):
        self.setWindowOpacity(0.0)
        # screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(600,600)
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.stdio = stdio
        thread = threading.Thread(target=self.animate)
        thread.start()

        settings = get_settings(stype="prompt")
        settings2 = get_settings(stype="developer_mode")
        settings3 = get_settings(stype="dbl_click")
        settings4 = get_settings(stype="dc_in")
        settings5 = get_settings(stype="auto_replace")
        print(">>>>AUTO REPLACE : "+settings5)
        if settings == 100:
            self.prompt_no.setDisabled(True)
            self.label.setText("<span style = 'color:grey;'>Prompt for confirmation when copying/moving item more than : </span><br><br>Developer Mode<span style = 'color:grey;font-size:14px;'>  Will automatically launch BM 2 next time</span>")
        else:
            self.prompt_no.setDisabled(False)
            self.prompt_no.setCurrentIndex(self.prompt_list.index(str(settings)))
            self.prompt.setChecked(True)
            self.label.setText("Prompt for confirmation when copying/moving item more than : <br><br>Developer Mode<span style = 'color:grey;font-size:14px;'>  Will automatically launch BM 2 next time</span>")
            

        if settings2 == "True":
            self.developer_mode.setChecked(True)
        
        if "True" in settings3:
            self.dblclk_setting.setChecked(True)
        else:
            self.dblclk_setting2.setChecked(True)

        if "True" in settings5:
            self.replace_checkBox.setChecked(True)
        else:
            self.replace_checkBox.setChecked(False)

        self.show()
    def animate(self):
        opcty = 0.0
        for i in range(10):
            time.sleep(0.06)
            self.setWindowOpacity(opcty)
            opcty+=0.1
    def save(self):
        print(validate_file(location=r"Data\settings"))
        S_file = open(r'Data\settings','w')
        # print(s())
        S_file.write("PROMPT:"+str(self.prompt.isChecked())+ ";" + self.prompt_no.currentText()  +"\nDEVELOPER_MODE:"+str(self.developer_mode.isChecked()) + "\nDOUBLE-CLICK_OPEN:"+str(self.dblclk_setting.isChecked())+"\nDC_INSIDE:"+str(self.dblclk_setting2.isChecked())+"\nAUTO_REPLACE:"+str(self.replace_checkBox.isChecked()))
        S_file.close()

        self.close()
        self.stdio.showNotification()

class StudioMain(QWidget):
    def __init__(self,parent=None):
        super(StudioMain,self).__init__(parent)
        self.theme = ""
        self.setting = ""
        self.folder1 = ""
        self.folder2 = ""
        self.selectedFiles1 = []
        self.selectedFiles2 = []
        self.currentlySelectedBtn = ""
        self.currentButtonSide = 0
        self.settings = get_settings(stype="prompt")
        self.multi_selection_state = False
        self.new_file1 = []
        self.new_file2 = []
        self.old_newFile1 = ""
        self.old_newFile2 = ""
        self.animation_complete1 = []
        self.animation_complete2 = []
        self.oldKey1 = ""
        self.oldKey2 = ""
        self.forward_dir = []
        self.forward_dir2 = []
        self.dc_in = False
        self.visitedLocations1 = []
        self.visitedLocations2 = []
        self.itemHeight = 35
        self.actionOngoing = "NO"
        # self.next_btn = ""
        settings3 = get_settings(stype="dbl_click")
        self.dblClickOpen = False
        if "True" in settings3 :
            self.dblClickOpen = True
        else:
            self.dc_in = True
        settings5 = get_settings(stype="auto_replace")
        if "True" in settings5:
            self.auto_replace = True
        else:
            self.auto_replace = False

        self.prompt_int = int(self.settings)

    def window(self):

        
        self.move(0,0)
        thread = threading.Thread(target=self.animate)
        thread.start()
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(Qt.AA_DontShowIconsInMenus)
        font = QFont("Ubuntu",25)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)
        self.setWindowIcon(QIcon(r"Icons\\2.png"))
        self.setWindowTitle("Backup Manager 2")
        self.resize(screen.width(),screen.height()-40)
        position_animator(self,0,screen.width(),0,0,duration=600)
        #MACBOOK (BELOW)
        # self.resize(1440,900)
        # self.resize(1440,800)
        # self.resize(1366,768)
        self.setStyleSheet(parse("MainBody",self.theme).getStyle())

        # print(self.theme)

        THEME = self.theme
        HEIGHT = self.height()
        WIDTH  = self.width()

        FILES  = os.listdir(self.folder1)
        FILES.sort()

        FILES2  = os.listdir(self.folder2)
        FILES2.sort()
        if self.setting == "SAF":
            pass
        elif self.setting == "SCF":
            SCF_FILES = list(set(FILES).intersection(FILES2))
            FILES = SCF_FILES
            FILES2 = SCF_FILES
        elif self.setting == "HCF":
            for i in FILES[:]:
                if i in FILES2:
                    FILES.remove(i)
                    FILES2.remove(i)

        self.files1 = FILES
        self.files2 = FILES2

        title = QPushButton(self)
        title.setGeometry(0,0,WIDTH,40)
        title.setStyleSheet(parse("titleBar",THEME).getStyle())
        title.setIcon(QIcon(r"Icons\title.png"))
        title.setIconSize(QSize(200,200))
        
        close = QPushButton(self)
        close.setGeometry(WIDTH-45,0,46,40)
        close.setStyleSheet(parse("closeBtn",THEME).getStyle())
        close.setIcon(QIcon(r"Icons\close.png"))
        close.setIconSize(QSize(13,13))
        close.setCursor(Qt.PointingHandCursor)
        close.clicked.connect(self.close)
        
        minim = QPushButton(self)
        minim.setGeometry(WIDTH-90,0,46,40)
        minim.setStyleSheet(parse("minimizeBtn",THEME).getStyle())
        minim.setIcon(QIcon(r"Icons\minimize.png"))
        minim.setIconSize(QSize(12,12))
        minim.setCursor(Qt.PointingHandCursor)
        minim.clicked.connect(self.showMinimized)
        
        settings_windows = SettingsWindow(THEME)

        self.aboutWin = QWidget(self)
        self.aboutWin.resize(self.width(),self.height()-40)
        self.aboutWin.move(0,40)
        # self.aboutWin.setWindowTitle("Please Wait")
        self.aboutWin.setStyleSheet(parse("aboutWin",THEME).getStyle())
        self.aboutWin.setWindowFlags(QtCore.Qt.FramelessWindowHint|Qt.SplashScreen)

        aw = self.aboutWin
        self.aboutLogo = QPushButton(aw)
        self.aboutLogo.setIcon(QIcon(r"Icons\aboutWindow.png"))
        self.aboutLogo.setIconSize(QSize(600,577))
        self.aboutLogo.move((aw.width()/2)-self.aboutLogo.width()-220,(aw.height()/2)-280)

        self.aboutBackBtn = QPushButton(aw)
        self.aboutBackBtn.setGeometry(20,20,150,50)
        self.aboutBackBtn.setText("   Back")
        self.aboutBackBtn.setStyleSheet(parse("about_BackBtn",THEME).getStyle())
        self.aboutBackBtn.setIcon(QIcon(r"Icons\back.png"))
        self.aboutBackBtn.clicked.connect(self.aboutBack)
        self.aboutBackBtn.setCursor(Qt.PointingHandCursor)

        settingBtn = QPushButton(self)
        settingBtn.setGeometry(WIDTH-150,0,50,40)
        settingBtn.setStyleSheet(parse("titlebtn",THEME).getStyle())
        settingBtn.setIcon(QIcon(r"Icons\settings.png"))
        settingBtn.setIconSize(QSize(18,18))
        settingBtn.setCursor(Qt.PointingHandCursor)
        # settingBtn.setText("    Settings   ")
        settingBtn.setToolTip("Settings")
        settingBtn.clicked.connect(lambda: settings_windows.win(self))


        self.aboutBtn = QPushButton(self)
        self.aboutBtn.setGeometry(WIDTH-(150+50),0,50,40)
        self.aboutBtn.setStyleSheet(parse("titlebtn",THEME).getStyle())
        self.aboutBtn.setIcon(QIcon(r"Icons\aboutIcon.png"))
        self.aboutBtn.setIconSize(QSize(18,18))
        self.aboutBtn.setToolTip("About")
        self.aboutBtn.clicked.connect(self.showAboutWin)
        self.aboutBtn.setCursor(Qt.PointingHandCursor)



        self.helpWin = QWidget(self)
        self.helpWin.resize(self.width(),self.height()-40)
        self.helpWin.move(0,40)
        self.helpWin.setStyleSheet(parse("helpWin",THEME).getStyle())
        self.helpWin.setWindowFlags(QtCore.Qt.FramelessWindowHint|Qt.SplashScreen)
        
        self.helpImage = QPushButton(self.helpWin)
        if "dark" in THEME:
            self.helpImage.setIcon(QIcon(r"Icons\aboutBM_DARK.png"))
        else:
            self.helpImage.setIcon(QIcon(r"Icons\aboutBM.png"))
        self.helpImage.setIconSize(QSize(1000,1000))
        self.helpImage.move(0,-100)

        self.helpBtn = QPushButton(self)
        self.helpBtn.setGeometry(WIDTH-(150+50+50),0,50,40)
        self.helpBtn.setStyleSheet(parse("titlebtn",THEME).getStyle())
        self.helpBtn.setIcon(QIcon(r"Icons\help2.png"))
        self.helpBtn.setIconSize(QSize(18,18))
        self.helpBtn.setToolTip("Help")
        self.helpBtn.clicked.connect(self.showHelpWin)
        self.helpBtn.setCursor(Qt.PointingHandCursor)
        
        self.helpBackBtn = QPushButton(self.helpWin)
        self.helpBackBtn.setGeometry(43,20,150,50)
        self.helpBackBtn.setText("   Back")
        self.helpBackBtn.setStyleSheet(parse("about_BackBtn",THEME).getStyle())
        self.helpBackBtn.setIcon(QIcon(r"Icons\back.png"))
        self.helpBackBtn.clicked.connect(self.helpBack)
        self.helpBackBtn.setCursor(Qt.PointingHandCursor)



        self.updateWin = QWidget(self)
        self.updateWin.resize(self.width(),self.height()-40)
        self.updateWin.move(0,40)
        self.updateWin.setStyleSheet(parse("updateWin",THEME).getStyle())
        self.updateWin.setWindowFlags(QtCore.Qt.FramelessWindowHint|Qt.SplashScreen)

        
        movie = QtGui.QMovie(r"Icons\loader2.gif")
        movie.setScaledSize(QSize(800,600))
        self.checkingBtn_loader = QLabel(self.updateWin)
        self.checkingBtn_loader.setStyleSheet(parse("updateLabel",THEME).getStyle())
        self.checkingBtn_loader.move(self.updateWin.width()/2-self.checkingBtn_loader.width()-300,self.updateWin.height()/2-350)
        self.checkingBtn_loader.setMovie(movie)
        movie.start()

        updateScroller = QScrollBar(self.updateWin)
        updateScroller.setStyleSheet(parse("scrollBar",THEME).getStyle())

        self.checkingBtn = QTextEdit(self.updateWin)
        self.checkingBtn.setText("Checking For Updates")
        self.checkingBtn.setStyleSheet(parse("updateLabel",THEME).getStyle())
        self.checkingBtn.resize(1300,self.height()-160)
        self.checkingBtn.setAlignment(Qt.AlignTop)
        self.checkingBtn.setReadOnly(True)
        self.checkingBtn.move(self.updateWin.width()/2-self.checkingBtn.width()/2+400,self.updateWin.height()/2+100)
        self.checkingBtn.setVerticalScrollBar(updateScroller)


        
        self.updateBackBtn = QPushButton(self.updateWin)
        self.updateBackBtn.setGeometry(43,20,150,50)
        self.updateBackBtn.setText("   Back")
        self.updateBackBtn.setStyleSheet(parse("about_BackBtn",THEME).getStyle())
        self.updateBackBtn.setIcon(QIcon(r"Icons\back.png"))
        self.updateBackBtn.clicked.connect(self.updateBack)
        self.updateBackBtn.setCursor(Qt.PointingHandCursor)
        
        self.updateNow = QPushButton(self.updateWin)
        self.updateNow.setStyleSheet(parse("about_BackBtn",THEME).getStyle())
        # self.updateNow.clicked.connect(self.openUpdtWebsite)
        self.updateNow.setCursor(Qt.PointingHandCursor)
        self.updateNow.setText("Download Now")
        self.updateNow.setGeometry(self.updateBackBtn.x()+self.updateBackBtn.width()+30,-100,180,50)
        
        self.updateBtn = QPushButton(self)
        self.updateBtn.setGeometry(WIDTH-(150+50+50+50),0,50,40)
        self.updateBtn.setStyleSheet(parse("titlebtn",THEME).getStyle())
        self.updateBtn.setIcon(QIcon(r"Icons\update.png"))
        self.updateBtn.setIconSize(QSize(18,18))
        self.updateBtn.setToolTip("Check for Updates")
        self.updateBtn.clicked.connect(self.showUpdatesWin)
        self.updateBtn.setCursor(Qt.PointingHandCursor)
 


        self.loading = QWidget()
        self.loading.resize(200,200)
        self.loading.move(QtGui.QApplication.desktop().screen().rect().center()- self.loading.rect().center())
        self.loading.setWindowTitle("Please Wait")
        self.loading.setStyleSheet(parse("loadingWin",THEME).getStyle())
        self.loading.setWindowFlags(QtCore.Qt.FramelessWindowHint|Qt.SplashScreen)
        
        
        self.loading_label = QLabel(self.loading)
        self.loading_label2 = QLabel(self.loading)
        self.loading_label2.move(60,150)
        self.loading_label2.setText("<span style='font-size:20px;'>Loading . . .</span>")
        movie = QtGui.QMovie(r"Icons\loading.gif")
        movie.setScaledSize(QSize(198,150))
        self.loading_label.setMovie(movie)
        self.loading_label.move(1,1)
        movie.start()
        self.loading.setWindowIcon(QIcon(r'Icons\2.png'))

        self.prop_win = QWidget()
        self.prop_win.resize(500,500)
        self.prop_win.move(QtGui.QApplication.desktop().screen().rect().center()- self.prop_win.rect().center())
        self.prop_win.setWindowTitle("Properties")
        self.prop_win.setStyleSheet(parse("propertiesWin",THEME).getStyle())
        

        self.prop_label = QLabel(self.prop_win)
        self.prop_label.move(30,30)
        self.prop_label.resize(400,450)
        self.prop_label.setStyleSheet("font-size:15px;")
        self.prop_label.linkActivated.connect(self.fetchExtensionDetail)

        self.prop_name = QLabel(self.prop_win)
        self.prop_name.setGeometry(150,20,320,100)
        # self.prop_name.move(150,20)
        self.prop_name.setWordWrap(True)
        self.prop_name.setStyleSheet("font-size:20px;")
        
        self.prop_icon = QPushButton(self.prop_win)
        self.prop_icon.move(20,20)
        self.prop_icon.setStyleSheet("border:0;background-color:transparent;")



        self.copy_right = QPushButton(self)
        self.copy_right.setIcon(QIcon(r"Icons\copy_RIGHT.png"))
        self.copy_right.setIconSize(QSize(50,50))
        self.copy_right.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.copy_right.move((self.width()/2)-36,140)
        self.copy_right.resize(QSize(70,70))
        self.copy_right.setCursor(Qt.PointingHandCursor)
        self.copy_right.setToolTip("Copy Selected File(s) to Right        ")
        self.copy_right.setDisabled(True)
        self.copy_right.clicked.connect(self.copy_file_right)


        self.copy_left = QPushButton(self)
        self.copy_left.setIcon(QIcon(r"Icons\copy_LEFT.png"))
        self.copy_left.setIconSize(QSize(50,50))
        self.copy_left.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.copy_left.move((self.width()/2)-36,200+20)
        self.copy_left.resize(70,70)
        self.copy_left.setCursor(Qt.PointingHandCursor)
        self.copy_left.setToolTip("Copy Selected File(s) to Left       ")
        self.copy_left.setDisabled(True)
        self.copy_left.clicked.connect(self.copy_file_left)

        self.move_right = QPushButton(self)
        self.move_right.setIcon(QIcon(r"Icons\move_RIGHT.png"))
        self.move_right.setIconSize(QSize(50,50))
        self.move_right.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.move_right.move((self.width()/2)-36,270+30)
        self.move_right.resize(70,70)
        self.move_right.setCursor(Qt.PointingHandCursor)
        self.move_right.setToolTip("Move Selected File(s) to Right       ")
        self.move_right.setDisabled(True)
        self.move_right.clicked.connect(self.move_file_right)

        self.move_left = QPushButton(self)
        self.move_left.setIcon(QIcon(r"Icons\move_LEFT.png"))
        self.move_left.setIconSize(QSize(50,50))
        self.move_left.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.move_left.move((self.width()/2)-36,340+40)
        self.move_left.resize(70,70)
        self.move_left.setCursor(Qt.PointingHandCursor)
        self.move_left.setToolTip("Move Selected File(s) to Left       ")
        self.move_left.setDisabled(True)
        self.move_left.clicked.connect(self.move_file_left)

        self.send_to_trash = QPushButton(self)
        self.send_to_trash.setIcon(QIcon(r"Icons\send_to_trash.png"))
        self.send_to_trash.setIconSize(QSize(50,50))
        self.send_to_trash.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.send_to_trash.move((self.width()/2)-36,410+50)
        self.send_to_trash.resize(70,70)
        self.send_to_trash.setCursor(Qt.PointingHandCursor)
        self.send_to_trash.setToolTip("Send Selected File(s) to Recycle Bin      ")
        self.send_to_trash.setDisabled(True)
        self.send_to_trash.clicked.connect(self.trash_file)
     
        self.delete_permanently = QPushButton(self)
        self.delete_permanently.setIcon(QIcon(r"Icons\delete.png"))
        self.delete_permanently.setIconSize(QSize(50,50))
        self.delete_permanently.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.delete_permanently.move((self.width()/2)-36,480+60)
        self.delete_permanently.resize(70,70)
        self.delete_permanently.setCursor(Qt.PointingHandCursor)
        self.delete_permanently.setToolTip("Delete Selected File(s) Permanently       ")
        self.delete_permanently.setDisabled(True)
        self.delete_permanently.clicked.connect(self.delete_file)
     
        self.multi_select = QPushButton(self)
        self.multi_select.setIcon(QIcon(r"Icons\multiselect_DIS.png"))
        self.multi_select.setIconSize(QSize(40,40))
        self.multi_select.resize(70,70)
        self.multi_select.setStyleSheet(parse("actionButtons",THEME).getStyle())
        self.multi_select.move((self.width()/2)-36,573+50)
        self.multi_select.setCursor(Qt.PointingHandCursor)
        self.multi_select.setToolTip("Toggle Multiple Selection      ")
        self.multi_select.clicked.connect(self.togglemultiselection)


        self.mdi = QMdiArea(self)
        self.mdi.setGeometry(10,140,(WIDTH/2)-100,(HEIGHT/2)+200)
        self.mdi.setStyleSheet("background-color:white;")
        self.mdi.setAttribute(Qt.WA_TranslucentBackground)
        self.mdi.setBackground(QtGui.QColor('#ffffff'))
        
        
        #-----
        self.viewMenu = QtGui.QMenu(self)
        self.viewMenu.setStyleSheet(parse("PopMenu2",THEME).getStyle())
        self.big = self.viewMenu.addAction("Big View")
        self.big.triggered.connect(self.viewBig)
        
        self.normal = self.viewMenu.addAction("Normal View")
        self.normal.triggered.connect(self.viewNormal)

        self.compact = self.viewMenu.addAction("Compact View")
        self.compact.triggered.connect(self.viewCompact)
        
        self.small = self.viewMenu.addAction("Small View")
        self.small.triggered.connect(self.viewSmall)

        self.viewBtn = QPushButton(self)
        self.viewBtn.setGeometry(self.mdi.width()+35,90,140,30)
        self.viewBtn.setStyleSheet(parse("viewButton",THEME).getStyle())
        self.viewBtn.setIcon(QIcon(r"Icons\view.png"))
        self.viewBtn.setIconSize(QSize(18,18))
        self.viewBtn.setToolTip("Change View")
        self.viewBtn.setText("   Normal View")
        self.viewBtn.setMenu(self.viewMenu)
        
        
        self.optionMenu = QtGui.QMenu(self)
        self.optionMenu.setStyleSheet(parse("PopMenu2",THEME).getStyle())
        self.all = self.optionMenu.addAction("Show All Files")
        self.all.triggered.connect(self.optionALL)
        
        self.scf = self.optionMenu.addAction("Show Common Files")
        self.scf.triggered.connect(self.optionSCF)

        self.hcf = self.optionMenu.addAction("Hide Common Files")
        self.hcf.triggered.connect(self.optionHCF)
        
        self.optionBtn = QPushButton(self)
        self.optionBtn.setGeometry(self.mdi.width()+35,50,140,30)
        self.optionBtn.setStyleSheet(parse("viewButton",THEME).getStyle())
        self.optionBtn.setIcon(QIcon(r"Icons\settings.png"))
        self.optionBtn.setIconSize(QSize(18,18))
        self.optionBtn.setToolTip("Change Option")
        if self.setting == "SAF":
            self.optionBtn.setText("   Show All Files")
        elif self.setting == "SCF":
            self.optionBtn.setText("   Show Common Files")
        else:
            self.optionBtn.setText("   Hide Common Files")
        self.optionBtn.setMenu(self.optionMenu)
        #------

        self.shortScreenHider = QPushButton(self)
        self.shortScreenHider.setGeometry(10,80,self.mdi.width(),30)
        self.shortScreenHider.setStyleSheet(parse("Default_Color",THEME).getStyle())

        self.goBack = QPushButton(self)
        self.goBack.setIcon(QIcon(r"Icons\back.png"))
        self.goBack.setIconSize(QSize(18,18))
        self.goBack.setGeometry(10,80,40,30)
        self.goBack.setToolTip("Go to Parent Directory")
        self.goBack.setStyleSheet(parse("back_forward_button",THEME).getStyle())
        self.goBack.clicked.connect(self.parentDir)

        if self.folder1 == os.path.abspath(os.path.join(self.folder1, os.pardir)):
            self.goBack.setDisabled(True)

        self.forward = QPushButton(self)
        self.forward.setIcon(QIcon(r"Icons\forward.png"))
        self.forward.setIconSize(QSize(18,18))
        self.forward.setGeometry(50,80,40,30)
        self.forward.setToolTip("Go to Previous Directory")
        self.forward.setStyleSheet(parse("back_forward_button",THEME).getStyle())
        self.forward.clicked.connect(self.forwardDir)
        self.forward.setDisabled(True)


        self.newFolderBtn = QPushButton(self)
        self.newFolderBtn.setGeometry(70+20,80,110,30)
        self.newFolderBtn.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.newFolderBtn.clicked.connect(self.createNewFolder1)
        self.newFolderBtn.setIcon(QIcon(r"Icons\newFolder.png"))
        self.newFolderBtn.setIconSize(QSize(16,16))
        self.newFolderBtn.setText("New Folder")
        
        self.openFile = QPushButton(self)
        self.openFile.setGeometry(70+110+20,80,110,30)
        self.openFile.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.openFile.setIcon(QIcon(r"Icons\open.png"))
        self.openFile.setIconSize(QSize(16,16))
        self.openFile.setText("Pop Open")
        self.openFile.clicked.connect(self.popOpen)
        self.openFile.setDisabled(True)
        
        self.renameFile = QPushButton(self)
        self.renameFile.setGeometry(70+110+110+20,80,100,30)
        self.renameFile.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.renameFile.setIcon(QIcon(r"Icons\rename.png"))
        self.renameFile.setIconSize(QSize(18,18))
        self.renameFile.setText("Rename")
        self.renameFile.clicked.connect(self.rename)
        self.renameFile.setDisabled(True)
        
        self.selectBtn = QPushButton(self)
        self.selectBtn.setGeometry(70+110+110+90+30,80,160,30)
        self.selectBtn.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.selectBtn.setIcon(QIcon(r"Icons\select.png"))
        self.selectBtn.setIconSize(QSize(18,18))
        self.selectBtn.setText("Select All")
        self.selectBtn.clicked.connect(self.selectBtnFunc)
       
        self.openInside = QPushButton(self)
        self.openInside.setGeometry(70+110+110+90+30+160,80,140,30)
        self.openInside.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.openInside.clicked.connect(self.openDirInside)
        self.openInside.setIcon(QIcon(r"Icons\folder2.png"))
        self.openInside.setIconSize(QSize(16,16))
        self.openInside.setText("Open Folder Here")
        self.openInside.setDisabled(True)

        if self.openInside.x()+self.openInside.width() < self.mdi.x()+self.mdi.width()+1:
            print("Not Overlapping")
        else:
            self.openInside.move(-1000,0)
        
        self.locationBar = QPushButton(self)
        self.locationBar.setGeometry(10,50,self.mdi.width(),30)
        self.locationBar.setStyleSheet(parse("LocationBar",THEME).getStyle())
        self.locationBar.setIcon(QIcon(r"Icons\location.png"))
        self.locationBar.setIconSize(QSize(18,18))
        self.locationBar.setText(self.folder1.replace("\\","  >  "))
        self.locationBar.clicked.connect(self.reSelect1)
        
        
        self.recentMenu = QtGui.QMenu(self)
        self.recentMenu.setStyleSheet(parse("PopMenu2",THEME).getStyle())
        self.action = self.recentMenu.addAction(self.folder1)
        self.action.triggered.connect(self.changeLocation)
        self.visitedLocations1.append(self.folder1)

        self.recentFoldersBtn = QPushButton(self)
        self.recentFoldersBtn.setGeometry(self.mdi.width()+10-30,50,30,30)
        self.recentFoldersBtn.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.recentFoldersBtn.setIcon(QIcon(r"Icons\folderRecent.png"))
        self.recentFoldersBtn.setIconSize(QSize(18,18))
        self.recentFoldersBtn.setToolTip("Recently Visited Locations")
        self.recentFoldersBtn.setMenu(self.recentMenu)

        self.sourceFolder = QPushButton(self)
        self.sourceFolder.setGeometry(self.mdi.width()+10-90,50,30,30)
        self.sourceFolder.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.sourceFolder.setIcon(QIcon(r"Icons\folder.png"))
        self.sourceFolder.setIconSize(QSize(18,18))
        self.sourceFolder.setToolTip("Open Source Folder")
        self.sourceFolder.clicked.connect(lambda: os.startfile(self.folder1))
        
        self.refreshBtn = QPushButton(self)
        self.refreshBtn.setGeometry(self.mdi.width()+10-60,50,30,30)
        self.refreshBtn.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.refreshBtn.setIcon(QIcon(r"Icons\refresh.png"))
        self.refreshBtn.setIconSize(QSize(18,18))
        self.refreshBtn.setToolTip("Refresh Files")
        self.refreshBtn.clicked.connect(self.refreshFiles)
        

        self.search1 = QLineEdit(self)
        self.search1.setGeometry(10,110,self.mdi.width(),30)
        self.search1.setPlaceholderText("Search for Items")
        self.search1.setStyleSheet(parse("searchBox",THEME).getStyle())
        self.search1.textChanged.connect(self.searchitem1)
    
        self.closeSearch1 = QPushButton(self)
        self.closeSearch1.clicked.connect(lambda:self.search1.setText(""))
        self.closeSearch1.setGeometry(self.search1.width()-21,110,30,0)
        self.closeSearch1.setStyleSheet(parse("clearSearchButton",THEME).getStyle())
        self.closeSearch1.setIcon(QIcon(r'Icons\close.png'))
        self.closeSearch1.setIconSize(QSize(12,12))

        self.workspace1 = QMdiSubWindow(self.mdi)
        self.workspace1.setWindowFlags(Qt.FramelessWindowHint)
        self.workspace1.setGeometry(0,0,self.mdi.width()-100,self.mdi.height())
        self.workspace1.setStyleSheet(parse("explorerBox",THEME).getStyle())

        workspace1_sc = QMdiSubWindow(self.mdi)
        workspace1_sc.setWindowFlags(Qt.FramelessWindowHint)
        workspace1_sc.setGeometry(self.mdi.width()-30,0,30,self.mdi.height())

        self.scroller = QScrollBar(workspace1_sc)
        self.scroller.setGeometry(0,0,30,self.mdi.height())
        self.scroller.setStyleSheet(parse("scrollBar",THEME).getStyle())

        self.animator = QPushButton(self.workspace1)
        self.animator.setGeometry(-1000,0,self.mdi.width()-40,40)
        self.animator.setStyleSheet(parse("FileExplorerBtn_SELECTED",THEME).getStyle())
        
        self.s_animator = QPushButton(self.workspace1)
        self.s_animator.setGeometry(-1000,0,self.mdi.width()-40,40)
        self.s_animator.setStyleSheet(parse("FileExplorerBtn_SUCCESS(COLOR-ONLY)",THEME).getStyle())

        pos = 5
        for i in FILES:
            btn = QPushButton(self.workspace1)
            btn.setText(i)
            btn.setObjectName(i)
            btn.setGeometry(7,pos,self.mdi.width()-40,self.itemHeight)
            btn.setStyleSheet(parse("FileExplorerBtn",THEME).getStyle())
            btn.installEventFilter(self)
            btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(self.on_context_menu)
            btn.clicked.connect(lambda: self.select1())
            

            fileInfo = QtCore.QFileInfo(self.folder1 + "\\" +i)
            iconProvider = QtGui.QFileIconProvider()
            icon = iconProvider.icon(fileInfo)
            btn.setIcon(QIcon(icon))

            btn.type = QLabel(self.workspace1)
            btn.type.setText(iconProvider.type(fileInfo))
            btn.type.setGeometry(self.mdi.width()-250,pos,200,self.itemHeight)
            btn.type.setStyleSheet(parse("FileExplorerBtn",THEME).getStyle())

            from hurry.filesize import size

            btn.size = QLabel(self.workspace1)
            btn.size.setText(str(size(fileInfo.size())))
            btn.size.setGeometry(self.mdi.width()-150,pos,200,self.itemHeight)
            btn.size.setStyleSheet(parse("FileExplorerBtn",THEME).getStyle())
            
            pos+=self.itemHeight
        
        self.bottom_border2 = QPushButton(self)
        self.bottom_border2.setGeometry(self.mdi.x(),self.mdi.y()+self.mdi.height(),self.mdi.width(),2)
        self.bottom_border2.setStyleSheet(parse("explorerBox",THEME).getStyle())
        
        self.searchResultCount = QPushButton(self)
        self.searchResultCount.setGeometry(self.mdi.x()+2,self.mdi.y()+self.mdi.height()-30,self.mdi.width()-30,0)
        self.searchResultCount.setStyleSheet(parse("noResultFound",THEME).getStyle())
        self.searchResultCount.setText("No Match Found")

        self.popMenu = QtGui.QMenu(self.workspace1)
        # self.action1 = self.popMenu.addAction('Unexpected Error!')
        # self.action1.setEnabled(False)

        self.popMenu.addSeparator()
        self.action2 = self.popMenu.addAction('Open')
        self.action2.triggered.connect(self.popOpen)
        # self.action2.setIcon(QIcon(r"Icons\open2.png"))
        self.action3 = self.popMenu.addAction('Open Inside')
        # self.action3.setIcon(QIcon(r"Icons\folder2.png"))
        self.action3.triggered.connect(self.openDirInside)
        self.action4 = self.popMenu.addAction('Reveal in Explorer')
        # self.action4.setIcon(QIcon(r"Icons\reveal.png"))
        self.action4.triggered.connect(self.reveal)
        self.action5 = self.popMenu.addAction('Rename..')
        # self.action5.setIcon(QIcon(r"Icons\rename2.png"))
        self.action5.triggered.connect(self.rename)

        self.action7 = self.popMenu.addMenu('Copy Name/Path')
        self.action7_name = self.action7.addAction("Copy Name")
        self.action7_path = self.action7.addAction("Copy Path")
        self.action7_name.triggered.connect(self.copyName)
        self.action7_path.triggered.connect(self.copyPath)

        self.action6 = self.popMenu.addAction('Properties')
        self.action6.triggered.connect(self.showProperties)

        self.popMenu.setStyleSheet(parse("PopMenu2",THEME).getStyle())

        self.workspace1.resize(self.mdi.width()-30 ,pos+650)
        self.scroller.setMaximum(pos-400)
        self.scroller.sliderMoved.connect(self.scroll1)

        # self.workspace1.resize(self.mdi.width()-30 ,pos+650)
        # if pos <= 400:
        #     self.scroller.setMaximum(pos)
        # else:
        #     self.scroller.setMaximum(pos-400)
        # self.scroller.sliderMoved.connect(self.scroll1)

        self.empty = QPushButton(self)
        self.empty.setIcon(QIcon(r"Icons\empty.png"))
        self.empty.setIconSize(QSize(400,400))
        self.empty.setStyleSheet("background-color:transparent;")

        if len(self.files1) == 0:
            self.empty.move(130,self.mdi.y()+100)
        else:
            self.empty.move(-1000,0)

        self.mdi2 = QMdiArea(self)
        self.mdi2.resize((WIDTH/2)-100,(HEIGHT/2)+200)
        self.mdi2.move(self.width() -(self.mdi2.width()+10),140)
        self.mdi2.setStyleSheet("background-color:white;")
        self.mdi2.setAttribute(Qt.WA_TranslucentBackground)
        self.mdi2.setBackground(QtGui.QColor('#ffffff'))

        self.shortScreenHider2 = QPushButton(self)
        self.shortScreenHider2.setGeometry(self.mdi2.x(),80,self.mdi.width(),30)
        self.shortScreenHider2.setStyleSheet(parse("Default_Color",THEME).getStyle())

        self.goBack2 = QPushButton(self)
        self.goBack2.setIcon(QIcon(r"Icons\back.png"))
        self.goBack2.setIconSize(QSize(18,18))
        self.goBack2.setGeometry(self.mdi2.x(),80,40,30)
        self.goBack2.setToolTip("Go to Parent Directory")
        self.goBack2.setStyleSheet(parse("back_forward_button",THEME).getStyle())
        self.goBack2.clicked.connect(self.parentDir2)

        if self.folder2 == os.path.abspath(os.path.join(self.folder2, os.pardir)):
            self.goBack2.setDisabled(True)

        self.forward2 = QPushButton(self)
        self.forward2.setIcon(QIcon(r"Icons\forward.png"))
        self.forward2.setIconSize(QSize(18,18))
        self.forward2.setGeometry(self.mdi2.x()+40,80,40,30)
        self.forward2.setToolTip("Go to Previous Directory")
        self.forward2.setStyleSheet(parse("back_forward_button",THEME).getStyle())
        self.forward2.clicked.connect(self.forwardDir2)
        self.forward2.setDisabled(True)


        self.newFolderBtn2 = QPushButton(self)
        self.newFolderBtn2.setGeometry(self.mdi2.x()+70+10,80,110,30)
        self.newFolderBtn2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.newFolderBtn2.clicked.connect(self.createNewFolder2)
        self.newFolderBtn2.setIcon(QIcon(r"Icons\newFolder.png"))
        self.newFolderBtn2.setIconSize(QSize(16,16))
        self.newFolderBtn2.setText("New Folder")
        
        self.openFile2 = QPushButton(self)
        self.openFile2.setGeometry(self.mdi2.x()+70+110+10,80,110,30)
        self.openFile2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.openFile2.setIcon(QIcon(r"Icons\open.png"))
        self.openFile2.setIconSize(QSize(16,16))
        self.openFile2.setText("Pop Open")
        self.openFile2.clicked.connect(self.popOpen2)
        self.openFile2.setDisabled(True)
        
        self.renameFile2 = QPushButton(self)
        self.renameFile2.setGeometry(self.mdi2.x()+70+110+110+10,80,100,30)
        self.renameFile2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.renameFile2.setIcon(QIcon(r"Icons\rename.png"))
        self.renameFile2.setIconSize(QSize(18,18))
        self.renameFile2.setText("Rename")
        self.renameFile2.clicked.connect(self.rename2)
        self.renameFile2.setDisabled(True)
        
        self.selectBtn2 = QPushButton(self)
        self.selectBtn2.setGeometry(self.mdi2.x()+70+110+110+90+20,80,160,30)
        self.selectBtn2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.selectBtn2.setIcon(QIcon(r"Icons\select.png"))
        self.selectBtn2.setIconSize(QSize(18,18))
        self.selectBtn2.setText("Select All")
        self.selectBtn2.clicked.connect(self.selectBtnFunc2)
        
        self.openInside2 = QPushButton(self)
        self.openInside2.setGeometry(self.mdi2.x()+70+110+110+90+20+160,80,140,30)
        self.openInside2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.openInside2.clicked.connect(self.openDirInside2)
        self.openInside2.setIcon(QIcon(r"Icons\folder2.png"))
        self.openInside2.setIconSize(QSize(16,16))
        self.openInside2.setText("Open Folder Here")
        self.openInside2.setDisabled(True)

        if self.openInside2.x()+self.openInside2.width() < self.mdi2.x()+self.mdi2.width()+1:
            print("Not Overlapping")
        else:
            self.openInside2.move(-1000,0)

        self.locationBar2 = QPushButton(self)
        self.locationBar2.setGeometry(self.mdi2.x(),50,self.mdi.width(),30)
        self.locationBar2.setStyleSheet(parse("LocationBar",THEME).getStyle())
        self.locationBar2.setIcon(QIcon(r"Icons\location.png"))
        self.locationBar2.setIconSize(QSize(18,18))
        self.locationBar2.setText(self.folder2.replace("\\","  >  "))
        self.locationBar2.clicked.connect(self.reSelect2)
        
        self.recentMenu2 = QtGui.QMenu(self)
        self.recentMenu2.setStyleSheet(parse("PopMenu2",THEME).getStyle())
        self.action_two = self.recentMenu2.addAction(self.folder2)
        self.visitedLocations2.append(self.folder2)
        self.action_two.triggered.connect(self.changeLocation2)

        self.recentFoldersBtn2 = QPushButton(self)
        self.recentFoldersBtn2.setGeometry(self.mdi2.x()+self.mdi2.width()-30,50,30,30)
        self.recentFoldersBtn2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.recentFoldersBtn2.setIcon(QIcon(r"Icons\folderRecent.png"))
        self.recentFoldersBtn2.setIconSize(QSize(18,18))
        self.recentFoldersBtn2.setToolTip("Recently Visited Locations")
        self.recentFoldersBtn2.clicked.connect(self.openRecentContext)
        self.recentFoldersBtn2.setMenu(self.recentMenu2)

        self.sourceFolder2 = QPushButton(self)
        self.sourceFolder2.setGeometry(self.mdi2.x()+self.mdi2.width()-90,50,30,30)
        self.sourceFolder2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.sourceFolder2.setIcon(QIcon(r"Icons\folder.png"))
        self.sourceFolder2.setIconSize(QSize(18,18))
        self.sourceFolder2.setToolTip("Open Source Folder")
        self.sourceFolder2.clicked.connect(lambda: os.startfile(self.folder2))
        
        self.refreshBtn2 = QPushButton(self)
        self.refreshBtn2.setGeometry(self.mdi2.x()+self.mdi2.width()-60,50,30,30)
        self.refreshBtn2.setStyleSheet(parse("menuButtons",THEME).getStyle())
        self.refreshBtn2.setIcon(QIcon(r"Icons\refresh.png"))
        self.refreshBtn2.setIconSize(QSize(18,18))
        self.refreshBtn2.setToolTip("Refresh Files")
        self.refreshBtn2.clicked.connect(self.refreshFiles)

        self.search2 = QLineEdit(self)
        self.search2.setGeometry(self.mdi2.x(),110,self.mdi2.width(),30)
        self.search2.setPlaceholderText("Search for Items")
        self.search2.setStyleSheet(parse("searchBox",THEME).getStyle())
        self.search2.textChanged.connect(self.searchitem2)
    
        self.closeSearch2 = QPushButton(self)
        self.closeSearch2.clicked.connect(lambda:self.search2.setText(""))
        self.closeSearch2.setGeometry(self.search2.x()+self.search2.width()-31,110,30,0)
        self.closeSearch2.setStyleSheet(parse("clearSearchButton",THEME).getStyle())
        self.closeSearch2.setIcon(QIcon(r'Icons\close.png'))
        self.closeSearch2.setIconSize(QSize(12,12))


        self.workspace2 = QMdiSubWindow(self.mdi2)
        self.workspace2.setWindowFlags(Qt.FramelessWindowHint)
        self.workspace2.setGeometry(0,0,self.mdi2.width()-100,self.mdi2.height())
        self.workspace2.setStyleSheet("background-color:white;")
        self.workspace2.setStyleSheet(parse("explorerBox",THEME).getStyle())

        workspace2_sc = QMdiSubWindow(self.mdi2)
        workspace2_sc.setWindowFlags(Qt.FramelessWindowHint)
        workspace2_sc.setGeometry(self.mdi2.width()-30,0,30,self.mdi2.height())

        self.scroller2 = QScrollBar(workspace2_sc)
        self.scroller2.setGeometry(0,0,30,self.mdi2.height())
        self.scroller2.setStyleSheet(parse("scrollBar",THEME).getStyle())

        self.animator2 = QPushButton(self.workspace2)
        self.animator2.setGeometry(-1000,0,self.mdi2.width()-40,40)
        self.animator2.setStyleSheet(parse("FileExplorerBtn_SELECTED",THEME).getStyle())

        self.s_animator2 = QPushButton(self.workspace2)
        self.s_animator2.setGeometry(-1000,0,self.mdi2.width()-40,40)
        self.s_animator2.setStyleSheet(parse("FileExplorerBtn_SUCCESS(COLOR-ONLY)",THEME).getStyle())
        
        pos = 5
        for i in FILES2:
            btn = QPushButton(self.workspace2)
            btn.setText(i)
            btn.setObjectName(i+"@F2")
            btn.setGeometry(7,pos,self.mdi2.width()-40,self.itemHeight)
            btn.setStyleSheet(parse("FileExplorerBtn",THEME).getStyle())
            btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(self.on_context_menu2)
            btn.clicked.connect(lambda: self.select2())

            btn.installEventFilter(self)

            from hurry.filesize import size
            
            
            fileInfo = QtCore.QFileInfo(self.folder2 + "\\" +i)
            iconProvider = QtGui.QFileIconProvider()
            icon = iconProvider.icon(fileInfo)
            btn.setIcon(QIcon(icon))

            btn.type = QLabel(self.workspace2)
            btn.type.setText(iconProvider.type(fileInfo))
            btn.type.setGeometry(self.mdi2.width()-250,pos,200,self.itemHeight)
            btn.type.setStyleSheet(parse("FileExplorerBtn",THEME).getStyle())


            btn.size = QLabel(self.workspace2)
            btn.size.setText(str(size(fileInfo.size())))
            btn.size.setGeometry(self.mdi2.width()-150,pos,200,self.itemHeight)
            btn.size.setStyleSheet(parse("FileExplorerBtn",THEME).getStyle())
            
            pos+=self.itemHeight
        
        self.bottom_border2 = QPushButton(self)
        self.bottom_border2.setGeometry(self.mdi2.x(),self.mdi2.y()+self.mdi2.height(),self.mdi2.width(),2)
        self.bottom_border2.setStyleSheet(parse("explorerBox",THEME).getStyle())
       
        self.searchResultCount2 = QPushButton(self)
        self.searchResultCount2.setGeometry(self.mdi2.x()+2,self.mdi2.y()+self.mdi2.height()-30,self.mdi2.width()-30,0)
        self.searchResultCount2.setStyleSheet(parse("noResultFound",THEME).getStyle())
        self.searchResultCount2.setText("No Match Found")

        self.popMenu2 = QtGui.QMenu(self.workspace2)
        # self.action1_2 = self.popMenu2.addAction('Unexpected Error!')
        # self.action1_2.setEnabled(False)

        self.popMenu2.addSeparator()
        self.action2_2 = self.popMenu2.addAction('Open')
        self.action2_2.triggered.connect(self.popOpen2)
        self.action3_2 = self.popMenu2.addAction('Open Inside')
        self.action3_2.triggered.connect(self.openDirInside2)
        self.action4_2 = self.popMenu2.addAction('Reveal in Explorer')
        self.action4_2.triggered.connect(self.reveal2)
        self.action5_2 = self.popMenu2.addAction('Rename..')
        self.action5_2.triggered.connect(self.rename2)
        
        
        self.action7_2 = self.popMenu2.addMenu('Copy Name/Path')
        self.action7_name_2 = self.action7_2.addAction("Copy Name")
        self.action7_path_2 = self.action7_2.addAction("Copy Path")
        self.action7_name_2.triggered.connect(self.copyName2)
        self.action7_path_2.triggered.connect(self.copyPath2)


        self.action6_2 = self.popMenu2.addAction('Properties')
        self.action6_2.triggered.connect(self.showProperties)
        self.popMenu2.setStyleSheet(parse("PopMenu2",THEME).getStyle())

        self.bottom_border2 = QPushButton(self)
        self.bottom_border2.setGeometry(self.mdi2.x(),self.mdi2.y()+self.mdi2.height(),self.mdi2.width(),2)
        self.bottom_border2.setStyleSheet(parse("explorerBox",THEME).getStyle())

        self.workspace2.resize(self.mdi2.width()-30 ,pos+650)
        self.scroller2.setMaximum(pos-400)
        self.scroller2.sliderMoved.connect(self.scroll2)
        
        self.empty2 = QPushButton(self)
        self.empty2.setIcon(QIcon(r"Icons\empty.png"))
        self.empty2.setIconSize(QSize(400,400))
        self.empty2.setStyleSheet("background-color:transparent;")

        if len(self.files2) == 0:
            self.empty2.move(self.mdi2.x()+120,self.mdi2.y()+100)
        else:
            self.empty2.move(-1000,0)
        
        self.fileInfoBox = QPushButton(self)
        self.fileInfoBox.setGeometry(0,self.mdi.y()+self.mdi.height()+10,WIDTH,80)
        self.fileInfoBox.setStyleSheet(parse("fileInfoBox",THEME).getStyle())

        self.fileInfoIcon = QPushButton(self)
        self.fileInfoIcon.move(self.mdi.x()-17,self.mdi.y()+self.mdi.height()+20)
        self.fileInfoIcon.resize(90,60)
        self.fileInfoIcon.setIcon(QIcon(r"Icons\2.png"))
        self.fileInfoIcon.setIconSize(QSize(60,60))
        self.fileInfoIcon.setStyleSheet("background-color:transparent;")

        self.fileInfoLabel = QLabel(self)
        self.fileInfoLabel.resize(self.width()-100,self.fileInfoIcon.height()-20)
        self.fileInfoLabel.move(self.fileInfoIcon.x()+self.fileInfoIcon.width(),self.fileInfoIcon.y()-10)
        self.fileInfoLabel.setText("Backup Manager 2")
        self.fileInfoLabel.setStyleSheet(parse("fileInfoLabel",THEME).getStyle())

        self.fileInfoProperties = QLabel(self)
        self.fileInfoProperties.resize(self.width()-100,self.fileInfoIcon.height()-20)
        self.fileInfoProperties.move(self.fileInfoIcon.x()+self.fileInfoIcon.width(),self.fileInfoLabel.y()+32)
        self.fileInfoProperties.setText("V" + VERSION + "<br>By Ahmad Taha")
        self.fileInfoProperties.setStyleSheet(parse("fileInfoProperties",THEME).getStyle())
        self.fileInfoProperties.linkActivated.connect(self.fetchExtensionDetail)        

        self.hidefileinfo = QPushButton(self)
        self.hidefileinfo.setGeometry(self.width()-105,self.height()-34,100,30)
        self.hidefileinfo.setStyleSheet(parse("hide_show_propertiesBtn",THEME).getStyle())
        self.hidefileinfo.setCursor(Qt.PointingHandCursor)
        self.hidefileinfo.setText("Hide Properties")
        self.hidefileinfo.clicked.connect(self.hideProperties)

        
        # ------------------------------- SHOULD BE AT TOP --------------------- #

        self.notification_box = QLabel(self)
        self.notification_box.setGeometry(self.width()/2-280,-40,400,40)
        self.notification_box.setText("Settings Saved Successfully")
        self.notification_box.setStyleSheet(parse("notificationBox",THEME).getStyle())

        self.notificationOK = QPushButton(self)
        self.notificationOK.setText("Got It!")
        self.notificationOK.setGeometry(self.notification_box.x()+self.notification_box.width()-80,-70,80,50)
        self.notificationOK.setStyleSheet(parse("notificationOKBtn",THEME).getStyle())
        self.notificationOK.setCursor(Qt.PointingHandCursor)
        self.notificationOK.clicked.connect(self.hideNotification)

        self.show()
    
    
    def reveal(self):
        path = self.folder1 + "\\" + self.SelectedButton1.text()
        path =path.replace("\\\\","\\")
        subprocess.Popen('explorer /select,"' + path +'"')
    
    def reveal2(self):
        path = self.folder2 + "\\" + self.SelectedButton2.text()
        path =path.replace("\\\\","\\")
        subprocess.Popen('explorer /select,"' + path +'"')
    def optionALL(self):
        self.setting = "SAF"
        self.optionBtn.setText("   Show All Files")
        self.refreshFiles()
    def optionSCF(self):
        self.setting = "SCF"
        self.optionBtn.setText("   Show Common Files")
        self.refreshFiles()
    def optionHCF(self):
        self.setting = "HCF"
        self.optionBtn.setText("   Hide Common Files")
        self.refreshFiles()
    def hideProperties(self):
        if "Hide" in self.hidefileinfo.text():
            self.hidefileinfo.setText("Show Properties")
            position_animator(self.fileInfoBox,self.fileInfoBox.x(),self.fileInfoBox.y(),self.fileInfoBox.x(),self.fileInfoBox.y()+200,1800)
            position_animator(self.fileInfoLabel,self.fileInfoLabel.x(),self.fileInfoLabel.y(),self.fileInfoLabel.x(),self.fileInfoLabel.y()+200,1800)
            position_animator(self.fileInfoIcon,self.fileInfoIcon.x(),self.fileInfoIcon.y(),self.fileInfoIcon.x(),self.fileInfoIcon.y()+200,1800)
            position_animator(self.fileInfoProperties,self.fileInfoProperties.x(),self.fileInfoProperties.y(),self.fileInfoProperties.x(),self.fileInfoProperties.y()+200,1800)

        else:
            position_animator(self.fileInfoBox,self.fileInfoBox.x(),self.fileInfoBox.y(),self.fileInfoBox.x(),self.mdi.y()+self.mdi.height()+10,1800)
            position_animator(self.fileInfoIcon,self.fileInfoIcon.x(),self.fileInfoIcon.y(),self.fileInfoIcon.x(),self.mdi.y()+self.mdi.height()+20,1800)
            position_animator(self.fileInfoLabel,self.fileInfoLabel.x(),self.fileInfoLabel.y(),self.fileInfoLabel.x(),self.mdi.y()+self.mdi.height()+20-10,1800)
            position_animator(self.fileInfoProperties,self.fileInfoProperties.x(),self.fileInfoProperties.y(),self.fileInfoProperties.x(),self.mdi.y()+self.mdi.height()+20-10+32,1800)
            self.hidefileinfo.setText("Hide Properties")

    def showAboutWin(self):
        self.aboutBtn.setStyleSheet(parse("titleBtn_ON",self.theme).getStyle())
        self.aboutWin.show()
        w = self.aboutWin
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),self.height(),w.width(),w.height()))
        animation.setEndValue(QRect(w.x(),40,w.width(),w.height()))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(1000)
        animation.start()
    def showUpdatesWin(self):
        self.updateBtn.setStyleSheet(parse("titleBtn_ON",self.theme).getStyle())
        self.updateWin.show()
        w = self.updateWin
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),self.height(),w.width(),w.height()))
        animation.setEndValue(QRect(w.x(),40,w.width(),w.height()))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(1000)
        animation.start()

        checker = self.checkUpdates()
        checker.on_done.connect(self.checkComplete)
        checker.start()

        time.sleep(0.2)
    class checkUpdates(QtCore.QThread):
        on_done = QtCore.pyqtSignal(object)
        def __init__(self):
            QtCore.QThread.__init__(self)
        def run(self):
            try:
                res = requests.get("http://textuploader.com/dkoly/raw")
                self.on_done.emit(res)
            except Exception as err:
                self.on_done.emit("Error : "+str(err))
    def checkComplete(self,soup):
        if "Error" in soup:
                if "Not Found" in soup:
                    QMessageBox.warning(self,"Error!","No Information found on selected extention!")
                else:
                    QMessageBox.critical(self,"Error!","Backup Manager cannot connect to network to fetch update details!")
                self.loading.hide()
                return
        ud = str(soup.text).split(";")
        latest_version = ud[0]
        update_type = ud[1]
        update_url = ud[2]
        update_url = update_url.replace("url=","")
        update_notes = ud[3]
        if latest_version != VERSION:
            self.checkingBtn.setText("New Updates Are Available!<br><br><span style='font-size:30px;'><b>Current Version</b> : " + VERSION + "<br><b>Latest Version</b> : " + latest_version + "<br><b>Update Type</b> : " + update_type + "<br><br><b>Update Notes</b> : <br>" + update_notes + "</span>")
            position_animator(self.checkingBtn,self.checkingBtn.x(),self.checkingBtn.y(),43,90,2000)
            position_animator(self.checkingBtn_loader,self.checkingBtn_loader.x(),self.checkingBtn_loader.y(),self.checkingBtn_loader.x(),-800,1300)
            position_animator(self.updateNow,self.updateNow.x(),-100,self.updateNow.x(),20,1300)
            self.updateNow.clicked.connect(lambda: webbrowser.open(update_url,new=0,autoraise=True))
        else:
            self.checkingBtn.setText("Congo! You are using latest version of Backup Manager<br><br><span style='font-size:30px;'><b>Latest Version</b> : " + latest_version + "<br><b>Version Type</b> : " + update_type + "<br><br><b>Update Notes</b> : <br>" + update_notes + "</span>")
            position_animator(self.checkingBtn,self.checkingBtn.x(),self.checkingBtn.y(),43,90,2000)
            position_animator(self.checkingBtn_loader,self.checkingBtn_loader.x(),self.checkingBtn_loader.y(),self.checkingBtn_loader.x(),-800,1300)
    def showHelpWin(self):
        self.helpBtn.setStyleSheet(parse("titleBtn_ON",self.theme).getStyle())
        self.helpWin.show()
        w = self.helpWin
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),self.height(),w.width(),w.height()))
        animation.setEndValue(QRect(w.x(),40,w.width(),w.height()))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(1000)
        animation.start()
    def aboutBack(self):
        self.aboutBtn.setStyleSheet(parse("titlebtn",self.theme).getStyle())
        w = self.aboutWin
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),40,w.width(),w.height()))
        animation.setEndValue(QRect(w.x(),self.height(),w.width(),w.height()))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(1000)
        animation.start()
        QtCore.QTimer.singleShot(1000, lambda: w.close())
    def updateBack(self):
        self.updateBtn.setStyleSheet(parse("titlebtn",self.theme).getStyle())
        w = self.updateWin
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),40,w.width(),w.height()))
        animation.setEndValue(QRect(w.x(),self.height(),w.width(),w.height()))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(1000)
        animation.start()
        QtCore.QTimer.singleShot(1000, lambda: w.close())
    def helpBack(self):
        self.helpBtn.setStyleSheet(parse("titlebtn",self.theme).getStyle())
        w = self.helpWin
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),40,w.width(),w.height()))
        animation.setEndValue(QRect(w.x(),self.height(),w.width(),w.height()))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(1000)
        animation.start()
        QtCore.QTimer.singleShot(1000, lambda: w.close())
    def selectBtnFunc(self):
        self.copy_right.setEnabled(True)
        self.move_right.setEnabled(True)
        self.send_to_trash.setEnabled(True)
        self.delete_permanently.setEnabled(True)
        if len(self.selectedFiles1) == 0 or len(self.selectedFiles1)==1:
            self.selectedFiles1 = []
            for i in self.files1:
                btn = self.findChild(QPushButton,i)
                if btn.text() in self.new_file1:
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED_NEW",self.theme).getStyle())
                else:
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED",self.theme).getStyle())
                self.selectedFiles1.append(i)
            self.selectBtn.setText("Deselect All (" + str(len(self.selectedFiles1))+")")
        else:
            for i in self.selectedFiles1:
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
            self.selectedFiles1 = []
            self.selectBtn.setText("Select All")
    def selectBtnFunc2(self):
        self.copy_left.setEnabled(True)
        self.move_left.setEnabled(True)
        self.send_to_trash.setEnabled(True)
        self.delete_permanently.setEnabled(True)
        if len(self.selectedFiles2) == 0 or len(self.selectedFiles2)==1:
            self.selectedFiles2 = []
            for i in self.files2:
                btn = self.findChild(QPushButton,i+"@F2")
                if btn.text() in self.new_file2:
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED_NEW",self.theme).getStyle())
                else:
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED",self.theme).getStyle())
                self.selectedFiles2.append(btn.objectName())
            self.selectBtn2.setText("Deselect All (" + str(len(self.selectedFiles2))+")")
        else:
            for i in self.selectedFiles2:
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
            self.selectedFiles2 = []
            self.selectBtn2.setText("Select All")
    def reSelect1(self):
        choose = QFileDialog.getExistingDirectory(self, 'Choose Folder 1', os.path.abspath(os.path.join(self.folder1, os.pardir)), QtGui.QFileDialog.ShowDirsOnly)
        if choose == "":
            print("Press Cancell")
        elif choose == self.folder1:
            return
        else:
            self.folder1 = choose
            self.refreshFiles()
    def reSelect2(self):
        choose = QFileDialog.getExistingDirectory(self, 'Choose Folder 1', os.path.abspath(os.path.join(self.folder2, os.pardir)), QtGui.QFileDialog.ShowDirsOnly)
        if choose == "":
            print("Press Cancell")
        elif choose == self.folder2:
            return
        else:
            self.folder2 = choose
            self.refreshFiles()
    def copyName(self):
        pyperclip.copy(self.SelectedButton1.text())
    def copyPath(self):
        path = self.folder1 + "\\" + self.SelectedButton1.text()
        path = path.replace("\\\\","\\")
        pyperclip.copy(path)
    def copyName2(self):
        pyperclip.copy(self.SelectedButton2.text())
    def copyPath2(self):
        path = self.folder2 + "\\" + self.SelectedButton2.text()
        path = path.replace("\\\\","\\")
        pyperclip.copy(path)
    def rename(self):
        c_text = self.SelectedButton1.text()
        filename, file_extension = os.path.splitext(c_text)
        dialog = QInputDialog(self)
        dialog.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
        dialog.setTextValue(filename)
        dialog.setLabelText("Enter new name for file/folder <b>" + c_text + "</b> :")
        dialog.setWindowTitle("Rename Item")
        ok = dialog.exec_()
        if ok:
            new_name = dialog.textValue() + file_extension
            old_path = self.folder1 + "\\" + c_text
            path = self.folder1 + "\\" + new_name
            path = path.replace("\\\\","\\")
            old_path = old_path.replace("\\\\","\\")
            if os.path.exists(path):
                ok = QMessageBox.critical(self,"File/Folder already Exists!","There is already a file named <b>" + new_name + "</b>. Please choose a different name and try again.")
                return
            os.rename(old_path,path)
            self.scroll_bottom1()
            self.new_file1.append(new_name)
            self.refreshFiles()
            self.animate_new_item(new_name,1)
        else:
            print("Cancelled")
    def rename2(self):
        c_text = self.SelectedButton2.text()
        filename, file_extension = os.path.splitext(c_text)
        dialog = QInputDialog(self)
        dialog.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
        dialog.setTextValue(filename)
        dialog.setLabelText("Enter new name for file/folder <b>" + c_text + "</b> :")
        dialog.setWindowTitle("Rename Item")
        ok = dialog.exec_()
        if ok:
            new_name = dialog.textValue() + file_extension
            old_path = self.folder2 + "\\" + c_text
            path = self.folder2 + "\\" + new_name
            path = path.replace("\\\\","\\")
            old_path = old_path.replace("\\\\","\\")
            if os.path.exists(path):
                ok = QMessageBox.critical(self,"File/Folder already Exists!","There is already a file named <b>" + new_name + "</b>. Please choose a different name and try again.")
                return
            os.rename(old_path,path)
            self.scroll_bottom2()
            self.new_file2.append(new_name)
            self.refreshFiles()
            self.animate_new_item(new_name,2)
        else:
            print("Cancelled")
    def popOpen(self):
        sFile = self.SelectedButton1.text()
        sFile = self.folder1 + "\\" + sFile
        sFile = sFile.replace("\\\\","\\")
        os.startfile(sFile)
    def popOpen2(self):
        sFile = self.SelectedButton2.text()
        sFile = self.folder2 + "\\" + sFile
        sFile = sFile.replace("\\\\","\\")
        os.startfile(sFile)
    def createNewFolder1(self):
        dialog = QInputDialog(self)
        dialog.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
        dialog.setTextValue("New Folder")
        dialog.setLabelText("Enter the name of new folder:")
        dialog.setWindowTitle("Confirm Name")
        ok = dialog.exec_()
        if ok:
            new_name = dialog.textValue()
            path = self.folder1 + "\\" + new_name
            path = path.replace("\\\\","\\")
            if os.path.isdir(path):
                ok = QMessageBox.critical(self,"Directory already Exists!","There is already a folder named <b>" + new_name + "</b>. Please choose a different name and try again.")
                return
            os.makedirs(path)
            self.scroll_bottom1()
            self.new_file1.append(new_name)
            self.refreshFiles()
            self.animate_new_item(new_name,1)
        else:
            print("Cancelled")
    def createNewFolder2(self):
        dialog = QInputDialog(self)
        dialog.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
        dialog.setTextValue("New Folder")
        dialog.setLabelText("Enter the name of new folder:")
        dialog.setWindowTitle("Confirm Name")
        ok = dialog.exec_()
        if ok:
            new_name = dialog.textValue()
            path = self.folder2 + "\\" + new_name
            path = path.replace("\\\\","\\")
            if os.path.isdir(path):
                ok = QMessageBox.critical(self,"Directory already Exists!","There is already a folder named <b>" + new_name + "</b>. Please choose a different name and try again.")
                return
            os.makedirs(path)
            self.scroll_bottom2()
            self.new_file2.append(new_name)
            self.refreshFiles()
            self.animate_new_item(new_name,2)
        else:
            print("Cancelled")
    def parentDir(self):
        self.forward_dir.insert(0,self.folder1)
        self.folder1 = os.path.abspath(os.path.join(self.folder1, os.pardir))
        self.forward.setDisabled(False)
        if self.folder1 == os.path.abspath(os.path.join(self.folder1, os.pardir)):
            self.goBack.setDisabled(True)
        self.refreshFiles()
        
        self.workspace1.move(self.workspace1.x(),0)
        self.scroller.setValue(0)
    
    def parentDir2(self):
        self.forward_dir2.insert(0,self.folder1)
        self.folder2 = os.path.abspath(os.path.join(self.folder2, os.pardir))
        self.forward2.setDisabled(False)
        if self.folder2 == os.path.abspath(os.path.join(self.folder2, os.pardir)):
            self.goBack2.setDisabled(True)
        self.refreshFiles()
        
        self.workspace2.move(self.workspace2.x(),0)
        self.scroller2.setValue(0)

    def forwardDir(self):
        self.folder1 = self.forward_dir[0]
        self.forward_dir.remove(self.forward_dir[0])
        if len(self.forward_dir) == 0:
            self.forward.setDisabled(True)
        self.goBack.setDisabled(False)
        self.refreshFiles()

        self.workspace1.move(self.workspace1.x(),0)
        self.scroller.setValue(0)
    def forwardDir2(self):
        self.folder2 = self.forward_dir2[0]
        self.forward_dir2.remove(self.forward_dir2[0])
        if len(self.forward_dir2) == 0:
            self.forward2.setDisabled(True)
        self.goBack2.setDisabled(False)
        self.refreshFiles()

        self.workspace2.move(self.workspace2.x(),0)
        self.scroller2.setValue(0)
    def openDirInside(self):
        dirr = self.SelectedButton1.text()
        if not os.path.isdir(self.folder1 + "\\" + dirr):
            return
        self.folder1 = self.folder1 + "\\" + dirr
        self.forward_dir = []
        self.forward.setDisabled(True)
        self.goBack.setDisabled(False)
        self.refreshFiles()

        self.workspace1.move(self.workspace1.x(),0)
        self.scroller.setValue(0)
    def openDirInside2(self):
        dirr = self.SelectedButton2.text()
        if not os.path.isdir(self.folder2 + "\\" + dirr):
            return
        self.folder2 = self.folder2 + "\\" + dirr
        self.forward_dir2 = []
        self.forward2.setDisabled(True)
        self.goBack2.setDisabled(False)
        self.refreshFiles()

        self.workspace2.move(self.workspace2.x(),0)
        self.scroller.setValue(0)
    def eventFilter(self,object,event):
        if self.dblClickOpen == True:
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                if self.currentButtonSide == 1:
                    path = self.folder1 + "\\" + object.text()
                    path = path.replace("\\\\","\\")
                    print(path)
                    os.startfile(path)
                    return True
                else:
                    os.startfile(self.folder2 + "\\" + object.text())
                    return True
        if self.dc_in == True:
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                if self.currentButtonSide == 1:
                    if os.path.isdir(self.folder1 + "\\" + self.SelectedButton1.text()) == False:
                        return True
                    else:
                        self.openDirInside()
                        return True
                else:
                    if os.path.isdir(self.folder2 + "\\" + self.SelectedButton2.text()) == False:
                        return True
                    else:
                        self.openDirInside2()
                        return True
        # if event.type() == QtCore.QEvent.moi
        return False
    def on_context_menu(self, point):
        # self.action1.setText(self.sender().text())
        self.select1(sbtn = self.sender())
        self.popMenu.exec_(self.sender().mapToGlobal(point))
    def openRecentContext(self, point):
        # self.action1.setText(self.sender().text())
        # self.select1(sbtn = self.sender())
        print("clicked!")
        self.action1 = self.recentMenu.addAction('Click to open here!')
        self.action1 = self.recentMenu.addAction('Click to open here!')

        # self.recentMenu.exec_(self.sender().mapToGlobal(point))
    def on_context_menu2(self, point):
        # self.action1_2.setText(self.sender().text())
        self.select2(sbtn = self.sender())
        self.popMenu2.exec_(self.sender().mapToGlobal(point))
    def showProperties(self):
        if self.currentButtonSide == 1:
            btn = self.SelectedButton1
        else:
            btn = self.SelectedButton2


        self.prop_win.setWindowIcon(btn.icon())
        self.prop_win.setWindowTitle(btn.text()+" Properties")
    

        if self.currentButtonSide == 1:
            full_path = self.folder1 + "\\" +btn.text()
            loc = self.folder1
        else:
            full_path = self.folder2 + "\\" +btn.text()
            loc = self.folder2
        fileInfo = QtCore.QFileInfo(full_path)
        icon = self.fetchIcon(btn.text())
        self.prop_icon.setIcon(QIcon(r"Icons\File\\"+icon))
        self.prop_icon.setIconSize(QSize(100,100))
        

        prop = os.stat(full_path)
        data_modified = datetime.datetime.utcfromtimestamp(prop.st_mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_modified = data_modified.replace("T"," ")
        data_modified = data_modified.replace("Z"," ")
        data_created = datetime.datetime.utcfromtimestamp(prop.st_ctime).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_created = data_created.replace("T"," ")
        data_created = data_created.replace("Z"," ")
        date_assessed = datetime.datetime.utcfromtimestamp(prop.st_atime).strftime('%Y-%m-%dT%H:%M:%SZ')
        date_assessed = date_assessed.replace("T"," ")
        date_assessed = date_assessed.replace("Z"," ")

        mime = MimeTypes()
        url = urllib.request.pathname2url(self.folder1 + btn.objectName())
        mime_type = mime.guess_type(url)
        mime_type = mime_type[0]
        if mime_type == None:
            mime_type = "Unknown"
        filename, file_extension = os.path.splitext(full_path)
        details = self.getExtentionDetail(file_extension)
        self.prop_label.setText("<br><br><br>" + "<br><br><b>Location</b> : " + str(loc)+"<br><br><b>MIME Type</b> : " + str(mime_type) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Size</b> : " + str(round( os.path.getsize(full_path)/(1024*1024),2)) + " MB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Modified</b> : " + data_modified + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Created</b> : " + data_created + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Assessed</b> : " + date_assessed + "<br><br><b>Extention Details</b> : " + str(details) + "<BR><br><a href = '#' style = 'color:#3498db;text-decoration:none;'>About File Extension</a>")
        if os.path.isdir(full_path) == True:
            details = "Folder"
            self.prop_icon.setIcon(QIcon(r"Icons\File\folder.png"))
            self.prop_label.setText("<br><br><br>" + "<br><br><b>Location</b> : " + str(loc)+"<br><br><b>MIME Type</b> : " + str(mime_type) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Size</b> : " + str(round( os.path.getsize(full_path)/(1024*1024),2)) + " MB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Modified</b> : " + data_modified + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Created</b> : " + data_created + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br><br><b>Assessed</b> : " + date_assessed + "<br><br><b>Extention Details</b> : " + str(details))

        self.prop_name.setText(btn.text())


        self.prop_win.show()
    def fetchExtensionDetail(self):
        if self.currentButtonSide == 1:
            btn = self.SelectedButton1.text()
            full_path = self.folder1 + "\\" + btn
        else:
            btn = self.SelectedButton2.text()
            full_path = self.folder2 + "\\" + btn
        full_path = full_path.replace("\\\\","\\")
        if os.path.isdir(full_path):
            return
        filename, file_extension = os.path.splitext(full_path)
        self.file_extension = file_extension.replace(".","")

        loader = self.loadExt(self.file_extension,self,self.theme)
        loader.on_done.connect(self.extComplete)
        loader.start()
        self.loading.show()
        w = self.loading
        animation = QPropertyAnimation(w,"geometry",w)
        animation.setStartValue(QRect(w.x(),w.y(),w.width(),0))
        animation.setEndValue(QRect(w.x(),w.y(),w.width(),200))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(400)
        animation.start()
        time.sleep(0.2)

    def extComplete(self,soup):
            if "Error" in soup:
                if "Not Found" in soup:
                    QMessageBox.warning(self,"Error!","No Information found on selected extention!")
                else:
                    QMessageBox.critical(self,"Error!","Backup Manager cannot connect to network to fetch extension details!")
                self.loading.hide()
                return
            info = soup.select('.infoBox')
            name = soup.select('h2 span')
            box = QMessageBox(self)
            box.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
            box.setText("<br><span style = 'font-size:25px;'>" + self.file_extension.upper()+"</span>&nbsp;&nbsp;&nbsp;<span style='font-size:20px;color:#666665;'>" + name[1].get_text() + "</span><br><br> " +info[0].get_text()+"<br><br><br>Information from <b>fileinfo.com</b>. <br><A href = '" + "https://fileinfo.com/extension/"+self.file_extension + "' style= 'font-size:13px;'>Click to Show More</a>")
            box.setWindowTitle("About Extension")
            box.setStandardButtons(QMessageBox.Ok)
            self.loading.hide()
            ans = box.exec_()
            # self.prop_win.showMaximized()
            # self.prop_win.showNormal()
    class loadExt(QtCore.QThread):
        on_done = QtCore.pyqtSignal(object)
        def __init__(self,file_extension,win,theme):
            QtCore.QThread.__init__(self)
            self.file_extension = file_extension
            self.win = win
            self.theme = theme
        def run(self):
            try:
                res = urllib.request.urlopen("https://fileinfo.com/extension/"+self.file_extension).read()
                soup = bs4.BeautifulSoup(res,"html.parser")
                self.on_done.emit(soup)
            except Exception as err:
                print(err)
                self.on_done.emit("Error : "+str(err))

    def searchitem1(self):
        key = self.search1.text()
        backspacing = False
        if len(key) < len(self.oldKey1):
            backspacing = True
        self.oldKey1 = key
        if key == "":
            animation = QPropertyAnimation(self.closeSearch1,"geometry",self.closeSearch1)
            animation.setStartValue(QRect(self.closeSearch1.x(),self.closeSearch1.y(),30,30))
            animation.setEndValue(QRect(self.closeSearch1.x(),self.closeSearch1.y(),30,0))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(400)
            animation.start()
            animation = QPropertyAnimation(self.searchResultCount,"geometry",self.searchResultCount)
            animation.setStartValue(QRect(self.searchResultCount.x(),self.searchResultCount.y(),self.searchResultCount.width(),30))
            animation.setEndValue(QRect(self.searchResultCount.x(),self.searchResultCount.y(),self.searchResultCount.width(),0))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(600)
            animation.start()
            self.refreshFiles()
            self.search1.setFocus(True)
            return
        if len(key) == 1 and backspacing == False:
            animation = QPropertyAnimation(self.closeSearch1,"geometry",self.closeSearch1)
            animation.setStartValue(QRect(self.closeSearch1.x(),self.closeSearch1.y(),30,0))
            animation.setEndValue(QRect(self.closeSearch1.x(),self.closeSearch1.y(),30,30))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(400)
            animation.start()
            
            animation = QPropertyAnimation(self.searchResultCount,"geometry",self.searchResultCount)
            animation.setStartValue(QRect(self.searchResultCount.x(),self.searchResultCount.y(),self.searchResultCount.width(),0))
            animation.setEndValue(QRect(self.searchResultCount.x(),self.searchResultCount.y(),self.searchResultCount.width(),30))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(600)
            animation.start()

        result = []
        for i in self.files1:
            if key.lower() in i.lower():
                result.append(i)
        if len(result) == 0:
            self.searchResultCount.setStyleSheet(parse("noResultFound",self.theme).getStyle())
            self.searchResultCount.setText("No Match Found")
        else:
            self.searchResultCount.setStyleSheet(parse("searchResult",self.theme).getStyle())
            self.searchResultCount.setText(str(len(result))+" Matching Files/Folder")
        self.refreshFiles(search1 = True,searchList= result)
        self.workspace1.move(self.workspace1.x(),0)
        self.scroller.setValue(0)
        self.search1.setFocus(True)
        self.search1.setText(key)
    def searchitem2(self):
        key = self.search2.text()
        backspacing = False
        if len(key) < len(self.oldKey2):
            backspacing = True
        self.oldKey2 = key
        if key == "":
            animation = QPropertyAnimation(self.closeSearch2,"geometry",self.closeSearch2)
            animation.setStartValue(QRect(self.closeSearch2.x(),self.closeSearch2.y(),30,30))
            animation.setEndValue(QRect(self.closeSearch2.x(),self.closeSearch2.y(),30,0))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(400)
            animation.start()
            animation = QPropertyAnimation(self.searchResultCount2,"geometry",self.searchResultCount2)
            animation.setStartValue(QRect(self.searchResultCount2.x(),self.searchResultCount2.y(),self.searchResultCount2.width(),30))
            animation.setEndValue(QRect(self.searchResultCount2.x(),self.searchResultCount2.y(),self.searchResultCount2.width(),0))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(600)
            animation.start()
            self.refreshFiles()
            self.search2.setFocus(True)
            return
        if len(key) == 1 and backspacing == False:
            animation = QPropertyAnimation(self.closeSearch2,"geometry",self.closeSearch2)
            animation.setStartValue(QRect(self.closeSearch2.x(),self.closeSearch2.y(),30,0))
            animation.setEndValue(QRect(self.closeSearch2.x(),self.closeSearch2.y(),30,30))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(400)
            animation.start()

            animation = QPropertyAnimation(self.searchResultCount2,"geometry",self.searchResultCount2)
            animation.setStartValue(QRect(self.searchResultCount2.x(),self.searchResultCount2.y(),self.searchResultCount2.width(),0))
            animation.setEndValue(QRect(self.searchResultCount2.x(),self.searchResultCount2.y(),self.searchResultCount2.width(),30))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(600)
            animation.start()
        result = []
        for i in self.files2:
            if key.lower() in i.lower():
                result.append(i)
        if len(result) == 0:
            self.searchResultCount2.setStyleSheet(parse("noResultFound",self.theme).getStyle())
            self.searchResultCount2.setText("No Match Found")
        else:
            self.searchResultCount2.setStyleSheet(parse("searchResult",self.theme).getStyle())
            self.searchResultCount2.setText(str(len(result))+" Matching Files/Folder")
        self.refreshFiles(search2 = True,searchList= result)
        self.workspace2.move(self.workspace2.x(),0)
        self.scroller2.setValue(0)
        self.search2.setFocus(True)
        self.search2.setText(key)
    def scroll_bottom1(self):
        self.workspace1.move(self.workspace1.x(),-(self.scroller.maximum()))
        self.scroller.setValue(self.scroller.maximum())
    def scroll_bottom2(self):
        self.workspace2.move(self.workspace2.x(),-(self.scroller2.maximum()))
        self.scroller2.setValue(self.scroller2.maximum())
        
    def togglemultiselection(self):
        if self.multi_selection_state == True:
            self.multi_selection_state = False
            self.multi_select.setIcon(QIcon(r"Icons\multiselect_DIS.png"))
            self.multi_select.setIconSize(QSize(40,40))
            # self.multi_select.move((self.width()/2)-26,573)
            for i in self.selectedFiles1:
                print(i)
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
            self.selectedFiles1 = []

            for i in self.selectedFiles2:
                print(i)                
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
            self.selectedFiles2 = []
            self.selectBtn.setText("Select All")
            self.selectBtn2.setText("Select All")
        else:
            self.multi_selection_state = True
            self.multi_select.setIcon(QIcon(r"Icons\multiselect_EN.png"))
            self.multi_select.setIconSize(QSize(40,40))
            # self.multi_select.move((self.width()/2)-24,573)
    def showNotification(self,title = "Untitled Notification ",ok_text = "Got It!",type = "success"):
        self.toX = 50
        # position_animator(self.notification_box,self.width()/2-280,-70,self.width()/2-280,self.toX,duration=200)
        # position_animator(self.notificationOK,self.notification_box.x()+self.notification_box.width()-80,-70,self.notification_box.x()+self.notification_box.width()-80,self.toX,duration=200)

        animation = QPropertyAnimation(self.notification_box,"geometry",self.notification_box)
        animation.setStartValue(QRect(self.width()/2,0,0,40))
        animation.setEndValue(QRect((self.width()/2)-200,0,400,40))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(700)
        animation.start()

        hider = self.notification_auto_hider()
        hider.on_done.connect(self.hideNotification)
        hider.start()
        time.sleep(0.1)
    def hideNotification(self):
        self.toX = -70
        animation = QPropertyAnimation(self.notification_box,"geometry",self.notification_box)
        animation.setStartValue(QRect(self.notification_box.x(),0,self.notification_box.width(),40))
        animation.setEndValue(QRect(self.width()/2,0,0,40))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(700)
        animation.start()
        # position_animator(self.notification_box,self.width()/2-280,50,self.width()/2-280,self.toX,duration=200)
        # position_animator(self.notificationOK,self.notification_box.x()+self.notification_box.width()-80,50,self.notification_box.x()+self.notification_box.width()-80,self.toX,duration=200)
    class notification_auto_hider(QtCore.QThread):
        on_done = QtCore.pyqtSignal(object)
        def __init__(self):
            QtCore.QThread.__init__(self)
        def run(self):
            time.sleep(2.5)
            self.on_done.emit(self)

    def animate(self):
        opcty = 0.0
        for i in range(11):
            time.sleep(0.06)
            self.setWindowOpacity(opcty)
            opcty+=0.1
    def scroll1(self):
        value = self.scroller.value()
        # print(value)
        if -(value) >= 0:
            return
            # self.scroller.setMaximum(self.scroller.maximum()-400)
        self.workspace1.move(self.workspace1.x(),-(value))
        # print(self.workspace1.y())
    def scroll2(self):
        value = self.scroller2.value()
        if -(value) >= 0:
            return
        self.workspace2.move(self.workspace2.x(),-(value))
    def select1(self,sbtn = None):
        btn = self.sender()
        btn2 = btn
        self.animator2.move(-1000,0)
        if sbtn != None:
            btn = sbtn
        full_path = self.folder1 + "\\" +btn.text()
        fileInfo = QtCore.QFileInfo(full_path)
        icon = self.fetchIcon(btn.text())
        self.fileInfoIcon.setIcon(QIcon(r"Icons\File\\"+icon))
        self.fileInfoIcon.setIconSize(QSize(60,60))

        prop = os.stat(full_path)
        data_modified = datetime.datetime.utcfromtimestamp(prop.st_mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_modified = data_modified.replace("T"," ")
        data_modified = data_modified.replace("Z"," ")
        data_created = datetime.datetime.utcfromtimestamp(prop.st_ctime).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_created = data_created.replace("T"," ")
        data_created = data_created.replace("Z"," ")
        date_assessed = datetime.datetime.utcfromtimestamp(prop.st_atime).strftime('%Y-%m-%dT%H:%M:%SZ')
        date_assessed = date_assessed.replace("T"," ")
        date_assessed = date_assessed.replace("Z"," ")

        mime = MimeTypes()
        url = urllib.request.pathname2url(self.folder1 + btn.objectName())
        mime_type = mime.guess_type(url)
        mime_type = mime_type[0]
        if mime_type == None:
            mime_type = "Unknown"
        filename, file_extension = os.path.splitext(full_path)
        details = self.getExtentionDetail(file_extension)
        if os.path.isdir(full_path) == True:
            details = "Folder"
            self.fileInfoIcon.setIcon(QIcon(r"Icons\File\folder.png"))
            self.openInside.setDisabled(False)
            self.fileInfoProperties.setText("<b>MIME Type</b> : " + str(mime_type) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Size</b> : " + str(size(fileInfo.size())) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Modified</b> : " + data_modified + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Created</b> : " + data_created + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Assessed</b> : " + date_assessed + "<br><b>Extention Details : </b>" + str(details))
        else:
            self.fileInfoProperties.setText("<b>MIME Type</b> : " + str(mime_type) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Size</b> : " + str(size(fileInfo.size())) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Modified</b> : " + data_modified + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Created</b> : " + data_created + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Assessed</b> : " + date_assessed + "<br><b>Extention Details : </b>" + str(details)+"&nbsp;-&nbsp;<a href = '#' style = 'color:#d9dadb'>About Extension</a>")
            self.openInside.setDisabled(True)

        self.fileInfoLabel.setText(btn.objectName() + "&nbsp;&nbsp;&nbsp;<span style = 'font-size:10px;'>FOLDER 1</span>")

        # self.revealExploBtn.setDisabled(False)
        self.openFile.setDisabled(False)
        self.renameFile.setDisabled(False)

        # self.revealExploBtn2.setDisabled(True)
        self.openFile2.setDisabled(True)
        self.renameFile2.setDisabled(True)
        self.openInside2.setDisabled(True)

        self.copy_left.setDisabled(True)
        self.move_left.setDisabled(True)
        if self.currentButtonSide == 2:
            try:
                for i in self.selectedFiles2:
                    self.currentlySelectedBtn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                    btn = self.findChild(QPushButton,i)
                    btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())           
                self.selectedFiles2 = []       
            except Exception as e:
                print(e)

        self.move_right.setDisabled(False)
        self.send_to_trash.setDisabled(False)
        self.delete_permanently.setDisabled(False)
        self.currentlySelectedBtn = btn2
        self.currentButtonSide = 1
        self.copy_right.setDisabled(False)

        if self.multi_selection_state == False:
            try:
                for i in self.selectedFiles1:
                    self.findChild(QPushButton,i).setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                self.selectedFiles1 = []
            except:
                pass
        

        self.SelectedButton1 = btn2
        if self.SelectedButton1.objectName() in self.selectedFiles1:
            self.SelectedButton1.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
            self.selectedFiles1.remove(self.SelectedButton1.objectName())
            
        else:
            animation = QPropertyAnimation(self.animator,"geometry",self.animator)
            animation.setStartValue(QRect(self.SelectedButton1.width()/2,self.SelectedButton1.y(),0,self.itemHeight))
            animation.setEndValue(QRect(7,self.SelectedButton1.y(),self.SelectedButton1.width(),self.itemHeight))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(400)
            animation.start()
            QtCore.QTimer.singleShot(430, lambda: self.animator.move(-1000,10))
            if self.SelectedButton1.objectName() not in self.selectedFiles1:
                self.selectedFiles1.append(self.SelectedButton1.objectName())
            QtCore.QTimer.singleShot(430,self.crashHandler1)
        for i in self.new_file1:
            try:
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn_NEW",self.theme).getStyle())
            except:
                pass
        for i in self.new_file2:
            try:
                btn = self.findChild(QPushButton,i+"@F2")
                btn.setStyleSheet(parse("FileExplorerBtn_NEW",self.theme).getStyle())
            except:
                pass
        QtCore.QTimer.singleShot(440,self.crashHandler3)
        self.crashHandler4()
    def crashHandler3(self):
        if len(self.selectedFiles1) > 1:
            self.selectBtn.setText("Deselect All (" + str(len(self.selectedFiles1))+")")
        else:
            self.selectBtn.setText("Select All")
    def crashHandler1(self):
        try:
            for i in self.selectedFiles1:
                if i in self.new_file1:
                    btn = self.findChild(QPushButton,i)
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED_NEW",self.theme).getStyle())
                else:
                    btn = self.findChild(QPushButton,i)
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED",self.theme).getStyle())
        except:
            pass
    def select2(self,sbtn=None):
        self.animator.move(-1000,1000)
        btn = self.sender()
        btn2 = btn
        if sbtn != None:
            btn = sbtn
        full_path = self.folder2 + "\\" +btn.text()
        fileInfo = QtCore.QFileInfo(full_path)
        icon = self.fetchIcon(btn.text())
        self.fileInfoIcon.setIcon(QIcon(r"Icons\File\\"+icon))
        self.fileInfoIcon.setIconSize(QSize(60,60))

        prop = os.stat(full_path)
        data_modified = datetime.datetime.utcfromtimestamp(prop.st_mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_modified = data_modified.replace("T"," ")
        data_modified = data_modified.replace("Z"," ")
        data_created = datetime.datetime.utcfromtimestamp(prop.st_ctime).strftime('%Y-%m-%dT%H:%M:%SZ')
        data_created = data_created.replace("T"," ")
        data_created = data_created.replace("Z"," ")
        date_assessed = datetime.datetime.utcfromtimestamp(prop.st_atime).strftime('%Y-%m-%dT%H:%M:%SZ')
        date_assessed = date_assessed.replace("T"," ")
        date_assessed = date_assessed.replace("Z"," ")

        mime = MimeTypes()
        url = urllib.request.pathname2url(self.folder2 + btn.objectName().replace("@F2",""))
        mime_type = mime.guess_type(url)
        mime_type = mime_type[0]
        if mime_type == None:
            mime_type = "Unknown"
        filename, file_extension = os.path.splitext(full_path)
        details = self.getExtentionDetail(file_extension)
        if os.path.isdir(full_path) == True:
            details = "Folder"
            self.fileInfoIcon.setIcon(QIcon(r"Icons\File\folder.png"))
            self.openInside2.setDisabled(False)
            self.fileInfoProperties.setText("<b>MIME Type</b> : " + str(mime_type) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Size</b> : " + str(size(fileInfo.size())) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Modified</b> : " + data_modified + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Created</b> : " + data_created + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Assessed</b> : " + date_assessed + "<br><b>Extention Details : </b>" + str(details))
        else:
            self.openInside2.setDisabled(True)
            self.fileInfoProperties.setText("<b>MIME Type</b> : " + str(mime_type) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Size</b> : " + str(size(fileInfo.size())) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Modified</b> : " + data_modified + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Created</b> : " + data_created + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Assessed</b> : " + date_assessed + "<br><b>Extention Details : </b>" + str(details)+"&nbsp;-&nbsp;<a href = '#' style = 'color:#d9dadb'>About Extension</a>")


        self.fileInfoLabel.setText(btn.objectName().replace("@F2","") + "&nbsp;&nbsp;&nbsp;<span style = 'font-size:10px;'>FOLDER 2</span>")

        self.renameFile.setDisabled(True)
        # self.revealExploBtn.setDisabled(True)
        self.openInside.setDisabled(True)
        self.openFile.setDisabled(True)
        
        self.renameFile2.setDisabled(False)
        # self.revealExploBtn2.setDisabled(False)
        self.openFile2.setDisabled(False)

        self.copy_right.setDisabled(True)
        self.move_right.setDisabled(True)
        if self.currentButtonSide == 1:
            try:
                for i in self.selectedFiles1:
                    self.currentlySelectedBtn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                    btn = self.findChild(QPushButton,i)
                    btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())                  
                self.selectedFiles1 = []
            except Exception as e:
                print(e)

        self.currentlySelectedBtn = btn2
        self.send_to_trash.setDisabled(False)
        self.delete_permanently.setDisabled(False)
        self.move_left.setDisabled(False)
        self.currentButtonSide = 2
        self.copy_left.setDisabled(False)

        if self.multi_selection_state == False:
            try:
                for i in self.selectedFiles2:
                    self.findChild(QPushButton,i).setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                self.selectedFiles2 = []
            except:
                pass

        
        self.SelectedButton2 = btn2
        if self.SelectedButton2.objectName() in self.selectedFiles2:
            self.selectedFiles2.remove(self.SelectedButton2.objectName())
            self.SelectedButton2.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
        else:
            animation = QPropertyAnimation(self.animator2,"geometry",self.animator2)
            animation.setStartValue(QRect(self.SelectedButton2.width()/2,self.SelectedButton2.y(),0,self.itemHeight))
            animation.setEndValue(QRect(7,self.SelectedButton2.y(),self.SelectedButton2.width(),self.itemHeight))
            animation.setEasingCurve(QEasingCurve.OutQuart)
            animation.setDuration(400)
            animation.start()
            QtCore.QTimer.singleShot(430, lambda: self.animator2.move(-1000,10))
            if self.SelectedButton2.objectName() not in self.selectedFiles2:
                self.selectedFiles2.append(self.SelectedButton2.objectName())
            QtCore.QTimer.singleShot(430,self.crashHandler2)
        for i in self.new_file1:
            try:
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn_NEW",self.theme).getStyle())
            except:
                pass
        for i in self.new_file2:
            try:
                btn = self.findChild(QPushButton,i+"@F2")
                btn.setStyleSheet(parse("FileExplorerBtn_NEW",self.theme).getStyle())
            except:
                pass
        QtCore.QTimer.singleShot(440,self.crashHandler4)
        self.crashHandler3()
    def crashHandler4(self):
        if len(self.selectedFiles2) > 1:
            self.selectBtn2.setText("Deselect All (" + str(len(self.selectedFiles2))+")")
        else:
            self.selectBtn2.setText("Select All")
    def crashHandler2(self):
        try:
            for i in self.selectedFiles2:
                if i.replace("@F2","") in self.new_file2:
                    btn = self.findChild(QPushButton,i)
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED_NEW",self.theme).getStyle())
                else:
                    btn = self.findChild(QPushButton,i)
                    btn.setStyleSheet(parse("FileExplorerBtn_SELECTED",self.theme).getStyle())
        except Exception as err:
            print(err)
            pass
    def viewNormal(self):
        self.itemHeight = 35
        self.refreshFiles()
        self.viewBtn.setText("   Normal View")
    def viewBig(self):
        self.itemHeight = 43
        self.refreshFiles()
        self.viewBtn.setText("   Big View")
    def viewCompact(self):
        self.itemHeight = 28
        self.refreshFiles()
        self.viewBtn.setText("   Compact View")
    def viewSmall(self):
        self.itemHeight = 22
        self.refreshFiles()
        self.viewBtn.setText("   Small View")
    def getExtentionDetail(self,ext):
        ext = ext.replace(".","")
        validate_file("Data\\extention")
        fl = open("Data\\extention","r")
        content = fl.readlines()
        fl.close()
        for i in content:
            splitter = i.split(":")
            if ext.lower() == splitter[0].lower():
                return splitter[1]
        return "Unknown File Type"

    def fetchIcon(self,name):
        for i in os.listdir(r"Icons\File\\"):
            j = i.replace(".png","")
            if j in name:
                return i
        return "file.png"
    def prompt_for_confirmation(self,prompt_text):
            prompt = QMessageBox(self)
            prompt.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
            
            
            
            txt = prompt_text.split("@:|")
            lines = txt[1].split("<br>")

            if len(lines) >= 20:
                names = txt[1]
                names = names.replace("<br>","\n")
                names = names.split("</i></span></blockquote>")
                prompt.setText(txt[0]+"</i></span></blockquote>"+names[1])
                print(names[1])
                prompt.setDetailedText(" >   "+names[0])
            else:
                prompt_text = prompt_text.replace("@:|"," >   ")
                prompt.setText(prompt_text)

            prompt.setWindowTitle("Confirm Your Action")
            prompt.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ans = prompt.exec_()
            if ans == QMessageBox.Yes:
                return "YES"
            else:
                return "NO"
    def prompt_for_confirmation2(self,prompt_text):
            prompt = QMessageBox(self)
            prompt.setStyleSheet(parse("prompt_action_btns",self.theme).getStyle())
            prompt.setText(prompt_text)
            prompt.setWindowTitle("Confirm Your Action")
            prompt.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ans = prompt.exec_()
            if ans == QMessageBox.Yes:
                return "YES"
            else:
                return "NO"
    def returnFolder1(self):
        return self.folder1
    def copy_file_right(self):
        prompt_text = "Are you sure want to copy the following file(s) to <b>" + self.folder2 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles1))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles1))
        # cIndex = self.files1.index(self.selectedFiles1[-1])
        # self.next_btn = cIndex
        if len(self.selectedFiles1) >= self.prompt_int:
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return

        files = []
        for i in self.selectedFiles1:
            if not self.auto_replace:
                if i in self.files2:
                    prompt_text = "The file " + i + " already exist in " + self.folder1 + " . Would you like to replace it?"
                    prompt = self.prompt_for_confirmation2(prompt_text)
                    
                    if prompt == "NO":
                        continue
            files.append(i)
            self.old_newFile1 = "False"
            self.old_newFile2 = "True" 
            self.new_file2.append(i)

        
        
        CThread = Copy_Thread(files,self.folder1,self.folder2)
        self.connect(CThread, CThread.signal, self.refreshFiles)
        CThread.start()

        time.sleep(0.2)

        self.search1.setText("")
        self.search2.setText("")
    def copy_file_left(self):
        prompt_text = "Are you sure want to copy the following file(s) to <b>" + self.folder1 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles2))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles2))
        if len(self.selectedFiles2) >= self.prompt_int:
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return
        files=[]
        for i in self.selectedFiles2:
            if not self.auto_replace:
                if i.replace("@F2","") in self.files1:
                    prompt_text = "The file " + i + " already exist in " + self.folder1 + " . Would you like to replace it?"
                    prompt = self.prompt_for_confirmation2(prompt_text)
                    
                    if prompt == "NO":
                        continue

            files.append(i)
            self.old_newFile1 = "True"
            self.old_newFile2 = "False"


            if i.replace("@F2","") not in self.new_file1:
                self.new_file1.append(i.replace("@F2",""))

        CThread2 = Copy_Thread(files,self.folder2,self.folder1)
        self.connect(CThread2, CThread2.signal, self.refreshFiles)
        CThread2.start()
        time.sleep(0.2)

        self.search1.setText("")
        self.search2.setText("")
    def move_file_right(self):
        prompt_text = "Are you sure want to move the following file(s) to <b>" + self.folder2 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles1))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles1))        
        if len(self.selectedFiles1) >= self.prompt_int:
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return
        files=[]
        for i in self.selectedFiles1:
            if i in self.files2:
                if not self.auto_replace:
                    prompt_text = "The file " + i + " already exist in " + self.folder1 + " . Would you like to replace it?"
                    prompt = self.prompt_for_confirmation2(prompt_text)
                    
                    if prompt == "NO":
                        continue

            files.append(i)
            self.old_newFile1 = "False"
            self.old_newFile2 = "True" 
            self.new_file2.append(i)


        MThread = Move_Thread(files,self.folder1,self.folder2)
        self.connect(MThread, MThread.signal, self.refreshFiles)
        MThread.start()
        time.sleep(0.2)

        self.search1.setText("")
        self.search2.setText("")
    def move_file_left(self):
        prompt_text = "Are you sure want to move the following file(s) to <b>" + self.folder1 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles2))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles2))        
        if len(self.selectedFiles2) >= self.prompt_int:
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return
        files=[]
        for i in self.selectedFiles2:
            if not self.auto_replace:
                if i.replace("@F2","") in self.files1:
                    prompt_text = "The file " + i + " already exist in " + self.folder1 + " . Would you like to replace it?"
                    prompt = self.prompt_for_confirmation2(prompt_text)                
                    if prompt == "NO":
                        continue
            files.append(i)
            self.old_newFile1 = "True"
            self.old_newFile2 = "False"
            if i.replace("@F2","") not in self.new_file1:
                self.new_file1.append(i.replace("@F2",""))

        MThread2 = Move_Thread(files,self.folder2,self.folder1)
        self.connect(MThread2, MThread2.signal, self.refreshFiles)
        MThread2.start()
        
        time.sleep(0.2)
        
        self.search1.setText("")
        self.search2.setText("")
    def animate_new_item(self,new_file,side):
        btn = self.findChild(QPushButton,new_file)
        if side == 2:
            btn = self.findChild(QPushButton,new_file+"@F2")

        if side ==1:
            animation = QPropertyAnimation(self.s_animator,"geometry",self.s_animator)
        else:
            animation = QPropertyAnimation(self.s_animator2,"geometry",self.s_animator2)
        animation.setStartValue(QRect(btn.width()/2,btn.y(),0,self.itemHeight))
        animation.setEndValue(QRect(7,btn.y(),btn.width(),self.itemHeight))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(420)
        animation.start()
        if side ==1:
            animation = QPropertyAnimation(self.s_animator,"geometry",self.s_animator)
        else:
            animation = QPropertyAnimation(self.s_animator2,"geometry",self.s_animator2)
        animation.setStartValue(QRect(7,btn.y(),btn.width(),self.itemHeight))
        animation.setEndValue(QRect(btn.width()/2,btn.y(),0,self.itemHeight))
        animation.setEasingCurve(QEasingCurve.OutQuart)
        animation.setDuration(500)
        QtCore.QTimer.singleShot(1000, lambda:animation.start())
    def changeLocation(self):
        btn = self.sender()
        txt = btn.text()
        if txt == self.folder1:
            return
        else:
            self.folder1 = txt
            self.refreshFiles()
    def changeLocation2(self):
        btn = self.sender()
        txt = btn.text()
        if txt == self.folder2:
            return
        else:
            self.folder2 = txt
            self.refreshFiles()
    def refreshFiles(self,f1 = True,f2 = True,reverse = False,search1 = False,search2 = False,searchList= None):
        self.folder1 = self.folder1.replace("\\\\","\\")
        self.folder2 = self.folder2.replace("\\\\","\\")
        if self.folder1 not in self.visitedLocations1:
            self.visitedLocations1.append(self.folder1)
            self.addaction = self.recentMenu.addAction(self.folder1)
            self.addaction.triggered.connect(self.changeLocation)
        if self.folder2 not in self.visitedLocations2:
            self.visitedLocations2.append(self.folder2)
            self.addaction_two = self.recentMenu2.addAction(self.folder2)
            self.addaction_two.triggered.connect(self.changeLocation2)
        if search1 == False:
            # self.revealExploBtn2.setDisabled(True)            
            self.renameFile2.setDisabled(True)            
            self.openInside2.setDisabled(True)
            self.openFile2.setDisabled(True)
            self.locationBar2.setText(self.folder2)
            for i in self.files2:
                try:
                    btn = self.findChild(QPushButton,i+"@F2") 
                    btn.setObjectName("DELETED")
                    btn.type.deleteLater()
                    btn.size.deleteLater()
                    btn.deleteLater()
                except:
                    pass
            try:
                self.currentlySelectedBtn.deleteLater()
                self.currentlySelectedBtn.type.deleteLater()                
                self.currentlySelectedBtn.size.deleteLater()    
            except:
                pass
            self.selectedFiles2 = []
            self.SelectedButton2 = ""
            self.workspace2.close()

        if search2 == False:
            # self.revealExploBtn.setDisabled(True)            
            self.renameFile.setDisabled(True)            
            self.openInside.setDisabled(True)
            self.openFile.setDisabled(True)
            self.locationBar.setText(self.folder1)
            for i in self.files1:
                try:
                    btn = self.findChild(QPushButton,i)
                    btn.setObjectName("DELETED")
                    btn.type.deleteLater()
                    btn.size.deleteLater()
                    btn.deleteLater()
                except:
                    pass
            try:
                self.currentlySelectedBtn.deleteLater()
                self.currentlySelectedBtn.type.deleteLater()                
                self.currentlySelectedBtn.size.deleteLater()    
            except:
                pass

            self.selectedFiles1 = []
            self.SelectedButton1 = ""
            self.workspace1.close()

        if searchList == None:
            self.refreshFilesVariable()

        if searchList == None:
            if self.old_newFile1 == "True":
                self.scroll_bottom1()
            if self.old_newFile2 == "True":     
                self.scroll_bottom2()

            for i in self.new_file1:
                if i in self.files1:
                    self.files1.append(self.files1.pop(self.files1.index(i)))

            for i in self.new_file2:
                if i in self.files2:
                    self.files2.append(self.files2.pop(self.files2.index(i)))

        if searchList == None:
            list1 = self.files1
        else:
            list1 = searchList

        if search2 == False:
            pos = 5
            for i in list1:
                btn = QPushButton(self.workspace1)
                btn.setText(i)
                btn.setObjectName(i)
                btn.setGeometry(7,pos,self.mdi.width()-40,self.itemHeight)
                btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                btn.installEventFilter(self)
                btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                btn.customContextMenuRequested.connect(self.on_context_menu)
                btn.clicked.connect(lambda: self.select1())

                fileInfo = QtCore.QFileInfo(self.folder1 + "\\" +i)
                iconProvider = QtGui.QFileIconProvider()
                icon = iconProvider.icon(fileInfo)
                btn.setIcon(QIcon(icon))

                btn.type = QLabel(self.workspace1)
                btn.type.setText(iconProvider.type(fileInfo))
                btn.type.setGeometry(self.mdi.width()-250,pos,200,self.itemHeight)
                btn.type.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())

                from hurry.filesize import size

                btn.size = QLabel(self.workspace1)
                btn.size.setText(str(size(fileInfo.size())))
                btn.size.setGeometry(self.mdi.width()-150,pos,200,self.itemHeight)
                btn.size.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                
                pos+=self.itemHeight

            if len(self.files1) == 0:
                self.empty.move(130,self.mdi.y()+100)
            else:
                self.empty.move(-1000,0)
                
            self.workspace1.resize(self.mdi.width()-30 ,pos+650)
            self.scroller.setMaximum(self.workspace1.height()-650)
            # if pos <= 400:
            #     self.scroller.setMaximum(pos)
            # else:
            #     self.scroller.setMaximum(pos-400)
            # self.scroller.setValue(400)
            # self.scroller.sliderMoved.connect(self.scroll1)
            self.workspace1.show()

        pos = 5

        if searchList == None:
            list2 = self.files2
        else:
            list2 = searchList
        

        if search1 == False:
            for i in list2:
                btn = QPushButton(self.workspace2)
                btn.setText(i)
                btn.setObjectName(i+"@F2")
                btn.setGeometry(7,pos,self.mdi2.width()-40,self.itemHeight)
                btn.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                btn.clicked.connect(lambda: self.select2())
                btn.installEventFilter(self)               
                btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                btn.customContextMenuRequested.connect(self.on_context_menu2) 

                
                fileInfo = QtCore.QFileInfo(self.folder2 + "\\" +i)
                iconProvider = QtGui.QFileIconProvider()
                icon = iconProvider.icon(fileInfo)
                btn.setIcon(QIcon(icon))

                btn.type = QLabel(self.workspace2)
                btn.type.setText(iconProvider.type(fileInfo))
                btn.type.setGeometry(self.mdi2.width()-250,pos,200,self.itemHeight)
                btn.type.setStyleSheet("background-color:transparent;")
                btn.type.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())

                from hurry.filesize import size

                btn.size = QLabel(self.workspace2)
                btn.size.setText(str(size(fileInfo.size())))
                btn.size.setGeometry(self.mdi2.width()-150,pos,200,self.itemHeight)
                btn.size.setStyleSheet("background-color:transparent;")
                btn.size.setStyleSheet(parse("FileExplorerBtn",self.theme).getStyle())
                
                pos+=self.itemHeight


            if len(self.files2) == 0:
                self.empty2.move(self.mdi2.x()+120,self.mdi2.y()+100)
            else:
                self.empty2.move(-1000,0)
    
            self.workspace2.resize(self.mdi2.width()-30 ,pos+700)
            # print(self.scroller2.maximum())
            if pos <= 400:
                self.scroller2.setMaximum(pos)
            else:
                self.scroller2.setMaximum(pos-400)
            self.scroller2.sliderMoved.connect(self.scroll2)
            self.workspace2.show()


        self.animator.move(-1000,0)
        self.animator2.move(-1000,0)

        for i in self.new_file1:
            try:
                btn = self.findChild(QPushButton,i)
                btn.setStyleSheet(parse("FileExplorerBtn_NEW",self.theme).getStyle())
            except:
                # self.new_file1.remove(i)
                pass
        for i in self.new_file2:
            try:
                btn = self.findChild(QPushButton,i+"@F2")
                btn.setStyleSheet(parse("FileExplorerBtn_NEW",self.theme).getStyle())
            except:
                # self.new_file2.remove(i)
                pass
        
        if searchList == None:
            try:
                if self.old_newFile1 == "True":
                    if self.new_file1[-1] not in self.animation_complete1:
                        self.animate_new_item(self.new_file1[-1],1)
                        self.animation_complete1.append(self.new_file1[-1])
                if self.old_newFile2 == "True":     
                    if self.new_file2[-1] not in self.animation_complete2:
                        self.animate_new_item(self.new_file2[-1],2)
                        self.animation_complete2.append(self.new_file2[-1])
            except:
                pass
        
    def delete_file(self):        
        if self.currentButtonSide == 1:
            prompt_text = "Are you sure want to delete the following file(s) <b>permantly</b> from <b>" + self.folder1 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles1))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles1))        
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return

            Dthread = Delete_Thread(self.selectedFiles1,self.folder1)
            self.connect(Dthread, Dthread.signal, self.refreshFiles)
            Dthread.start()
            time.sleep(0.2)

        else:
            prompt_text = "Are you sure want to delete the following file(s) <b>permantly</b> from <b>" + self.folder2 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles2))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles2))        
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return

            Dthread2 = Delete_Thread(self.selectedFiles2,self.folder2)
            self.connect(Dthread2, Dthread2.signal, self.refreshFiles)
            Dthread2.start()
            time.sleep(0.2)

        self.search1.setText("")
        self.search2.setText("")
    def trash_file(self):        
        if self.currentButtonSide == 1:
            prompt_text = "Are you sure want to send the following file(s) <b>to recycle bin</b> from <b>" + self.folder1 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles1))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles1))        
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return

            Dthread = Trash_Thread(self.selectedFiles1,self.folder1)
            self.connect(Dthread, Dthread.signal, self.refreshFiles)
            Dthread.start()
            time.sleep(0.2)

        else:
            prompt_text = "Are you sure want to send the following file(s) <b>to recycle bin</b> from <b>" + self.folder2 + "</b><blockquote><span style='font-size:13px;'><i>@:|" + ("<br> >   ".join(self.selectedFiles2))+"</i></span></blockquote>TOTAL - " + str(len(self.selectedFiles2))        
            prompt = self.prompt_for_confirmation(prompt_text)
            if prompt == "YES":
                pass
            else:
                return

            Dthread2 = Trash_Thread(self.selectedFiles2,self.folder2)
            self.connect(Dthread2, Dthread2.signal, self.refreshFiles)
            Dthread2.start()
            time.sleep(0.2)

        self.search1.setText("")
        self.search2.setText("")
    def refreshFilesVariable(self):
        FILES  = os.listdir(self.folder1)
        FILES.sort()

        FILES2  = os.listdir(self.folder2)
        FILES2.sort()
        if self.setting == "SAF":
            pass
        elif self.setting == "SCF":
            SCF_FILES = list(set(FILES).intersection(FILES2))
            FILES = SCF_FILES
            FILES2 = SCF_FILES
        elif self.setting == "HCF":
            for i in FILES[:]:
                if i in FILES2:
                    FILES.remove(i)
                    FILES2.remove(i)

        self.files1 = FILES
        self.files2 = FILES2
def fader(obj = None,From = 0.0,to = 1.0,duration = 400):
    animation = QPropertyAnimation(obj,"opacity",obj)
    animation.setStartValue(From)
    animation.setEndValue(to)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuad)
    animation.start()

def validate_file(location,def_content = ""):
    try:
        filee = open(location,"r")
        filee.close()
        return "File Validation Successfull"
    except:
        try:
            filee = open(location,"w")
            if def_content != "":
                filee.write(def_content)
            filee.close()
            return "File Not Found : FIXED"
        except Exception as e:
            return "File Not Found : FAILED TO FIX"
def get_settings(stype="all"):
    validate_file(location=r"Data\settings",def_content = DEFAULT_SETTINGS)
    sfile = open("Data\\settings","r")
    content = sfile.read()
    sfile.close()

    for i in SETTING_NAMES:
        content = content.replace(i,"")
    content = content.split("\n")

    if stype == "all":
        return content
    elif stype == "prompt":
        if "True" in content[0]:
            prompt_int = content[0]
            prompt_int = prompt_int.replace("True;","")
            prompt_int = prompt_int.replace(" ","")
            prompt_int = prompt_int.replace("\n","")
            return prompt_int
        else:
            return 75
    elif stype == "developer_mode":
        return str(content[1])
    elif stype == "dbl_click":
        return content[2]
    elif stype == "dc_in":
        return content[3]
    elif stype == "auto_replace":
        return content[4]

def position_animator(obj = None,from_x = 0,from_y = 0,to_x = 0,to_y = 0,duration=500,easingcurve = QEasingCurve.OutQuart):
    animation = QPropertyAnimation(obj,"geometry",obj)
    animation.setStartValue(QRect(from_x,from_y,obj.width(),obj.height()))
    animation.setEndValue(QRect(to_x,to_y,obj.width(),obj.height()))
    animation.setEasingCurve(easingcurve)
    animation.setDuration(duration)
    animation.start()


class Copy_Thread(QtCore.QThread):
    def __init__(self,files,folder1,folder2):
        QtCore.QThread.__init__(self, parent=None)
        self.signal = QtCore.SIGNAL("signal")
        self.files = files
        self.folder1 = folder1
        self.folder2 = folder2
    def run(self):
        pythoncom.CoInitialize()
        for i in self.files:
            src = self.folder1 + "\\" + i.replace("@F2","")
            dst = self.folder2

            src = src.replace("\\\\","\\")
            dst = dst.replace("\\\\","\\")
            winutils.copy(src,dst)
            self.emit(self.signal)        

class Move_Thread(QtCore.QThread):
    def __init__(self,files,folder1,folder2):
        QtCore.QThread.__init__(self, parent=None)
        self.signal = QtCore.SIGNAL("signal")
        self.files = files
        self.folder1 = folder1
        self.folder2 = folder2
    def run(self):
        pythoncom.CoInitialize()
        for i in self.files:
            src = self.folder1 + "\\" + i.replace("@F2","")
            dst = self.folder2
            src = src.replace("\\\\","\\")
            dst = dst.replace("\\\\","\\")
            winutils.move(src,dst)
            self.emit(self.signal)

class Delete_Thread(QtCore.QThread):
    def __init__(self,files,folder):
        QtCore.QThread.__init__(self, parent=None)
        self.signal = QtCore.SIGNAL("signal")
        self.files = files
        self.folder = folder
    def run(self):
        pythoncom.CoInitialize()
        for i in self.files:
            self.src = self.folder + "\\" + i.replace("@F2","")
            self.src = self.src.replace("\\\\","\\")
            winutils.delete(self.src)
            self.emit(self.signal)
class Trash_Thread(QtCore.QThread):
    def __init__(self,files,folder):
        QtCore.QThread.__init__(self, parent=None)
        self.signal = QtCore.SIGNAL("signal")
        self.files = files
        self.folder = folder
    def run(self):
        pythoncom.CoInitialize()
        for i in self.files:
            self.src = self.folder + "\\" + i.replace("@F2","")
            self.src = self.src.replace("\\\\","\\")
            send2trash(self.src)
            self.emit(self.signal)