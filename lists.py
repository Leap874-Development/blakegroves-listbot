from tinydb import TinyDB, Query

db = TinyDB('database.json')
List = Query()

class ListExists(Exception): pass
class ListNotFound(Exception): pass

def get_list(name):
	results = db.search(List.name == name)

	if len(results):
		return results[0]
	else:
		raise ListNotFound()

def new_list(name, length):
	try:
		get_list(name)
		raise ListExists()
	except ListNotFound:
		db.insert({
			'name': name,
			'data': [0] * length
		})

def delete_list(name):
	if not get_list(name):
		raise ListNotFound()
	
	db.remove(List.name == name)

def add_member(name, uid, posn):
	orig = get_list(name)['data']
	orig[posn] = uid
	db.update({'data': orig}, List.name == name)

def remove_member(name, uid):
	orig = get_list(name)['data']
	for i,c in enumerate(orig):
		if c == uid:
			orig[i] = 0
	db.update({'data': orig}, List.name == name)

def clear_position(name, posn):
	orig = get_list(name)['data']
	orig[posn] = 0
	db.update({'data': orig}, List.name == name)

def see_all():
	return db.all()