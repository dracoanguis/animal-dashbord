"""
Document to update the general informaion about switzerland in the switzerland.csv file
"""

import pandas as pd
import os.path as op

cantons = ['AG','AI','AR','BE','BL','BS','FR','GE','GL','GR','JU','LU','NE','NI','OW','SG','SH','SO','SZ','TG','TI','UR','VD','VS','ZG','ZU']

def checkSwiss():
    swisspath = op.join('Data','swissInfo.csv')
    modSwiss = op.getmtime(swisspath)

    for id in cantons:
        if op.getmtime(op.join('Data','cantonInfo',(id + '.csv'))) > modSwiss:
            updateSwiss()
            print('Updated Swiss')
            return 

def countCanton(canton,pop):
    fn = canton + '.csv'
    path = op.join('Data','cantonInfo',fn)
    df = pd.read_csv(path)
    counter = len(df[df['populationDensity']>=pop])
    return counter

def updateSwiss():
    allcounts = []
    listcol = ['id'] + [('pop'+str(pop*100)) for pop in range(0,11)]

    for id in cantons:
        countlist = [id]
        for pop in [x*100 for x in range(0,11)]:
            countlist.append(countCanton(id,pop))

        allcounts.append(countlist)

    result = pd.DataFrame(allcounts,columns=listcol)
    result.set_index('id',inplace=True)

    swisspath = op.join('Data','swissInfo.csv')

    result.to_csv(swisspath)


if __name__ == '__main__':
    checkSwiss()