%%%% Spec
%% member(b, [a,b,c]) = True
%% member(b, [a, [b,c]]) = False
%% member([b,c], [a,[b,c]]) = True

member(X, [X|Tail]).
member(X, [Head|Tail]) :- member(X, Tail).
