import os, fnmatch
import shutil
from distutils.dir_util import copy_tree
import csv,logging,traceback
import sys, ntpath

# ceci est un script qui permet de copier les dossiers et sous dossiers des snapshots provenant de slimfitToWork
# dont les resultats de l'outil SFSRP ne contiennent pas de fichier RxML.xml a l'interieur



if len(sys.argv)==5:
    input_path_1 = sys.argv[1]
    input_path_2 = sys.argv[2]
	output_path = sys.argv[3]
    check_this = sys.argv[4]


if len(sys.argv)!=5:
    print "-> Usage: rxml_missing.py input_path output_path nb_ss_dos"
    sys.exit(1)

output_path = "C:\\Users\\rajaspk\\Documents\\data\\test_rxml_missing\\copies"
input_path_1 = "C:\\Users\\rajaspk\\Documents\\data\\test_rxml_missing\\_SlimFitRxMLOut"
input_path_2 = "C:\\Users\\rajaspk\\Documents\\data\\test_rxml_missing\\_SnapshotsToWork"
check_this = "RxML.xml"

def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def recup(input_path_1,input_path_2,output_path):
    message = {}
    logging.basicConfig(filename=output_path + '\\formatage.log', level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Start of the copy script:')

    count = 0
    path = None
    good_paths =[]

    nb_part = len(input_path_1.split('\\'))
    paths = []
    baddir = []
    for root,dirnames,filenames in os.walk(input_path_1):
        count = len(root.split('\\'))- nb_part
        if count == 1:
            path = root
            paths.append(path)
        goodfiles = fnmatch.filter(filenames,check_this)
        if len(goodfiles) > 0:
            good_paths.append(path)
        continue

    for good_path in good_paths:
        try:
            paths.remove(good_path)
        except Exception as e:
            pass
    for gp in good_paths:
        print "good_paths:" + gp
    for path in paths:
        print "paths are:"+path
        base = ntpath.basename(path)
        new_base = base.rsplit('_',1)[0]
        temp = input_path_2.rsplit('\\',0)[0]
        input2 = ntpath.join(temp,new_base)
        make_dir(os.path.join(output_path,new_base))
        print "input2"+input2
        try:
            copy_tree(input2,os.path.join(output_path,new_base))
            message = 'Copying bad one s ' + path.rsplit('\\',0)[0] + "  to " + output_path
            logging.info(message)
        except Exception as e:
            message = "Error on " +path.rsplit('\\',0)[0] + " " + e.message + "\n" + traceback.format_exc()
            logging.error(message)
        finally:
            logging.info('End for this folder')
    logging.info('End of the script')


recup(input_path_1,input_path_2,output_path)

if __name__=="__main__":
	print "rxml_missing is being run directly"
	recup(input_path_1,input_path_2,output_path)
else:
	print "	rxml_missing.py is being imported in another module"

	
