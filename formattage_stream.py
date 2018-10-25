import os, re
from base64 import b64encode
import xml.etree.ElementTree as ET
import gzip
import glob
from zipfile import ZipFile
#************************************** Functions  ****************************

#******************************************************************************


def delNul_and_jump(file):
    content = str()
    with open(file, 'rb', 1) as f:
            hasData = True
            while hasData:
                buffer = f.read(buffer_size)
                if not buffer:
                    hasData = False
                else:
                    buffer = buffer.replace('\x00', '')
                    buffer = buffer.replace('\n', '')
                    cleanfile.write(buffer)



def identification(file):
    with open(file, 'rb') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        identification = root.get('identification')
        xml_file.close()
    return identification


def zip_encode64(filename):
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

def recup_trackid(tab):
   for fname in tab:
       res = re.findall("File(\d+).xml", fname)[0]  # le [0] c pour enlever les crochets
       track_id.append(res)
   return track_id

def recup_trackid_outofrange(tab):
    for fname in tab:
        posi1 = fname.find('File')
        posi2 = fname.find('.xml')
        track_id=fname[posi1+4:posi2]
    return track_id



def zip_csv():
    with open('out.csv', 'rb') as csv_file:
        buffer = csv_file.read(buffer_size)
        zippe = os.path.splitext('out.csv')[0]+'.zip'
        with ZipFile("zippe.zip", mode='w')as zipped:
            zipped.write(buffer)
    os.remove('out.csv')
#************************************** MAIN  ****************************
## MAIN FUNCTION
#******************************************************************************

ns = {'ns': 'http://www.essilor.com/business/schema/lensCalculation-2006'}
buffer_size = 1024 * 10000
out = str()
B = str()

#fr_date = []
#fr_expir = []
#*************************************************************************
#path = "C:\\Users\\Karl\\Documents\\code_python_essi\\test"
csv_out=open("out.csv","a")
csv_out.writelines("FR_ID"+"TYPE_FR"+"Identification"+"TRACK_ID_NO"+"FR_FILENAME"+"FR_DATE"+"FR_DATA"+"FR_EXPIRATIONDATE")


def format_all(path):
    filename = None
    j=0
    #for file in os.listdir(path):
    for fichier in glob.glob(path_rxml+"\\*_OUTPUT*.xml"):
        filename = fichier.replace(path_rxml+"\\","")

        with open("out_temp.txt","rb")as file:
            for buffer in file.read(buffer_size):
                print 'iciiiiii'
                buffer.write(fichier)
                file.close()
                print j
                delNul_and_jump(buffer)
                print buffer
                identification(buffer)
                zip_encode64(buffer)
                print identification(buffer)

        try:
            print recup_trackid(filename)
            recup_trackid(filename)
            csv_out.write('' +'2' + identification(file) + recup_trackid(filename) + filename + '' + FR_DATA + '')
        except:
            i=0
            i = i+1
            print(str(i)+" EXCEPTION GEREE: "+"il y a eu un ou plusieurs extension dans l'identification")
            track_id = 0
            recup_trackid_outofrange(filename)
            print recup_trackid_outofrange(filename)
            csv_out.write('' +'2' + identification(file) + recup_trackid_outofrange(filename) + filename + '' + FR_DATA + '')
        j=j+1
    # ********************************  creer notre csv  **************************

        csv_out.write('' +'2' + identification(file)[j] + recup_trackid_outofrange(filename)[j] + filename + '' + FR_DATA + '')
    # ******************************* Gzipper le csv obtenu **************************
        zip_csv()


#******************************************************************************
#               UTILISATEUR
#****************************************************************************

path_rxml = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\TEST"


format_all(path_rxml)
