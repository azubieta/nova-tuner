#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nova_tunner.py
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

import sys, os, os.path, string, re, shutil, time
from sys import path
# External 
import dialog  
##
## I18N
##
import gettext

usage_text="Utilice las teclas Arriba y Abajo, la primera letra de cada entrada como acceso de teclado, \
o las teclas de numeros del 1 al 9 para escoger las opciones. \n\
La tecla Espacio Habilita o Deshabilita las opciones. \n\n"

help="Estas son configuraciones altamente recomendadas para el sistema Nova Ligero. \n\n"


APP_DIR = os.path.join (sys.prefix, 'share')



class NovaTunnerExtension:
	def __init__(self, dialog_instance):
		self.d = dialog_instance
		
	def automatic_tune(self):
		pass
	def maunal_tune(self):
		pass
	def get_name(self):
		pass
	def get_description(self):
		pass

def loadExtensions():
	extensions = {}
	modules_path = os.getcwd()
	
	if os.path.exists(modules_path + '/nova_tunner_extensions'):
		# Development path
	   modules_path = 'nova_tunner_extensions'
	   sys.path.append(os.getcwd())
	else:
		# Deployed path
		modules_path = '/usr/share/pyshared/nova_tunner_extensions'
		sys.path.append('/usr/share/pyshared')
	
	lst = os.listdir(modules_path)
	mods_name = []
	for d in lst:
	   d = d.split('.')
	   if len(d) == 2 and d[0] != "__init__" and d[1] == 'py':
		   mods_name.append(d[0])
	  
	# load the modules
	modules = {}
	for d in mods_name:
	   print "DEBUG: loading extension " + d + " from " + modules_path
	   modules[d] =__import__('nova_tunner_extensions', globals(), locals(), [d], -1)
	
	# loading classes from modules
	for name in modules:
	   my_module = getattr(modules[name], name)
	   extensions[name] = getattr(my_module, name)
	   # use mods['classname']() to instantiate
	return extensions

class NovaTunner(object):
	def __init__(self):
		self.extensions = loadExtensions()
		self.done = False
		try:
			self.d = dialog.Dialog(dialog="dialog")
			self.d.add_persistent_args(["--backtitle", "Nova Tune 0.2"])
			self.show_main_menu()
		except dialog.error, exc_instance:
			sys.stderr.write("Error:\n\n%s\n" % exc_instance.complete_message())
	
	def show_main_menu(self):
		d = self.d
		active = True
		while active and not self.done:
			(code, tag) = d.menu(text=help, height=20, width=60, title="Configuraciones de Inicio para Nova Ligero",
									  choices=[("Recomendada", "Conjunto de configuraciones predefinidas."), 
											   ("Manual", "Configurar manualmente."),
											   ("Ninguna", "No se optimiza el sistema.")])
			if (tag == "Recomendada"):
				self.do_automatic_tune()
			
			elif (tag == "Manual"):
				self.do_manual_tune()
			
			elif (tag == "Ninguna"):
				if d.yesno("Desea abandonar?") == d.DIALOG_OK:
					active = False
					self.done = True
				 
			elif (handle_exit_code(d, code) == 0):
				active = False
				self.done = True
				
	def do_automatic_tune(self):	
		d = self.d
		#remove_services(d, services, "Quitando servicios opcionales.")	
		#do_prelink(d)
		
		msg = "Tunning your system...\n"
		for ext in self.extensions:
			cls = self.extensions[ext]
			instance = cls(d)
			d.infobox(msg+ "	Running " + instance.get_name() + "\n")
			
			instance.automatic_tune()
			
			msg = msg+ "	Done " + instance.get_name() + "\n"
			d.infobox(msg)
			
		
		d.msgbox(msg + "\nProcess finished.\n")
		
		#terminate()

	def do_manual_tune(self):
		d = self.d
		choices = []
		tunes = {}
		for ext in self.extensions:
			cls = self.extensions[ext]
			instance = cls(d)
			choices.append( (instance.get_name(), instance.get_description(), '') )
			tunes[instance.get_name()] = instance
		
		choices.append( ('Finish', 'Ends the configuration' , '') )
		active = True
		while active and not self.done:
			#TODO: Add entries help
			(code, tag) = d.menu(text='Elija las configuraciones a realizar', height=20, width=60, 
								 title="Configurar manualmente", item_help=1, choices=choices)
	
			if (tag == "Finish"):
				active = False
				self.done = True
			elif (tunes.has_key(tag)):
				tunes[tag].maunal_tune()
			elif (handle_exit_code(d, code) == 0):
				break

def handle_exit_code(d, code):
	"""
	This function is not used after every call to dialog in this demo
	for two reasons:

	   1. For some boxes, unfortunately, dialog returns the code for
		  ERROR when the user presses ESC (instead of the one chosen
		  for ESC). As these boxes only have an OK button, and an
		  exception is raised and correctly handled here in case of
		  real dialog errors, there is no point in testing the dialog
		  exit status (it can't be CANCEL as there is no CANCEL
		  button; it can't be ESC as unfortunately, the dialog makes
		  it appear as an error; it can't be ERROR as this is handled
		  in dialog.py to raise an exception; therefore, it *is* OK).

	   2. To not clutter simple code with things that are
		  demonstrated elsewhere.
	"""
	# d is supposed to be a Dialog instance
	if code in (d.DIALOG_CANCEL, d.DIALOG_ESC):
		if code == d.DIALOG_CANCEL:
			msg = "Ha elegido cancelar.\n" \
				  "Desea salir?"
		else:
			msg = "Ha presionado ESC.\n" \
				  "Desea salir?"
		# "No" or "ESC" will bring the user back.
		# DIALOG_ERROR is propagated as an exception and caught in main().
		# So we only need to handle OK here.
		if d.yesno(msg) == d.DIALOG_OK:
			return 0
	else:
		return 1						# code is d.DIALOG_OK


def replace(file_path, var, repl):
	"""
	Replace value of variable var with repl string.
	
	:param file_path: Path to the file.
	:param var: Variable to replace.
	:param repl: New variable's value.
	
	:warnig: The format of the file must be as follow
	<var>=<value>, with no spaces betwen tokens. 
	
	"""
	
	
	PATTERN = '^%s=.*$' % var
	REPL = '=%s' % repl
	REPLPATTER = '=.*$'
	
	pattern = re.compile(PATTERN)
	repl_pattern = re.compile(REPLPATTER)
	
	
	file_ =  open(file_path)
	lines = file_.readlines()
	new_lines = []
	
	for line in lines:
		if pattern.match(line):
			line = repl_pattern.sub(REPL, line)
		new_lines.append(line)
		
	file_.close()
	
	open(file_path, "w").writelines(new_lines)
			

def main():
	NovaTunner()


if __name__ == '__main__':
	main()
