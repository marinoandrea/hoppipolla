
-valid(Path) :- @floatGt(CarbonEmissionsKg, "$CarbonEmissionsKgThreshold"),
    carbonEmissionsKg(Reading, CarbonEmissionsKg)
    latestEnergyReading(Machine, Reading), 
    machine(Hop, Machine), 
    contains(Path, Hop),
    energyReading(Readings),
    hop(Hop), 
    path(Path).
