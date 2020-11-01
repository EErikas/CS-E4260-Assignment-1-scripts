import json
from geopy import distance


with open('results 10-30-2020_23-29-59.json') as target:
    data = json.load(target)
# The dictionaries were hardcoded to the names of our particular data files
vantage_point_locations = {
    'vilnius.csv': (54.6871555, 25.2796514),
    'helsinki.csv': (60.1733244, 24.9410248),
    'hong-kong.csv': (22.396428, 114.109497),
    'london.csv': (51.5073509, -0.1277583),
    'montreal.csv': (45.5016889, -73.567256),
    'salt-lake-city.csv': (40.7607793, -111.8910474),
    'sao-paolo.csv': (-23.550520, -46.633309),
    'singapore.csv': (1.352083, 103.819836),
    'sydney.csv': (-33.8674869, 151.2069902),
    'tokyo.csv': (35.709026, 139.731992)
}
nice_names = {
    'vilnius.csv': 'Vilnius-Lithuania',
    'helsinki.csv': 'Helsinki-Finland',
    'hong-kong.csv': 'Hong-Kong-Hong-Kong SAR',
    'london.csv': 'London-UK',
    'montreal.csv': 'Montreal-Canada',
    'salt-lake-city.csv': 'Salt Lake City-USA',
    'sao-paolo.csv': 'Sao Paolo-Brazil',
    'singapore.csv': 'Singapore-Singapore',
    'sydney.csv': 'Sydney-Australia',
    'tokyo.csv': 'Tokyo-Japan'
}
distances = []
for foo in data:
    vantage_point = foo.get('location')
    for bar in foo.get('urls'):

        for foobar in bar.get('locations'):
            server_location = foobar.get('city') + '-' + foobar.get('country')
            vpl = vantage_point_locations.get(vantage_point)
            url_location = (foobar.get('latitude'), foobar.get('longitude'))
            distances.append(
                (nice_names.get(vantage_point),
                 server_location,
                 str(int(distance.distance(vpl, url_location).km)))
            )
# print(*distances, sep='\n')
with open('distances.csv', 'w') as target:
    target.write('Vantage Point, CDN location, Distance\n')
    wd = [','.join(foo)+'\n' for foo in distances]
    target.writelines(wd)
