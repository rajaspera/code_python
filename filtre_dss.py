import os
import sys
import logging,traceback

input = "C:\\Users\\rajaspk\\Documents\\script4\\04_RxML_Selection"

def filtre_dss(A):
    message = {}
    logging.basicConfig(filename=A+'\\formatage.log',level=logging.DEBUG,format ='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Start of the application:')
    try:
        for_comparaison = open(os.path.join(A,'for_comparaison.csv'),"w+")
        for fichier in os.listdir(A):
            print fichier
            for_comparaison.write(fichier+"\n")
    except Exception as e:
        message = "couldn't write inside the file"
        logging.error(message)
    finally:
        for_comparaison.close()
        logging.info("End of the script")

filtre_dss(input)
