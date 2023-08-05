# -*- coding: utf-8 -*- 
'''
# Copyright (c) 2015 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
#  This file was generated and any changes will be overwritten.
'''

from __future__ import unicode_literals
from ..one_drive_object_base import OneDriveObjectBase


class Quota(OneDriveObjectBase):

    def __init__(self, prop_dict={}):
        self._prop_dict = prop_dict

    @property
    def deleted(self):
        """Gets and sets the deleted
        
        Returns: 
            int:
                The deleted
        """
        if "deleted" in self._prop_dict:
            return self._prop_dict["deleted"]
        else:
            return None

    @deleted.setter
    def deleted(self, val):
        self._prop_dict["deleted"] = val

    @property
    def remaining(self):
        """Gets and sets the remaining
        
        Returns: 
            int:
                The remaining
        """
        if "remaining" in self._prop_dict:
            return self._prop_dict["remaining"]
        else:
            return None

    @remaining.setter
    def remaining(self, val):
        self._prop_dict["remaining"] = val

    @property
    def state(self):
        """Gets and sets the state
        
        Returns: 
            str:
                The state
        """
        if "state" in self._prop_dict:
            return self._prop_dict["state"]
        else:
            return None

    @state.setter
    def state(self, val):
        self._prop_dict["state"] = val

    @property
    def total(self):
        """Gets and sets the total
        
        Returns: 
            int:
                The total
        """
        if "total" in self._prop_dict:
            return self._prop_dict["total"]
        else:
            return None

    @total.setter
    def total(self, val):
        self._prop_dict["total"] = val

    @property
    def used(self):
        """Gets and sets the used
        
        Returns: 
            int:
                The used
        """
        if "used" in self._prop_dict:
            return self._prop_dict["used"]
        else:
            return None

    @used.setter
    def used(self, val):
        self._prop_dict["used"] = val

