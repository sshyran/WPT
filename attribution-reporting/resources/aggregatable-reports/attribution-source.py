"""Register attribution source for aggregatable reports."""
import json


def main(request, response):
  if not request.method == "GET":
    return (405, "Method not allowed"), headers, json.dumps({
        "code": 405,
        "message": "Only GET method supported."
    })
  headers = [("Content-Type", "application/json"),
             ("Attribution-Reporting-Register-Aggregatable-Source",
              json.dumps([{
                  "id": "campaignCounts",
                  "key_piece": "0x159"
              }, {
                  "id": "geoValue",
                  "key_piece": "0x5"
              }]))]
  return (200, "OK"), headers, json.dumps({
      "code": 200,
      "message": "Successfully registered source.",
      "headers": headers,
  })
