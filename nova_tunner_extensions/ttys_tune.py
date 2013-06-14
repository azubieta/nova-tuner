#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tty_management.py
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

from  nova_tunner import NovaTunnerExtension
import dialog, os


class ttys_tune(NovaTunnerExtension):
		
	def __init__(self, dialog_instance):
		print 'DEBUG: ttys_tune instantiated'
		self.dialog_instance = dialog_instance

	def automatic_tune(self):
		self.remove_tty(self.dialog_instance)

	def maunal_tune(self):
		#TODO: implement
		self.dialog_instance.msgbox("Not implemented yet...")
		

	def remove_tty(self, d, tty_list=[2, 3, 4, 5, 6, 7]):
		"""
		Removes system ttys.
		
		:param d: dialog instace.
		:param tty_list: list of ttys to be removed.
		"""
		msg = "Removing ttys:\n"
		
		for tty in tty_list:
			msg = msg + " - " + str(tty) + "\n"
		
		d.clear()
		d.infobox(msg)
		
		for tty in tty_list:
			os.system("mv /etc/init/tty"+str(tty)+".conf /etc/init/tty"+str(tty)+".conf.back")
	
	def get_name(self):
		return 'TTYS tune'
	def get_description(self):
		return 'Disable unused ttys.'