import codecademylib3
import pandas as pd
import numpy as np

ad_clicks = pd.read_csv('ad_clicks.csv')

# 1
# print(ad_clicks.head(10))

# 2
most_view_plat = ad_clicks.groupby(['utm_source']).user_id.count().reset_index()
# print(most_view_plat.max())

# 3
ad_clicks['is_click'] = ad_clicks.ad_click_timestamp.isnull()
# print(ad_clicks)

# 4
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
cbs_pivot = clicks_by_source.pivot(
  columns='is_click',
  index='utm_source',
  values='user_id'
).reset_index()

# cbs_pivot.columns = ['utm_source', 'False', 'True']
cbs_pivot.rename(columns={False: 'False', True: 'True'}, inplace=True)
cbs_pivot['Total'] = (cbs_pivot['False']) + (cbs_pivot['True'])

cbs_pivot['False (%)'] = round(((cbs_pivot['False'] / cbs_pivot['Total'])*100), 2)
cbs_pivot['True (%)'] = round(((cbs_pivot['True'] / cbs_pivot['Total'])*100), 2)

only_percs = cbs_pivot.copy()
only_percs.drop((['False', 'True', 'Total']), axis='columns', inplace=True)

# print(only_percs)
# print(cbs_pivot)

# 7
cba = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()
cba_piv = cba.pivot(
  columns='is_click',
  index='experimental_group',
  values='user_id'
).reset_index()
cba_piv['Total'] = cba_piv[False] + cba_piv[True]

cba_piv['T%'] = cba_piv[True]/cba_piv['Total']*100

# print(cba_piv.max())

# 8
clicks = ad_clicks.groupby(['experimental_group', 'day', 'is_click']).user_id.count().reset_index()

a_clicks = clicks[(clicks['experimental_group'] == "A")]
a_piv = a_clicks.pivot(
  columns='is_click',
  index='day',
  values='user_id'
)
a_piv['Total'] = a_piv[False]+a_piv[True]
a_piv['A%'] = round((a_piv[True]/a_piv['Total']*100), 2)

print(a_piv)

b_clicks = clicks[(clicks['experimental_group'] == "B")]
b_piv = b_clicks.pivot(
  columns='is_click',
  index='day',
  values='user_id'
)
b_piv['Total'] = b_piv[False]+b_piv[True]
b_piv['B%'] = round((b_piv[True]/b_piv['Total']*100), 2)

print(b_piv)

colA = a_piv['A%']
colB = b_piv['B%']

comp = pd.concat([colA, colB], axis=1).reset_index()
comp['Best'] = comp.apply((lambda x: "A" if x['A%'] > x['B%'] else "B"), axis=1)

print(comp)






