% A policy that denies all AS with border routers operating outside of the 
% GDPR regulated area.
gdprArea(AS) :- operates(AS, "AT").  % Austria
gdprArea(AS) :- operates(AS, "BE").  % Belgium
gdprArea(AS) :- operates(AS, "BG").  % Bulgaria
gdprArea(AS) :- operates(AS, "HR").  % Croatia
gdprArea(AS) :- operates(AS, "CY").  % Cyprus
gdprArea(AS) :- operates(AS, "CZ").  % Czechia
gdprArea(AS) :- operates(AS, "DK").  % Denmark
gdprArea(AS) :- operates(AS, "EE").  % Estonia
gdprArea(AS) :- operates(AS, "FI").  % Finland
gdprArea(AS) :- operates(AS, "FR").  % France
gdprArea(AS) :- operates(AS, "DE").  % Germany
gdprArea(AS) :- operates(AS, "GR").  % Greece
gdprArea(AS) :- operates(AS, "HU").  % Hungary
gdprArea(AS) :- operates(AS, "IS").  % Iceland
gdprArea(AS) :- operates(AS, "IE").  % Ireland
gdprArea(AS) :- operates(AS, "IT").  % Italy
gdprArea(AS) :- operates(AS, "LV").  % Latvia
gdprArea(AS) :- operates(AS, "LI").  % Liechtenstein
gdprArea(AS) :- operates(AS, "LT").  % Lithuania
gdprArea(AS) :- operates(AS, "LU").  % Luxembourg
gdprArea(AS) :- operates(AS, "MT").  % Malta
gdprArea(AS) :- operates(AS, "NL").  % Netherlands
gdprArea(AS) :- operates(AS, "NO").  % Norway
gdprArea(AS) :- operates(AS, "PL").  % Poland
gdprArea(AS) :- operates(AS, "PT").  % Portugal
gdprArea(AS) :- operates(AS, "RO").  % Romania
gdprArea(AS) :- operates(AS, "SK").  % Slovakia
gdprArea(AS) :- operates(AS, "SI").  % Slovenia
gdprArea(AS) :- operates(AS, "ES").  % Spain
gdprArea(AS) :- operates(AS, "SE").  % Sweden

:- chosen(AS, _, _, _), not gdprArea(AS).