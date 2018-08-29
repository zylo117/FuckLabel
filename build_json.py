import os
import json


class ImageLabels:
    def __init__(self, json_path):
        self.json_path = json_path
        if not os.path.exists(json_path):
            # create json if not exists
            open(json_path, 'w').close()

        self.json_file = open(json_path, 'rb')
        try:
            self.json_data = json.loads(self.json_file.read().decode('utf-8'))
        except json.decoder.JSONDecodeError:
            self.json_data = {}

    def add_serial(self, filename='', size=0,
                   region_type='polygon', region_points=[],
                   file_attributes={}, obj_name=''):
        # define key
        serial_name = filename + str(size)
        try:
            key = self.json_data[serial_name]
        except KeyError or AttributeError:
            serial = {
                # 'filename': filename.encode('unicode_escape'),  # translate Chinese characters into unicode
                'filename': filename,
                'size': size,
                'regions': [],
                'file_attributes': file_attributes
            }
            # update json_data
            self.json_data[serial_name] = serial

        # if serial exists, append region directly
        self._add_regions(serial_name, region_points, region_type, obj_name)

    def remove_serial(self, serial_name, filesize):
        self.json_data.pop(serial_name + str(filesize))

    def _add_regions(self, serial_name, region_points, region_type='polygon', obj_name=''):
        region = {'shape_attributes': {},
                  'region_attributes': {}}
        region['shape_attributes']['name'] = region_type
        region['shape_attributes']['all_points_x'] = [int(p[0]) for p in region_points]
        region['shape_attributes']['all_points_y'] = [int(p[1]) for p in region_points]

        region['region_attributes']['obj'] = obj_name

        self.json_data[serial_name]['regions'].append(region)

    def update(self):
        json_data_output = json.dumps(self.json_data, ensure_ascii=False)  # dict to json string
        self.json_file = open(self.json_path, 'wb')
        self.json_file.write(json_data_output.encode())

    def close(self):
        self.json_file.close()


if __name__ == '__main__':
    il = ImageLabels('./j.json')
    il.add_serial('广州', 123456, region_points=[[1, 1], [2, 2], [3, 4], [45, 99]], obj_name='city')
    il.add_serial('广州', 123456, region_points=[[333, 333], [2333, 2333], [31, 41], [415, 919]], obj_name='city')
    il.add_serial('猴子', 555555, region_points=[[333, 333], [2333, 2333], [31, 41], [415, 919]], obj_name='animal')
    il.remove_serial('广州', 123456)
    il.add_serial('广州', 123456, region_points=[[1, 1], [2, 2], [3, 4], [45, 99]], obj_name='city')

    il.update()
    il.close()
