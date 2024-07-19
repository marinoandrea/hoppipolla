
-valid(Path) :- @listContains(CountryCodes, "$CountryCode"),
    operatingCountryCodes(GeoReading, CountryCodes),
    latestGeoReading(Hop, GeoReading),
    hasGeoReading(Hop, GeoReading),
    contains(Path, Hop),
    geoReading(GeoReading),
    hop(Hop),
    path(Path).
