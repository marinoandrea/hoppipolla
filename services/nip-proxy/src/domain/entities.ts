import { z } from "zod";

/** A unique identifier for the domain entities. */
export type Identifier = string;

const identifierSchema = z.string().uuid();

/** String specialization for ISD-AS tuple addresses */
export const isdAsSchema = z
  .string()
  .regex(
    /^[0-9]+-([0-9a-fA-F]{1,4}:){2}[0-9a-fA-F]{1,4}$/,
    "invalid ISD-AS tuple"
  );
export type IsdAs = z.infer<typeof isdAsSchema>;

const dateInThePastSchema = z
  .date()
  .refine((d) => d <= new Date(), { message: "date cannot be in the future" });

const dataReadingSchema = z.object({
  id: identifierSchema.describe(
    "Uniquer identifier for the data reading entry"
  ),
  isdAs: isdAsSchema.describe(
    "Identifier for the autonomous system (ISD-AS) this reading belongs to"
  ),
  collectedAt: dateInThePastSchema.describe(
    "The date and time when the reading was taken"
  ),
});

export type DataReading = z.infer<typeof dataReadingSchema>;

export enum PowerSource {
  GRID = "grid",
  BATTERY = "battery",
  SOLAR = "solar",
  EOLIC = "eolic",
  HYDRO = "hydro",
}

export enum MachineStatus {
  IDLE = "idle",
  OPERATIONAL = "operational",
  MAINTENANCE = "maintenance",
  OFF = "off",
}

const percentageSchema = z.number().min(0).max(1);

export const energyReadingSchema = z
  .object({
    energyConsumptionKwh: z
      .number()
      .min(0)
      .describe(
        "The amount of energy consumed by the machine, measured in kilowatt-hours (kWh)"
      ),
    cpuUsagePercentage: percentageSchema.describe(
      "The percentage of CPU utilization at the time of the reading"
    ),
    memoryUsagePercentage: percentageSchema.describe(
      "The percentage of memory utilization at the time of the reading"
    ),
    networkTrafficMB: z
      .number()
      .min(0)
      .describe(
        "The amount of network traffic in megabytes (MB) at the time of the reading"
      ),
    temperatureCelsius: z
      .number()
      .min(-273.15) // absolute zero
      .describe(
        "The temperature of the machine in degrees Celsius at the time of the reading"
      ),
    powerSource: z
      .nativeEnum(PowerSource)
      .describe("The source of power (e.g., 'grid', 'battery', 'solar')"),
    status: z
      .nativeEnum(MachineStatus)
      .describe(
        "Operational status of the machine (e.g., 'operational', 'idle', 'maintenance')"
      ),
    carbonEmissionsKg: z
      .number()
      .min(0)
      .describe(
        "The amount of carbon emissions in kilograms (kg) generated by the machine at the time of the reading"
      ),
    renewableEnergyPercentage: percentageSchema.describe(
      "The percentage of energy consumed from renewable sources"
    ),
    energyEfficiencyRating: z
      .string() // TODO: better validation
      .describe(
        "A rating that describes the energy efficiency of the machine (e.g., 'A++', 'A+', 'A', 'B')"
      ),
  })
  .partial()
  .merge(
    z.object({
      machineId: z
        .string()
        .describe(
          "Unique identifier for the machine from which the reading was taken"
        ),
    })
  )
  .merge(dataReadingSchema)
  .readonly();

export type EnergyReading = z.infer<typeof energyReadingSchema>;
export const validateEnergyReading = energyReadingSchema.parse;
