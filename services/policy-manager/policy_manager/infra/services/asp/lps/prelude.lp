% basic types
hop(Hop)    :- contains(Path, Hop), path(Path).
path(Path)  :- contains(Path, Hop), hop(Hop).
data(Data)  :- collected(Hop, Data), hop(Hop).
hop(Hop)    :- collected(Hop, Data), data(Data).
path(Path)  :- valid(Path).

% sanity check for typization
:- hop(X), data(X).
:- hop(X), path(X).
:- data(X), path(X).

% utilities
latest_data_collected_date(Hop, MaxTmp) :-
    hop(Hop),
    MaxTmp = #max {
        Tmp : data_collected_date(Data, Tmp), collected(Hop, Data) }.
% FIXME: MaxTmp breaks if timestamps are equal

latest_data(Hop, Data) :-
    latest_data_collected_date(Hop, MaxTmp),
    data_collected_date(Data, MaxTmp).
