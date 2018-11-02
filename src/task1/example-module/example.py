import json
import sys

command_line_args = sys.argv
print("writing data to" + command_line_args[1])

data = object()
data["test"] = "Hello World"

with open(command_line_args[1], 'w') as outfile:
    json.dump(data, outfile)
