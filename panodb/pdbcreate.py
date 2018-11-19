# pdbreate.py 
# create an initial database panorama file storage system
#
# tables:
#   images
#   ingests
#   panoramas
#   equirect
#   tilesets
#

# import the core database configuration variables
import pipeconfig

# import the api for interacting with the filestore database
import dbfsapi

#define the string to the database
dbaseloc = pipeconfig.GPANBASE +"/" + pipeconfig.GDBASE
print(dbaseloc)

#instantiate the object for interface with the database
adbfs = dbfsapi.DBFS(dbaseloc)

#make a connection to the databsase file store
adbfs.ConnectDB()

#now call the method to create a fresh set of tables in the database
adbfs.CreateStore()

#call the method to create an initialy empty database with fresh tables
#pdb.execute('''CREATE TABLE images (date text, folder text, filename text, panorama int, ingest int, eye text)''')
#pdb.execute('''CREATE TABLE ingests (date text, basefolder text, folder text, eye text, site text)''')
#pdb.execute('''CREATE TABLE panoramas (date text, panoname text, leftpano text, rightpano text, numimages int)''')
#pdb.execute('''CREATE TABLE equirect (date text, folder text, filename text, panorma int)''')
#pdb.execute('''CREATE TABLE tilesets (date text, folder text, filename text, panorama int)''')
#pdb.commit();

#pdb.close();

adbfs.DisconnectDB()
print("Panorama Creation Ended");
