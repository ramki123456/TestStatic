import sqlite3 as lite
import sys

data = (
    ('batch_no', 'item_no','cmpy_name','prc/unt','manf_dt','exp_dt','qty','delar','comment' ),
    ( 01, 521,'dettol',25,'09_2016','09_2020','500ml','sri krishna','for handwash'),
    ( 01, 522,'pears',25,'09_2016','09_2020','500gms','sri krishna','for bath'),
    ( 01, 523,'horlicks',25,'09_2016','09_2020','500gms','sri krishna','for drinking')
)


"""con = lite.connect('pavan.db')

with con:
    
    cur = con.cursor()    
    
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data('batch_no','item_no','cmpy_name','prc/unt','manf_dt','exp_dt','qty','delar','comment')")
    cur.executemany("INSERT INTO data VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)"""
#for retriving data
import sqlite3 as lite
import sys


con = lite.connect('pavan.db')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM data")

    rows = cur.fetchall()

    for row in rows:
        print row