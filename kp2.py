import psycopg2
import os
import csv
import numpy as np
def write_in_file(dict_history, regions):
    if os.path.exists('history_average2.csv'):
        os.remove('history_average2.csv')
    with open('history_average2.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(["Регіони", "2019", "2020"])
        for i in regions:
            writer.writerow([i, dict_history[i][0], dict_history[i][1]])

query="""SELECT RegName, examyear, AVG(BALL100)	
FROM public.test
LEFT JOIN public.student
USING (student_id)
LEFT JOIN public.place
USING (place_id)
WHERE Subject_ID=2 AND teststatus='Зараховано'
GROUP BY RegName, examyear
ORDER BY RegName, examyear; """


dbname='postgres'
user='postgres'
password='postgres'
host='localhost'
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor=conn.cursor()
cursor.execute(query)
history_query=np.array(cursor.fetchall())
regions = set(history_query[:, 0])
dict_history={}
print(history_query)
for i in regions:
    marks=np.where(history_query==i)[0]
    dict_history[i]=[history_query[marks[0]][2], history_query[marks[1]][2]]

write_in_file(dict_history, regions)
cursor.close()
conn.commit()
conn.close()