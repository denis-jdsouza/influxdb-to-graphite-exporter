#!/usr/bin/env python3.6
from socket import socket
from influxdb import InfluxDBClient
import defs

# Graphite-Carbon Deatils
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003  # plaintext port


def get_metrics_influx(query, query_index):
    """ Function to Query InfluxDB """
    influx_connect = InfluxDBClient(
        host=defs.INFLUX_DETAILS[query_index][0],
        database=defs.INFLUX_DETAILS[query_index][1],
        port=8086,
        timeout=5,
        retries=5)
    response = influx_connect.query(query, epoch='s')
    return response


def process_metrics(data_points, data_groupby, query_index):
    """ Function to process InfluxDB metics into Graphite format """
    lines_list = []
    for value in data_points:
        lines = defs.GRAPHITE_TAGS[query_index] % (data_groupby[defs.INFLUX_QUERY_GROUPBY[query_index]], value.get(
            ''.join(key for key in value if key != 'time')), value.get('time'))
        lines_str = str(lines).strip("[]'")
        lines_list.append(lines_str)
    return lines_list


def send_metrics_graphite(message):
    """ Function to send metrics to Graphite/Carbon """
    sock = socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message.encode())
    sock.close()


if __name__ == "__main__":
    metric_count = 0
    query_index = -1
    for query in defs.INFLUX_QUERY:
        metric_count += 1
        query_index += 1
        response = get_metrics_influx(query, query_index)
        if response != []:
            keys = response.keys()
            for key in keys:
                data_points = list(response.get_points(tags=key[1]))
                data_groupby = key[1]
                message = process_metrics(data_points, data_groupby, query_index)
                message_formatted = '\n'.join(message) + '\n'
                print(message_formatted)
                send_metrics_graphite(message_formatted)
        else:
            print(f'No hits for query: {query}')
            metric_count -= 1
    print(f'Metrics sent for: {str(metric_count)} queries')