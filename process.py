def process_bars(command,level,param):
    if(level==len(command)):
        return
    if(command[level].split('=')[0] == 'sellcountry'): 
        param[0] = 'inner join Countries on Countries.EnglishName=Bars.CompanyLocation'
        param[3] = 'where Countries.Alpha2=\'{}\''.format(command[level].split('=')[1])

    elif(command[level].split('=')[0] == 'sourcecountry'):
        param[0] = 'inner join Countries on Countries.EnglishName=Bars.BroadBeanOrigin'
        param[3] = 'where Countries.Alpha2=\'{}\''.format(command[level].split('=')[1])
    
    elif(command[level].split('=')[0]=='sellregion'):
        param[0] = 'inner join Countries on Countries.EnglishName=Bars.CompanyLocation'
        param[3] = 'where Countries.region=\'{}\''.format(command[level].split('=')[1])

    elif(command[level].split('=')[0]=='sourceregion'):
        param[0] = 'inner join Countries on Countries.EnglishName=Bars.BroadBeanOrigin'
        param[3] = 'where Countries.region=\'{}\''.format(command[level].split('=')[1])
    
    elif(command[level]=='ratings'):
        pass
    
    elif(command[level]=='cocoa'):
        param[1] = 'CocoaPercent'
         
    elif(command[level].split('=')[0]=='top'):
        param[4] = command[level].split('=')[1]
    
    else:
        param[2] = 'ASC'
        param[4] = command[level].split('=')[1]
    process_bars(command,level+1,param)

def process_company(command, level, param):
    if(level==len(command)):
        return
    
    if(command[level].split('=')[0]=='country'):
        param[1] = "where Countries.Alpha2='{}'".format(command[level].split('=')[1])
    
    elif(command[level].split('=')[0]=='region'):
        param[1] = "where Countries.region='{}'".format(command[level].split('=')[1])
        
    elif(command[level]=='ratings'):
        pass
    
    elif(command[level]=='cocoa'):
        param[0] = 'AVG(CocoaPercent)'
        param[2] = 'AVG(CocoaPercent)'
        
    elif(command[level]=='bars_sold'):
        param[0] = 'count(SpecificBeanBarName)'
        param[2] = 'count(SpecificBeanBarName)'
    
    elif(command[level].split('=')[0]=='top'):
        param[4] = command[level].split('=')[1]
        
    elif(command[level].split('=')[0]=='bottom'):
        param[3] = 'ASC'
        param[4] = command[level].split('=')[1]
        
    process_company(command, level+1, param)
    
def process_country(command, level, param):
    if(level==len(command)):
        return
    
    if(command[level].split('=')[0]=='region'):
        param[2] = 'where Countries.Region=\'{}\''.format(command[level].split('=')[1])
    
    elif(command[level]=='sellers'):
        param[0] = 'CompanyLocation'
        
    elif(command[level]=='sources'):
        param[0] = 'BroadBeanOrigin'
    
    elif(command[level]=='ratings'):
        pass
        
    elif(command[level]=='cocoa'):
        param[1] = 'AVG(Cocoapercent)'
        
    elif(command[level]=='bars_sold'):
        param[1] = 'count(SpecificBeanBarName)'
        
    elif(command[level].split('=')[0]=='top'):
        param[4] = command[level].strip().split('=')[1]
    
    else:
        param[4] = command[level].strip().split('=')[1]
        param[3] = 'asc'
    process_country(command, level+1, param)