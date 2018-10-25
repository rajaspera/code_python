import os, re
from shutil import copyfile, copy
from base64 import b64encode
import pandas as pd
import xml.etree.ElementTree as ET
import gzip
#************************************** Functions  ****************************

#******************************************************************************




class formater:
    ns = {'ns': 'http://www.essilor.com/business/schema/lensCalculation-2006'}
    buffer_size = 1024 * 1000
    out = str()
    B = str()
    col_ident = []
    FR_DATA = []
    track_id = []

    # def __init__(self):
    #     self.path = "C:\\Users\\Karl\\Documents\\code_python_essi\\test"
    #     self.backup="C:\\"
    #     self.datacsv = {}
    #     self.NomFichier = []
    def __init__(self,w,x,y,z,a):
        self.path=w
        self.backup = x
        self.datacsv = y
        self.NomFichier = z
        self.filename = a


    def prepare(self):
        for file in os.listdir(self.path):
            filename = self.path + "\\" + file
            filename_original = self.backup
            # copy(filename, filename_original)
            NomFichier = [file for file in os.listdir(self.path)]
            return self.filename

    def delNul_and_jump(self,filename):
        content = str()
        with open(filename, 'rb', 1) as f:
            cleanfilename = filename + '.tmp'

            with open(cleanfilename, 'wb') as cleanfile:
                hasData = True
                while hasData:
                    buffer = f.read(buffer_size)
                    if not buffer:
                        hasData = False
                    else:
                        buffer = buffer.replace('\x00', '')
                        buffer = buffer.replace('\n', '')
                        cleanfile.write(buffer)
            copyfile(cleanfilename, filename)
            os.remove(cleanfilename)

    def identification(self,filename):
        with open(filename, 'rb') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            identification = root.get('identification')
            col_ident.append(identification)

    def zip_encode64(self,filename):
        with open(filename, 'rb') as xml_file:
            zipFilename = os.path.splitext(filename)[0] + '.gz'
            with gzip.open(zipFilename, 'wb') as zipfile:
                for buffer in xml_file.read(buffer_size):
                    zipfile.write(buffer)

            with open(zipFilename, 'rb') as zipfile:
                content = zipfile.read()
                base64str = content.encode("hex").upper()
                FR_DATA.append(base64str)
        os.remove(zipFilename)

    def recup_trackid(self,tab):
        for fname in tab:
            res = re.findall("File(\d+).xml", fname)[0]  # le [0] c pour enlever les crochets
            track_id.append(res)

    def merge_to_dataframe(self):
        df = pd.DataFrame({'FileName': NomFichier})
        df['Identification'] = col_ident
        df['TRACK_ID_NO'] = track_id
        df['FR_DATA'] = FR_DATA
        return df

    def zip_csv(self):
        with open('out.csv', 'rb') as csv_file:
            buffer = csv_file.read(buffer_size)
            zippe = os.path.splitext('out.csv')[0] + '.gz'
            with gzip.open(zippe, 'wb')as zipped:
                zipped.write(buffer)
        os.remove('out.csv')


    def ToCsv(self):
      return merge_to_dataframe().to_csv('out.csv', index=False, sep=',')

# prepare()
# delNul_and_jump(filename)
# identification(filename)
# zip_encode64(filename)
# recup_trackid(NomFichier)
# ToCsv()
# zip_csv()

first = formater("C:\\Users\\Karl\\Documents\\code_python_essi\\test","C:\\",{},[],[])
filename = first.prepare()
first.delNul_and_jump(filename)
first.identification(filename)
first.zip_encode64()
recup_trackid(NomFichier)
