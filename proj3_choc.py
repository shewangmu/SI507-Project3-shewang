import sqlite3
import csv
import json
import process

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
    	`CocoaPercent`	REAL,
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
        percent = float(line[4].strip('%'))
        cur.execute("INSERT INTO 'Bars' (Company, SpecificBeanBarName, REF, ReviewDate,CocoaPercent, CompanyLocation,CompanyLocationId, Rating,BeanType,BroadBeanOrigin,BroadBeanOriginId) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (line[0],line[1],line[2],line[3],percent,line[5],Id1,line[6],line[7],line[8],Id2))
    
    conn.commit()
    conn.close()
                



# Part 2: Implement logic to process user commands


def process_command(command):
    command = command.split(' ')
    conn  = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    try:
        if(command[0]=='bars'):
            join = ''
            order = 'Rating'
            seq = 'DESC'
            where = ''
            limit = 10
            param = [join,order,seq,where,limit]
            process.process_bars(command[1:],0,param)
            join,order,seq,where,limit = param
            statement = '''
            select SpecificBeanBarName,Company, CompanyLocation,
            Rating, CocoaPercent, BroadBeanOrigin
            from Bars
            {}
            {}
            order by {} {}
            limit {}
            '''.format(join, where, order, seq, limit)
            cur.execute(statement)
            return cur.fetchall()
        elif(command[0]=='companies'):
            select = 'AVG(Rating)'
            where = ''
            order = 'AVG(Rating)'
            seq = 'DESC'
            limit = 10
            param = [select, where, order,seq,limit]
            process.process_company(command[1:],0,param)
            select, where,order,seq,limit = param
            statement = '''
            select Company, CompanyLocation, {}
            from Bars
            inner join Countries on Countries.EnglishName=Bars.CompanyLocation
            {}
            group by Bars.Company
            having count(SpecificBeanBarName)>4
            order by {} {}
            limit {}
            '''.format(select, where, order, seq, limit)
            cur.execute(statement)
            return cur.fetchall()
        elif(command[0]=='countries'):
            select_country = 'CompanyLocation'
            order = 'AVG(Rating)'
            where = ''
            seq = 'desc'
            limit = 10
            param = [select_country,order,where,seq,limit]
            process.process_country(command[1:],0,param)
            select_country,order,where,seq,limit = param
            statement = '''
            select {}, Countries.Region, {}
            from Bars
            inner join Countries on Countries.EnglishName=Bars.{}
            {}
            group by Bars.{}
            having count(SpecificBeanBarName)>4
            order by {} {}
            limit {}
            '''.format(select_country,order,select_country,where,select_country,order,seq,limit)
            cur.execute(statement)
            return cur.fetchall()
        elif(command[0]=='regions'):
            select_country = 'CompanyLocation'
            order = 'AVG(Rating)'
            seq = 'desc'
            limit = 10
            param = [select_country,order,seq,limit]
            process.process_regions(command[1:],0,param)
            select_country,order,seq,limit = param
            statement = '''
            select Countries.Region, {}
            from Bars
            inner join Countries on Countries.EnglishName=Bars.{}
            group by Countries.Region
            having count(SpecificBeanBarName)>4
            order by {} {}
            limit {}
            '''.format(order,select_country,order,seq,limit)
            cur.execute(statement)
            return cur.fetchall()
        else:
            return "Command not recognized: "
    except:
        return ''

        

    
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
        elif response == 'exit':
            print('bye')
            break
        else:
            res = process_command(response)
            if(type(res)==str and len(res) !=0):
                res += response
                print(res)
            elif(len(res)==0):
                print()
            else:
                print_result(response, res)
            continue

def print_result(command, res):
    result = []
    for line in res:
        result.append(list(line))
    if(command.split()[0] =='companies'):
        for line in result:
            line[2] = round(line[2],1)
            
    elif(command.split()[0]=='countries'):
        for line in result:
            line[2] = round(line[2],1)
    
    elif(command.split()[0]=='regions'):
        for line in result:
            line[1] = round(line[1],1)
    else:
        for line in result:
            line[4] = str(line[4])+'%'
        
        
    for line in result:
        s = ''
        for word in line:
            if(type(word)==str and len(word)>12):
                word = word[:12]+'...'
            s += '{:<20}'.format(word)
        print(s)

# Make sure nothing runs or prints out when this file is run as a module

if __name__=="__main__":
    interactive_prompt()