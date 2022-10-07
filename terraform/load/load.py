# @file load.py
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

from pandas import DataFrame, read_excel

from terraform.common.common import Common

class Load:
   common = None 
   data = None

   def __init__(self, common):
      self.common = common
      return

   def loadFile(self):
      propext = self.common.getExtension()
      propfile = self.common.getFile()

      if (propext.lower() == 'xls' or propext.lower() == 'xlsx'):
         sheets = read_excel(propfile, sheet_name=None, dtype=object, header=0)
      else:
         self.common.printInvalidInput(propfile)
         sheets = None

      return sheets

   def loadFrame(self, sheet):
      propext = self.common.getExtension()
      propfile = self.common.getFile()

      df = DataFrame(sheet)

      if (propext.lower() == 'xls' or propext.lower() == 'xlsx'):
         # Remove leading asterisk from column names
         df.rename(columns=lambda x: x[1:] if x[0]=='*' else x, inplace=True)
      else:
         self.common.printInvalidInput(propfile)
         sheets = None

      return df
