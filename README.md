# Controlling the Opentron Robot from the terminal
This is a python script that uses the argparse library to allows the user to control the Opentron Robot from the terminal. It can be used to develop remote control of the Opentrons, or to develop a custom made app for the robots.

## Sending the commands
Information on the argparse library can be found in the [argparse documentation]("https://docs.python.org/3/library/argparse.html").
The commands follow a general shape

The command:
```
python3 main.py --arg1 ARG1 --arg2 ARG2 --function
```

where the user passes the arguments needed for the function, and also passes the function. The order does not matter.


## Example commands

### Uploading a protocol
```
python3 main.py --robot_ip 192.0.2.0 --filename test_protocol.py  --upload_protocol
```
As of now, the protocol has to be in the same directory as the main python file

### Deleting a protocol
```
python3 main.py --robot_ip 192.0.2.0 --protocol_id test_protocol  --delete_protocol
```

### Creating a session
```
python3 main.py --robot_ip 192.0.2.0 --protocol_id test_protocol  --create_session
```

### Deleting a session
```
python3 main.py --robot_ip 192.0.2.0 --session_id 27d6390-3d1f-4b20-8d9c-25bfe925657a  --delete_session
```
