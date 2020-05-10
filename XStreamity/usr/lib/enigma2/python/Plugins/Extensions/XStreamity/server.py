#!/usr/bin/python
# -*- coding: utf-8 -*-

# for localized messages     
from . import _

import owibranding
from Screens.Screen import Screen
from plugin import skin_path, json_file, playlist_path, cfg
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from xStaticText import StaticText
from Screens.MessageBox import MessageBox
from Components.ConfigList import ConfigListScreen 
from Components.config import config, getConfigListEntry, NoSave, ConfigText, ConfigSelection, ConfigSelectionNumber, ConfigNumber, ConfigPassword, ConfigYesNo, ConfigEnableDisable

from collections import OrderedDict
import json
import os
import xstreamity_globals as glob

class XStreamity_AddServer(ConfigListScreen, Screen):

	def __init__(self, session, editmode):
		Screen.__init__(self, session)
		self.session = session
		
		skin = skin_path + 'settings.xml'
		
		try:
			from boxbranding import getImageDistro, getImageVersion, getOEVersion
		except:
			
			if owibranding.getMachineBrand() == "Dream Multimedia" or owibranding.getOEVersion() == "OE 2.2":
				skin = skin_path + 'DreamOS/settings.xml'

		with open(skin, 'r') as f:
			self.skin = f.read()
			
		self.setup_title = (_('Add Server'))
		
		self.editmode = editmode
		if self.editmode:
			self.setup_title = (_('Edit Server'))
			
		self.onChangedEntry = []
		
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
		
		self['key_red'] = StaticText(_('Close'))
		self['key_green'] = StaticText(_('Save'))
		
		self['VirtualKB'].setEnabled(False)
		self['HelpWindow'] = Pixmap()
		self['VKeyIcon'] = Pixmap()
		self['HelpWindow'].hide()
		self['VKeyIcon'].hide()
		
		self.name = ''
		self.protocol = 'http://'
		self.server = 'domain.xyz'
		self.port = 80
		self.username = 'username'
		self.password = 'password'
		self.listType = 'm3u'
		self.output = 'ts'
		self.livetype = cfg.livetype.getValue()
		self.vodtype = cfg.vodtype.getValue()
		self.epgShift = 0
		
		self['actions'] = ActionMap(['XStreamityActions'],
		 {
		 'cancel': self.cancel,
		 'red': self.cancel,
		 'green': self.save,
		 }, -2)
		 
		self.onFirstExecBegin.append(self.initConfig)
		
		self.onLayoutFinish.append(self.__layoutFinished)

	
	def __layoutFinished(self):
		self.setTitle(self.setup_title)
		
		
	def cancel(self, answer = None):
		if answer is None:
			if self['config'].isChanged():
				self.session.openWithCallback(self.cancel, MessageBox, _('Really close without saving settings?'))
			else:
				self.close()
		elif answer:
			for x in self['config'].list:
				x[1].cancel()
				
			self.close()
		return
		
		
	def initConfig(self): 
		
		streamtypechoices = [('1', 'DVB(1)'), ('4097', 'IPTV(4097)')]

		if os.path.exists("/usr/bin/gstplayer"):
			streamtypechoices.append( ('5001', 'GStreamer(5001)' ) )
			
		if os.path.exists("/usr/bin/exteplayer3"):
			streamtypechoices.append( ('5002', 'ExtePlayer(5002)') )
			
		if os.path.exists("/usr/bin/apt-get"):
			streamtypechoices.append( ('8193', 'DreamOS GStreamer(8193)') )
				
		if self.editmode == False: 
			self.nameCfg = NoSave(ConfigText(default= _('My IPTV'), fixed_size=False))
			self.protocolCfg = NoSave(ConfigSelection(default='http://', choices=[('http://', _('http://')), ('https://', _('https://'))]))
			self.serverCfg = NoSave(ConfigText(default='domain.xyz', fixed_size=False))
			self.portCfg = NoSave(ConfigNumber(default=80))
			self.usernameCfg = NoSave(ConfigText(default= _('username'), fixed_size=False))
			self.passwordCfg = NoSave(ConfigText(default= _('password'), fixed_size=False))
			self.typeCfg = NoSave(ConfigSelection(default='m3u', choices=[('m3u', 'm3u'), ('m3u_plus', 'm3u_plus')]))
			self.outputCfg = NoSave(ConfigSelection(default='ts', choices=[('ts', 'ts'), ('m3u8', 'm3u8')]))
			self.liveTypeCfg = NoSave(ConfigSelection(default=self.livetype, choices=streamtypechoices))
			self.vodTypeCfg = NoSave(ConfigSelection(default=self.vodtype, choices=streamtypechoices))

			self.epgShiftCfg = NoSave(ConfigSelectionNumber(min = -12, max = 12, stepwidth = 1, default=0))
		else: 
			
			self.name = str(glob.current_playlist['playlist_info']['name'])
			self.protocol = str(glob.current_playlist['playlist_info']['protocol'])
			self.domain = str(glob.current_playlist['playlist_info']['domain'])
			self.port = str(glob.current_playlist['playlist_info']['port'])
			self.username = str(glob.current_playlist['playlist_info']['username'])
			self.password = str(glob.current_playlist['playlist_info']['password'])
			self.listType = str(glob.current_playlist['playlist_info']['type'])
			self.output = str(glob.current_playlist['playlist_info']['output'])
			self.liveType = str(glob.current_playlist['player_info']['livetype'])
			self.vodType = str(glob.current_playlist['player_info']['vodtype'])
			self.epgshift = str(glob.current_playlist['player_info']['epgshift'])
			  
			self.nameCfg = NoSave(ConfigText(default=self.name, fixed_size=False))
			self.protocolCfg = NoSave(ConfigSelection(default=self.protocol, choices=[('http://', _('http://')), ('https://', _('https://'))]))
			self.serverCfg = NoSave(ConfigText(default=self.domain, fixed_size=False))
			self.portCfg = NoSave(ConfigNumber(default=self.port))
			self.usernameCfg = NoSave(ConfigText(default=self.username, fixed_size=False))
			self.passwordCfg = NoSave(ConfigText(default=self.password, fixed_size=False)) 
			self.typeCfg = NoSave(ConfigSelection(default=self.listType, choices=[('m3u', 'm3u'), ('m3u_plus', 'm3u_plus')]))   
			self.outputCfg = NoSave(ConfigSelection(default=self.output, choices=[('ts', 'ts'), ('m3u8', 'm3u8')]))
			self.liveTypeCfg = NoSave(ConfigSelection(default=self.liveType, choices=streamtypechoices))
			self.vodTypeCfg = NoSave(ConfigSelection(default=self.vodType, choices=streamtypechoices))
			self.epgShiftCfg = NoSave(ConfigSelectionNumber(min = -12, max = 12, stepwidth = 1, default=self.epgshift))
			
		self.createSetup()
			
			
	def createSetup(self):  
		self.list = []  
		self.list.append(getConfigListEntry(_('Display name:'), self.nameCfg))
		self.list.append(getConfigListEntry(_('Protocol:'), self.protocolCfg))
		self.list.append(getConfigListEntry(_('Server URL:'), self.serverCfg))
		self.list.append(getConfigListEntry(_('Port:'), self.portCfg))
		self.list.append(getConfigListEntry(_('Username:'), self.usernameCfg))
		self.list.append(getConfigListEntry(_('Password:'), self.passwordCfg))
		self.list.append(getConfigListEntry(_('Type:'), self.typeCfg))
		self.list.append(getConfigListEntry(_('Output:'), self.outputCfg))
		self.list.append(getConfigListEntry(_('Stream Type Live:'), self.liveTypeCfg))
		self.list.append(getConfigListEntry(_('Stream Type VOD:'), self.vodTypeCfg))
		self.list.append(getConfigListEntry(_('EPG Timeshift:'), self.epgShiftCfg))
		
		self['config'].list = self.list
		self['config'].l.setList(self.list)
		self.handleInputHelpers()	
		
		
	def handleInputHelpers(self):
		if self['config'].getCurrent() is not None:
			
			if self.has_key('VKeyIcon'):
				self['VirtualKB'].setEnabled(False)
				self['VKeyIcon'].hide()	
			
			if isinstance(self['config'].getCurrent()[1], ConfigText) or isinstance(self['config'].getCurrent()[1], ConfigPassword):
				if self.has_key('VKeyIcon'):
					if isinstance(self['config'].getCurrent()[1], ConfigNumber):
						self['VirtualKB'].setEnabled(False)
						self['VKeyIcon'].hide()
					else:
						self['VirtualKB'].setEnabled(True)
						self['VKeyIcon'].show()
				
				if not isinstance(self['config'].getCurrent()[1], ConfigNumber):
					
					 if isinstance(self['config'].getCurrent()[1].help_window, ConfigText) or isinstance(self['config'].getCurrent()[1].help_window, ConfigPassword):
						if self['config'].getCurrent()[1].help_window.instance is not None:
							helpwindowpos = self['HelpWindow'].getPosition()

							if helpwindowpos:
								helpwindowposx, helpwindowposy = helpwindowpos
								if helpwindowposx and helpwindowposy:
									from enigma import ePoint
									self['config'].getCurrent()[1].help_window.instance.move(ePoint(helpwindowposx,helpwindowposy))
		
	def save(self):
		if self['config'].isChanged():
			name = self.nameCfg.value.strip()
			protocol = self.protocolCfg.value
			domain = self.serverCfg.value.strip()
			port = self.portCfg.value
			username = self.usernameCfg.value.strip()
			password = self.passwordCfg.value.strip()
			listtype = self.typeCfg.value
			output = self.outputCfg.value
			livetype = self.liveTypeCfg.value
			vodtype = self.vodTypeCfg.value
			epgshift = self.epgShiftCfg.value
			
			if glob.current_playlist:
				glob.current_playlist['playlist_info']['name'] = name
				glob.current_playlist['playlist_info']['protocol'] = protocol
				glob.current_playlist['playlist_info']['domain'] = domain
				glob.current_playlist['playlist_info']['port'] = port
				glob.current_playlist['playlist_info']['username'] = username
				glob.current_playlist['playlist_info']['password'] = password
				glob.current_playlist['playlist_info']['type'] = listtype
				glob.current_playlist['playlist_info']['output'] = output
				glob.current_playlist['player_info']['livetype'] = livetype
				glob.current_playlist['player_info']['vodtype'] = vodtype
				glob.current_playlist['player_info']['epgshift'] = epgshift
			
			playlistline = '%s%s:%s/get.php?username=%s&password=%s&type=%s&output=%s' % (protocol, domain, port, username, password, listtype, output)
			
			# update playlists.txt file 
			with open(playlist_path, 'r+') as f:
				lines = f.readlines()
				f.seek(0)
				exists = False
				for line in lines:
					if not line.startswith('http://') and not line.startswith('https://') and not line.startswith('#'):
						line = '# ' + line
					if domain in line and username in line and password in line:
						line = "\n" + str(playlistline) + "\n"
						exists = True
					f.write(line)
				if exists == False:
					f.write("\n" + str(playlistline) + "\n")
				f.truncate()	
				
				
			#update json file
			
			if os.path.isfile(json_file) and os.stat(json_file).st_size > 0:
				self.playlists_all = []
				with open(json_file) as f:
					self.playlists_all = json.load(f, object_pairs_hook=OrderedDict)
				
				x = 0
				for playlist in self.playlists_all:
					if playlist['playlist_info']['domain'] == str(domain).strip() and playlist['playlist_info']['username'] == str(username).strip() and playlist['playlist_info']['password'] == str(password).strip(): 
						self.playlists_all[x] =  glob.current_playlist
						break
					x += 1

				with open(json_file, 'w') as f:
					json.dump(self.playlists_all, f)	
			
			if self.editmode == False: 	
				glob.configchanged = True
	
		self.close()
		
		
	def changedEntry(self):
		self.item = self['config'].getCurrent()
		for x in self.onChangedEntry:
			x()
		try:
			if isinstance(self['config'].getCurrent()[1], ConfigEnableDisable) or isinstance(self['config'].getCurrent()[1], ConfigYesNo) or isinstance(self['config'].getCurrent()[1], ConfigSelection):
				self.createSetup()
		except:
			pass
	
