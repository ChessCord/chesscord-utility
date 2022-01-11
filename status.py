import os

from dotenv import load_dotenv

import statuspageio

load_dotenv()

statuses = {
    "operational": "🟢",
    "under_maintenance": "🛠️",
    "degraded_performance": "🟡",
    "partial_outage": "🟠",
    "major_outage": "🔴"
}

status = statuspageio.Client(api_key=os.getenv("API_KEY"), page_id=os.getenv("PAGE_ID"))


def get_status():
    comps = {}
    incidents = {}
    for component in status.components.list():
        comps[component.name] = {
            "Status": component.status
        }

    for incident in status.incidents.list_unresolved():
        incidents[incident.name] = {
            "Statuses": [[c.name, c.new_status.replace("_", " ").title()] for c in incident.incident_updates[0].affected_components],
            "StatusMessage": incident.incident_updates[0].body
        }
    
    return comps, incidents
