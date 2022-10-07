# @file messages.py
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

from sys import stderr

class Messages:
   toolHeader = 'Transform data into Terraform resources\n'
   startToolMessage = 'Starting with input from %s\n'
   doneToolMessage = 'Completed with output to %s\n'
   startProviderMessage = 'Generating Resource for provider\n'
   startVersionsMessage = 'Generating Resource for versions\n'
   doneTFMessage = '\nCompleted Resources for %s with output to folder %s\n'
   backupDirectoryMessage = 'Backed up existing output directory %s to %s\n'
   invalidInputDirectoryMessage = '(Error) Invalid input directory: %s'
   invalidInputFileMessage = '(Error) Invalid input file: %s'
   invalidProtocolMessage = '(Error) Invalid protocol: %s'
   invalidGatewaySpecMessage = '(Error) Invalid gateway specification: %s'
   invalidNicMessage = '(Error) Invalid nic: %s'
   invalidSecondaryNicMessage = '(Error) Invalid secondary nic: %s'
   missingInputMessage = '(Error) No input files found: %s'
   missingImageMessage = '(Error) Image %s not found'
   missingZoneMessage = '(Error) Zone %s not found'
   missingSubnetMessage = '(Error) Subnet for %s not found'
   missingImageProfileMessage = '(Error) Image profile %s not found'
   missingVolumeProfileMessage = '(Error) Volume profile %s not found'
   missingValueMessage = '(Error) Required value missing on column %s, row %s'
   processingSheetMessage = 'Processing %s'

   def __init__(self, options):
      return

   def printError(self, *args):
      print(*args, file=stderr)

   def printMessage(self, *args):
      print(*args, file=stderr)


   def printToolHeader(self):
      self.printMessage(self.toolHeader)

   def printStart(self, inputFolder):
      self.printMessage(self.startToolMessage % inputFolder)

   def printDone(self, outputFolder):
      self.printMessage(self.doneToolMessage % outputFolder)

   def printSheet(self, sheet):
      self.printMessage(self.processingSheetMessage % sheet)

   def printProvider(self):
      self.printMessage(self.startProviderMessage)

   def printVersion(self):
      self.printMessage(self.startVersionsMessage)

   def printDoneTerraform(self, inputFolder, outputFolder):
      self.printMessage(self.doneTFMessage % (inputFolder, outputFolder))

   def printBackupDirectory(self, folder1, folder2):
      self.printMessage(self.backupDirectoryMessage % (folder1, folder2))

   def printInvalidInput(self, inputFolder):
      self.printMessage(self.invalidInputDirectoryMessage % inputFolder)

   def printInvalidFile(self, inputFile):
      self.printMessage(self.invalidInputFileMessage % inputFile)

   def printInvalidProtocol(self, protocol):
      self.printMessage(self.invalidProtocolMessage % protocol)

   def printInvalidGateway(self, gateway):
      self.printMessage(self.invalidGatewaySpecSMessage % gateway)

   def printInvalidNIC(self, nic):
      self.printMessage(self.invalidNicMessage % nic)

   def printInvalidSecondaryNIC(self, nic):
      self.printMessage(self.invalidSecondaryNicMessage % nic)

   def printMissingInput(self, inputFolder):
      self.printMessage(self.missingInputMessage % inputFolder)

   def printMissingImage(self, image):
      self.printMessage(self.missingImageMessage % image)

   def printMissingZone(self, zone):
      self.printMessage(self.missingZoneMessage % zone)

   def printMissingSubnet(self, subnet):
      self.printMessage(self.missingSubnetMessage % subnet)

   def printMissingImageProfile(self, profile):
      self.printMessage(self.missingImageProfileMessage % profile)

   def printMissingVolumeProfile(self, profile):
      self.printMessage(self.missingVolumeProfileMessage % profile)

   def printMissingValue(self, column, row):
      self.printMessage(self.missingValueMessage % (column, row))


