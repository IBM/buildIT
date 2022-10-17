# @file generate.py
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
   
from os import listdir, makedirs, path
from shutil import copy, copytree, move
   
from terraform.common.common import Common
from terraform.load.load import Load
from terraform.generate.tables import headers, footers, resources 
   
class Generate:
   common = None
   load = None
   
   def __init__(self, common):
       self.common = common
       self.load = Load(self.common)
   
   def providers(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
   
      self.common.printSheet(name)
   
      name = name.replace(' ', '')
      pos = name.find('-')
      if pos >= 0:
         sheettype = name[0:pos]
         sheetgroup = name[pos+1:]
      else:
         sheettype = name
         sheetgroup = ''
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfname = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfname)
         if empty:
            continue
         else:
            tfname = tfname.replace(' ', '')
   
         #resource = row['resource']
         #empty = self.common.noValue(resource)
         #if empty:
         #   print(missingvaluemessage % ('resource', rowindex))
         #   continue
   
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
    
         tfname = path.join(module, tfname)
   
         comments = row['comments']
         empty = self.common.noValue(comments)
         if not empty:
           self.common.printLine(tfname, '# ' + comments)
   
         #self.common.printLine(tfname, providerheader % name)
         self.common.printLine(tfname, headers['provider'] % 'ibm')
   
         savegroup = None
   
         # Loop through columns skipping first column (file) and last 2 columns (modules and comments).
         for columnindex in range(columns.size-2):
            if columnindex < 1:
               continue
   
            column = columns[columnindex]
            value = row[column]
            empty = self.common.noValue(value)
            if empty:
               continue
   
            if isinstance(value, int):
               value = str(value)
   
            column = column.replace(' ', '')
   
            dotpos = column.find('.')
            if dotpos >= 0:
               subgroup = column[0:dotpos]
               subcolumn = column[dotpos+1:]
               column = subcolumn
               if savegroup == None:
                  # No group yet so start group.
                  savegroup = subgroup
                  # Remove trailing digits from duplicated columns of arrays.
                  subgroup = subgroup.rstrip('0123456789')
                  self.common.printLine(tfname, subgroup + ' {')
               elif savegroup != subgroup:
                  # Adjacent groups so close previous group and start next group.
                  savegroup = subgroup
                  # Remove trailing digits from duplicated columns of arrays.
                  subgroup = subgroup.rstrip('0123456789')
                  self.common.printLine(tfname, '}')
                  self.common.printLine(tfname, subgroup + ' {')
            elif savegroup != None:
               # End of group so close group.
               savegroup = None
               self.common.printLine(tfname, '}')
   
            if column != 'name':
               self.common.printLine(tfname, column + ' = ' + value)
   
         if savegroup != None:
            # End of row so close group.
            savegroup = None
            self.common.printLine(tfname, '}')
   
         self.common.printLine(tfname, footers['provider'])
   
      return
   
   def versions(self, name, sheet, df):
   
      #self.common.printLine(tfname, 'terraform {')
      #self.common.printLine(tfname, 'required_version = ">= ' + terraformversion + '"')
      #self.common.printLine(tfname, 'required_providers {')
      #self.common.printLine(tfname, 'ibm = {')
      #self.common.printLine(tfname, 'source = "ibm-cloud/ibm"')
      #self.common.printLine(tfname, 'version = "' + providerversion + '"')
      #self.common.printLine(tfname, '}')
      #self.common.printLine(tfname, '}')
      #self.common.printLine(tfname, '}')
   
      outputdirectory = self.common.getOutputDirectory()
   
      self.common.printSheet(name)
   
      name = name.replace(' ', '')
      pos = name.find('-')
      if pos >= 0:
         sheettype = name[0:pos]
         sheetgroup = name[pos+1:]
      else:
         sheettype = name
         sheetgroup = ''
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfname = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfname)
         if empty:
            continue
         else:
            tfname = tfname.replace(' ', '')
   
         #resource = row['resource']
         #empty = self.common.noValue(resource)
         #if empty:
         #   print(missingvaluemessage % ('resource', rowindex))
         #   continue
   
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
    
         tfname = path.join(module, tfname)
   
         comments = row['comments']
         empty = self.common.noValue(comments)
         if not empty:
           self.common.printLine(tfname, '# ' + comments)
   
         self.common.printLine(tfname, headers['terraform'])
   
         savegroup = None
   
         # Loop through columns skipping first column (file) and last 2 columns (modules and comments).
         for columnindex in range(columns.size-2):
            if columnindex < 1:
               continue
   
            column = columns[columnindex]
            value = row[column]
            empty = self.common.noValue(value)
            if empty:
               continue
   
            if isinstance(value, int):
               value = str(value)
   
            column = column.replace(' ', '')
   
            dotpos = column.rfind('.')
            if dotpos >= 0:
               subgroup = column[0:dotpos]
               subcolumn = column[dotpos+1:]
               column = subcolumn
               if savegroup == None:
                  # No group yet so start group.
                  savegroup = subgroup
                  # Remove trailing digits from duplicated columns of arrays.
                  subgroup = subgroup.rstrip('0123456789')
                  if subgroup == 'required_providers.ibm':
                     self.common.printLine(tfname, 'required_providers {')
                     self.common.printLine(tfname, 'ibm = {')
                  else:
                     self.common.printLine(tfname, subgroup + ' {')
               elif savegroup != subgroup:
                  # Adjacent groups so close previous group and start next group.
                  savegroup = subgroup
                  # Remove trailing digits from duplicated columns of arrays.
                  subgroup = subgroup.rstrip('0123456789')
                  self.common.printLine(tfname, '}')
                  if subgroup == 'required_providers.ibm':
                     self.common.printLine(tfname, 'required_providers {')
                     self.common.printLine(tfname, 'ibm = {')
   
                  else:
                     self.common.printLine(tfname, subgroup + ' {')
            elif savegroup != None:
               # End of group so close group.
               savegroup = None
               self.common.printLine(tfname, '}')
               if subgroup == 'required_providers.ibm':
                  self.common.printLine(tfname, '}')
   
            if column != 'name':
               self.common.printLine(tfname, column + ' = ' + value)
   
         if savegroup != None:
            # End of row so close group.
            savegroup = None
            self.common.printLine(tfname, '}')
            if subgroup == 'required_providers.ibm':
               self.common.printLine(tfname, '}')
   
         self.common.printLine(tfname, footers['terraform'])
   
      return
   
   def outputs(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
      
      self.common.printSheet(name)
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfname = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfname)
         if empty:
            continue
         else:
            tfname = tfname.replace(' ', '')
   
         name = row['name']
         empty = self.common.noValue(name)
         if empty:
            self.common.printMissingValue('name', rowindex)
            continue
         
         value = row['value']
         empty = self.common.noValue(value)
         if empty:
            self.common.printMissingValue('value', rowindex)
            continue
   
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
   
         tfname = path.join(module, tfname)
   
         comments = row['comments']
         empty = self.common.noValue(comments)
         if not empty:
           self.common.printLine(tfname, '# ' + comments)
   
         self.common.printLine(tfname, headers['output'] % name)
         self.common.printLine(tfname, 'value = ' + str(value))
         self.common.printLine(tfname, footers['output'])
   
      return
   
   def cloudinits(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
      
      self.common.printSheet(name)
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfname = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfname)
         if empty:
            continue
         else:
            tfname = tfname.replace(' ', '')
   
         resource = row['resource']
         empty = self.common.noValue(resource)
         if empty:
            self.common.printMissingValue('resource', rowindex)
            continue
         
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
   
         inputdirectory = self.common.getInputDirectory()
         initspath = path.join(inputdirectory, 'cloudinits')
         tfname = path.join(initspath, tfname)
   
         if path.isdir(initspath) and path.isfile(tfname):
            filepath = path.join(outputdirectory, module)
            # Check for existing module directory.
            if not path.exists(filepath):
               # Create new module directory.
               makedirs(filepath)
            copy(tfname, filepath)
   
      return
   
   def variables(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
      
      self.common.printSheet(name)
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfname = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfname)
         if empty:
            continue
         else:
            tfname = tfname.replace(' ', '')
   
         name = row['name']
         empty = self.common.noValue(name)
         if empty:
            self.common.printMissingValue('name', rowindex)
            continue
         
         emptyvalue = False
         value = row['value']
         empty = self.common.noValue(value)
         if empty:
            emptyvalue = True
            #print(missingvaluemessage % ('value', rowindex))
            #continue
   
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
   
         tfname = path.join(module, tfname)
   
         self.common.printLine(tfname, headers['variable'] % name)
   
         comments = row['comments']
         empty = self.common.noValue(comments)
         if not empty:
            #self.common.printLine(tfname, '# ' + comments)
            self.common.printLine(tfname, 'description = "' + comments + '"')
   
         if not emptyvalue:
            self.common.printLine(tfname, 'default = ' + str(value))
   
         self.common.printLine(tfname, footers['variable'])
   
      return
   
   def modules(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
      
      self.common.printSheet(name)
   
      tfname = 'modules.tf'
      module = name.split('-')[1]
   
      self.common.printLine(tfname, headers['module'] % module)
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfnameignore = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfnameignore)
         if empty:
            continue
   
         name = row['name']
         empty = self.common.noValue(name)
         if empty:
            self.common.printMissingValue('name', rowindex)
            continue
         
         emptyvalue = False
         value = row['value']
         empty = self.common.noValue(value)
         if empty:
            emptyvalue = True
            #print(missingvaluemessage % ('value', rowindex))
            #continue
   
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
   
         #tfname = os.path.join(module, tfname)
   
         #self.common.printLine(tfname, moduleheader % name)
   
         comments = row['comments']
         empty = self.common.noValue(comments)
         if not empty:
            self.common.printLine(tfname, '# ' + comments)
            #self.common.printLine(tfname, 'description = "' + comments + '"')
   
         if not emptyvalue:
            #self.common.printLine(tfname, 'default = ' + str(value))
            self.common.printLine(tfname, name + ' = ' + value)
   
         #self.common.printLine(tfname, endvariable)
   
      self.common.printLine(tfname, footers['module'])
   
      return
   
   def localfiles(self, name, sheet, df):
      outputdirectory = self.common.get[OutputDirectory]
      
      self.common.printSheet(name)
   
      name = name.replace(' ', '')
      pos = name.find('-')
      if pos >= 0:
         sheettype = name[0:pos]
         sheetgroup = name[pos+1:]
      else:
         sheettype = name
         sheetgroup = ''
   
      columns = df.columns
   
      header = True
      tfname = None
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         if header:
            tfname = row['file']
            # Skip empty rows.
            empty = self.common.noValue(tfname)
            if empty:
               continue
            else:
               tfname = tfname.replace(' ', '')
   
            resource = row['resource']
            empty = self.common.noValue(resource)
            if empty:
               self.common.printMissingValue('resource', rowindex)
               continue
            else:
               resource = resource.replace(' ', '')
   
            header = False
   
            module = row['module']
            empty = self.common.noValue(module)
            if empty:
               module = '.'
            else:
               module = module.replace(' ', '')
   
            tfname = os.path.join(module, tfname)
   
            comments = row['comments']
            empty = self.common.noValue(comments)
            if not empty:
               self.common.printLine(tfname, '# ' + comments)
   
            self.common.printLine(tfname, headers['resourceHeader'] % (resources[sheettype], resource))
   
            filename = row['filename']
            empty = self.common.noValue(filename)
            if empty:
               self.common.printMissingValue('filename', rowindex)
               continue
            else:
               filename = filename.replace(' ', '')
   
            self.common.printLine(tfname, 'filename = ' + filename)
   
            content = row['content']
            empty = self.common.noValue(content)
            if empty:
               self.common.printMissingValue('content', rowindex)
               continue
            #else:
            #   content = content.replace(' ', '')
   
            self.common.printLine(tfname, 'content = <<EOT')
   
            self.common.printLine(tfname, content)
   
         else:
   
            tfnameignore = row['file']
            # Skip empty rows.
            empty = self.common.noValue(tfnameignore)
            if empty:
               continue
   
            content = row['content']
            empty = self.common.noValue(content)
            if empty:
               self.common.printMissingValue('content', rowindex)
               continue
            #else:
            #   content = content.replace(' ', '')
   
            self.common.printLine(tfname, content)
   
      self.common.printLine(tfname, 'EOT')
   
      self.common.printLine(tfname, endmodule)
   
      return
   
   def aclresources(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
      
      self.common.printSheet(name)
   
      name = name.replace(' ', '')
      pos = name.find('-')
      if pos >= 0:
         sheettype = name[0:pos]
         sheetgroup = name[pos+1:]
      else:
         sheettype = name
         sheetgroup = ''
   
      columns = df.columns
   
      header = True
      tfname = None
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         if header:
            tfname = row['file']
            # Skip empty rows.
            empty = self.common.noValue(tfname)
            if empty:
               continue
            else:
               tfname = tfname.replace(' ', '')
   
            resource = row['resource']
            empty = self.common.noValue(resource)
            if empty:
               self.common.printMissingValue('resource', rowindex)
               continue
            else:
               resource = resource.replace(' ', '')
   
            #resource_data = False
            #resource = resource.replace(' ', '')
            #pos = resource.find('.')
            #if pos >= 0:
            #   if resource[0:pos] == 'data':
            #      resource_data = True
            #      resource = resource[pos+1:]
   
            header = False
   
            module = row['module']
            empty = self.common.noValue(module)
            if empty:
               module = '.'
            else:
               module = module.replace(' ', '')
   
            tfname = path.join(module, tfname)
   
            comments = row['comments']
            empty = self.common.noValue(comments)
            if not empty:
               self.common.printLine(tfname, '# ' + comments)
   
            #if resource_data == True:
            #   self.common.printLine(tfname, dataheader % (resources[sheettype], resource))
            #else:
            self.common.printLine(tfname, headers['resource'] % (resources[sheettype], resource))
   
            # Loop through columns skipping first 2 columns (file and resource) and last 2 columns (module and comments).
            for columnindex in range(columns.size-2):
               if columnindex < 2:
                  continue
   
               column = columns[columnindex]
               value = row[column]
               empty = self.common.noValue(value)
               if empty:
                  continue
   
               if isinstance(value, int):
                  value = str(value)
   
               self.common.printLine(tfname, column + ' = ' + value)
         else:
            name = row['name']
            # End of rule group when name is empty.
            empty = self.common.noValue(name)
            if empty:
               self.common.printLine(tfname, '}')
               header = True
               continue
   
            self.common.printLine(tfname, 'rules {')
   
            savegroup = None
   
            # Loop through columns skipping first 2 columns (file and resource) and last 2 columns (module and comments).
            for columnindex in range(columns.size-2):
               if columnindex < 2:
                  continue
   
               column = columns[columnindex]
               value = row[column]
               empty = self.common.noValue(value)
               if empty:
                  continue
   
               if isinstance(value, int):
                  value = str(value)
   
               column = column.replace(' ', '')
               dotpos = column.find('.')
               if dotpos >= 0:
                  subgroup = column[0:dotpos]
                  subcolumn = column[dotpos+1:]
                  column = subcolumn
                  if savegroup == None:
                     # No group yet so start group.
                     savegroup = subgroup
                     # Remove trailing digits from duplicated columns of arrays.
                     subgroup = subgroup.rstrip('0123456789')
                     self.common.printLine(tfname, subgroup + ' {')
                  elif savegroup != subgroup:
                     # Adjacent groups so close previous group and start next group.
                     savegroup = subgroup
                     # Remove trailing digits from duplicated columns of arrays.
                     subgroup = subgroup.rstrip('0123456789')
                     self.common.printLine(tfname, '}')
                     self.common.printLine(tfname, subgroup + ' {')
               elif savegroup != None:
                  # End of group so close group.
                  savegroup = None
                  self.common.printLine(tfname, '}')
   
               self.common.printLine(tfname, column + ' = ' + value)
   
            if savegroup != None:
               # End of row so close group.
               savegroup = None
               self.common.printLine(tfname, '}')
   
            self.common.printLine(tfname, '}')
   
      if tfname != None:
         self.common.printLine(tfname, footers['resource'])
   
      return
   
   def resources(self, name, sheet, df):
      outputdirectory = self.common.getOutputDirectory()
      
      self.common.printSheet(name)
   
      name = name.replace(' ', '')
      pos = name.find('-')
      if pos >= 0:
         sheettype = name[0:pos]
         sheetgroup = name[pos+1:]
      else:
         sheettype = name
         sheetgroup = ''
   
      columns = df.columns
   
      # Loop thru rows.
      for rowindex, row in df.iterrows():
         tfname = row['file']
         # Skip empty rows.
         empty = self.common.noValue(tfname)
         if empty:
            continue
         else:
            tfname = tfname.replace(' ', '')
   
         resource = row['resource']
         empty = self.common.noValue(resource)
         if empty:
            self.common.printMissingValue('resource', rowindex)
            continue
         else:
            resource = resource.replace(' ', '')
   
         resource_data = False
         resource = resource.replace(' ', '')
         pos = resource.find('.')
         if pos >= 0:
            if resource[0:pos] == 'data':
               resource_data = True
               resource = resource[pos+1:]
   
         module = row['module']
         empty = self.common.noValue(module)
         if empty:
            module = '.'
         else:
            module = module.replace(' ', '')
    
         tfname = path.join(module, tfname)
   
         comments = row['comments']
         empty = self.common.noValue(comments)
         if not empty:
            self.common.printLine(tfname, '# ' + comments)
   
         if resource_data == True:
            self.common.printLine(tfname, dataheader % (resources[sheettype], resource))
            value = row['name']
            empty = self.common.noValue(value)
            if empty:
               self.common.printMissingValue('resource', rowindex)
               continue
            self.common.printLine(tfname, 'name = ' + value)
            self.common.printLine(tfname, enddata)
            continue
   
         self.common.printLine(tfname, headers['resource'] % (resources[sheettype], resource))
   
         savegroup = None
   
         # Loop through columns skipping first 2 columns (file and resource) and last 2 columns (module and comments).
         for columnindex in range(columns.size-2):
            if columnindex < 2:
               continue
   
            column = columns[columnindex]
            value = row[column]
            empty = self.common.noValue(value)
            if empty:
               continue
   
            if isinstance(value, int):
               value = str(value)
   
            column = column.replace(' ', '')
   
            dotpos = column.find('.')
            if dotpos >= 0:
               subgroup = column[0:dotpos]
               subcolumn = column[dotpos+1:]
               column = subcolumn
               if savegroup == None:
                  # No group yet so start group.
                  savegroup = subgroup
                  # Remove trailing digits from duplicated columns of arrays.
                  subgroup = subgroup.rstrip('0123456789')
                  self.common.printLine(tfname, subgroup + ' {')
               elif savegroup != subgroup:
                  # Adjacent groups so close previous group and start next group.
                  savegroup = subgroup
                  # Remove trailing digits from duplicated columns of arrays.
                  subgroup = subgroup.rstrip('0123456789')
                  self.common.printLine(tfname, '}')
                  self.common.printLine(tfname, subgroup + ' {')
            elif savegroup != None:
               # End of group so close group.
               savegroup = None
               self.common.printLine(tfname, '}')
   
            self.common.printLine(tfname, column + ' = ' + value)
   
         if savegroup != None:
            # End of row so close group.
            savegroup = None
            self.common.printLine(tfname, '}')
   
         self.common.printLine(tfname, footers['resource'])
   
      return
   
   def terraform(self):
      outputdirectory = self.common.getOutputDirectory()
      propfile = self.common.getFile()
      propname = self.common.getName()
   
      #print(starttfmessage % propfile)
   
      sheets = self.load.loadFile()
      for name, sheet in sheets.items():
         name = name.replace(' ', '')
   
         df = self.load.loadFrame(sheet)
   
         if name.find('variables', 0, 9) >= 0:
            self.variables(name, sheet, df)
         elif name.find('outputs', 0, 7) >= 0:
            self.outputs(name, sheet, df)
         elif name.find('cloudinits', 0, 10) >= 0:
            self.cloudinits(name, sheet, df)
         elif name.find('modules', 0, 7) >= 0:
            self.modules(name, sheet, df)
         elif name.find('providers', 0, 9) >= 0:
            self.providers(name, sheet, df)
         elif name.find('versions', 0, 8) >= 0:
            self.versions(name, sheet, df)
         elif name.find('aclrules', 0, 8) >= 0:
            self.aclresources(name, sheet, df)
         elif name.find('localfiles', 0, 10) >= 0:
            self.localfiles(name, sheet, df)
         else:
            self.resources(name, sheet, df)
   
      #print(donetfmessage % (propname, outputdirectory))
   
      return
   
   def all(self):
      genbackup = None
      outputdirectory = self.common.getOutputDirectory()
      # Check for existing output directory and backup if exists.
      if path.exists(outputdirectory):
         backup = 1
         found = False
         genbackup = None
         # Find a new backup directory.
         while not found:
            genbackup = outputdirectory + '.backup' + str(backup)
            if path.exists(genbackup):
               backup += 1
            else:
               found = True
         # Move existing output directory to backup directory.
         move(outputdirectory, genbackup)
         self.common.printBackupDirectory(outputdirectory, genbackup)
   
      # Create new empty output directory.
      makedirs(outputdirectory)
   
      # Copy existing terraform.tfstate to output directory.
      if genbackup != None and path.isfile(path.join(genbackup, 'terraform.tfstate')):
         copy(path.join(genbackup, 'terraform.tfstate'), path.join(outputdirectory, 'terraform.tfstate'))
   
      # Copy existing .terraform to output directory.
      if genbackup != None and path.isdir(path.join(genbackup, '.terraform')):
         copytree(path.join(genbackup, '.terraform'), path.join(outputdirectory, '.terraform'))
   
      inputdirectory = self.common.getInputDirectory()
      inputtype = self.common.getInputType()
      #filelist = os.listdir(os.path.join(inputdirectory, datatype))
      filelist = listdir(inputdirectory)
   
      # Copy terraform-cloudinits if exists to output directory.
      #if os.path.isdir(os.path.join(inputdirectory, 'terraform-cloudinits')):
      #   terraformfiles = os.listdir(os.path.join(inputdirectory, 'terraform-cloudinits'))
      #   for terraformfile in terraformfiles:
      #      shutil.copy(os.path.join(inputdirectory, 'terraform-cloudinits', terraformfile), outputdirectory)
   
      # Copy ansible if exists to output directory.
      if path.isdir(path.join(inputdirectory, 'playbooks')):
         copytree(path.join(inputdirectory, 'playbooks'), path.join(outputdirectory, 'playbooks'))
   
      # Generate provider.
      #print(startprovidermessage)
      #genprovider(self.common.get)
   
      # Generate versions.
      #print(startversionsmessage)
      #genversions(self.common.get)
   
      # Process all files in specified directory.
      found = False
      for afile in filelist:
         if (not afile.endswith(inputtype)):
            continue
         #propfile = os.path.join(inputdirectory, datatype, afile)
         propfile = path.join(inputdirectory, afile)
         propfilenopath = path.basename(propfile)
         propname = path.splitext(propfilenopath)[0]
         propext = path.splitext(propfilenopath)[1][1:]
         if (path.isfile(propfile)):
            found = True
            self.common.setFile(propfile)
            self.common.setName(propname)
            self.common.setExtension(propext)
            self.terraform()
      if (not found):
         self.common.printMissingInput(inputdirectory)
   
      return
