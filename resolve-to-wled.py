import socket
import struct
from xml.etree import ElementTree as ET

def connect_to_server(ip, port=20002):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ip, port))
        print("Connected to server.")
        
        while True:
            # Read the length of the incoming XML message (4 bytes)
            raw_msglen = client_socket.recv(4)
            if not raw_msglen:
                print("Server closed the connection.")
                break  # Server closed the connection
            msglen = struct.unpack(">I", raw_msglen)[0]
            
            # Read the XML message based on its length
            xml_data = client_socket.recv(msglen)
            xml_str = xml_data.decode("utf-8")
            
            # Parse the XML to extract information
            try:
                root = ET.fromstring(xml_str)
                color = root.find('color')
                if color is not None:
                    red = color.get('red')
                    green = color.get('green')
                    blue = color.get('blue')
                    print(f"Received RGB: Red={red}, Green={green}, Blue={blue}")
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")

# Example usage
connect_to_server("127.0.0.1")


