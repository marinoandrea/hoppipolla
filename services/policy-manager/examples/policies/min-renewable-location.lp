% Traffic can be routed through AS that have a renewable energy percentage 
% inferior to 0.5 only if their location is one of the following: Italy, Greece,
% or Spain.
#const min_renewable_energy_percentage = 50.

invalid_renewable_energy(Hop) :- Perc < min_renewable_energy_percentage,
    renewable_energy_percentage(Data, Perc),
    latest_data(Hop, Data).

-valid(Path) :- invalid_renewable_energy(Hop), -location(Hop, "italy"), contains(Path, Hop).
-valid(Path) :- invalid_renewable_energy(Hop), -location(Hop, "greece"), contains(Path, Hop).
-valid(Path) :- invalid_renewable_energy(Hop), -location(Hop, "spain"), contains(Path, Hop).
