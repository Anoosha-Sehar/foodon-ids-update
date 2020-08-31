

# A Script that receives ncbitaxon_ontofox.txt file and a list of
# ontology id's, their respective species from tsv file and then
# adds them in the right section in file.

import pandas as pd



def main():

    #Opens input file CDNO organism sample for nutrient composition.tsv
    # in a dataframe
    df = pd.read_csv(r"/Users/anoosha/GitHub/foodon-ids-update/CDNO.tsv",
                     sep="\t",skiprows = [1],encoding="utf-8")

    #Input file po_ontofox.txt
    f = open("/Users/anoosha/GitHub/foodon/src/ontology/imports"
             "/po_ontofox.txt", "r")
    lines = f.readlines()

    #Checks if PO id is present in column and assigns PO_id as key in
    # dictionary and harvested_food_material as a value.
    thisdict={}
    for x in range(0, len(df['PO_term'])):
        if "PO" in (df.loc[x, 'PO_term']):
            thisdict[df.loc[x,"PO_term"]] = df.loc[x,
                                             "harvested_food_material"]
    print(thisdict)
    print(len(thisdict))

    subject_id = []
    counter=0
    for i in range(0,len(lines)):
        if "PO_" in lines[i] and " #" in lines[i]:
            subject = lines[i][lines[i].index("PO_"):lines[
                i].index(
                " #")]
            subject = subject.replace("_", ":")
            subject_id.append(subject)
            if "[Top level source" in lines[i+2]:
                counter=i+2

    f.close()

    #Unmatched taxon ids between CDNO.tsv and ncbitaxon_ontofox.txt
    diff = set(thisdict.keys()) - set(subject_id)

    #Length of mismatched id's
    print(len(diff))

    f = open("/Users/anoosha/GitHub/foodon/src/ontology/imports"
             "/po_ontofox.txt", 'w')
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
