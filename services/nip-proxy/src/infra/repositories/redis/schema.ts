import { Schema } from "redis-om";

export const energyReadingSchema = new Schema(
  "energyReading",
  {
    id: { type: "string", sortable: false },
    isdAs: { type: "string", sortable: false },
    machineId: { type: "string", sortable: false },
    collectedAt: { type: "date", sortable: true },
    energyConsumptionKwh: { type: "number", sortable: true },
    cpuUsagePercentage: { type: "number", sortable: true },
    memoryUsagePercentage: { type: "number", sortable: true },
    networkTrafficMB: { type: "number", sortable: true },
    temperatureCelsius: { type: "number", sortable: true },
    powerSource: { type: "string", sortable: false },
    status: { type: "string", sortable: false },
    carbonEmissionsKg: { type: "number", sortable: true },
    renewableEnergyPercentage: { type: "number", sortable: true },
    energyEfficiencyRating: { type: "string", sortable: true },
  },
  { dataStructure: "JSON" }
);

export type EnergyReadingSchema = typeof energyReadingSchema;

export const geoReadingSchema = new Schema(
  "geoReading",
  {
    id: { type: "string", sortable: false },
    isdAs: { type: "string", sortable: false },
    collectedAt: { type: "date", sortable: true },
    operatingCountryCodes: { type: "string[]" },
  },
  { dataStructure: "JSON" }
);
