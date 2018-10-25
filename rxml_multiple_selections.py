import os, csv, shutil,glob,zipfile,random
from collections import defaultdict
import rxml_selection,logging,traceback,sys,ntpath




input_path = "C:\\SLIM_FIT_PROJECT\\Data\\00-divers_csv_test\\for_script_rxml_selection_multiple.csv"
#input_path = "C:\\Users\\Karl\\Documents\\code_python_essi\\rxml_select_multile\\for_script_rxml_selection_multiple.csv"
#input_path = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\input_rxml_sel_multiple\\for_script_rxml_selection_multiple.csv"
input_filename = os.path.basename(input_path)
labs = ['EOLT','EMTC']
#batches_extractions = ['Extraction10','Extraction5']

batches_extractions = ['Extraction_20180621','Extraction_20180716']
materiaux_bases = [(1.665,600.0),(1.665,275.0)]


input_path_rxmlselection = "C:\\SLIM_FIT_PROJECT\\Data\\02_RxML_un7z"
output_path_rxmlselection = "C:\\SLIM_FIT_PROJECT\\Data\\00-divers_csv_test\\out_rxml_multi"
# input_path_rxmlselection = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\De JC Deledalle-20180703T080700Z-001\\De JC Deledalle"
# output_path_rxmlselection = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\data\\out_rxml_multi"


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
def row_eraser(text):
    for i in text:
        text = text.replace(i,'')



def random_ratio(file):
    with open(file,'rb')as f:
        nb_ligne = nbnf = nbf = 0
        for line in f:
            nb_ligne +=1
            if ("noFrame" in line)==False:
                nbnf+=1
            else:
                nbf+=1
        f.seek(0)

        make_dir("C:\\work_temp\\with_ratio")
        #tache 1: rajouter compteur noframe et frame pour avoir min(frame,nbtotal)
        #tache 2: enlever carrement les lignes deja lu pour eviter tout doublon

        name = ntpath.basename(file)
        result=os.path.join("C:\\work_temp\\with_ratio",name)
        with open(result,'w+')as res:
            i=j=0
            line_list = f.readlines()
            f.seek(0)
            while(i in range(min(nbf,nb_ligne//3))):
                #line = random.choice(line_list)
                for line in line_list:
                    if (("noFrame" in line)==False):
                        #print line
                        i=i+1
                        #line.split(",")[0]
                        res.write(line)

            f.seek(0)
            while(j in range(2*(min(nbf,nb_ligne)//3))):
                if(line_list!=''):
                    linee = random.choice(line_list)
                    if (("noFrame" in linee)==True):
                        j=j+1
                        #line.split(",")[0]
                        res.write(linee)
                        row_eraser(linee)
##            for line in res:
##                line = line.split(",")[0]
    make_dir("C:\\work_temp\\with_ratio_with_onecol")
    with open(result,'r') as rd_res:
        for line in rd_res:
            temp = line.split(",")[0]
            out = os.path.join("C:\\work_temp\\with_ratio_with_onecol",os.path.basename(file))
            with open(out,'a') as sortie:
                sortie.write(temp+"\n")
                
            



def multi_extract(input_path,labs,batches_extractions,materiaux_bases):
    message = {}
    logging.basicConfig(filename=output_path_rxmlselection+"\\rxml_selection_multi.log",level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Start of the script:')
    m1 = m2 = b1 = b2 = 0

    columns = defaultdict(list)

    with open(input_path,'rb') as input:
        reader = csv.DictReader(input)
        make_dir("C:\\work_temp")
        for row in reader:
            # for (k,v) in row.items():
            #     columns[k].append(v)
            logging.debug("Checking for selection: "+row['FR_FILENAME'])
            for i in batches_extractions:
                for j in labs:
                    for l in materiaux_bases:

                        new_name = i+"_"+j+"_"+str(l[0])+"_"+str(l[1])+".csv"
                        path_temp = os.path.join("C:\\work_temp",new_name)
                        try:
                            with open(path_temp,'a') as f:
                                Entetes = "FR_FILENAME"
                                ligne_entetes = Entetes+"\n"
                                test1=i in (row['ExtractionNumber'])
                                test2=row['Geometrical_Base'] == str(l[1])
                                test3=row['Material_Index'] == str(l[0])
                                test4=row['Lab'] == j
                                A=[test1,i+'    '+row['ExtractionNumber'],test2,test3,test4]
                                print A
                                if (i in(row['ExtractionNumber']))and(row['Geometrical_Base']==str(l[1]))and (row['Material_Index']==str(l[0]))and(row['Lab']==j):
                                    f.write(row['FR_FILENAME']+','+row['Frame']+"\n")
                        except Exception as e:
                            message="Open Error on  " + path_temp.rstrip() + " " + e.message + "\n" + traceback.format_exc()
    list_csv_created = glob.glob('C:\\work_temp\\*.csv')

    for i in list_csv_created:
        if (os.path.getsize(i)!=0):
            random_ratio(i)

            logging.debug("Calling for rxml_selection for Extraction : "+i)

            i_base=ntpath.basename(i)
            make_dir(os.path.join(output_path_rxmlselection,i_base.rstrip('.csv')))
            output_path_rxmlselection2 = os.path.join(output_path_rxmlselection,i_base.rstrip('.csv'))
            input_path_from_random_ratio = "C:\\work_temp\\with_ratio_with_onecol\\"+i_base
            rxml_selection.retrieve_files_from_csv(input_path_from_random_ratio,input_path_rxmlselection,output_path_rxmlselection2)

    #shutil.rmtree("C:\\work_temp")







multi_extract(input_path,labs,batches_extractions,materiaux_bases)


#
# if __name__=="__main__":
#     if len(sys.argv)==5:
#         input_path = sys.argv[1]
#         labs = sys.argv[2]
#         batches_extractions = sys.argv[3]
#         materiaux_bases = sys.argv[4]
#     if len(sys.argv)!=5:
#         print "-> Usage: rxml_multiple_selection.py input_path labs batches_extractions materiaux_bases"
#         sys.exit(1)
# 	print "rxml_selection_script.py is being run directly"
# 	multi_extract(input_path,labs,batches_extractions,materiaux_bases)
# else:
# 	print "	rxml_multiple_selections.py is being imported in another module"
