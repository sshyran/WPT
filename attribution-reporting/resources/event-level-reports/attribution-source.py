"""Register attribution source for event-level reports."""
import json
from typing import Optional, TypedDict
import uuid


def main(request, response):
  source_event = {
      "source_event_id": str(uuid.uuid1().int >> 64),
      "destination": "http://localhost:8001",
      "expiry": "604800000",
  }
  headers = [("Content-Type", "application/json"), ("Attribution-Reporting-Register-Source", json.dumps(source_event))
            ]
  return (200, "OK"), headers, json.dumps({
      "code": 200,
      "message": "Successfully registered source.",
      "headers": headers,
  })
