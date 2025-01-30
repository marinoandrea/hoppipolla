% A policy that adds a soft-constraint a soft constraint which prioritizes nodes
% with higher average device PFS.
total_avg_psf(TotAvgPsf) :- 
    TotAvgPsf=#sum{AvgPsf: avg_psf(AS, AvgPsf),
    chosen(AS, _, _, _)}.
    
#maximize { Psf: total_avg_psf(TotAvgPsf) }.