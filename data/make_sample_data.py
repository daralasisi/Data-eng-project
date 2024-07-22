import csv

sample_data = [{'Date': '2023-07-17', 'Open' : '192.7798', 'High' : '194.1100', 
                'Low' : '190.6800', 'Close' : '191.6800', 'Volume': '67220100', 'Symbol' : 'AAPL'},
                {'Date': '2023-07-14', 'Open' : '191.8300', 'High' : '194.9700', 
                'Low' : '191.8000', 'Close' : '193.1600', 'Volume': '59052500', 'Symbol' : 'AAPL'}
               ]
fields = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol']

# name of csv file
filename = "small_data.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(sample_data)