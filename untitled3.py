# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rQ0brS1dAxryAKUP2nlr0chAf0PydQhF
"""

!pip install stem

!apt-get install tor

import requests
import socket
import re

def resolve_onion_address(onion_address):
    """Attempts to resolve an onion address (without Tor) - generally fails."""
    try:
        response = requests.get(f"http://{onion_address}")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {onion_address}: {e}")
        return None

def extract_potential_ips_and_domains(text):
    """Extracts potential IP addresses and domain names from text."""
    ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    domain_regex = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'

    ips = re.findall(ip_regex, text)
    domains = re.findall(domain_regex, text)
    return ips, domains

def check_ip_location(ip):
    """Checks the location of an IP address using an external service."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error checking IP location: {e}")
        return None

def reverse_dns_lookup(ip):
    """Performs a reverse DNS lookup on an IP address."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return None

def analyze_onion_site(onion_address):
    """Analyzes an onion site for potential IP leaks and other information (without Tor)."""
    content = resolve_onion_address(onion_address) #Will almost always fail.
    if content:
        ips, domains = extract_potential_ips_and_domains(content)
        print(f"Potential IPs found: {ips}")
        print(f"Potential Domains found: {domains}")

        for ip in ips:
            location = check_ip_location(ip)
            if location:
                print(f"IP: {ip}, Location: {location}")
            hostname = reverse_dns_lookup(ip)
            if hostname:
                print(f"IP: {ip}, Hostname: {hostname}")

        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_regex, content)
        print(f"Potential Emails found: {emails}")

        social_media_regex = r"(facebook|twitter|instagram|telegram|discord|reddit)\.com\/[a-zA-Z0-9_.-]+"
        social_media_links = re.findall(social_media_regex, content)
        print(f"Potential Social Media Links: {social_media_links}")

# Example usage:
onion_address = "someonionsite.onion" # This will almost always fail without Tor.
analyze_onion_site(onion_address)