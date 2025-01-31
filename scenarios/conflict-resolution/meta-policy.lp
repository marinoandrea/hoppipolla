% Meta-policy always allowing a policy to override any previous one
overrides(P1, P2) :- conflicting(P1, P2),
    issued(_, P1, T1), 
    issued(_, P2, T2),
    T1 > T2.
