import json
d={"pipeline":"Sales Data Pipeline","expected":"INTEGER","actual":"STRING","root_cause":"Schema Drift","confidence":96,"impact":{"pipelines":7,"dashboards":2,"ml_models":1},"recommended_fix":"Update schema mapping and rerun validation."}
print(json.dumps(d,indent=2))
