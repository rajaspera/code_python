import os
import shutil
from distutils.dir_util import copy_tree
import csv,logging,traceback
import sys

#



if len(sys.argv)==4:
	input_path = sys.argv[1]
	output_path = sys.argv[2]
	nb_ss_dos = sys.argv[3]

if len(sys.argv)!=4:
    print "-> Usage: third_sort_script.py input_path output_path nb_ss_dos"
    sys.exit(1)








#output_path = "/home/andry/Documents/copie"

#input_path = "/home/andry/Documents/dossiers_a_tester"
check_this1 = "LeftLxML"
check_this2 = "RightLxML"

def split(path):
    if os.name == 'nt':
        path = os.path.normpath(path)
    return path.split(os.sep)



def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def recup(input_path,output_path,nb_ss_dos):
    message = {}
    logging.basicConfig(filename=output_path + '\\formatage.log', level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Start of the copy script:')

    for root,dirnames,filenames in os.walk(input_path):
        for fn in filenames:
            logging.debug("Checking for complete folder in: "+input_path)
            if (check_this1 in fn) or (check_this2 in fn):
                abs_path = os.path.join(root,fn)
                dir_path= os.path.join(*split(abs_path)[1:nb_ss_dos+1])
                #dir_path="C:\\"+dir_path
                
                print "dir_path "+dir_path
                name =  os.path.join(*split(abs_path)[nb_ss_dos:nb_ss_dos+1])
                print "name "+ name
                make_dir(os.path.join(output_path,name))
                try:
                    copy_tree(dir_path,os.path.join(output_path,name))
                    message = 'Copying good one s '+input_path+" "+output_path
                    logging.info(message)

                except Exception as e:
                    message=message = "Error on " +fn.rstrip() + " " + e.message + "\n" + traceback.format_exc()
                    logging.error(message)
                finally:
                    logging.info('End for this subfolder')
    logging.info('End of the script')
    
if __name__=="__main__":
	print "third_sort_script.py is being run directly"
	recup(input_path,output_path,nb_ss_dos)
else:
	print "	third_sort_script.py is being imported in another module"
	
	
