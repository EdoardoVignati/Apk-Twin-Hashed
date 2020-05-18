#!/usr/bin/env python

import sys
import hashlib
import glob
import zipfile
import ntpath
import shutil
import os
from os import path
import re


# Max apk size in byte
BUF_SIZE = 30720
regexFilter="";
apkroot="./apk/"
extractionFolder="./extracted/";


def check_regex():
	try:
		re.compile(regexFilter)
	except re.error:
		print("Regex failed")
		exit()
	print("Regex loaded: \n " + regexFilter + "\n")


# Unzip and check single file hashes
def deep_hash(apklist):
	pathFilesPerApk = []
	nameFilesPerApk = []
	result = True;
	
	try:
		shutil.rmtree(extractionFolder)
	except:
		pass
	
	os.mkdir(extractionFolder)

	# Extract and create a list of files
	for apk in apklist:
		with zipfile.ZipFile(apk, 'r') as zip_ref:
			filename = ntpath.basename(apk)
			fullpath = extractionFolder + filename
			zip_ref.extractall(fullpath)

			pathFiles = []
			nameFiles = []
			for r, d, f in os.walk(fullpath):
				for apkfile in f:
					if bool(re.match(regexFilter,apkfile)):
						pathFiles.append(os.path.join(r, apkfile))
						nameFiles.append(ntpath.basename(os.path.join(r, apkfile)))
			
			pathFilesPerApk.append(sorted(pathFiles))
			nameFilesPerApk.append(sorted(nameFiles))
	
	# Check same files
	check=nameFilesPerApk[0]
	listlen=0	
	for apkfiles in nameFilesPerApk:
		if check!=apkfiles:
			return
		listlen=len(apkfiles)
	
	# Check same hashes
	for i in range(0,listlen):
		checkmd5 = []
		checksha1 = []
		checksha256 = []
		for apkfiles in pathFilesPerApk:
			md5 = hashlib.md5()
			sha1 = hashlib.sha1()
			sha256 = hashlib.sha256()
			
			file = open(apkfiles[i],mode='r')
			fullcontent = file.read()
			file.close()
			
			md5.update(fullcontent)
			sha1.update(fullcontent)
			sha256.update(fullcontent)
			
			checkmd5.append(md5.hexdigest())
			checksha1.append(sha1.hexdigest())
			checksha256.append(sha256.hexdigest())	
			
		lmd5=len(set(checkmd5))!=1
		lsha1=len(set(checksha1))!=1
		lsha256=len(set(checksha256))!=1
		
		if lmd5 or lsha1 or lsha256:
			result = False
			break
			
	shutil.rmtree(extractionFolder)
	return result

# Load all apk in apk folder
def get_apks():
	if not path.exists(apkroot):
		print("\nPlease feed the folder '" + apkroot + "' with your apks\n")
		exit()
	apklist = glob.glob(apkroot+"*.apk")
	print("Loaded apks:")
	for apk in apklist:
		print(" " + apk)
	print("")
	return apklist

# Trivial hash of full apk
def simple_hash(apklist):

	md5results = []
	sha1results = []
	sha256results = []

	for apk in apklist:
		with open(apk, "rb") as f:
			md5 = hashlib.md5()
			sha1 = hashlib.sha1()
			sha256 = hashlib.sha256()
			while True:
				data = f.read(BUF_SIZE)
				if not data:
					break
				md5.update(data)
				sha1.update(data)
				sha256.update(data)
		
		md5results.append((apk,md5.hexdigest()))
		sha1results.append((apk,sha1.hexdigest()))
		sha256results.append((apk,sha256.hexdigest()))
	
	results = [("MD5", md5results),("SHA1", sha1results),("SHA256", sha256results)]
	
	for algo in results:
		digests = []
		for hashes in algo[1]:
			digests.append(hashes[1])
		if len(set(digests))!=1:
			return False
	return True

def main():
	global regexFilter

	print("Hello to Apk Twin-Hashed\n")

	if len(sys.argv)!=2:
		print("How to use:\n - Create the folder " + apkroot)
		print(" - Fill the folder " + apkroot + " with your apks")
		print(" - Run with $ ./apk-twin-hashed.py \"whitelist_regex\"")
		print("\n where 'whitelist_regex' is a regex to include \n only specific files from your apk list")

		exit()	
	else:
		regexFilter = sys.argv[1]
	
	print("Crypto algorithms applied: MD5, SHA1, SHA256\n")
	apklist = get_apks()

	check_regex()
	
	if simple_hash(apklist):
		print("Apks are equals!")
		exit()
	
	if deep_hash(apklist):
		print("Apks are equals!")
	else:
		print("Apks are different!")


if __name__ == '__main__':
    main()


