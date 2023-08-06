from dfply import *

# d = pd.DataFrame({
#     'a':[1,2,3]
# })
#
# d >>= mutate(b=X.a*2) >> mutate(c=X.a+X.b) >> select(X.b, X.c)
# print d

#print diamonds >> select([0, X.cut], X.price)
#print diamonds >> mutate(tmp=desc(X.cut)) >> head(3)

#print (X*-1).__repr__

#print diamonds >> select(starts_with('c')) >> head(4)
#
# print diamonds >> select(X.y, starts_with('c'), ~starts_with('ca')) >> head(4)
# print diamonds >> select(X.y, X.carat) >> head(2)
# print diamonds >> select(~X.y, ~X.x, ~X.z) >> head(2)
# print diamonds >> select([~X.carat, 'x', 'price']) >> head(2)
# print diamonds >> select(~X.carat, ~X.price) >> head(2)
# print diamonds >> select(~X.carat, ~X.price, X.carat, ['x', 'y']) >> head(2)
#
# print diamonds >> select(columns_from(X.price)) >> head(2)
# print diamonds >> select(~columns_from(X.price)) >> head(2)
# print diamonds >> select(columns_from('price')) >> head(2)
# print diamonds >> select(columns_from(6)) >> head(2)
#
# print '----------------------------------------------------\n'
# print diamonds >> select(columns_to(X.price)) >> head(2)
# print diamonds >> select(columns_to('price')) >> head(2)
# print diamonds >> select(columns_to(6)) >> head(2)
#
# print '----------------------------------------------------\n'
# print diamonds >> select(~columns_to(X.price)) >> head(2)
# print diamonds >> select(~np.array([1,2,3])) >> head(2)
#
# print '----------------------------------------------------\n'
# print diamonds >> select(~0) >> head(2)
# print diamonds >> select(~1, ~2) >> head(2)
# print diamonds >> select(~(~X.carat)) >> head(2)

#print '----------------------------------------------------\n'
#print diamonds >> head(2)
###
# df1 = pd.DataFrame({'x':[1,2,3,4,5], 'y':[10,20,40,50,100]})
# df2 = pd.DataFrame({'x':[3,4], 'y':[40,51], 'z':[600,800]})
# anti_join(df2, by =['x','y'])
