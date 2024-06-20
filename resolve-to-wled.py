import socket
import struct
import requests


def send_rgb_to_wled(ip, port, red, green, blue):
    # Construct the JSON payload with the RGB values
    payload = {"seg":[{"col":[[red,green,blue]]}]}
    
    # Send the JSON payload to the WLED instance
    url = f"http://{ip}:{port}/json/state"
    response = requests.put(url, json=payload)

    if response.status_code == 200:
        print("RGB values sent to WLED instance.")
        print(f"URL: {url}")
        print(f"Response: {response.text}")
    else:
        print(f"Failed to send RGB values to WLED instance. Error: {response.text}")


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
                    red = int(int(color.get('red')) * 255 / 1023)
                    green = int(int(color.get('green')) * 255 / 1023)
                    blue = int(int(color.get('blue')) * 255 / 1023)
                    print(f"Received RGB: Red={red}, Green={green}, Blue={blue}")
                    # Example usage
                    send_rgb_to_wled("192.168.69.49", 80, red, green, blue)
                    print("RGB values sent to WLED instance.")
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")

# Example usage
connect_to_server("127.0.0.1")

