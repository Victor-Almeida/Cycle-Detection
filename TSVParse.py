import csv

def decode_konect_tsv(file_name):
    tsv_list = []
    with open(file_name) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        skip = True
        meta = False
        line_counter = 1
        for line in tsvreader:
            if not skip:
                if not meta:
                    tup = decode_tsv_line(line[0])
                    if not tup:
                        print("Parse error on line " + str(line_counter) + ". The program will continue.")
                    else:
                        tsv_list.append(tup)
                else:
                    aux = line[0].replace('% ', '')
                    tup = decode_tsv_line(aux)
                    if not tup:
                        print("Parse error on line " + str(line_counter) + ". The program will continue.")
                    else:
                        tsv_list.append(tup)
                    meta = False
            else:
                skip = False
                meta = True
        line_counter = line_counter + 1
    return tsv_list
                
def decode_tsv_line(string):    
    nodes = ''
    edges = ''
    node = False
    edge = True
    for char in string:
        if node and char == ' ':
            break
        if node:
            nodes = nodes + char
        if edge and char == ' ':
            edge = False
            node = True
        if edge:
            edges = edges + char
    try:
        return ((int(nodes, 10), int(edges, 10)))
    except:
        return False
