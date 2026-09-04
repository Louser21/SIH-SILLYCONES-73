# Ingestion Notes

This folder handles sensor data generation and MQTT publishing.

- `simulator/`: synthetic payload generation.
- `mqtt/`: broker publisher/subscriber integration.

Start with contract-compliant payloads only:

```json
{
  "station_id": "S01",
  "timestamp": "2026-09-05T12:30:00Z",
  "temperature": 34.2,
  "humidity": 71.0
}
```
