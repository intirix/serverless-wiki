#!/usr/bin/python

import server
import sys

if sys.argv[1]=="upload-website":
	srv = server.Server(None)
	srv.copyWebsiteToWebpageBucket(sys.argv[2],sys.argv[3],sys.argv[4])
