% Traffic can be routed through AS that have a renewable energy percentage 
% inferior to 0.5 only if their location is one of the following: Italy, Greece,
% or Spain.

#const min_renewable_energy_percentage = "0.5".

invalid_renewable_energy(Hop) :- Perc<min_renewable_energy_percentage,
    renewable_energy_percentage(Data, Perc),
    latest_data(Hop, Data).

:- invalid_renewable_energy(Hop), location(Hop, "italy").
:- invalid_renewable_energy(Hop), location(Hop, "greece").
:- invalid_renewable_energy(Hop), location(Hop, "spain").
