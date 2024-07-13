overrides(P1, P2) :-
    has_issued(I1, P1),
    has_issued(I2, P2),
    has_power_over(I1, I2).

#show overrides/2.