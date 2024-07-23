import { ServerUnaryCall, sendUnaryData } from "@grpc/grpc-js";

import logger from "./logging";
import { hoppipolla as pb } from "./protos/nip";
import { NipProxyService } from "./service";

function execute<TRequest, TResponse>(
  call: ServerUnaryCall<TRequest, TResponse>,
  callback: sendUnaryData<TResponse>,
  func: () => Promise<TResponse>
) {
  func()
    .then((res) => {
      logger.info(`${call.getPath()} OK`);
      logger.debug(res);
      callback(null, res);
    })
    .catch((err) => {
      logger.error(`${call.getPath()} ERROR`);
      logger.debug(err);
      callback(err, null);
    });
}

export class NipProxyGrpcService extends pb.nip.UnimplementedNipProxyService {
  GetEnergyReadings(
    call: ServerUnaryCall<
      pb.nip.GetEnergyReadingsRequest,
      pb.nip.GetEnergyReadingsResponse
    >,
    callback: sendUnaryData<pb.nip.GetEnergyReadingsResponse>
  ): void {
    execute(call, callback, async () => {
      const response = new pb.nip.GetEnergyReadingsResponse();

      const output = await NipProxyService.executeGetAsEnergyData({
        isdAs: call.request.isd_as,
        startTime: new Date(call.request.start_time),
        endTime: new Date(call.request.end_time),
      });

      response.data = output.map(
        (reading) =>
          new pb.nip.EnergyReading({
            id: reading.id,
            isd_as: reading.isdAs,
            collected_at: reading.collectedAt.toISOString(),
            carbon_emissions_kg: reading.carbonEmissionsKg,
            cpu_usage_percentage: reading.cpuUsagePercentage,
            energy_consumption_kWh: reading.energyConsumptionKwh,
            energy_efficiency_rating: reading.energyEfficiencyRating,
            machine_id: reading.machineId,
            memory_usage_percentage: reading.memoryUsagePercentage,
            network_traffic_MB: reading.networkTrafficMB,
            power_source: reading.powerSource,
            renewable_energy_percentage: reading.renewableEnergyPercentage,
            status: reading.status,
            temperature_celsius: reading.temperatureCelsius,
          })
      );

      return response;
    });
  }

  GetGeoReadings(
    call: ServerUnaryCall<
      pb.nip.GetGeoReadingsRequest,
      pb.nip.GetGeoReadingsResponse
    >,
    callback: sendUnaryData<pb.nip.GetGeoReadingsResponse>
  ): void {
    execute(call, callback, async () => {
      const response = new pb.nip.GetGeoReadingsResponse();

      const output = await NipProxyService.executeGetAsGeoData({
        isdAs: call.request.isd_as,
        startTime: new Date(call.request.start_time),
        endTime: new Date(call.request.end_time),
      });

      response.data = output.map(
        (reading) =>
          new pb.nip.GeoReading({
            id: reading.id,
            isd_as: reading.isdAs,
            collected_at: reading.collectedAt.toISOString(),
            operating_country_codes: reading.operatingCountryCodes,
          })
      );

      return response;
    });
  }
}
