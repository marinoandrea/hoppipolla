% The aggregated sum across the path for energy_consumption_per_hour
% cannot be higher than 1500.

#const max_sum_energy_consumption_per_hour = 1500.

sum_energy_consumption_per_hour(Path, Sum) :-
    path(Path),
    Sum = #sum { Value : energy_consumption_per_hour(Data, Value),
                latest_data(Hop, Data),
                contains(Path, Hop) }.

:- Value > max_sum_energy_consumption_per_hour,
    sum_energy_consumption_per_hour(_, Value).
