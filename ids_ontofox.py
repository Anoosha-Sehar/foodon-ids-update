

"""
    **********************************************************************
    A Script receives a list of ontology id's with their respective
    species/labels from tsv file, check those ids in the ontofox text file
    and if not found, adds them in the right section in file.

    Input Parameters:
    -c : Tab Separated Values file (containing  ontology ids and labels)
    -o: ontofox.txt file (e.g ncbitaxon_ontofox.txt/po_ontofox.txt)
    -t: Type of Ontology (NCBITaxon/PO)
    -I: Name of column having IDs (from tsv file)
    -l: Name of column having labels (from tsv file)

    Output:
    Output will be stored in new (output.txt) file. Change the location to
    “ontofoxfile” in the script to store the output in the same ontofoxfile.

    Example:
    python ids_ontofox.py -c ../CDNO.tsv -o ../po_ontofox.txt -t PO
    -i PO_term -l harvested_food_material
    **********************************************************************
"""

import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawTextHelpFormatter)

requiredName = parser.add_argument_group('required arguments')

requiredName.add_argument("-c", "--CDNO",
                 help= "Tsv file as an input file.", required=True )

requiredName.add_argument("-o", "--ontofoxfile",
                help= "Text file as an input file." , required=True )

requiredName.add_argument("-t", "--type",
                 help= "Ontology type: PO or NCBITaxon"
                       "PO - Plant Ontology",
                          required=True )

requiredName.add_argument("-i", "--id_column",
                help= "Column name having ids." , required=True )

requiredName.add_argument("-l", "--label_column",
                help= "Column name having labels" , required=True )

args = parser.parse_args()
if not args.type: print("Ontology name not specified")
if not args.CDNO: print("Tsv file not provided")
if not args.ontofoxfile: print("Text file not provided")
if not (args.CDNO or args.ontofoxfile): sys.exit(1)
if not args.id_column: print("Column having IDs  not provided")
if not args.label_column: print("Column having labels not "
                                    "provided")


ontology = str(args.type)
CDNO = args.CDNO
ontofoxfile = args.ontofoxfile
id_column= args.id_column
label_column=args.label_column

def main():

    #Opens input file CDNO organism sample for nutrient composition.tsv
    # in a dataframe
    df = pd.read_csv(CDNO,sep="\t",skiprows = [1], encoding= 'utf-8')
    print(df)

    #Input file ontofox.txt
    f = open(ontofoxfile, "r",encoding="utf-8")
    lines = f.readlines()

    #Checks if PO id is present in column and assigns PO_id as key in
    # dictionary and harvested_food_material as a value.
    thisdict={}
    for x in range(0, len(df[id_column])):
        if ontology in (df.loc[x, id_column]):
            if "_" in  df.loc[x, id_column]:
                df.loc[x, id_column]=df.loc[x, id_column].replace("_",":")
            thisdict[df.loc[x,id_column]] = df.loc[x,label_column]
    print(ontology)
    print(df[id_column])
    print(thisdict)
    print(len(thisdict))

    subject_id = []
    counter=0
    for i in range(0,len(lines)):
        if (ontology + "_") in lines[i] and " #" in lines[i]:
            subject = lines[i][lines[i].index(ontology + "_"):lines[
                i].index(
                " #")]
            subject = subject.replace("_", ":")
            subject_id.append(subject)
            if "[Top level source" in lines[i+2]:
                counter=i+2

    f.close()

    #Unmatched taxon ids between CDNO.tsv and ncbitaxon_ontofox.txt
    diff = set(thisdict.keys()) - set(subject_id)
    print(diff)
    #Length of mismatched id's
    print(len(diff))

    #Write output in new text file, or choose "ontofoxfile" if you
    # wish to write in previous ontofoxfile text file.
    f = open("output.txt", 'w')
    for x in range(0, counter):
        f.write(lines[x])
    URL = "http://purl.obolibrary.org/obo/"

    for i in diff:
        f.write(URL + i.replace(":", "_") + " # " + thisdict[i] + "\n")
    f.write("\n")
    for x in range(counter, len(lines)):
        f.write(lines[x])
    f.close()

if __name__ == '__main__':
    main()
