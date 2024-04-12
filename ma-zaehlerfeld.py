modulname = 'Ma_Zählerfeld'
_c_ = '(c) 2024, Matthias Mittelstein, Germany, 23816 Neversdorf, Hauptstraße 23'

class Zählerfeld(object):
	'''
	Zählerfeld :=: jede Instanz bietet beliebig viele benannte Zähler an.
	
	Die Zahler werden mit Angabe eines Namens dynamisch hinzugefügt.
	Die Zähler können entwerder ganzzahlig sein oder 
	    ein kurzes Array aus ganzen Zahlen.
	'''

	def __init__(self):
		pass
	
	def addvarI(self,name):
		''' Füge einen Int-Zähler hinzu. 
		    Die Zäh
		    er sind nicht geschützt und können direkt manipuliert werden.
		    Siehe z.B. den Selbsttest an. '''
		self.__dict__.update({name:0})
	
	def addvarArrI(self,name):
		''' Füge ein Array mit 10 Int-Zählern hinzu. '''
		self.__dict__.update({name:[0,0,0,0,0,0,0,0,0]})
	
	def addvarIs(self,liste):
		''' Füge mehrere Int-Zähler hinzu.
		    Der Parameter ist eine Liste von Namen. '''
		for n in liste:
			self.addvarI(n)
	
	def addvarArrIs(self,liste):
		''' Füge mehrere Arrays mit jeweils 10 Int-Zählern hinzu.
		    Der Parameter ist eine Liste von Namen. '''
		for n in liste:
			self.addvarArrI(n)

	def druckeAlleDerInstanz(self):
		''' Drucke alle Attribute der Instanz aus.
		    Das sind normalerweile genau die Zähler. '''
		print ('Alle Instanzen-Attribute\n========================')
		for key in self.__dict__:
			if not(key.startswith("__") and key.endswith("__")) :
				attr = getattr(self, key)
				print ("{0:20s} = {1}".format( key, attr ))

	def größterZähler(self):
		''' Bestimme den höchsten Wert, der in einem Einzelzähler oder als Summe in
		    einem Zählerarray vorkommt. '''
		m = 0
		for key in self.__dict__:
			if not(key.startswith("__") and key.endswith("__")) :
				attr = getattr(self, key)
				# not callable(attr)
				if type(attr) == int:
					if attr > m:
						m = attr
				elif type(attr) == list:
					mi = 0
					for einzel in attr:
						if type(einzel) == int:
							mi += einzel
					if mi > m:
						m = mi
				else:
					print(key,':',type(attr))
		return m
	
	def druckeAlle(self):
		''' Drucke alle Attribute aus. Das könnensowohl Klassenattribute als auch
		    Instanzenattribute sein. Systemattribute werden dabei übersprungen.
		    Einfache Abfragefunktionen werden ausgeführt und das Ergebnis gedruckt.
		    Das ist gut für getter().
		    '''
		print ('Alle Attribute\n==============')
		attrnamen = []
		for key in self.__dict__:
			if not(key.startswith("__") and key.endswith("__")) :
				attrnamen.append(key)
		for key in self.__class__.__dict__:
			if not(key.startswith("__") and key.endswith("__")) :
				attrnamen.append(key)
		for attrname in attrnamen:
			#deb: print(attrname[0:8])
			attr = getattr(self, attrname)
			if attrname[0:10] == 'druckeAlle':
				print ("{0:20s}-> <keine Rekursion>".format( attrname ))
			elif callable(attr):
				try:
					print ("{0:20s}-> {1}".format( attrname, attr()) )
				except:
					print ("{0:20s}-> <braucht Parameter>".format( attrname ))
			else:
				print ("{0:20s} = {1}".format( attrname, attr ))
		
#endclass Zählerfeld

if __name__ == '__main__':
	print('Teste {}\n'.format(modulname))
	mc = Zählerfeld()
	mc.addvarI('fullname')
	mc.addvarArrIs(('email','url'))
	
	mc.fullname += 1
	mc.email[1] += 2
	mc.email[3] += 3
	
	mc.druckeAlleDerInstanz()
	mc.druckeAlle()