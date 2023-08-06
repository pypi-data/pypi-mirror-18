class STATUS(object):
    wtf = -1          # Something went wrong
    ready = 100       # Waiting to connect or listen
    starting = 101    # Starting to bind
    listening = 102   # bound
    connecting = 200
    connected = 201
    stopping = 300
    stopped = 301


class CLIENT_TYPE(object):
    worker = 'worker'
    scheduler = 'scheduler'


# See doc/protocol.rst
PROTOCOL_VERSION = 'eMQP/1.0'

# PROTOCOL COMMANDS
DISCONNECT = "DISCONNECT"
KBYE = "KBYE"
