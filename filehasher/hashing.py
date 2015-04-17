import hashlib


def hash_file(path, chunking=1024*1024):
	hasher = hashlib.sha1()
	with open(path, 'rb') as input_data:
		while True:
			data = input_data.read(chunking)
			if len(data):
				hasher.update(data)
			else:
				break
		return hasher.hexdigest().lower()
