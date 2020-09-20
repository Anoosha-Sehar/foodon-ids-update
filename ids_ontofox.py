

# A Script that receives ncbitaxon_ontofox.txt file and a list of
# ontology id's, their respective species from tsv file and then
# adds them in the right section in file.
import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawTextHelpFormatter)

requiredName = parser.add_argument_group('required arguments')

requiredName.add_argument("-c", "--CDNO",
                 help= "Tsv file as an input file.", required=True )
requiredName.add_argument("-i", "--ontofoxfile",
                help= "Text file as an input file." , required=True )
requiredName.add_argument("-t", "--type",
                 help= "Ontology type: PO or NCBITaxon"
                       "PO - Plant Ontology",
                          required=True )

args = parser.parse_args()
if not args.type: print("Ontology name not specified")
if not args.CDNO: print("Tsv file not provided")
if not args.ontofoxfile: print("Text file not provided")
if not (args.CDNO or args.ontofoxfile): sys.exit(1)

ontology = str(args.type)
CDNO = args.CDNO
ontofoxfile = args.ontofoxfile

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
    for x in range(0, len(df[ontology + "_term"])):
        if ontology in (df.loc[x, ontology + "_term"]):
            if "_" in  df.loc[x, ontology + "_term"]:
                df.loc[x, ontology + "_term"]=df.loc[x, ontology +
                                                     "_term"].replace("_",":")
            thisdict[df.loc[x,ontology + "_term"]] = df.loc[x,
                                             "harvested_food_material"]
    print(ontology)
    print(df[ontology + "_term"])
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

    f = open("/Users/anoosha/GitHub/foodon-ids-update/output.txt", 'w')
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
