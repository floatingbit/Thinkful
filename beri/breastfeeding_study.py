import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

i_fullybreastfeeding = pd.read_csv('Infants_Exclusively_Breastfeeding.csv')
i_fullybreastfeeding['Who'] = 'Infants'
i_fullybreastfeeding['How'] = 'Exclusively Breastfeeding'

i_notbreastfeeding = pd.read_csv('Infants_Not_Breastfeeding.csv')
i_notbreastfeeding['Who'] = 'Infants'
i_notbreastfeeding['How'] = 'Not Breastfeeding'

sample = [i_fullybreastfeeding, i_notbreastfeeding]
composite = pd.concat(sample)
composite.dropna(inplace=True)
composite.notnull()
keys = {'State Agency or Indian Tribal Organization':'Where','Average Participation':'Average','2015-10-01 00:00:00':'October 2015','2015-11-01 00:00:00':'November 2015','2015-12-01 00:00:00':'December 2015','2016-01-01 00:00:00':'January 2016','2016-02-01 00:00:00':'February 2016','2016-03-01 00:00:00':'March 2016','2016-04-01 00:00:00':'April 2016','2016-05-01 00:00:00':'May 2016','2016-06-01 00:00:00':'June 2016','2016-07-01 00:00:00':'July 2016','2016-08-01 00:00:00':'August 2016','2016-09-01 00:00:00':'September 2016'}
composite.rename(columns=keys, inplace=True)
composite.sort_values(by='Where',inplace=True)

sns.set_style("white")

summary = composite.groupby('How').sum()
summary.sort_values(by='Average',inplace=True)
summary.head()

averages = pd.DataFrame(summary['Average'],index=['Exclusively Breastfeeding','Not Breastfeeding'],columns=['Average'])
#sns.barplot(data = averages, x = averages.index, y = 'Average')

infants = composite.sort_values(by='Average', ascending=True)

sns.set(rc={'figure.figsize':(20,40)})
sns.set_style("white")
print(infants)


# Extract the states where the infants who are not being breastfed have averages > the 80th quantile
infants_nbf = infants[infants['How'] == 'Not Breastfeeding']
quantiles_95_nbf = infants_nbf[infants_nbf['Average'] > infants_nbf['Average'].quantile(0.80)]

sns.barplot(data=infants[infants['Where'].isin(quantiles_95_nbf['Where'])], y='Where', x='Average', hue='How', hue_order=['Exclusively Breastfeeding','Not Breastfeeding'],palette=sns.color_palette(palette=['seagreen','indianred']))
