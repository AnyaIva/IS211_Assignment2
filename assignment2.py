import argparse
import urllib.request
import csv
import logging
from datetime import datetime
import sys




def downloadData(url):
                                                                  ##downloads the data
    try:
        with urllib.request.urlopen(url) as response:
            res= response.read()
            data = res.decode('utf-8')
            
        return data
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
    pass
  

def processData(content, logger):
    content = content.decode('utf-8').split('\n')[1:-1]           ## takes the contents of the file and  returns a dictionary that maps a person’s ID 
                                                                  ## to a tuple of the form (name, birthday)
    fixed_data = dict()

    for x in range(len(content)):
        line_num = x + 2
        content[x] = content[x].split(',')
        try:
            content[x][2] = datetime.datetime.strptime(content[x][2], '%m/%d/%Y')
            fixed_data[content[x][0]] = (content[x][1], content[x][2])
        except ValueError:
            logger.error(f"Error processing line #{line_num} for ID #{content[x][0]}")

    return fixed_data
    pass
 
def displayPerson(id, personData):                             ## prints the name and birthday of a given user identified by the input id
    try:
        name, date = personData[id]
        print(f'Person #{id} is {name} with a birthday of {date.strftime("%Y-%m-%d")}')
    except ValueError:
        print('No user found with that id')
    pass
  
def main(url):
    
    csvData = downloadData()
    id = int(input("Enter an ID number: "))
    personData = processData(id, csvData)
    displayPerson(id, personData)
    print(f"Running main with URL = {url}...")

if __name__ == "__main__":
                                                                ## Main entry point
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
