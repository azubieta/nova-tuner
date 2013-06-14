#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prelink_tune.py
#  
#  Copyright 2013 Alexis López Zubieta <azubieta@estudiantes.uci.cu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from  nova_tunner import replace, NovaTunnerExtension, handle_exit_code
import os
import dialog

class prelink_tune(NovaTunnerExtension):
	def __init__(self, dialog_instance):
		self.d = dialog_instance
		
	def automatic_tune(self):
		os.system("sed -i 's/PRELINKING\=unknown/PRELINKING\=yes/g' /etc/default/prelink");
		os.system("/etc/cron.daily/prelink");
		
	def maunal_tune(self):
		self.do_prelink()
		
	def get_name(self):
		return 'Prelink tune'
	
	def get_description(self):
		return 'Improve application load time.'
	
	def do_prelink(self):
		self.d.infobox("Running Prelink, this can take several minutes.\n"
		"Please be patient.")
		os.system("sed -i 's/PRELINKING\=unknown/PRELINKING\=yes/g' /etc/default/prelink");
		os.system("/etc/cron.daily/prelink");
		self.d.msgbox('Prelink finished.\n')
	