import rethinkdb as r
import arrow as a
import collections

class Logstah(object):
    # Store config info as class attributes.
    rethinkdb_host = None
    rethinkdb_port = None
    timestamp_format = None
    timezone = None


    # Initialize the RelogR class with config info - a running RethinkDB instance's host & port, a format for storing timestamps
    # and a timezone.
    def __init__(self, rethinkdb_host, rethinkdb_port, timestamp_format, timezone):
        self.rethinkdb_host = rethinkdb_host
        self.rethinkdb_port = rethinkdb_port
        self.timestamp_format = timestamp_format
        self.timezone = timezone
    

    # Log an incoming message with the current timestamp in the relogr_logs table in a special RethinkDB database called relogr.
    def log(self, message):
        timestamp = a.now().to(self.timezone).format(self.timestamp_format)
        r.connect(self.rethinkdb_host, self.rethinkdb_port).repl()
        payload = collections.OrderedDict()
        payload['timestamp'] = timestamp
        payload['message'] = message
        r.db('relogr').table('relogr_logs').insert(payload).run()
        return True

    
