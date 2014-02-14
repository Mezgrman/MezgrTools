#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2013 Julian Metzler

"""
Script to scan ports on IP subnets
"""

import argparse
import nmap
import requests

from lxml import etree

def main():
	parser = argparse.ArgumentParser(description = "A tool to scan IP subnets for open ports")
	parser.add_argument('-s', '--subnet', required = True, type = str, help = "The subnet to scan, e.g. 1.2.3.0/24")
	parser.add_argument('-p', '--port', required = True, type = int, default = 80, help = "The port to scan")
	parser.add_argument('-v', '--verbose', action = 'store_true', help = "Show extra details, e.g. HTML Title")
	args = parser.parse_args()
	
	scanner = nmap.PortScanner()
	scanner.scan(args.subnet, str(args.port), arguments = '-n')
	hosts = scanner.all_hosts()
	
	for host in hosts:
		try:
			if scanner[host]['tcp'][args.port]['state'] != 'open':
				continue
		except:
			continue
		
		details = scanner[host].tcp(args.port)
		
		if args.verbose:
			if args.port in [80, 443]:
				scheme = "https://" if args.port == 443 else "http://"
				try:
					http_response = requests.get(scheme + host)
					tree = etree.HTML(http_response.text)
				except:
					title = None
				else:
					title_nodes = tree.xpath('/html/head/title')
					if title_nodes:
						title = title_nodes[0].text
					else:
						title = None
				
				if title:
					print "%s%s/ - %s (Product: %s)" % (scheme, host, title, details['product'])
				else:
					print "%s%s/ (Product: %s)" % (scheme, host, details['product'])
			else:
				print "%s - %s" % (host, details['product'])

if __name__ == "__main__":
	main()