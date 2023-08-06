import json
import os
import kenessa



class Province:
    def __init__(self, identifier):
        self.path = os.path.dirname(kenessa.__file__)
        self.identifier = identifier
        self.params = ''
        self.json_province  = json.loads(open(self.path + '/json/province.json').read())
        self.json_district =  json.loads(open(self.path + '/json/district.json').read())
        self.json_sector =  json.loads(open(self.path + '/json/sector.json').read())

        try:
            if self.identifier.lower() == 'all':
                self.params = 'all'

            elif isinstance(self.identifier, str):
                if self.identifier[0] == '0':
                    self.params = 'code'
                else:
                    try:
                        self.identifier = int(self.identifier)
                        self.params = 'id'
                    except ValueError:
                        self.params = 'name'
            self.status = 'success'
        except AttributeError:
            self.status = 'error'




    def province(self):


        if self.status == 'error':
            return json.dumps({'error': 'class Province allow string not int'})


        if self.params == 'all':
            return json.dumps({'provinces': self.json_province},
                        sort_keys=True,
                        indent=3,
                        separators=(',', ': ')
                    )
        else:
            json_data = {'province':[]}
            for province in self.json_province:
                try:
                    if province[self.params].lower() == self.identifier.lower():
                        json_data['province'].append(province)
                except AttributeError:
                    if province[self.params] == self.identifier:
                        json_data['province'].append(province)
            return json.dumps(json_data,
                        sort_keys=True,
                        indent=3,
                        separators=(',', ': ')
                    )


    def district(self):

        data = []

        if self.status == 'error':
            return json.dumps({'error': 'class Province allow string not int'})

        if self.params == 'all':
            for province in self.json_province:
                json_p = {province['name']:[]}
                province['district'] = ''
                json_d = []
                for district in self.json_district:
                    if province['id'] == district['province_id']:
                        json_d.append(district)

                province['district'] = json_d
                json_p[province['name']].append(province)

                data.append(json_p)

            return json.dumps(data,
                    sort_keys=False,
                    indent=3,
                    separators=(',', ': ')
                )
        else:
            data = {}
            province = json.loads(Province(str(self.identifier)).province())['province']
            for item in province:
                data['id'] = item['id']
                data['name'] = item['name']
                data['code'] = item['code']

            json_p = {data['name']:[]}
            json_d = []


            for district in self.json_district:
                if data['id'] == district['province_id']:
                    json_d.append(district)

            data['district'] = json_d
            json_p[data['name']].append(data)

            return json.dumps(json_p,
                    sort_keys=False,
                    indent=3,
                    separators=(',', ': ')
                )

    def sector(self):
        if self.status == 'error':
            return json.dumps({'error': 'class Province allow string not int'})

        if self.params == 'all':
            data = []
            for province in self.json_province:
                json_p = {province['name']: []}
                data_district = []
                for district in self.json_district:
                    if province['id'] == district['province_id']:
                        json_d = {district['name']:[]}
                        json_c = []
                        for sector in self.json_sector:
                            if district['id'] == sector['district_id']:
                                json_c.append(sector)
                        district['sector'] = json_c
                        json_d[district['name']].append(district)
                        data_district.append(json_d)
                        province['district'] = data_district
                json_p[province['name']].append(province)
                data.append(json_p)

            return json.dumps(data,
                    sort_keys=False,
                    indent=3,
                    separators=(',', ': ')
                )
        else:
            data = {}
            province = json.loads(Province(str(self.identifier)).province())['province']
            for item in province:
                data['id'] = item['id']
                data['name'] = item['name']
                data['code'] = item['code']

            json_p = {data['name']: []}

            data_district = []
            for district in self.json_district:
                if district['province_id'] == data['id']:
                    json_d = {district['name']: []}
                    json_c = []
                    for sector in self.json_sector:
                        if sector['district_id'] == district['id']:
                            json_c.append(sector)
                    district['sector'] = json_c
                    json_d[district['name']].append(district)
                    data_district.append(json_d)
            data['district'] = data_district
            json_p[data['name']].append(data)

            return json.dumps(json_p,
                    sort_keys=False,
                    indent=3,
                    separators=(',', ': ')
                )




class District:
    def __init__(self, identifier):
        self.path = os.path.dirname(myrw.__file__)
        self.identifier = identifier
        self.params = ''
        self.json_province = json.loads(open(self.path + '/json/province.json').read())
        self.json_district = json.loads(open(self.path + '/json/district.json').read())
        self.json_sector = json.loads(open(self.path + '/json/sector.json').read())







class Sector:
    pass










