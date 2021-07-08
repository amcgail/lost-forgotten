from knowknow import *

db = Dataset('sociology-wos-74b')

db.groupings.append([
    'c', {
        'Coleman, J.|f social theory': 'Coleman, J.|fdn social theory',
        'Coleman, J.|fdn social theory': 'Coleman, J.|fdn social theory',
        'Coleman, J.|foundations of socia': 'Coleman, J.|fdn social theory'
    }
])

db.groupings.append([
    'c', {
        'Tocqueville, A.|1945|democracy in america,v1':'Tocqueville, A.|democracy am',
        'Tocqueville, A.|democracy am':'Tocqueville, A.|democracy am',
        'Detocqueville, A.|democracy am':'Tocqueville, A.|democracy am',
        'Tocqueville, A.|democracy am':'Tocqueville, A.|democracy am',
        'Detocqueville, A.|1945|democracy am,v2':'Tocqueville, A.|democracy am'
    }
])

db.groupings.append([
    'c', {
        'Latour, B.|lab life constructio':'Latour, B.|laboratory life soci',
        'Latour, B.|laboratory life soci':'Latour, B.|laboratory life soci'
    }
])

db.groupings.append([
    'c', {'Castells, M.|inform age ec soc cu': 'Castells, M.|inform age ec soc cu',
        'Castells, M.|1996|inform age ec soc cu,v1': 'Castells, M.|inform age ec soc cu',
        'Castells, M.|1996|information age ec s,v1': 'Castells, M.|inform age ec soc cu',
        'Castells, M.|2000|inform age ec soc cu,v1': 'Castells, M.|inform age ec soc cu'}
])

db.groupings.append([
    'c',{'Hochschild, A.|1989|2 shift':'Hochschild, A.|Second Shift',
        'Hochschild, A.|1989|2 shift working pare':'Hochschild, A.|Second Shift',
        'Hochschild, A.|1989|2nd shift':'Hochschild, A.|Second Shift',
        'Hochschild, A.|1989|2nd shift working pa':'Hochschild, A.|Second Shift',
        'Hochschild, A.|2003|2 shift':'Hochschild, A.|Second Shift'}
])