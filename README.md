## Apk hash checker

This is a simple tool to check whether two (or more) apk are the same or not.

To accomplish this easy task, a simple hash is done over the applications.

Anyway, this is not the classic usage. 

In fact we are interested in something more complex, for example comparing an apk from Google Play and the same built from the open source repository.

This tool basically unzip the different apks and using a provided whitelist regex, compares the filtered files with 3 different hashing algorithms: MD5, SHA1 and SHA256

### Usage

     git clone https://github.com/EdoardoVignati/Apk-Twin-Hashed
     cd ./Apk-Twin-Hashed
     mkdir ./apk

and put your apk in the ./apk directory.

Choose your preferred regex from the list and run: 
 
`./check.py "regex_here"`

### Regex list examples

     ".*\.dex"	 		#select all dex files 
     ".*"	 			#select all files
     "myownregex"	 	#build yours

