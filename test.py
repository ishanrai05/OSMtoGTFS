import json
AGENCY_URL = "agency_url.com"
AGENCY_TIMEZONE = "UTC + 5:30"
with open('mock.json') as fp:
    OSMData = json.load(fp)

agencies = []
stops = []
routes = []
shapes = []

def readTagValue(tags, key):
    filteredTagArray = list(filter(lambda f: f['k']==key, tags))
    return filteredTagArray[0]['v']

for routeMaster in OSMData["routeMasters"]:
    
    tags = routeMaster["tags"]
    # print(tags)
    name, ref, color = '','',''
    for t in tags:
        if t['k'] == 'name':
            name = t['v']
        elif t['k'] == 'ref':
            ref = t['v']
        elif t['k'] == 'color':
            color = t['v']
    operatorsArray = list(filter(lambda f: f['k']=='operator',tags))
    # print (operatorsArray)
    if operatorsArray:
        for operators in operatorsArray:
            operator = operators['v']
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
    # print (agencies)
    routeTypeArray = list(filter(lambda f: f['k']=='route_master',tags))
    if routeTypeArray:
        # print (routeTypeArray)
        for routeInfo in routeTypeArray:
            route_type = 0 # Default value to avoid error
            if routeInfo['v'] == 'subway':
                route_type = 1
            routes.append({
                "route_id" : routeMaster["id"],
                "route_short_name" : name,
                "route_long_name" : ref,
                "route_type" : route_type,
                "route_color" : color,
            })

    members = routeMaster['members']
    for member in members:
        List = member['data']['members']
        stop = list(filter(lambda f: f['role']=='stop', List))
        for s in stop:
            stops.append({
                "stop_id" : s['ref'],
                'stop_name' : readTagValue(s['data']['tags'], 'name'),
                "stop_lat" : s['data']['lat'],
                "stop_lon" : s['data']['lon']
            })

        shapeSequence = 1
        shape = []

        wayList = list(filter(lambda f: f['type']=='way', List))
        for ways in wayList:
            way = ways['data']['nds']
            for node in way:
                shape.append({
                    'shape_id' : member['ref'],
                    'shape_pt_lat' : node['data']['lat'],
                    'shape_pt_lon' : node['data']['lon'],
                    'shape_pt_sequence' : shapeSequence
                })
                shapeSequence += 1

import json

with open('agencies.json','w') as f:
    json.dump(agencies, f)
with open('stops.json','w') as f:
    json.dump(stops, f)
with open('routes.json','w') as f:
    json.dump(routes, f)
with open('shapes.json','w') as f:
    json.dump(shape, f)

