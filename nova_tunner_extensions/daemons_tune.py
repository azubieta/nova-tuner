#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
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

class daemons_tune(NovaTunnerExtension):
	

	def __init__(self,dialog_instance):
		self.d = dialog_instance
		self.services = ["bluetooth", "powernowd", "powernowd.early", "unattended-upgrades", "pppd-dns", "avahi-daemon"]
		
	def automatic_tune(self):
		self.remove_services(self.services, 'Removing services')
		
	def maunal_tune(self):
		self.show_daemons_selection_dialog()
		
	def get_name(self):
		return 'Daemons tune'
	def get_description(self):
		return 'Disable unused services.'
	
	def remove_services(self, services, msg):
		if len(services) == 0:
			return
		
		inc = 100 / len(services)
		av = 0;
		
		self.d.gauge_start("Progress: 0%", title=msg)
		self.d.gauge_update(0, "\nProgreso: %d%%" % 0, update_text=1)
		
		for service in services:
			os.system("if [ `which update-rc.d` ] && [ -f /etc/init.d/" + service + " ] ; then update-rc.d -f "+ service +" remove; fi")
			
			av += inc
			self.d.gauge_update(av, "Quitando servicios opcionales.\n Progreso: %d%%" % av, update_text=1)
		
		self.d.gauge_stop()
		
	def get_system_daemons_list(self):
		# get Default Run Level (D_RL)
		f = open("/etc/init/rc-sysinit.conf")
		for line in f:
			if line.startswith('env DEFAULT_RUNLEVEL='):
				D_RL=line.split('=')[1]
				# cast it as an int
				D_RL = int (D_RL)
				break
		f.close()
					
		daemon_list = []
		for daemon in os.listdir("/etc/rc" + str(D_RL) + ".d/"):
			# include only those that can be executed
			if (os.access("/etc/rc"+ str(D_RL) +".d/"+daemon, os.X_OK)):
				# cuting precedence numbers (S00)
				daemon_list.append(daemon[3:])
	
		return daemon_list
	
	def get_daemon_short_description(self, daemon):
		short_description = ""
		f = open("/etc/init.d/" + daemon)
		for line in f:
			if line.startswith('# Short-Description:'):
				return line.split(':')[1].strip().capitalize()
		f.close()
		return short_description;
	
	def show_daemons_selection_dialog(self):
		daemons_list = self.get_system_daemons_list()
		# build dialog choises
		choices = []
		for daemon in daemons_list:
			description = self.get_daemon_short_description(daemon)
			if daemon in self.services:
				optional = 1
			else:
				optional = 0
			choices.append((daemon, description, optional))
		
		
		self.d.clear()
		while 1:
			(code, tag) = self.d.checklist(text="Marque los servicios que desee deshabilitar .", 
									   title="Deshabilitar servicios.", choices= choices)
			
			list = ""
			for daemon in tag:
				list += " - " + daemon + "\n"	
			
			if code in (self.d.DIALOG_CANCEL, self.d.DIALOG_ESC):
				break
			
			if self.d.yesno(height=20, width=60, text="Seguro que desea deshabilitar los siguientes servicios?\n" + list) == self.d.DIALOG_OK:
				self.remove_services(tag, "Deshabilitando servicios")
				self.d.msgbox('Servicios deshabilitados: '+list + '\n')
				break
