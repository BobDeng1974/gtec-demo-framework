#!/usr/bin/env python3

#****************************************************************************************************************************************************
# Copyright (c) 2016 Freescale Semiconductor, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
#    * Neither the name of the Freescale Semiconductor, Inc. nor the names of
#      its contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#****************************************************************************************************************************************************

from typing import List
import os
import os.path
import xml.etree.ElementTree as ET
from FslBuildGen import IOUtil
from FslBuildGen.BasicConfig import BasicConfig
from FslBuildGen.DataTypes import PackageLanguage
from FslBuildGen.Exceptions import FileNotFoundException
from FslBuildGen.Xml.Exceptions import XmlException
from FslBuildGen.Xml.Exceptions import XmlInvalidRootElement
from FslBuildGen.Xml.XmlBase import XmlBase


class XmlNewVSProjectTemplate(XmlBase):
    def __init__(self, basicConfig: BasicConfig, xmlElement: ET.Element) -> None:
        super(XmlNewVSProjectTemplate, self).__init__(basicConfig, xmlElement)
        self.Name = XmlBase._ReadAttrib(self, xmlElement, 'Name')
        self.Description = XmlBase._ReadAttrib(self, xmlElement, 'Description')
        packageLanguage = XmlBase._ReadAttrib(self, xmlElement, 'PackageLanguage')
        self.PackageLanguage = PackageLanguage.FromString(packageLanguage)
        self.ProjectExtension = XmlBase._ReadAttrib(self, xmlElement, 'ProjectExtension', 'vcxproj')


class XmlNewVSProjectTemplateFile(XmlBase):
    def __init__(self, basicConfig: BasicConfig, filename: str) -> None:
        if not os.path.isfile(filename):
            raise FileNotFoundException("Could not locate config file %s", filename)

        tree = ET.parse(filename)
        elem = tree.getroot()
        if elem.tag != 'FslBuildNewVSProjectTemplate':
            raise XmlInvalidRootElement("The file did not contain the expected root tag 'FslBuildNewVSProjectTemplate'")

        super(XmlNewVSProjectTemplateFile, self).__init__(basicConfig, elem)
        strVersion = XmlBase._ReadAttrib(self, elem, 'Version')
        if strVersion != "1":
            raise Exception("Unsupported version")

        xmlTemplate = self.__LoadTemplateConfiguration(basicConfig, elem)
        if len(xmlTemplate) != 1:
            raise XmlException("The file did not contain exactly one Template element")

        directoryName = IOUtil.GetDirectoryName(filename)
        self.Name = IOUtil.GetFileName(directoryName)
        self.Id = self.Name.lower()
        self.Version = 1
        self.Template = xmlTemplate[0]
        self.Path = IOUtil.GetDirectoryName(filename)
        self.Prefix = ("%s_" % (self.Name)).upper()

        if self.Name != self.Template.Name:
            raise Exception("The parent template directory name '{0}' does not match the template name '{1}' {2}".format(self.Name, self.Template.Name, self.Path))

    def __LoadTemplateConfiguration(self, basicConfig: BasicConfig, element: ET.Element) -> List[XmlNewVSProjectTemplate]:
        res = []
        foundElements = element.findall("Template")
        for foundElement in foundElements:
            res.append(XmlNewVSProjectTemplate(basicConfig, foundElement))
        return res