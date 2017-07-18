from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading,sys,os,time
from themeParser import parse
import qtawesome as qta
from studio import StudioMain

class Launcher(QWidget):
    def __init__(self,parent=None):
        super(Launcher,self).__init__(parent)

        QtGui.QFontDatabase.addApplicationFont('Data\\Fonts\\Ubuntu-Light.ttf')
        QtGui.QFontDatabase.addApplicationFont('Data\\Fonts\\Junction-regular.otf')

        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())
        pos1 = self.x()
        pos2 = self.y()
        thread = threading.Thread(target=self.animate)
        thread.start()
        self.setGeometry(100,100,640,550)
        position_animator(self,pos1,900,pos1,pos2,duration=600)
        self.setWindowOpacity(0.0)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        font = QFont("Times",25)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)
        self.setWindowIcon(QIcon(r"Icons\\2.png"))
        self.setWindowTitle("Backup Manager 2")

        self.setAttribute(Qt.WA_TranslucentBackground)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(10)
        effect.setColor(QColor("#bdc3c7"))
        effect.setOffset(2,2)


        border = QLabel(self)
        border.setGeometry(2,2,640-7,550-7)
        border.setStyleSheet("border-radius:2px;border:0px solid #ddd;border-left:4px solid #2ecc71; background-color:white;border-radius: 0px;")
        border.setGraphicsEffect(effect)

        # self.setStyleSheet("border:0px solid grey;background-color:rgba(0,0,0,100);font-family:'Ubuntu Light';")
        self.setStyleSheet("border:0px solid grey;background-color:white;font-family:'Ubuntu Light';")
        close = QPushButton(self)
        close.setGeometry(590-4,2,50,50)
        close.setStyleSheet(".QPushButton{background-color:#e5796e;border:0;} .QPushButton:hover{background-color:#e74c3c;}")
        close.setIcon(QIcon(r"Icons\close.png"))
        close.setIconSize(QSize(20,20))
        close.setCursor(Qt.PointingHandCursor)
        close.clicked.connect(self.close)

        label = QLabel(self)
        label.setText("Choose Folder 1 Location<br><br><br><br><br>Choose Folder 2 Location<br><br><br><br><br><span style='font-size:24px;'>Theme : </span><br><br><br><span style='font-size:24px;'>Setting : </span>")
        label.setStyleSheet("font-family:'Ubuntu Light';font-size:12px;")
        label.move(80,210)

        title = QPushButton(self)
        title.setIcon(QIcon(r"Icons\bmcover.png"))
        title.setStyleSheet("background-color:None;border:0;")
        title.setIconSize(QSize(350,170))
        title.move(130,20)

        directory = r"Data\\"
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("ERROR DIRECTORY 'DATA' WAS NOT FOUND: FIXED")

        print(self.validate_file(r"Data\workspace1"))
        print(self.validate_file(r"Data\workspace2"))
        print(self.validate_file(r"Data\themeChosen",def_content = "Light Theme"))
        print(self.validate_file(r"Data\settingChosen",def_content = "Show All Files"))
        reader = open(r"Data\workspace1","r")
        folders1 = reader.readlines()
        reader.close()

        reader = open(r"Data\workspace2","r")
        folders2 = reader.readlines()
        reader.close()
        
        reader = open(r"Data\themeChosen","r")
        themeChosen = reader.read()
        reader.close()
        
        reader = open(r"Data\settingChosen","r")
        settingChosen = reader.read()
        reader.close()


        combo_box_style = """.QComboBox{
                font-size:18px;
                font-family:'Ubuntu Light';
                color : black;
            } 
            .QComboBox::drop-down{
                background-color:#2ecc71;
                width:40px;
                border:0px solid #2ecc71;
                border-left:0;
            } 
            .QComboBox::drop-down::hover{
                background-color:#29b765;
            } 
            QComboBox::down-arrow {
                image:  url("Icons/history.png");
            }
            QComboBox QAbstractItemView {
                border: 2px solid #2ecc71;
                selection-background-color: #2ecc71;
                selection-color:white;
                outline:0;
            }
            """

        self.loc1 = QLineEdit(self)
        self.loc1.setStyleSheet("border-radius:2px;border:2px solid #3e3e3e;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")
        self.loc1.setGeometry(80,230,400,40)
        self.loc1.setPlaceholderText("Choose a location for Workspace 1")

        historyBox = QComboBox(self)

        hist1 = []
        for i in folders1:
            if i.replace("\n","") not in hist1:
                j=i.replace("\n","")
                if j == "\n" or j=="" or j==" ":
                    continue
                hist1.append(j)
        for i in hist1[:5]:
            historyBox.addItem(i)

        historyBox.setLineEdit(self.loc1)
        historyBox.setGeometry(80,230,400,40)
        historyBox.setStyleSheet(combo_box_style)

        for i in folders1:
            if i != "\n" and i != "" and i != " ":
                j = i[:-1]
                self.loc1.setText(j)
                break
        self.loc1.textChanged.connect(self.validateFields)

        choose1 = QPushButton(self)
        choose1.setStyleSheet(".QPushButton{border-radius:2px;background-color:#57ace5;border:0;} .QPushButton:hover{background-color:#3498db;}")
        choose1.setGeometry(500,230,80,40)
        choose1.setCursor(Qt.PointingHandCursor)
        choose1.setIcon(QIcon(r"Icons\folder.png"))
        choose1.setIconSize(QSize(24,24))
        choose1.clicked.connect(self.choose1)

        self.loc2 = QLineEdit(self)
        self.loc2.setStyleSheet("border-radius:2px;border:2px solid #3e3e3e;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")
        self.loc2.setGeometry(80,310,400,40)
        self.loc2.setPlaceholderText("Choose a location for Workspace 2")


        historyBox2 = QComboBox(self)

        hist2 = []
        for i in folders2:
            if i.replace("\n","") not in hist2:
                j=i.replace("\n","")
                if j == "\n" or j=="" or j==" ":
                    continue
                hist2.append(j)
        for i in hist2[:5]:
            historyBox2.addItem(i)

        historyBox2.setLineEdit(self.loc2)
        historyBox2.setGeometry(80,310,400,40)
        historyBox2.setStyleSheet(combo_box_style)

        
        for i in folders2:
            if i != "\n" and i != "" and i != " ":
                j = i[:-1]
                self.loc2.setText(j)
                break
        self.loc2.textChanged.connect(self.validateFields)


        choose2 = QPushButton(self)
        choose2.setStyleSheet(".QPushButton{border-radius:2px;background-color:#57ace5;border:0;} .QPushButton:hover{background-color:#3498db;}")
        choose2.setGeometry(500,310,80,40)
        choose2.setCursor(Qt.PointingHandCursor)
        choose2.setIcon(QIcon(r"Icons\folder.png"))
        choose2.setIconSize(QSize(24,24))
        choose2.clicked.connect(self.choose2)

        self.themes = os.listdir(path='Themes\\')
        self.themes_NAME = []

        self.theme = QComboBox(self)
        self.theme.setGeometry(187,367,130,40)
        self.theme.setStyleSheet(".QComboBox{border-radius:2px;border:2px solid #3e3e3e;font-size:16px;font-family:'Ubuntu Light';color : #3e3e3e;padding-left:10px;} .QListView{background-color:red;} .QComboBox::drop-down{background-color:grey;} .QComboBox .QListView{background-color:red;} QComboBox QAbstractItemView {border: 2px solid #3e3e3e;selection-background-color: #3e3e3e;selection-color:white;outline:0;}")
        
        self.setting_Select = QComboBox(self)
        self.setting_Select.setGeometry(187,430,180,40)
        self.setting_Select.setStyleSheet(".QComboBox{border-radius:2px;border:2px solid #3e3e3e;font-size:16px;font-family:'Ubuntu Light';color : #3e3e3e;padding-left:10px;} .QListView{background-color:red;} .QComboBox::drop-down{background-color:grey;} .QComboBox .QListView{background-color:red;} QComboBox QAbstractItemView {border: 2px solid #3e3e3e;selection-background-color: #3e3e3e;selection-color:white;outline:0;}")
        self.setting_Select.addItem("Show All Files")
        self.setting_Select.addItem("Show Common Files")
        self.setting_Select.addItem("Hide Common Files")

        for i in self.themes:
            if ".bm2" in i:
                pass
            else:
                self.themes.remove(i)
        for i in self.themes:
            name = parse.getName("",i)
            self.themes_NAME.append(name)
            self.theme.addItem(name)

        themeChosen = themeChosen.replace("\n","")
        settingChosen = settingChosen.replace("\n","")
        self.theme.setCurrentIndex(self.themes_NAME.index(themeChosen))
        
        self.setting_NAME = []
        self.setting_NAME.append("Show All Files")
        self.setting_NAME.append("Show Common Files")
        self.setting_NAME.append("Hide Common Files")

        self.setting_Select.setCurrentIndex(self.setting_NAME.index(settingChosen))

        self.launch = QPushButton(self)
        self.launch.setGeometry(486,492-1,149,54)
        self.launch.setStyleSheet(".QPushButton{border-radius:2px;background-color:#48db86;border:0;} .QPushButton:hover{background-color:#2ecc71;} .QPushButton:disabled{background-color:#b3f2cd;}")
        self.launch.setCursor(Qt.PointingHandCursor)
        self.launch.setIcon(QIcon(r"Icons\launch.png"))
        self.launch.setIconSize(QSize(100,100))
        self.launch.clicked.connect(self.launchStudio)

        help_icon = QPushButton(self)
        help_icon.setIcon(QIcon(r"Icons\help.png"))
        help_icon.move(4+2,512)
        help_icon.setStyleSheet("background-color:white;border:0;padding:8px;")
        help_icon.setCursor(Qt.PointingHandCursor)
        help_icon.clicked.connect(about.show)

        info = QLabel(self)
        info.setText("Made By Ahmad Taha - Version 1.0 Beta")
        info.move(37+2,520)
        info.setStyleSheet("color:grey;")
        self.show()

        settings2 = get_settings(stype="developer_mode")
        if "True" in settings2:
            self.launchStudio()

        self.validateFields()
    def launchStudio(self):
        position_animator(self,self.x(),self.y(),self.x(),-600,duration=600)     

        save_file = open(r"Data\workspace1","r")
        content = save_file.read()
        save_file.close()

        save_file = open(r"Data\workspace1","w")
        save_file.write(self.loc1.text()+"\n"+content)
        save_file.close()

        save_file = open(r"Data\workspace2","r")
        content = save_file.read()
        save_file.close()

        save_file = open(r"Data\workspace2","w")
        save_file.write(self.loc2.text()+"\n" +content)
        save_file.close()

        studio.theme = r"Themes\\" + self.themes[self.themes_NAME.index(self.theme.currentText())]

        save_file = open(r"Data\themeChosen","w")
        save_file.write(self.theme.currentText())
        save_file.close()
        
        save_file = open(r"Data\settingChosen","w")
        save_file.write(self.setting_Select.currentText())
        save_file.close()

        setting_Selected = self.setting_Select.currentText()
        if setting_Selected == "Show All Files":
            setting_Selected = "SAF"
        elif setting_Selected == "Show Common Files":
            setting_Selected = "SCF"
        elif setting_Selected == "Hide Common Files":
            setting_Selected = "HCF"
        studio.setting = setting_Selected
        studio.folder1 = self.loc1.text()
        studio.folder2 = self.loc2.text()
        studio.window()
        QtCore.QTimer.singleShot(500, lambda: self.close())
    def validateFields(self):
        i=1
        if not os.path.exists(self.loc1.text()):
            self.loc1.setStyleSheet("border-radius:2px;border:2px solid #e74c3c;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")
            self.launch.setDisabled(True)
            if self.loc1.text() == "":
                self.loc1.setStyleSheet("border-radius:2px;border:2px solid #3e3e3e;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")
        else:
            self.loc1.setStyleSheet("border-radius:2px;border:2px solid #2ecc71;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")            
            # self.launch.setDisabled(False)
            i+=1

        if not os.path.exists(self.loc2.text()):
            self.loc2.setStyleSheet("border-radius:2px;border:2px solid #e74c3c;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")
            self.launch.setDisabled(True)
            if self.loc2.text() == "":
                self.loc2.setStyleSheet("border-radius:2px;border:2px solid #3e3e3e;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")
        else:
            self.loc2.setStyleSheet("border-radius:2px;border:2px solid #2ecc71;background-color:white;font-size:18px;font-family:'Ubuntu Light';padding-left:10px;")            
            # self.launch.setDisabled(False)
            i+=1
        if i==3:
            self.launch.setDisabled(False)
            
    def choose1(self):
        self.folder1 = QFileDialog.getExistingDirectory(self, 'Choose Folder 1', "D:", QtGui.QFileDialog.ShowDirsOnly)
        self.loc1.setText(self.folder1)
        print(self.validate_file(r"Data\workspace1"))

        save_file = open(r"Data\workspace1","r")
        content = save_file.read()
        save_file.close()

        save_file = open(r"Data\workspace1","w")
        save_file.write(self.folder1+"\n"+content)
        save_file.close()
    
    def choose2(self):
        self.folder2 = QFileDialog.getExistingDirectory(self, 'Choose Folder 2', "D:", QtGui.QFileDialog.ShowDirsOnly)
        self.loc2.setText(self.folder2)

        print(self.validate_file(r"Data\workspace2"))

        save_file = open(r"Data\workspace2","r")
        content = save_file.read()
        save_file.close()

        save_file = open(r"Data\workspace2","w")
        save_file.write(self.folder2+"\n" +content)
        save_file.close()

    def animate(self):
        opcty = 0.0
        for i in range(11):
            time.sleep(0.06)
            self.setWindowOpacity(opcty)
            opcty+=0.1
    def validate_file(self,location,def_content = ""):
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
def position_animator(obj = None,from_x = 0,from_y = 0,to_x = 0,to_y = 0,duration=500):
    animation = QPropertyAnimation(obj,"geometry",obj)
    animation.setStartValue(QRect(from_x,from_y,obj.width(),obj.height()))
    animation.setEndValue(QRect(to_x,to_y,obj.width(),obj.height()))
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuart)
    animation.start()
def fader(obj = None,From = 0.0,to = 1.0,duration = 400):
    animation = QPropertyAnimation(obj,"opacity",obj)
    animation.setStartValue(From)
    animation.setEndValue(to)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuad)
    animation.start()
class Help(QWidget):
    def __init__(self,parent = None):
        super(Help,self).__init__(parent)
        self.setWindowTitle("About Backup Manager 2")
        self.setWindowIcon(QIcon(r"Icons\\2.png"))
        self.setStyleSheet("Background-color:white;")

        btn = QPushButton(self)
        btn.setIcon(QIcon(r"Icons\about.png"))
        btn.setIconSize(QSize(400,400))
        btn.move(0,0)
        btn.setStyleSheet("background-color:None;border:0;")

        self.resize(390,400)
def get_settings(stype="all"):
    try:
        print(Launcher.validate_file("",location=r"Data\settings"))
        sfile = open("Data\\settings","r")
        content = sfile.readlines()
        sfile.close()

        if stype == "developer_mode":
            return str(content[1])
    except Exception as err:
        print("Error while validating Developer Mode Setting : " + str(err))
        return "False"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    about = Help()
    studio = StudioMain()
    wndw = Launcher()
    # wndw.show()
    sys.exit(app.exec_())