
#!/usr/bin/python3

#########################################################################################
# This pyton script is used to search and get the info related alzheimer
#
#########################################################################################

import requests
from bs4 import BeautifulSoup
import time

################################################################################################
#  search the disease and output the search result
################################################################################################
print('search the disease and output the search result...')


# use the 'requests' package to crawler
url = 'https://www.omim.org/search/?index=geneMap&start=1&search=ALZHEIMER&limit=100&format=tsv'
s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'} 

r = s.get(url, headers=headers)

if r.status_code == 200:
    with open('alzheimer_search_result.txt', 'w') as f:
        f.write(r.text)
else:
    print('error!!!')
    

#print(r.text)


################################################################################################
# combine the search result
################################################################################################
print('combine the search result...')

search_result = open('alzheimer_search_result.txt', 'r').readlines()

# we want to put the gene and mim_number into a dict
gene2mim_number = {}

for line in search_result:
    line = line.strip()
    if  not line.startswith('Downloaded') and not line.startswith('Cytogenetic'):
        if '\t' in line:
            line = line.split('\t')
            gene = line[2]
            if ',' in gene:
                gene = gene.split(',')[0]
            mim_number = line[4]
            
            if gene not in gene2mim_number.keys():
                gene2mim_number[gene] = mim_number
            else:
                pass

#for gene in gene2mim_number.keys():
    #print(gene + ' : ' + gene2mim_number[gene])


##################################################################################################
# get the mutation info related the disease by the mim_number
##################################################################################################
print('get the mutation info related the disease by the mim_number...')

with open('mutation_output.txt', 'a') as f:
    f.write('gene' + '\t' + 'mutation' + '\t' + 'dbSNP' + '\t' + 'ExAC' + '\t' + 'ClinVar')
    f.write('\n')


s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}

for gene in gene2mim_number.keys():
    mim_number = gene2mim_number[gene]
    
    url = 'https://www.omim.org/allelicVariant/' + str(mim_number) + '?format=tsv'

    r = s.get(url, headers=headers)
    time.sleep(2)

    if not r.status_code == 200:
        print('error!!!')
        break
    else:
        # we use 'bs4' package to parser the html
        soup = BeautifulSoup(r.text, 'html.parser')
        if not 'OMIM Error' in str(soup.title):

            #print(mim_number)

            for line in r.iter_lines():
                line = line.strip()
                line = str(line)
                if line.startswith("b'.0"):
                    if 'MOVED' in line:
                        pass
                    else:
                        line = line.split('\\t')
                        phenotype = line[1]
                        mutation = line[2]
                        dbSNP = line[3]
                        ExAC = line[4]
                        ClinVar = line[5]
                
                        if 'ALZHEIMER' in phenotype:
                            mutation_info = gene + '\t' + mutation + '\t' + dbSNP + '\t' + ExAC + '\t' + ClinVar
                            with open('mutation_output.txt', 'a') as f:
                                f.write(mutation_info)
                                f.write('\n')


print('done...')
	
