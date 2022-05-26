"""Returns trigger data for source attribution."""
import json


def main(request, response):
  aggregatable_trigger_data = json.dumps([{
      "key_piece": "0x400",
      "source_keys": ["campaignCounts"]
  }, {
      "key_piece": "0xA80",
      "source_keys": ["geoValue", "nonMatchingKeyIdsAreIgnored"]
  }])
  aggregatable_values = json.dumps({"campaignCounts": 32768, "geoValue": 1664})
  headers = [("Content-Type", "application/json"),
             ("Attribution-Reporting-Register-Aggregatable-Trigger-Data",
              aggregatable_trigger_data),
             ("Attribution-Reporting-Register-Aggregatable-Values",
              aggregatable_values)]
  return (200, "OK"), headers, json.dumps({
      "code": 200,
      "message": "Attribution trigger success.",
      "headers": headers
  })
