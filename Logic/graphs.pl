edge(a,c).
edge(a,b).
edge(b,d).
edge(d,e).

path(X, Y) :- edge(X, Y); edge(Y, X).
path(X, Y) :- path(X, Z), edge(Z, Y); edge(Y, Z).
