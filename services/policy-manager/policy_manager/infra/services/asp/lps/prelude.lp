hop(Hop) :- contains(Path, Hop), path(Path).
path(Path) :- contains(Path, Hop), hop(Hop).

% utilities
latestGeoReadingCollectedAt(Hop, MaxTmp) :-
    hop(Hop),
    collectedAt(Data, MaxTmp),
    collected(Hop, Data),
    geoReading(Data),
    #max {
        Tmp, 0 : collectedAt(Data, Tmp),
            collected(Hop, Data),
            geoReading(Data)
    } = MaxTmp.

latestEnergyReadingCollectedAt(Hop, MaxTmp) :-
    hop(Hop),
    collectedAt(Data, MaxTmp),
    collected(Hop, Data),
    energyReading(Data),
    #max {
        Tmp, 0 : collectedAt(Data, Tmp),
            collected(Hop, Data),
            energyReading(Data)
    } = MaxTmp.
% FIXME: MaxTmp breaks if timestamps are equal

latestGeoDataCollected(Hop, Data) :-
    latestGeoReadingCollectedAt(Hop, MaxTmp),
    collectedAt(Data, MaxTmp).

latestEnergyDataCollected(Hop, Data) :-
    latestEnergyReadingCollectedAt(Hop, MaxTmp),
    collectedAt(Data, MaxTmp).
