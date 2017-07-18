import os
class parse():
    def __init__(self,className,theme_path):
        try:
            path = os.getcwd()
            themeFile = open(theme_path,"r")
            themeContent = themeFile.readlines()
            themeFile.close()
        except Exception as Error:
            print ("Error While Loading Theme File : " + str(Error))
            return
        startRecording = 0
        global style
        style = ""
        for i in themeContent:
            if className in i:
                startRecording = 1
            if startRecording == 1:
                startRecording = 2
                continue
            if startRecording == 2 and "]" in i:
                break
            if startRecording == 2:
                style = style + "\n" + i
    def getStyle(self):
        return style
    def getName(self,theme_type):
        themeFile = open("Themes\\"+theme_type)
        themeContent = themeFile.readlines()
        # themeFile.close()
        themeFile.close()
        name = themeContent[0]
        name = name.replace("#name ","")
        name = name.replace("#name","")
        name = name.replace("\n","")
        return name
