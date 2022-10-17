# @file options.py
#
# Copyright contributors to the buildIT project
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

from enum import Enum
from os import path

class RunMode(Enum):
   BATCH = 'batch'
   GUI = 'gui'

class Options:
   runMode = None
   inputDirectory = ''
   outputDirectory = ''
   inputType = 'xlsx'
   propExt = 'xlsx'
   propFile = ''
   propName = '*'

   def __init__(self, toolName):
      self.runMode = RunMode.BATCH
      return

   def getInputDirectory(self):
      return self.inputDirectory

   def setInputDirectory(self, inputFolder):
      self.inputDirectory = inputFolder

   def getOutputDirectory(self):
      return self.outputDirectory

   def setOutputDirectory(self, outputFolder):
      self.outputDirectory = outputFolder

   def getInputType(self):
      return self.inputType

   def setInputType(self, inputType):
      self.inputType = inputType

   def getExtension(self):
      return self.propExt

   def setExtension(self, extension):
      self.extension = extension

   def getFile(self):
      return self.propFile

   def setFile(self, file):
      self.propFile = file

   def getName(self):
      return self.propName

   def setName(self, name):
      self.propName = name

   def isBatchMode(self):
      return self.runMode == RunMode.BATCH

   def isGUIMode(self):
      return self.runMode == RunMode.GUI

   def isBatchMode(self, value):
      return value == RunMode.BATCH.value

   def isGUIMode(self, value):
      return value == RunMode.GUI.value

   def getRunMode(self):
      return self.runMode

   def setRunMode(self, value):
      self.runMode = value
