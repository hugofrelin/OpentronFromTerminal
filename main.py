import requests
import time
import os
import argparse
import pprint
from icmplib import multiping

def upload_protocol(robot_ip, filename):

    print(open(filename, 'rb'))
    response = requests.post(
        url=f"http://{robot_ip}:31950/protocols",
        headers={"Opentrons-Version": "2"},
        files=[("protocolFile", open(filename, 'rb')),]
    )

    protocol_id_dictionary = {
        "protocol_id": response.json()['data']['id'],
    }

    return protocol_id_dictionary


def create_session(robot_ip, protocol_id):
    response = requests.post(
        url=f"http://{robot_ip}:31950/sessions",
        headers={"Opentrons-Version": "2"},
        json={
            "data": {
                "sessionType": "protocol",
                "createParams": {
                    "protocolId": protocol_id
                }
            }
        }
    )

    session_id_dictionary = {
        "session_id": response.json()['data']['id']
    }

    return session_id_dictionary



def run(robot_ip, session_id):
    while True:
        # Sleep for 1/2 a second. It does this to make sure the protocol is uploaded
        # before it runs the session
        time.sleep(.5)

        response = requests.get(
            url=f"http://{robot_ip}:31950/sessions/{session_id}",
            headers={"Opentrons-Version": "2"},
        )

        current_state = response.json()['data']['details']['currentState']
        if current_state == 'loaded':
            break
        elif current_state == 'error':
            raise RuntimeError(f"Error encountered {response.json()}")

    # Send a command to begin a protocol run
    response = requests.post(
        url=f"http://{robot_ip}:31950/sessions/{session_id}/commands/execute",
        headers={"Opentrons-Version": "2"},
        json={"data": {"command": "protocol.startRun", "data": {}}}
    )

    response_dictionary = {
        "response":str(response)
    }
    return response_dictionary


def delete_session(robot_ip, session_id):
    response = requests.delete(
        url=f"http://{robot_ip}:31950/sessions/{session_id}",
        headers={"Opentrons-Version": "2"},
    )

    response_dictionary = {
        "response":str(response)
    }

    return response_dictionary


def pause(robot_ip, session_id):
    response = requests.post(
        url=f"http://{robot_ip}:31950/sessions/{session_id}/commands/execute",
        headers={"Opentrons-Version": "2"},
        json={"data": {"command": "protocol.pause", "data": {}}}
    )

    response_dictionary = {
        "response":str(response)
    }

    return response_dictionary


def resume(robot_ip, session_id):
    response = requests.post(
        url=f"http://{robot_ip}:31950/sessions/{session_id}/commands/execute",
        headers={"Opentrons-Version": "2"},
        json={"data": {"command": "protocol.resume", "data": {}}}
    )

    response_dictionary = {
        "response":str(response)
    }

    return response_dictionary

def cancel(robot_ip, session_id):
    response = requests.post(
        url=f"http://{robot_ip}:31950/sessions/{session_id}/commands/execute",
        headers={"Opentrons-Version": "2"},
        json={"data": {"command": "protocol.cancel", "data": {}}}
    )

    response_dictionary = {
        "response":str(response)
    }

    return response_dictionary

def delete_protocol(robot_ip, protocol_id):
    response = requests.delete(
        url=f"http://{robot_ip}:31950/protocols/{protocol_id}",
        headers={"Opentrons-Version": "2"},
    )

    response_dictionary = {
        "response":str(response)
    }

    return response_dictionary


def get_current_state(robot_ip, session_id):
    response = requests.get(
        url=f"http://{robot_ip}:31950/sessions/{session_id}",
        headers={"Opentrons-Version": "2"},
    )

    current_state_dictionary = {
        "current_state": response.json()['data']['details']['currentState'],
    }
    return current_state_dictionary


def get_sessions():
    return None

