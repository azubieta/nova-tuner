#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  swap_tune.py
#  
#  Copyright 2013 Alexis López Zubieta <alexis@Laura>
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

class swap_tune(NovaTunnerExtension):
	def __init__(self, dialog_instance):
		self.d = dialog_instance
		
	def automatic_tune(self):
		self.set_swapines(80)
		
	def maunal_tune(self):
		d = self.d
		while 1:
			(code, value) =d.inputbox("Teclee el nivel a partir del cual el sistema debe comenzar"
									  " a utilizar la memoria swap.\n"
									  "Debe introducir un valor entero entre 0 y 100", init="60")
			
			# check if ESC was presed
			if (handle_exit_code(d, code) <> 0):
				if (value == ''):
					# back to the input box
					continue 
				
				try:
					value = int (value)
				except ValueError:
					d.msgbox('Debe introducir un valor entero entre 0 y 100.\n'
							 'Ejemplo: 60\n')
			
				if (value > 0) and (value <= 100):
					self.set_swapines(value)
					d.msgbox('Swapines establecido a ' + str(value) + ' .\n')
					break
				else:
					d.msgbox('Solo se permiten valores entre 0 y 100.\n')
				
			else:
				break
	
	def get_name(self):
		return 'Swap usage tune'
	def get_description(self):
		return 'Define swap usage criteria.'
	
	def set_swapines(self, val):
		if os.path.exists("/etc/sysctl.conf"):
			replace('/etc/sysctl.conf', 'vm.swappiness', val)
			f = open ("/etc/sysctl.conf", "rw")
		else:
			f = open ("/etc/sysctl.conf", "w")
			f.writeln("vm.swappiness=" + str(val))
			f.close()
