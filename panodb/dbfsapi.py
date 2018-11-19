# dbfsapi.py
#   database file store internal api commands
#
# tables:
#   images
#   ingests
#   panoramas
#   equirect
#   tilesets
#
import sqlite3
import pipeconfig
import os


class DBFS:
    def __init__(self, adbaseloc):
        #save the database locaion for later user
        self.dbloc = adbaseloc;

    def ConnectDB(self):
        print("connect to databse " + self.dbloc)
        self.pdb = sqlite3.connect(self.dbloc)
        print(self.pdb)

    def Commit(self):
         print("execute a commit")
         self.pdb.commit()


    def CreateStore(self):
        print ("create database file store " + self.dbloc)
        #create the initial table for timing jobs through the pipeline
        print("try creating a fresh timing table")
        try:
            self.pdb.execute('''CREATE TABLE timing (name text, function text, starttime integer, stoptime integer, timeid integer)''')
        except Exception as inst:
            print("Timing exists: "+str(inst))

        print("try creating a fresh folder table")
        try:
            self.pdb.execute('''CREATE TABLE folders (date text, foldername text)''')
        except Exception as inst:
            print("folders table exists: "+str(inst))

        print("try creating a fresh rawfiles table")
        try:
            self.pdb.execute('''CREATE TABLE rawfiles (fileid integer, date text, dstpath text, srcpath text, dstfolder text, filename text)''')
        except Exception as inst:
            print("rawfiles table exists: "+str(inst))

#self.pdb.execute('''CREATE TABLE panoramas (date text, panoname text, leftpano text, rightpano text, numimages int)''')
#self.pdb.execute('''CREATE TABLE equirect (date text, folder text, filename text, panorma int)''')
#self.pdb.execute('''CREATE TABLE tilesets (date text, folder text, filename text, panorama int)''')
#self.pdb.commit();
#self.pdb.close();

    def DisconnectDB(self):
         self.pdb.close()

#timing methods for the class
    def NewTimer(self):
        print("create a new timer record")
        return -1

    def StartTimer(self,timer):
        print("start a timer")

    def StopTimer(self,timer):
        print("start a timer")


#folder manipulation and management methods
    def NumFolders(self):
          print("return the number of existing folders")
          acurs = self.pdb.cursor()
          acurs.execute("SELECT max(rowid) FROM folders;")
          resnum = acurs.fetchall();
          (id,) = resnum[0]
          if (id is None):
              return '0'
          else:
              return id

    def NewFolder(self):
          print("create and return a new folder")
          acurs = self.pdb.cursor()
          acurs.execute("SELECT max(rowid) FROM folders;")
          resnum = acurs.fetchall()
          (id, ) = resnum[0]
          arowid = "folder1"
          if (id is None):
              imgfolder = 'folder1'
          else:
              imgfolder = 'folder' + str(id + 1)
              arowid = "folder" + str(id+1)
          print(imgfolder)
          os.mkdir(pipeconfig.GPANBASE + "/" +pipeconfig.GPANSTORE + "/" + imgfolder)
          sqlstring = "INSERT INTO folders VALUES (%s,%s);" % ("\'date\'","\'"+imgfolder+"\'")
          print (sqlstring)
          acurs.execute(sqlstring)
          self.pdb.commit()
          return arowid


#ingest files into img record
    def createRawFileRec(self, rootdir, filename):
         print("add file record to rawfiles table")
         acurs = self.pdb.cursor()
         acurs.execute("SELECT max(rowid) FROM rawfiles;")
         resnum = acurs.fetchall()
         (id, ) = resnum[0];
         rowid = id;
         if (id is None):
             rowid = 1;
         else:
             rowid = id +1;
         dstfolder =" "
         sqlstring = "INSERT INTO rawfiles VALUES (%d,%s,%s,%s,%s,%s);" % (rowid,"\'date\'", "\'dstpath\'", "\'"+rootdir+"\\"+filename+"\'", "\'"+dstfolder+"\'", "\'"+filename+"\'")
                            
         print (sqlstring)
         acurs.execute(sqlstring)
         return rowid

#get raw file info
    def getRawFileSrc(self, arecid):
         print("get file record to rawfiles table")
         acurs = self.pdb.cursor()
         acurs.execute("SELECT * FROM rawfiles WHERE ROWID=" +str(arecid)+" ;")
         resnum = acurs.fetchall()
         (id,adate,dpath,spath,flder,afname) = resnum[0]
         return spath

    def updateRawFileRec(self,recnum,dstfolder,afname):
         print("update raw file record")
         acurs = self.pdb.cursor()
         dstpath = dstfolder +"/" + afname
         sqlstring = "UPDATE rawfiles SET dstpath = \'"
         sqlstring += dstpath +"\', dstfolder = \'" 
         sqlstring += dstfolder + "\', filename = \'" + afname + "\' WHERE ROWID=" 
         sqlstring += str(recnum)+" ;"
         print (sqlstring)
         acurs.execute(sqlstring)
         print(afname)

