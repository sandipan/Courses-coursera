def week1():
	import re
	string = 'bat, lat, mat, bet, let, met, bit, lit, mit, bot, lot, mot'
	result = re.findall('b[ao]t', string)
	print(result)

	import numpy as np

	def l2_dist(a, b):
		result = ((a - b) * (a - b)).sum()
		result = result ** 0.5
		return result 
		
	a1 = np.random.rand(4)
	a2 = np.random.rand(4, 1)
	a3 = np.array([[1, 2, 3, 4]])
	a4 = np.arange(1, 4, 1)
	a5 = np.linspace(1 ,4, 4)

	#print(a1, a2, a3, a4, a5)
	#print(a1.shape, a2.shape, a3.shape, a4.shape, a5.shape)
	#print(a5.shape == a1.shape, a1.shape == a2.shape, a3.shape == a4.shape, a4.ndim == 1)

	import re
	s = 'ACAABAACAAAB'
	result = re.findall('A{1,2}', s)
	L = len(result)
	print(result, L)

	txt = 'Office of Research Administration: (734) 647-6333 | 4325 North Quad Office of Budget and Financial Administration: (734) 647-8044 | 309 Maynard, Suite 205 Health Informatics Program: (734) 763-2285 | 333 Maynard, Suite 500 Office of the Dean: (734) 647-3576 | 4322 North Quad UMSI Engagement Center: (734) 763-1251 | 777 North University Faculty Adminstrative Support Staff: (734) 764-9376 | 4322 North Quad'
	print(re.findall('[(]\d{3}[)]\s\d{3}[-]\d{4}', txt))

	txt = 'I refer to https://google.com and I never refer http://www.baidu.com if I have to search anything'
	print(re.findall('(?<=[https]:\/\/)([A-Za-z0-9.]*)', txt))

	text=r'''Everyone has the following fundamental freedoms:
		(a) freedom of conscience and religion;
		(b) freedom of thought, belief, opinion and expression, including freedom of the press and other media of communication;
		(c) freedom of peaceful assembly; and
		(d) freedom of association.'''

	import re
	pattern = '\(.\)' #X
	print(len(re.findall(pattern,text)))

def week2():

	import pandas as pd
	sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
	obj1 = pd.Series(sdata)
	states = ['California', 'Ohio', 'Oregon', 'Texas']
	obj2 = pd.Series(sdata, index=states)
	obj3 = pd.isnull(obj2)

	x = obj2['California']
	print(x, obj2['California'], obj2['California'] != x, obj2['California'] == None)

	import pandas as pd
	d = {'1': 'Alice','2': 'Bob','3': 'Rita','4': 'Molly','5': 'Ryan'}
	S = pd.Series(d)

	#print(S.loc[0:3]) 
	print(S.iloc[0:3])


	df = pd.DataFrame({'gre':[337,224,316,322,314], 'toefl':[118,107,104,110,103]})
	print(df.where(df['toefl'] > 105).dropna())
	print(df.where(df['toefl'] > 105))
	print(df[df['toefl'] > 105])
	print(df[df['toefl'].gt(105) & df['toefl'].lt(115)])


	import pandas as pd
	s1 = pd.Series({1: 'Alice', 2: 'Jack', 3: 'Molly'})
	s2 = pd.Series({'Alice': 1, 'Jack': 2, 'Molly': 3})

	print(s2[1])
	print(s2.iloc[1])
	#print(s2.loc[1])

	import pandas as pd
	df = pd.DataFrame({'name': ['Alice', 'Jack'], 'Age': [20, 22], 'Gender': ['M', 'F']})
	df.index = ['Math', 'Soci']
	print(df.T)
	print(df.T['Math'])
	
