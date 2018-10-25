import os
import logging,traceback
import sys

# #
# if len(sys.argv)==3:
#     input1 = sys.argv[1]
#     input2 = sys.argv[2]
#
# if len(sys.argv)!=4:
#     print "-> Usage: verify_input.py input_path csv_selection output_path"
#     sys.exit(1)

input1 = "C:\\Users\\rajaspk\\Documents\\script4\\test_input.txt"#fichier csv
input2 = "C:\\Users\\rajaspk\\Documents\\script4\\04_RxML_Selection"#dossier a verifier



def verify(A,B):
    message = {}
    logging.basicConfig(filename=B + '\\formatage.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Start of the copy script:')
    try:
        missing_files = open(os.path.join(B,"missing_files.txt"),"w+")
        try:
            i = 0
            fcsv = open(A,'rb')
            for fichier in os.listdir(B):
                for item in fcsv.readline():
                    # print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    # print "fichier: "+fichier
                    # print "item: "+item
                    # print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    print type(item)
                    print type(fichier)
                    print "ici"
                    if item.strip('\n') == fichier:
                        print"laaaaaaaaa"
                        message = "ok" + fichier + "is there"
                        logging.info(message)

                    else:
                        print"elseeeeee"
                        #missing_files.writelines(fichier)
                        message = fichier.rstrip() + " is missing" + e.message + "\n" + traceback.format_exc()
                        logging.error(message)
                        i = i+1
                    fcsv.seek(0)
        except Exception as e:
            message = "couldn't open the file to read "
            logging.error(message)
        finally:
            fcsv.close()
    except Exception as e:
        message = "couldn't open the file to write into"
        logging.error(message)
    finally:

        missing_files.close()
        logging.info('End of the script')
        logging.info(str(i)+"files are missing")

verify(input1,input2)
