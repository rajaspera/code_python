import os, re, sys, logging, traceback

#
# input_path = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\rxml_174_stacked_prepared_filtered.txt"
# output_path = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\out_dss_to_xml"
#
# output_path = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\DSS_TO_XML\\SORTIES\\CHLOE_275_167"
# input_path = "C:\\Users\\rajaspk\\Documents\\SLIM_FIT\\DSS_TO_XML\\ENTREES\\CHLOE_275_167\\CHLOE_275_167_RxML_prepared.csv"

if len(sys.argv)==3:
    input_path = sys.argv[1]
    output_path = sys.argv[2]
if len(sys.argv)!=3:
    print "-> Usage: From_Dss_to_xml.py input_files output_path"
    sys.exit(1)


def recup_ident(chain):
    res = {}
    temp = []
    temp = re.findall(r'identification=""(\d+)""',chain)
    res = ''.join(temp)
    return res



def ToXML(input_path,output_path):
    logging.basicConfig(filename=output_path+'\\From_Dss_to_xml.log',level=logging.DEBUG,format ='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Start of the application:')
    try:
        with open(input_path,'r') as CSV:
            ligne1 = CSV.readline()
            i=1

            for line in CSV:
                j = '%06d' % i
                #line = line.strip('""')
                #line = line.rstrip('"')
                line = line.lstrip('"')
                line = line[:-1]
                id = recup_ident(line)
                line = line.replace('""','"')
                line = line.replace('</Job>"','</Job>')
                i=i+1
                filename = j+"_OUTPUT_HeavyCalculationFile"+str(id)+".xml"
                temp = re.findall(r'',line)
                out = os.path.join(output_path,filename)
                try:
                    with open(out,'w+') as xml:
                        xml.writelines(line)
                except Exception as e:
                    message = "writing rror on "+out+" "+e.message+"\n"+traceback.format_exc()
                    logging.error(message)
    except Exception as e:
            message = "Reading error on "+line+" "+e.message+"\n"+traceback.format_exc()
            logging.error(message)


ToXML(input_path,output_path)



if __name__=="__main__":
	print "From_Dss_to_xml.py is being run directly"
	ToXML(input_path,output_path)
else:
	print "	From_Dss_to_xml.py is being imported in another module"




