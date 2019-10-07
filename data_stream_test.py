#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:11:45 2019

@author: kevin
"""

import numpy as np

filename = 'test_file' + 'tab.h5'
h5 = tb.open_file(filename, 'w')

# creating 2million rows for the database
rows = 2000000
table_model = {
'Num1': tb.IntCol(pos=1),
'Num2': tb.IntCol(pos=2)
}
filters = tb.Filters(complevel=0) # no compression 
table = h5.create_table('/', 'ints', table_model, title='Integers', expectedrows=rows, filters=filters)

print(table)

ran_int = np.random.randint(0, 10000, size=(rows, 2))

# rows to be written one by one
for i in range(rows):
  pointer['Num1'] = ran_int[i, 0]
  pointer['Num2'] = ran_int[i, 1]
  pointer.append()
  # this appends the data and
  # moves the pointer one row forward
tab.flush()

#%%time
#h5.create_table('/', 'ints_from_array', sarray,
#title='Integers', expectedrows=rows, filters=filters)
#h5.remove_node(‘/’, ‘ints_from_array’)