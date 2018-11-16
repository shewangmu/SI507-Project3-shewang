import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'

def reload_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #drop table to test
    statement = 'drop table if exists Bars'
    cur.execute(statement)
    statement = 'drop table if exists Countries'
    cur.execute(statement)
    conn.commit()
    
    statement = '''
    CREATE TABLE `Bars` (
    	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
    	`Company`	TEXT,
    	`SpecificBeanBarName`	TEXT,
    	`REF`	TEXT,
        'ReviewDate'  TEXT,
    	`CocoaPercent`	TEXT,
    	`CompanyLocation`	REAL,
    	`CompanyLocationId`	INTEGER,
    	`Rating`	REAL,
    	`BeanType`	TEXT,
    	`BroadBeanOrigin`	TEXT,
    	`BroadBeanOriginId`	INTEGER
    );
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
    CREATE TABLE `Countries` (
    	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
    	`Alpha2`	TEXT,
    	`Alpha3`	TEXT,
    	`EnglishName`	TEXT,
    	`Region`	TEXT,
    	`Subregion`	TEXT,
    	`Population`	INTEGER,
    	`Area`	REAL
    );
    '''
    cur.execute(statement)
    conn.commit()
    
    country = json.loads(open(COUNTRIESJSON).read())
    name_dic = {}
    i=1
    for line in country:
        Alpha2 = line['alpha2Code']
        Alpha3 = line['alpha3Code']
        EnglishName = line['name']
        Region = line['region']
        SubRegion = line['subregion']
        Population = line['population']
        Area = line['area']
        cur.execute("INSERT INTO Countries (Alpha2, Alpha3,EnglishName,Region,SubRegion,Population,Area) VALUES (?,?,?,?,?,?,?)",
                     (Alpha2,Alpha3,EnglishName,Region,SubRegion,Population,Area))
    conn.commit()
    
    bars_file = open(BARSCSV)
    parameter = csv.reader(bars_file,delimiter=',',quotechar='"')
    next(parameter)
    for line in parameter:
        cur.execute("select Id from Countries where EnglishName='{}'".format(line[5]))
        a = cur.fetchone()
        if(a!=None):
            Id1 = a[0]
        else:
            Id1 = None
        cur.execute('select Id from Countries where EnglishName=\"{}\"'.format(line[8]))
        b = cur.fetchone()
        if(b!=None):
            Id2 = b[0]
        else:
            Id2 = None
        cur.execute("INSERT INTO 'Bars' (Company, SpecificBeanBarName, REF, ReviewDate,CocoaPercent, CompanyLocation,CompanyLocationId, Rating,BeanType,BroadBeanOrigin,BroadBeanOriginId) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (line[0],line[1],line[2],line[3],line[4],line[5],Id1,line[6],line[7],line[8],Id2))
    
    conn.commit()
    conn.close()
                



# Part 2: Implement logic to process user commands
def process_command(command):
    res = []
    


def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

# Make sure nothing runs or prints out when this file is run as a module

if __name__=="__main__":
    interactive_prompt()
