from __future__ import print_function
import argparse
import os
import os.path

import filehasher.model as model
import filehasher.hashing as hasher



def main():
	arg_parser = argparse.ArgumentParser(description='hashing')
	arg_parser.add_argument('-c', '--check', default=False, action='store_true', required=False, help='Check if present, otherwise generate')
	arg_parser.add_argument('-p', '--path', default=os.getcwd(), required=False, help='path to process')
	arg_parser.add_argument('-db', '--database', required=True, help='Database to store the information')

	arguments = arg_parser.parse_args()

	data_model = model.DataModel(arguments.database)

	if arguments.check:
		print('Checking for files...')
		for path, directory, files in os.walk(arguments.path):
			print('	Checking directory: {0}'.format(path))
			for file_item in files:
				full_path = os.path.join(path, file_item)

				hash_data = hasher.hash_file(full_path)
				data_model.check_file(hash_data, full_path)

				print('.', end='')
			print('+', end='')

		for new_file in data_model.get_new_files():
			print('New File - hash: {0}, path: {1}'
			      .format(new_file['hash'],
				          new_file['path']))

		for missing_file in data_model.get_missing_files():
			print('Missing File - hash: {0}, path: {1}'
			      .format(missing_file['hash'],
				          missing_file['path']))

	else:
		print('Generating file data...')
		for path, directory, files in os.walk(arguments.path):
			for file_item in files:
				full_path = os.path.join(path, file_item)

				hash_data = hasher.hash_file(full_path)
				if not data_model.has_file(hash_data):
					data_model.add_file(hash_data, full_path)
				else:
					print('Duplicate file: {0}'.format(full_path))
				print('.', end='')
			print('+', end='')

if __name__ == '__main__':
	main()
