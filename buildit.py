# @file buildit.py
#
# Copyright IBM Corporation 2022
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from argparse import ArgumentParser
from configparser import ConfigParser
from os import path
from platform import system as platform_system
from sys import exit as sys_exit

from terraform.common.common import Common
from terraform.generate.generate import Generate

class Config:
    def __init__(self,appName):
        
        # platform specific...
        if self.isWindows():
            self.filename = appName + ".ini"
        else:
            self.filename =  path.expanduser('~') + '/Library/Application Support/' + appName + ".ini"
        
        self.config = ConfigParser()
        if path.exists(self.filename):
            self.config.read(self.filename)
        if not self.config.has_section("parameters"):
            self.config.add_section("parameters")

        # platform specific...
        if not self.has("inputDirectory"):
            if self.isWindows():
                self.setInputDirectory("./" + appName)
            else:
                self.setInputDirectory(path.expanduser('~') + '/' + appName)

        # platform specific...
        if not self.has("outputDirectory"):
            if self.isWindows():
                self.setOutputDirectory("./" + appName)
            else:
                self.setOutputDirectory(path.join(path.expanduser('~'), 'Documents', appName))

    def isWindows(self):
        #return hasattr(sys, 'getwindowsversion')
        return platform_system == 'Windows'

    def get(self,propertyName):
        if propertyName in self.config["parameters"]:
            return self.config["parameters"][propertyName]
        else:
            return None
    
    def set(self,propertyName,value):
        self.config.set("parameters",propertyName,value)
        
    def has(self,propertyName):
        return self.config.has_option("parameters",propertyName)

    def write(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
            
    #def getAPIKey(self):
    #    return self.get("apiKey")
    
    #def setAPIKey(self,apiKey):
    #    self.set("apiKey",apiKey)

    def getInputType(self):
        return self.get("inputType")
    
    def setInputType(self,inputType):
        self.set("inputType",inputType)

    def getInputDirectory(self):
        return self.get("inputDirectory")
    
    def setInputDirectory(self,inputDirectory):
        self.set("inputDirectory",inputDirectory)

    def getOutputDirectory(self):
        return self.get("outputDirectory")
    
    def setOutputDirectory(self,outputDirectory):
        self.set("outputDirectory",outputDirectory)

    def getRunMode(self):
        return self.get("runmode")

    def setRunMode(self, runmode):
        return self.set("runmode", runmode)

class buildit():
   title = None
   top = None
   statusText = None
   common = None
   generate = None

   def __init__(self):
      self.common = Common()
      self.title = self.common.getToolCopyright().split(' - ')

   #print(COPYRIGHT)
   #print(toolheader)

   def main(self): 

        config = Config("buildIT")  
        #self.apiKey = config.getAPIKey()
        inputtype = config.getInputType()
        inputdirectory = config.getInputDirectory()
        outputdirectory = config.getOutputDirectory()
        runmode = config.getRunMode()
      
        parser = ArgumentParser(description='buildIT')

        parser.add_argument('-input', dest='inputfolder',  default=self.common.getInputDirectory(), help='input directory')
        parser.add_argument('-output', dest='outputfolder', default=path.join(self.common.getOutputDirectory(), self.common.getOutputDirectory()), help='output folder')
        parser.add_argument('-type', dest='inputtype', default=self.common.getInputType(), help='input type')

        parser.add_argument('-mode', dest='runmode', default=self.common.getRunMode().value, help="No gui (batch mode)")
        parser.add_argument('--version', action='version', version='buildIT ' + self.common.getToolCopyright().split(' ')[1])
        
        args = parser.parse_args()

        inputfolder = args.inputfolder.replace(' ', '')
        outputfolder = args.outputfolder.replace(' ', '')
        inputtype = args.inputtype.replace(' ', '').lower()
        runmode = args.runmode.lower()

        self.common.setInputDirectory(inputfolder)
        self.common.setOutputDirectory(outputfolder)
        self.common.setInputType(inputtype)

        self.minInfo = False

        done = False

        if self.common.isBatchMode(args.runmode):
            #try: 
                #print(COPYRIGHT)
                #print(toolheader)

                # Check for existing input file and exit if not valid.
                #if not os.path.isfile(self.inputFile):
                #    print(invalidinputfilemessage % inputfile)
                #    return

                inputdirectory = self.common.getInputDirectory()
                outputdirectory = self.common.getOutputDirectory()

                #backupdirectory(userdata)

                #if apikey != KEY_PLACEHOLDER and apikey != None and apikey != '':
                #    userdata['inputtype'] = 'rias'
                #    inputbase = apikey
                #    outputfile = inputbase + '.' + outputtype
                #    userdata['outputfile'] = outputfile
                #    print(starttoolmessage % 'RIAS')
                #if inputfolder != INPUT_PLACEHOLDER and inputfolder != None and inputfolder != '':
                if inputdirectory != None and inputdirectory != '':
                    self.common.setInputType('xlsx')
                    #basename = os.path.basename(inputfolder)
                    #inputbase = os.path.splitext(basename)[0]
                    #inputtype = os.path.splitext(basename)[1][1:]
                    #outputfolder = inputbase + '.' + outputtype
                    #userdata['genpath'] = outputfolder
                    self.common.printStart(inputdirectory)
                else:
                    return

                basename = path.basename(inputdirectory)
                self.common.setOutputDirectory(path.join(outputdirectory, basename + '.resources'))

                self.generate = Generate(self.common)
                self.generate.all()

                self.common.printDone(self.common.getOutputDirectory())

                done = True

        elif self.common.isGUIMode(args.runmode):
            from tkinter import Button, Entry, filedialog, Frame, IntVar, Label, messagebox, OptionMenu, StringVar, Tk, LEFT, RIGHT, TOP, E, W, X
        
            self.top = Tk()
            self.title = self.common.getToolCopyright().split(' - ')
            self.top.title(self.title[0])
            self.statusText = StringVar()

            frame = Frame(self.top)
            frame.pack(fill=X, side=TOP)
            frame.grid_columnconfigure(1, weight=1)            
            row = 1
    
            genbutton = Frame(frame)
            eGenerate = Button(genbutton, text="Generate Terraform", state='normal', command=lambda: onClickGenerate())
            genbutton.grid(row=row, columnspan=2, sticky=E)
            eGenerate.pack(side=LEFT)
            row = row + 1
            
            #lAPIKey = tkinter.Entry(frame, bd=5)
            #lAPIKey.insert(0, apikey)
            #lAPIKey.grid(row=row, column=1, sticky=tkinter.W + tkinter.E)
            #config.set("apiKey",apikey)
            #config.write()
            #row = row + 1

            #tkinter.Label(frame, text="Yaml").grid(row=row)
            #lInputFile = tkinter.Label(frame, text=inputfile)
            lInputDirectory = Entry(frame, bd=5)
            #lInputDirectory.insert(0, inputdirectory)
            lInputDirectory.grid(row=row, column=1, sticky=W + E)
            row = row + 1

            #if apikey != KEY_PLACEHOLDER and apikey != None and apikey != '':
            #    lInputFile.delete(0, 'end')
            #    self.inputFile = ''
            #    config.set("inputFile", self.inputFile)
            #    config.write()

            def onClickSelectInputDirectory():
                folder_selected = filedialog.askdirectory(initialdir = inputfolder,title = "Select Input Directory")
                if folder_selected != None and len(folder_selected) > 0:
                    self.inputDirectory = folder_selected
                    #lAPIKey.delete(0, 'end')
                    lInputDirectory.delete(0, 'end')
                    lInputDirectory.insert(0, self.inputDirectory)
                    lInputDirectory.configure(text=self.inputDirectory)
                    #lAPIKey.delete(0, 'end')
                    #self.apiKey = ''
                    #config.set("apiKey", self.apiKey)
                    #config.write()
                    config.set("inputDirectory", self.inputDirectory)
                    config.write()
                    
            inputbutton = Frame(frame)
            eSelectInputDirectory = Button(inputbutton, text="Select Input Directory", command=lambda: onClickSelectInputDirectory())
            inputbutton.grid(row=row, columnspan=2, sticky=E)
            eSelectInputDirectory.pack(side=RIGHT)
            row = row + 1

            #inputfile = userdata['inputfile']
            #basename = os.path.basename(inputfile)
            #inputbase = os.path.splitext(basename)[0]
            #inputtype = os.path.splitext(basename)[1][1:]
            #outputfile = inputbase + '.' + outputtype
            #userdata['outputfile'] = outputfile

            #tkinter.Label(frame, text="Output").grid(row=row)
            #lOutputDirectory = tkinter.Label(frame, text=outputfolder)
            lOutputDirectory = Entry(frame, bd=5)
            lOutputDirectory.insert(0, outputdirectory)
            #lOutputDirectory.grid(row=row,column=1)
            lOutputDirectory.grid(row=row, column=1, sticky=W + E)
            row = row + 1

            def onClickSelectOutputDirectory():
                folder_selected = filedialog.askdirectory(initialdir = outputfolder, title = "Select Output Directory")
                if folder_selected != None and len(folder_selected) > 0:
                    self.outputDirectory = folder_selected
                    lOutputDirectory.delete(0, 'end')
                    lOutputDirectory.insert(0, self.outputDirectory)
                    lOutputDirectory.configure(text=self.outputDirectory)
                    config.set("outputDirectory",self.outputDirectory)
                    config.write()
                    self.common.setOutputDirectory(self.outputDirectory)
                    
            outputbutton = Frame(frame)
            eSelectOutputDirectory = Button(outputbutton, text="Select Output Directory", command=lambda: onClickSelectOutputDirectory())
            outputbutton.grid(row=row, columnspan=2, sticky=E)
            eSelectOutputDirectory.pack(side=RIGHT)
            row = row + 2

            #layoutoptions = [
            #    "Circular Layout", 
            #    "Distributed Recursive Layout", 
            #    "Fruchtermain-Reingold Layout",
            #    "Fruchtermain-Reingold 3D Layout",
            #    "Fruchtermain-Reingold Grid Layout",
            #    "Kamada-Kawai Layout",
            #    "Kamada-Kawai 3D Layout",
            #    "Large Graph Layout",
            #    "Random Layout",
            #    "Random 3D Layout",
            #    "Reingold-Tilford Tree Layout",
            #    "Reingold-Tilford Tree Polar Layout",
            #    "Spherical Layout"]
            #eOutputLayout = tkinter.StringVar(self.top)
            #eOutputLayout.set("Reingold-Tilford Tree Layout")
            #layoutmenu = tkinter.OptionMenu(self.top, eOutputLayout, *layoutoptions)
            #layoutmenu.pack()

            #typeoptions = [
            #    "Generate Drawio", 
            #    "Generate PlantUML"]
            #eOutputType = tkinter.StringVar(self.top)
            #eOutputType.set("Generate Drawio")
            #typemenu = tkinter.OptionMenu(self.top, eOutputType, *typeoptions)
            #typemenu.pack()

            #splitoptions = [
            #    "Generate Single File", 
            #    "Generate Files by Region", 
            #    "Generate Files by VPC"]
            #eOutputSplit = tkinter.StringVar(self.top)
            #eOutputSplit.set("Generate Single File")
            #splitmenu = tkinter.OptionMenu(self.top, eOutputSplit, *splitoptions)
            #splitmenu.pack()

            def onClickGenerate():
                try:
                    self.statusText.set("Starting")
                    frame.after_idle(onClickGenerate)                   

                    #outputlayout = str(eOutputLayout.get())
                    #if outputlayout == "Circular Layout": 
                    #    outputlayout = "circle"
                    #elif outputlayout == "Distributed Recursive Layout": 
                    #    outputlayout = "drl"
                    #elif outputlayout == "Fruchtermain-Reingold Layout":
                    #    outputlayout = "fr"
                    #elif outputlayout == "Fruchtermain-Reingold 3D Layout":
                    #    outputlayout = "fr3d"
                    #elif outputlayout == "Fruchtermain-Reingold Grid Layout":
                    #    outputlayout = "grid_fr"
                    #elif outputlayout == "Kamada-Kawai Layout":
                    #    outputlayout = "kk"
                    #elif outputlayout == "Kamada-Kawai 3D Layout":
                    #    outputlayout = "kk3d"
                    #elif outputlayout == "Large Graph Layout":
                    #    outputlayout = "large"
                    #elif outputlayout == "Random Layout":
                    #    outputlayout = "random"
                    #elif outputlayout == "Random 3D Layout":
                    #    outputlayout = "random_3d"
                    #elif outputlayout == "Reingold-Tilford Tree Layout":
                    #    outputlayout = "rt"
                    #elif outputlayout == "Reingold-Tilford Tree Polar Layout":
                    #    outputlayout = "rt_circular"
                    #elif outputlayout == "Spherical Layout":
                    #    outputlayout = "sphere"
                    #userdata['outputlayout'] = outputlayout

                    #outputtype = str(eOutputType.get())
                    #if outputtype == "Generate Drawio": 
                    #    outputtype = "drawio"
                    #elif outputtype == "Generate PlantUML":
                    #    outputtype = "puml"
                    #userdata['outputtype'] = outputtype

                    #outputsplit = str(eOutputSplit.get())
                    #if outputsplit == "Generate Single File":
                    #    outputsplit = "all"
                    #elif outputsplit == "Generate Files by Region":
                    #    outputsplit = "region"
                    #elif outputsplit == "Generate Files by VPC":
                    #    outputsplit = "vpc"
                    #userdata['outputsplit'] = outputsplit

                    #apikey = self.apiKey
                    #apikey = str(lAPIKey.get())
                    #userdata['apikey'] = apikey 

                    #inputfile = self.inputFile
                    inputdirectory = str(lInputDirectory.get())
                    self.common.setInputDirectory(inputdirectory)
                    basename = path.basename(inputdirectory)

                    outputdirectory = str(lOutputDirectory.get())
                    self.common.setOutputDirectory(path.join(outputdirectory, basename + '.resources'))

                    self.statusText.set("Starting")
                    #print(starttoolmessage % self.inputFile)

                    #if apikey != KEY_PLACEHOLDER and apikey != None and apikey != '':
                    #    userdata['inputtype'] = 'rias'
                    #    inputbase = apikey
                    #    outputfile = str(inputbase) + '.' + outputtype
                    #    userdata['outputfile'] = outputfile
                    #    print(starttoolmessage % 'RIAS')
                    #if inputdirectory != INPUT_PLACEHOLDER and inputdirector != None and inputdirectory != '':
                    #if inputdirectory != None and inputdirectory != '':
                    #    userdata['inputtype'] = 'xlsx'
                    #    #basename = os.path.basename(self.inputFile)
                    #    #inputbase = os.path.splitext(basename)[0]
                    #    #inputtype = os.path.splitext(basename)[1][1:]
                    #    #outputfile = inputbase + '.' + outputtype
                    #    #userdata['outputfile'] = outputfile
                    #    print(starttoolmessage % inputdirectory)
                    #else:
                    #    sys.exit()

                    self.generate = Generate(self.common)
                    self.generate.all()

                    #inputdata = load(userdata)
                    #if inputdata != None:
                    #    userdata['inputdata'] = inputdata

                    #    setupdata = analyze(userdata)
                    #    userdata['setupdata'] = setupdata

                    #    if outputtype == 'puml':
                    #        genpuml(userdata)
                    #    elif outputtype == 'drawio':
                    #        genxml(userdata)
                    #    else:
                    #        print(invalidoutputtypemessage % outputtype)

                    self.common.printDone(self.common.getOutputDirectory())
                    self.statusText.set("Completed")

                    sys_exit()

                except Exception as error:
                    self.statusText.set("Generate failed")
                    messagebox.showinfo("Generate failed", str(error))
                    #traceback.print_exc()
                    #traceback.print_last()

            eGenerate.pack(side=RIGHT)

            self.statusText.set("Ready")    
    
            statusLabel = Label(self.top, textvariable=self.statusText)
            statusLabel.pack(side=RIGHT)
    
            self.top.mainloop()

        else:
            self.common.printInvalidMode(args.runmode)

#main()

if __name__ == "__main__":
   main = buildit()
   main.main()
