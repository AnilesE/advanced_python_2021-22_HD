# author: Selina Ernst
# date: 10.11.2021

from collections import Counter
import csv
import matplotlib.pyplot as plt

def fasta_file(path, output_file_name):
    """count amino acids within the FASTA document (proteome) 

    Function opens .fasta file and counts all amino acids from all proteins. 
    The counts are saved as a .csv file.

    Args:
        path (string): Where is the .fasta file?
        output_file_name (string): Where should the .csv file be saved and what is the filename?
    """

    as_seq = []                 
    with open(path) as f:
        for line in f:                          # create list of strings 
            as_seq.append(line)   
    
    identifier = []             
    one_string = ""
    
    for i, line in enumerate(as_seq):           # i as index of each line
        line = line.replace("\n","")            # delete \n at the end of each string
        as_seq[i] = line                
        if line.startswith(">"):                # all the identifier lines (start of protein)
            identifier_line = as_seq.pop(i)     
            identifier.append(identifier_line)  # identifier lines are stored in variable identifier
        else:
            one_string += line                  # non identifiers are compressed into one single string 
    
    counts = dict(Counter(one_string))          # counting amino acids and output as dictionary  

    with open(output_file_name, "w", newline='') as output: # writing csv file
        w = csv.writer(output) 
        for row in counts.items():              # each row: key, value
            w.writerow(row)

def plot_hist(path, png_filename, hist_title = ""):
    """plot histogtam of .csv file of dictionary with amino acids counts

    Args:
        path (string): Where is the .csv file?
        png_filename (string): Where should the plot be saved and what is the filename?
        hist_title (string): Title of the histogram
    """
    with open(path) as f:                                   # open .csv file
        reader = csv.reader(f)
        as_counts = dict(reader)                            # change type to dictionary
        for keys in as_counts:
            as_counts[keys] = int(as_counts[keys])          # change data type of counts from strin to integer
        plt.bar(as_counts.keys(), as_counts.values())       # plot histogram
        plt.suptitle(hist_title)                            
        plt.savefig(png_filename, dpi = 400)                # save histogram



def main():
    path_fasta = str(input("path of .fasta file (input):"))
    path_csv = str(input("path of .csv file (output):"))
    path_png = str(input("path of .png file (output):"))

    # path_fasta = "uniprot-filtered-reviewed_yes+AND+organism__Homo+sapiens+(Human)+[96--.fasta"
    # path_csv = "human_aminoacids_counts.csv"
    # path_png = "human_hist.png"

    fasta_file(path_fasta, path_csv)
    plot_hist(path_csv, path_png, "Total counts of amino acids")

main()