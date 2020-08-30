

# A Script that receives ncbitaxon_ontofox.txt file and a list of
# ontology id's, their respective species from tsv file and then
# adds them in the right section in file.

import pandas as pd



def main():

    #Opens CDNO organism sample for nutrient composition.tsv in
    # dataframe
    df = pd.read_csv(r"/Users/anoosha/GitHub/foodon-ids-update/CDNO.tsv",
                     sep="\t",skiprows = [1],encoding="utf-8")

    #NCBITaxon_Ontofox.txt file
    f = open("/Users/anoosha/GitHub/foodon/src/ontology/imports"
             "/po_ontofox.txt", "r")
    lines = f.readlines()

    #List to retrieve lines which contain NCBI_taxon ids in
    # ncbitaxon_ontofox.txt
    subject_id = []
    for i in range(0,len(lines)):
        if "PO_" in lines[i] and " #" in lines[i]:
            subject = lines[i][lines[i].index("PO_"):lines[
                i].index(
                " #")]
            subject = subject.replace("_", ":")
            subject_id.append(subject)
            if "Top level source" in lines[i+3]:
                counter=i+2
    f.close()

    #Length of ncbi_taxon ids in NCBItaxon_ontofox.txt
    print(len(subject_id))

    #Dictionary have "taxon ids" as keys and "cultivated
    # species as "values" from CDNO organism sample for nutrient
    # composition.tsv
    thisdict= pd.Series(df.cultivated_species.values,
               index=df.taxon_id).to_dict()

    #Unmatched taxon ids between CDNO.tsv and ncbitaxon_ontofox.txt
    print(len(set(thisdict.keys()) - set(subject_id)))
    diff=set(thisdict.keys()) - set(subject_id)


    #Write in file after substituting colons with underscores.
    f = open("/Users/anoosha/GitHub/foodon/src/ontology/imports"
             "/po_ontofox.txt", 'w')
    for x in range(0,counter):
        #f.write(lines[x])
        print(lines[x])
    URL= "http://purl.obolibrary.org/obo/"

    for i in diff:
        #f.write(URL+ i.replace(":", "_") + " # "+ thisdict[i] + "\n")
        print(URL+ i.replace(":", "_") + " # "+ thisdict[i] + "\n")


    for x in range(counter,len(lines)):
        #f.write(lines[x])
        print(lines[x])
    f.close()

if __name__ == '__main__':
    main()
