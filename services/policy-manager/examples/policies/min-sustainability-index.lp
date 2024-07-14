% Do no route traffic through any AS that has a sustainability index which is 
% less than 10.

#const min_sustainability_index = 10.

-valid(Path) :- Idx < min_sustainability_index,
    sustainability_index(Data, Idx),
    latest_data(Hop, Data),
    contains(Path, Hop).

