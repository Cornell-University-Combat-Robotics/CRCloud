from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import chromadb

DEBUG = False
CLOUD_FOLDER_ID = '1qar5ULLVl7UWrkG_ZTV560gmCXFMQt55'
CRC_MEMBER_FOLDER_ID = '1eyUROdczHCL_b0s7ewa4JwpbKSDKUh7c'
TEST_FILE_ID = '1sW9TpNb-4k17yYnB0SyW1la5kuWHKNNDhTOSZlEvcZM'

# Google Drive authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
# Try to load pre-saved local credentials from the credits.txt file; will throw UserWarning if first time running without file
# For some reason the 'new OAuth experience' makes this not work anymore
# gauth.LoadCredentialsFile("credits.txt")
# if gauth.credentials is None:
# 	# No credits saved yet
# 	gauth.LocalWebserverAuth()
# elif gauth.access_token_expired:
#     # Refresh credits if expired
#     gauth.Refresh()
# else:
#     # Initialize the saved creds
#     gauth.Authorize()

# gauth.SaveCredentialsFile("credits.txt")
drive = GoogleDrive(gauth)

file_list = drive.ListFile({
	'q': "'{}' in parents and trashed=false".format(CLOUD_FOLDER_ID),
	'supportsAllDrives': 'true', # used for getting access to all drives, including shared
    'includeItemsFromAllDrives': 'true', # used to get info from all accessed drives
}).GetList()

if DEBUG: print(type(file_list))

if DEBUG:
	for file in file_list:
		print(type(file))
		print('title: %s, id: %s' % (file['title'], file['id']))
	print('--------------------------------')

# TEST: Read file contents from a file
if DEBUG:
	print("TESTING: Reading file contents from file")
	i = 0
	for file in file_list:
		if file['title'] == 'Facts' and file['id'] == TEST_FILE_ID:
			facts = file

	content = facts.GetContentString(mimetype='text/plain')

	# .CreateFile doesn't actually make a new file, it just creates a new object representation for the file/folder in Python
	print(content)
	print('--------------------------------')

# TEST: File type formatting
if DEBUG:
	print("TETING: File type format")
	test_type = type(file_list[0])
	print("Testing type:")
	print(test_type)

	# TEST: Read file type from mimetype
	# mimeType = 'application/vnd.google-apps.folder'

	file = file_list[1]
	print(file['mimeType'])
	print(type(file['mimeType']))
	# ___  = file.GetContentString(mimeType = 'application/vnd.google-apps.folder')
	print('--------------------------------')

	
# STEP 1: Get all the files and download them locally
"""
def vectorize(folder_ID):
	open folder using folder ID
	for each file:
		check type
		if folder:
			recurse with sub ID
		if document:
			get contents
			vectorize_text
		if image: ???
		if sheet/csv: ???

def vectorize_text(text : str):
	chunk text
	vectorize text
	write into database
"""

COMPLETED_DICT = {}

def download_all(folder_id):
	'''
	Adds all the Google Drive files to the 'COMPLETED_DICT'.
	Input:
		folder_id : A string containing the ID of the folder to parse through.
	'''
	if DEBUG:
		file_read_count = 0
	file_list = drive.ListFile({
		'q': "'{}' in parents and trashed=false".format(folder_id),
		'supportsAllDrives': 'true', # used for getting access to all drives, including shared
		'includeItemsFromAllDrives': 'true', # used to get info from all accessed drives
	}).GetList()
	
	for file in file_list:
		file_type = file['mimeType']
		if file_type == "application/vnd.google-apps.folder":
			if DEBUG: 
				print(f"Reading folder {file['title']}")
			folder_id = file['id']
			download_all(folder_id)
		elif file_type == "application/vnd.google-apps.document":
			if DEBUG: 
				file_read_count += 1
				print(f'Reading document #{file_read_count}: {file['title']}')
				print(f"COMPLETED_DICT = {COMPLETED_DICT}")
			content = file.GetContentString(mimetype='text/plain')
			COMPLETED_DICT[file['title']] = content
			# Save the content somehow
			# Save the metadata (for avoiding repeated vectorization)

def save_json(folder = CRC_MEMBER_FOLDER_ID):
	download_all(folder)
	with open('data.json', "w") as f:
		json.dump(COMPLETED_DICT, f, indent=4)

def vectorize_json(filepath : str):
	chroma_client = chromadb.Client()
	with open(filepath) as json_file:
		vec_json = json.load(json_file)

	if DEBUG:
		print(type(vec_json))
		print(vec_json)
	
	collection = chroma_client.get_or_create_collection(name="my_collection")
	
	collection.upsert(
    documents= list(vec_json.values()),
    ids= list(vec_json.keys())
	)
	return collection

if __name__ == "__main__":
	if DEBUG:
		collection = vectorize_json("data.json")
		print(f'Vectorize_json return: {collection}')