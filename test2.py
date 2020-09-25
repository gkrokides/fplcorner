from collections import defaultdict

list_of_dictionaries = [{'Name': 'A', 'amt': 100},
                        {'Name': 'B', 'amt': 200},
                        {'Name': 'A', 'amt': 300},
                        {'Name': 'C', 'amt': 400},
                        {'Name': 'C', 'amt': 500},
                        {'Name': 'A', 'amt': 600}]


c = defaultdict(int)
for d in list_of_dictionaries:
    c[d['Name']] += d['amt']