def week3():
	import pandas as pd
	student_df = pd.DataFrame({'School':['Business', 'Law', 'Engineering']}, index=pd.Index(['James', 'Mike', 'Sally'], name='Name'))
	staff_df = pd.DataFrame({'Role':['Director HR', 'Course Liasion', 'Grader']}, index=pd.Index(['Kelly', 'Sally', 'James'], name='Name'))
	df = pd.merge(student_df, staff_df, how='left', left_index=True, right_index=True)
	print(df.head())
	
	import numpy as np
	df = pd.DataFrame({'P2010':np.arange(5), 'P2011':np.random.random(5), 
					   'P2012':np.random.random(5), 'P2013':np.random.random(5), 
					   'P2014':np.random.random(5), 'P2015':np.random.random(5),
					   'P2016':np.random.random(5), 'P2017':np.random.random(5)})
	print(df.head())
	frames = ['P2010', 'P2011', 'P2012', 'P2013','P2014', 'P2015']
	x, y = 1, 1
	df['AVG'] = df[frames].apply(lambda z: np.mean(z), axis=x)
	result_df = df.drop(frames,axis=y)
	print(result_df)
	
	df = pd.DataFrame(['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D'], index=['excellent', 'excellent', 'excellent', 'good', 'good', 'good', 'ok', 'ok', 'ok', 'poor', 'poor'], columns = ['Grades'])
	#print(df)
	my_categories = pd.CategoricalDtype(categories=['D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'], ordered=True)
	grades = df['Grades'].astype(my_categories)
	#print(grades)
	result = grades[(grades>'B') & (grades<'A')]
	print(result)

	df = pd.DataFrame({'world_rank': range(1,8), 'Institution': ['Harvard', 'MIT', 'Stanford', 'Cambridge', 'Oxford', 'IIT', 'JU'], \
					   'country': ['USA','USA','USA','UK','UK','India','India'], 'Rank_Level': ['First Tier Top Univ']*5 +['Second Tier Top Univ', 'Third Tier Top Univ'], \
					   'score': [100, 100, 99, 99, 95, 80, 70]})
	print(df.pivot_table(values='score', index='country', columns='Rank_Level', aggfunc=[np.median], margins=True))
	
	print((pd.Timestamp('11/29/2019') + pd.offsets.MonthEnd()).weekday())
	
	print(pd.Period('01/12/2019', 'M') + 5)
	
#week3()	

def week4():

	import numpy as np
	a = np.arange(8)
	b = a[4:6]
	b[:] = 40
	c = a[4] + a[6]
	#print(a)
	print(c)
	
	import re
	s = 'ABCAC'
	#print(len(re.split('A', s)) == 2)
	#print(len(re.search('A', s)) == 2)
	print(re.match('A', s))
	print(bool(re.match('A', s)) == True)
	
	def result():
		s = 'ACAABAACAAABACDBADDDFSDDDFFSSSASDAFAAACBAAAFASD'

		result = []
		# compete the pattern below
		#pattern = '[^A]AAA'
		pattern = '([^A])AAA'
		for item in re.finditer(pattern, s):
		  # identify the group number below.
		  result.append(item.group(1))
		  
		return result
		
	print(result())
	
	import pandas as pd
	df = pd.Series([4,7,-5,3], index=['d',' b','a','c'])
	#print(df)
	print(df.index[0], df['d'], df.iloc[0], df[0])
	
	import pandas as pd
	s1 = pd.Series([20,15,18,31], index=['Mango','S','Blueberry','V'])
	s2 = pd.Series([20,30,15,20,20], index=['S','V','Blueberry', 'Mango', 'Plain'])
	s3 = s1.add(s2)
	print(s3)
	print(s3['Mango'] >=  s1.add(s2, fill_value = 0)['Mango'], s3['Blueberry'] == s1['Blueberry'], s3['Plain'] >= s3['Mango'], s3['Blueberry'] == s1.add(s2, fill_value = 0)['Blueberry'])
	print(s1.add(s2, fill_value = 0))
	
	S = pd.Series(np.arange(5), index=['a', 'b', 'c', 'd', 'e'])
	print(S['b':'e'], S[['b', 'c', 'd']], S[['b', 'c', 'd']], S[1:4])
	
	df = pd.DataFrame({'a':[5,5,71,67], 'b':[6,82,31,37], 'c':[20,28,92,49]}, index=['R1','R2','R3','R4'])
	print(df)
	f = lambda x: x.max() + x.min()
	df_new = df.apply(f)
	print(df_new)
	print(df_new[1])
	
	df = pd.DataFrame({'Item':['i1','i1','i1','i2','i2','i2'], 'Store':['A', 'B', 'C']*2, 'Quantity sold': [10, 20, np.nan, 5, 10, 15]})
	print(df)
	print(df.groupby('Item').sum())
	print(df.groupby('Item').sum().iloc[0]['Quantity sold'])
	
week4()