def scan_for_robots():
    ip_dict = {
        '192.0.2.0': 'ROBOT1',
        '192.0.2.0': 'ROBOT2',
        '192.0.2.0': 'ROBOT3',
        '192.0.2.0': 'ROBOT4',
        '192.0.2.0': 'ROBOT5'
    }
    robot_dict = {
        'ROBOT1': {'IP': '192.0.2.0', 'Available': 'unknown'},
        'ROBOT2': {'IP': '192.0.2.0', 'Available': 'unknown'},
        'ROBOT3': {'IP': '192.0.2.0', 'Available': 'unknown'},
        'ROBOT4': {'IP': '192.0.2.0', 'Available': 'unknown'},
        'ROBOT5': {'IP': '192.0.2.0', 'Available': 'unknown'}
    }
    ip_dictionary = []

    for key in robot_dict.keys():
        ip_dictionary.append(robot_dict[key]['IP'])
    hosts = multiping(ip_dictionary)

    for host in hosts:
        robot_name = ip_dict[host.address]
        if host.is_alive:
            robot_dict[robot_name]['Available'] = 'YES'
        else:
            robot_dict[robot_name]['Available'] = 'NO'

    return robot_dict

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    #Parsed variables
    parser.add_argument("--robot_ip", help = "The ip_address of the robot", type = str)
    parser.add_argument("--filename", help = "The filename of your protocol file", type = str)
    parser.add_argument("--protocol_id", help = "The protocol_id of your uploaded protocol", type = str)
    parser.add_argument("--session_id", help = "The session id of your session", type = str)

    #Parsed Functions
    parser.add_argument("--upload_protocol", help = "Uploads the protocol to the opentron", action = "store_true")
    parser.add_argument("--create_session", help = "Creates a session on the Opentron", action = "store_true")
    parser.add_argument("--run", help = "Runs the session on the opentron", action = "store_true")
    parser.add_argument("--delete_session", help = "Deletes the session", action = "store_true")
    parser.add_argument("--pause", help = "Pauses the run", action = "store_true")
    parser.add_argument("--resume", help = "Resumes the run", action = "store_true")
    parser.add_argument("--cancel", help = "Cancels the run", action = "store_true")
    parser.add_argument("--delete_protocol", help = "Deletes the protocol from the opentron", action = "store_true")
    parser.add_argument("--get_current_state", help = "Gets the current state of session", action = "store_true")
    parser.add_argument("--scan_for_robots", help = "Scans the wifi for Available robots", action = "store_true")



    args = parser.parse_args()

    #Uploading the Protocol - Works
    if(args.robot_ip and args.filename and args.upload_protocol):
        print("Uploading protcol: " + args.filename + "\nOn: " + args.robot_ip)
        protocol_id_dictionary = upload_protocol(args.robot_ip, args.filename)
        print("Protocol ID: " + protocol_id_dictionary["protocol_id"])

    #Creating the session - Works
    if(args.protocol_id and args.robot_ip and args.create_session):
        print("Session created with protocol id: " + args.protocol_id + "\nOn Robot: " + args.robot_ip)
        session_id_dictionary = create_session(args.robot_ip, args.protocol_id)
        print("The session ID is:  " + session_id_dictionary["session_id"])

    #Running the session - Works
    if(args.robot_ip and args.session_id and args.run):
        response_dictionary = run(args.robot_ip, args.session_id)
        print("Run initiated with response: " + response_dictionary["response"])

    #Deleting the session - Works
    if(args.robot_ip and args.session_id and args.delete_session):
        response_dictionary = delete_session(args.robot_ip, args.session_id)
        print("Session was deleted with response: " + response_dictionary["response"])

    #Deleting the protocol - Works
    if(args.robot_ip and args.protocol_id and args.delete_protocol):
        response_dictionary = delete_protocol(args.robot_ip, args.protocol_id)
        print("Protocol was deleted with response: " + response_dictionary["response"])

    #Pausing the run - Works
    if(args.robot_ip and args.session_id and args.pause):
        response_dictionary = pause(args.robot_ip, args.session_id)
        print("Protocol was paused with response: " +  response_dictionary["response"])

    #Resuming the run - Works
    if(args.robot_ip and args.session_id and args.resume):
        response_dictionary = resume(args.robot_ip, args.session_id)
        print("Protocol was resumed with response: " + response_dictionary["response"])

    #Canceling the run - Works
    if(args.robot_ip and args.session_id and args.cancel):
        response_dictionary = cancel(args.robot_ip, args.session_id)
        print("Protocol was canceled with response: " + response_dictionary["response"])

    #Getting the current state of the session - Works
    if(args.robot_ip and args.session_id and args.get_current_state):
        state_dict = get_current_state(args.robot_ip, args.session_id)
        print("The current state of session is: " + state_dict["current_state"])

    #Scanning Wi-Fi for robots -
    if(args.scan_for_robots):
        robot_dict = scan_for_robots()
        pprint.pprint(robot_dict, width = 1)
