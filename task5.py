import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import socket
import struct
import textwrap

def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

def parse_packet(packet):
    ip_header = packet[:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF

    iph_length = ihl * 4
    ttl = iph[5]
    protocol = iph[6]
    src_addr = socket.inet_ntoa(iph[8])
    dest_addr = socket.inet_ntoa(iph[9])

    return {
        'version': version,
        'ihl': ihl,
        'ttl': ttl,
        'protocol': protocol,
        'src_addr': src_addr,
        'dest_addr': dest_addr,
        'payload': packet[iph_length:]
    }

def start_sniffing():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sock.bind(('0.0.0.0', 0))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        while True:
            raw_data, addr = sock.recvfrom(65535)
            packet = parse_packet(raw_data)
            display_packet(packet)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_packet(packet):
    src = packet['src_addr']
    dest = packet['dest_addr']
    proto = packet['protocol']
    payload = format_multi_line('', packet['payload'].hex())
    
    packet_info = f"Source: {src}\nDestination: {dest}\nProtocol: {proto}\nPayload:\n{payload}\n\n"
    packet_display.insert(tk.END, packet_info)
    packet_display.yview(tk.END)

def start_sniffer_thread():
    sniffer_thread = threading.Thread(target=start_sniffing)
    sniffer_thread.daemon = True
    sniffer_thread.start()

# GUI setup
root = tk.Tk()
root.title("Comillas Negras - Network Packet Analyzer")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

start_button = tk.Button(frame, text="Start Sniffing", command=start_sniffer_thread)
start_button.grid(row=0, column=0, pady=10)

packet_display = scrolledtext.ScrolledText(frame, width=80, height=20)
packet_display.grid(row=1, column=0, pady=10)

root.mainloop()