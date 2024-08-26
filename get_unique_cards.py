import sqlite3

conn = sqlite3.connect('cards.db')
cursor = conn.cursor()

query2 = 'SELECT DISTINCT id FROM S1'
query3 = 'SELECT DISTINCT id FROM S2'
query4 = 'SELECT DISTINCT id FROM S3'

result1 = cursor.execute(query2).fetchall()
result2 = cursor.execute(query3).fetchall()
result3 = cursor.execute(query4).fetchall()

combined_names = set(
    [str(row[0]) for row in result1] +
    [str(row[0]) for row in result2] +
    [str(row[0]) for row in result3]
)

with open('cards_id.txt', 'w') as file:
    file.write('\n'.join(combined_names))

print('Distinct names saved to cards.txt')

conn.close()
