modulname = 'Ma_13_Kontakte_Statistik'
_c_ = '(c) 2024, Matthias Mittelstein, Germany, 23816 Neversdorf, Hauptstraße 23'
''' Erstelle eine Statistik darüber, wie oft die unteschiedlichen
    Attribute im Adressbuch benutzt werden.
    '''
import contacts
from datetime import datetime
import operator
import platform
import console

import ma_print
import ma_sendmail
from   ma_zaehlerfeld import Zählerfeld



def use_contact(p,z):
	
	''' #deb
	if p.id == 2 or p.id == 30 :
		print('>>>deb')
		print(p.phone)
		print('<<<deb')
		#i=5/0
	'''
	
	z.full_name += 1
	if p.prefix:
		z.prefix +=1
	if p.first_name:
		z.first_name +=1
	if p.first_name_phonetic:
		z.first_name_phonetic +=1
	if p.middle_name:
		z.middle_name +=1
	if p.middle_name_phonetic:
		z.middle_name_phonetic +=1
	if p.last_name:
		z.last_name +=1
	if p.last_name_phonetic:
		z.last_name_phonetic += 1
	if p.suffix:
		z.suffix +=1
	if p.nickname:
		z.nickname += 1
	if p.birthday:
		z.birthday += 1
	
	if p.address:
		z.address[len(p.address)] += 1
	else:
		z.address[0] += 1

	if p.organization:
		z.organization  += 1
	if p.department:
		z.department += 1
	if p.job_title:
		z.job_title +=1
		
	if p.email:
		z.email[len(p.email)] += 1
	else:
		z.email[0] += 1
	if p.instant_message:
		z.instant_message[len(p.instant_message)] += 1
	else:
		z.instant_message[0] += 1
	if p.phone:
		z.phone[len(p.phone)] += 1
	else:
		z.phone[0] += 1
	if p.related_names:
		z.related_names[len(p.related_names)] += 1
	else:
		z.related_names[0] += 1
		
	if p.social_profile:
		z.social_profile[len(p.social_profile)] += 1
	else:
		z.social_profile[0] += 1
	if p.url:
		z.url[len(p.url)] += 1
	else:
		z.url[0] += 1
	
	if p.kind:
		z.kind[p.kind] += 1
	if p.kind == 0:
		z.kind[p.kind] += 1
	else:
		z.kind[5] += 1    #5
		
	if p.note:
		z.note += 1

	if p.creation_date :
		z.creation_date +=1
	if p.modification_date :
		z.modification_date +=1
	
	if p.vcard:
		z.vcard += 1
		
#enddef use_contact

def name_of_kontakt(p):
	return p.full_name
	
def alle_kontakte(z):
	
	print(_c_)
	print(platform.node())
	now = datetime.now()
	print(str(now))
	print('-' * 30)
	print(' ')
	
	kontakte = contacts.get_all_people( )
	
	for p in kontakte:
		use_contact(p,z)

#main

print(modulname)
z   = Zählerfeld()
z.addvarIs(( 'full_name', 'prefix', 'first_name', 'first_name_phonetic',
             'middle_name', 'middle_name_phonetic', 
             'last_name', 'last_name_phonetic', 'suffix', 'nickname', 
             'birthday', 'organization', 'department', 'job_title' ))
z.addvarArrI('instant_message')
z.addvarIs(( 'note', 'creation_date', 'modification_date', 'vcard' ))
z.addvarArrIs(( 'address', 'email', 'phone','related_names', 
               'social_profile', 'url' ))
z.addvarArrI('kind')

alle_kontakte(z)


print('Anzahl der Einräge (wahrscheinlich) = {0:d}'.format( z.größterZähler()))
z.druckeAlleDerInstanz()
