#!/usr/bin/env python


import argparse
import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
import time 
from datetime import datetime, date, time, timedelta
import sys
import os
import glib

downloads_dir = glib.get_user_special_dir(glib.USER_DIRECTORY_DOWNLOAD)

print downloads_dir

parser = argparse.ArgumentParser()
parser.add_argument('path_to_json_file')
args = parser.parse_args()

import_file_path = args.path_to_json_file
import_file_name = os.path.splitext(os.path.basename(import_file_path))[0]
import_file_dir = os.path.dirname(import_file_path)
output_file_path = os.path.join(import_file_dir, import_file_name + '.gpx')

file_data = open(import_file_path).read()
json_dictionary = json.loads(file_data)

gpx = Element('gpx')
gpx.set('version', '1.1')
gpx.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
gpx.set('xmlns', 'http://www.topografix.com/GPX/1/1')
gpx.set('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')

trk = SubElement(gpx, 'trk')

workout = json_dictionary['workout']
laps = workout['laps']

total_duration = 0

workout_date = datetime.strptime(workout['workout_date'],'%Y-%m-%d %H:%M:%S')
start_time = workout_date - timedelta(seconds=total_duration)
current_time = start_time

for lap in laps:
		trkseg = SubElement(trk, 'trkseg')
		data_points = lap['data_points']
		for data_point in data_points:
			trkpt = SubElement(trkseg, 'trkpt')
			latlng = data_point['latlng']
			lat = str(latlng[0])
			lon = str(latlng[1])
			elevation = str(data_point['elevation'])
			json_time = data_point['time']
			trkpt.set('lat', lat)
			trkpt.set('lon', lon)
			ele = SubElement(trkpt, 'ele')
			ele.text = elevation
			time_element = SubElement(trkpt, 'time')
			delta = timedelta(seconds=json_time)
			time = start_time + delta
			time_element.text = time.strftime('%Y-%m-%dT%H:%M:%SZ')

tree = ElementTree(gpx)
tree.write(output_file_path, xml_declaration=True)