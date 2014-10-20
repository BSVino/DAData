import struct

import data_pb2

def db_store(buffer, database):
  length = struct.pack('L', len(buffer))
  database.write(length)
  database.write(buffer)

# location is an array with one entry, a silly trick so I can have pass-by-reference
def db_read_next(database):
  # First we packed a four byte length of the next buffer
  length = struct.unpack('L', database[location[0]:location[0]+struct.calcsize('L')])[0]

  # Advance the location four bytes, now location points to the buffer itself
  location[0] = location[0] + struct.calcsize('L')

  buffer = data_pb2.GameData()

  # Advance to the next location now in case there's a bad buffer
  location[0] = location[0] + length

  try:
    buffer.ParseFromString(database[location[0]-length:location[0]])
    return buffer
  except:
    return None

def db_read_next_fp(f):
  # First we packed a four byte length of the next buffer
  length = struct.unpack('L', f.read(struct.calcsize('L')))[0]

  buffer = data_pb2.GameData()

  try:
    buffer.ParseFromString(f.read(length))
    return buffer
  except:
    return None
