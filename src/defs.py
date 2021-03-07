'''
The items in each of the tuples (INFLUX_DETAILS, INFLUX_QUERY, INFLUX_QUERY_GROUPBY, GRAPHITE_TAGS) correspond to each other at a given index-number
Eg: item at INFLUX_DETAILS[0] corresponds to the items at INFLUX_QUERY[0], INFLUX_QUERY_GROUPBY[0], GRAPHITE_TAGS[0]
'''

# InfluxDB details (domain-name/IP, DB-name), different InfluxDB endpoints are supported
INFLUX_DETAILS = (
    ('influxdb.example.com', 'telegraf_db'),
    ('influxdb.example.com', 'telegraf_db')
)

# InfluxDB queries (includes time-range to query data)
INFLUX_QUERY = (
	'SELECT mean("usage_user") FROM "cpu" WHERE "server_name" =~ /^web-/ AND time > now() -1m GROUP BY time(1m), "host"',
    'SELECT mean("used_percent") FROM "mem" WHERE "server_name" =~ /^web-/ AND time > now() -1m GROUP BY time(1m), "host"'
)

# InfluxDB query groupby (used to extract values from InfluxDB query output)
INFLUX_QUERY_GROUPBY = (
    'host',
    'host'
)

# Series-name/tags to be processes in Graphite format, corresponds to InfluxDB Query defined in 'INFLUX_QUERY'
GRAPHITE_TAGS = (
    'cpu_usage.percentage;source=influx;type=metrics;host=%s %s %s',
    'mem_usage.percentage;source=influx;type=metrics;host=%s %s %s'
)