import { ServerUnaryCall, sendUnaryData } from "@grpc/grpc-js";

import logger from "./logging";
import { google } from "./protos/google/protobuf/timestamp";
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
        // FIXME: we lose precision here
        startTime: new Date(call.request.interval.start_time.seconds),
        endTime: new Date(call.request.interval.end_time.seconds),
      });

      response.data = output.map(
        (reading) =>
          new pb.nip.EnergyReading({
            id: reading.id,
            isd_as: reading.isdAs,
            collected_at: new google.protobuf.Timestamp({
              // FIXME: we lose precision here
              seconds: Math.round(reading.collectedAt.getTime() / 1000),
            }),
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
}
