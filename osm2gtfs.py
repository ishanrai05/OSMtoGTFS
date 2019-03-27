AGENCY_URL = "agency_url.com"
AGENCY_TIMEZONE = "UTC + 5:30"
def convertToGTFS(OSMData):
    agencies = []
    stops = []
    routes = []
    shapes = []

    for routemaster in OSMData["routeMasters"]:
        
        tags = routemaster["tags"]
        
        for tag in tags:
            # Agencies
            if tag["k"] == "operator":
                operator = tag["v"]
                # OSM tags are unique
                if not any(d.get("agency_name", None) == operator for d in agencies):
                    agency = {}
                    agency.update({
                        "agency_name" : operator,
                        "agency_url" : AGENCY_URL,
                        "agency_timezone" : AGENCY_TIMEZONE,
                    })
                    # Currently Agencies' GTFS fields not available on OSM 
                    # (Agency URL and Timezone) are hardcoded.
                    agencies.append(agency)

            # Routes
            # (GTFS Routes are based on OSM routemaster (eg. L1) information,
            # not on OSM route (eg. L1 A->B) information.)
            if tag["k"] == "route_master":
                route = tag["v"]
                if route == "subway":
                    route_type = 1
                else:
                    route_type = 0
                routes.append({
                    "route_id" : routemaster["id"],
                    "route_short_name" : tag
                })
        