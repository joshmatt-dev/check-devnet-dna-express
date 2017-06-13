#####################################################################
#																	#
#	Module: 		checkDevNet.py			 						#
#	Author: 		Joshua Matthews 2017							#
#	Company: 		Cisco Systems									#
#	Description:	Check user workstation is prepared for 			#
#					DevNet Express DNA v2 track			 			#
#																	#
#####################################################################

#####################################################################
#						Dependancy Imports							#
#####################################################################

# Used for checking user operating system
import platform

# Used for checking Python version
import sys

# Used for interacting with OS shell
import subprocess
import os

# Used for checking network connectivity
import socket

# Used for logging
import time

# Used for parsing Spark REST API responses
import json



#####################################################################
#						Environment Settings						#
#####################################################################

# Check platform
userPlatform = platform.system()
print(userPlatform)

# Check Python Version
userPython = sys.version_info

# SPARK TOKEN
SPARK_TOKEN = ""		## Paste your Cisco Spark Token here

# GIT
GIT_REPO = "https://github.com/CiscoDevNet/devnet-express-code-samples.git"

# Logging
log_file = time.strftime("%Y%m%d%H%M%S") + "_check_devnet_log.txt"
verbose_logging = False

# Network connectivity check
REMOTE_SERVER = "pypi.python.org"
REMOTE_PORT = 443

# Remediate Action
REMEDIATION = False



#####################################################################
#						Function Definitions						#
#####################################################################

"""
Function: 		run_cmd

Description:	Used to send commands to underlying os shell.
				This will be sent as a subprocess to a secondary shell.
				Useful when os level operations are required.

Arguments:		cmd 	- command string to run in cmd

Return:			result 	- output from running the command
"""
def run_cmd(cmd):

	# Initialize result array
	result = []
	print_result = False

	# Open pipe in subprocess
	process = subprocess.Popen(cmd,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE,
								universal_newlines=True)

	# Check if verbose logging is enabled
	if verbose_logging:
		for stdout_line in iter(process.stdout.readline, ""):
			result.append(stdout_line)
			print(stdout_line)
	else:
		for line in process.stdout:
			result.append(line)
	errcode = process.returncode

	# Set print_result to True if full output to shell is desired
	if print_result:
		for line in result:
			print(line)

	# If Error code is returned, raise exception
	if errcode is not None:
		raise Exception('cmd %s failed, see above for details', cmd)
	return result





"""
Function: 		text_colour

Description:	Aussie function to paint some colour to ya strings mate!
				Uses ANSI escape sequences so not all terminals will support.
				Cheers!

Arguments:		string 	- String to colourize 
				colour	- Colour to set on string

Return:			result 	- Colourized String
"""
def text_colour(string, colour):

	# Linux with Python 2 not supported
	if userPython.major == 2:
		return string
	if userPlatform == 'Windows' and not platform.version().startswith("10"):
		return string

	# ANSI Escape Code Strings
	ansi_black = "\u001b[30m"
	ansi_red = "\u001b[31m"
	ansi_green = "\u001b[32m"
	ansi_yellow = "\u001b[33m"
	ansi_blue = "\u001b[34m"
	ansi_magenta = "\u001b[35m"
	ansi_cyan = "\u001b[36m"
	ansi_white = "\u001b[37m"
	ansi_reset = "\u001b[0m"

	# Switch based on colour
	if colour == "black":
		result = (u"" + ansi_black + string + ansi_reset) 
	elif colour == "red":
		result = (u"" + ansi_red + string + ansi_reset) 
	elif colour == "green":
		result = (u"" + ansi_green + string + ansi_reset) 
	elif colour == "yellow":
		result = (u"" + ansi_yellow + string + ansi_reset) 
	elif colour == "blue":
		result = (u"" + ansi_blue + string + ansi_reset) 
	elif colour == "magenta":
		result = (u"" + ansi_magenta + string + ansi_reset) 
	elif colour == "cyan":
		result = (u"" + ansi_cyan + string + ansi_reset) 
	elif colour == "white":
		result = (u"" + ansi_white + string + ansi_reset) 

	# Return the original string encapsulated in ANSI colour codes
	return result





"""
Function: 		check_network

Description:	Used to check network connectivity

Arguments:		remote_host - Remote host to check TCP network connectivity against
				remote_port - Remote TCP port to check network connectivity against

Return:			result 	- Boolean of whether connection was successfuly.
"""
def check_network(remote_host, remote_port):

	print(u"\tConnecting to %s on TCP port %s..." % (text_colour(remote_host,"blue"),text_colour(str(remote_port),"blue")))

	# Try-catch to open tcp session with remote host
	try:
		host = socket.gethostbyname(remote_host)
		s = socket.create_connection((host, remote_port), 2)
		print("\t%s\n" % text_colour("SUCCESS","green"))
		return True

	except:
		pass

	print("\t%s\n" % text_colour("FAIL","red"))
	return False





"""
Function: 		check_python_version

Description:	Checks that underlying OS has at least Python 3.5 installed.

Arguments:		majorRelease 	- Major Python Release i.e 2 or 3
				minorRlease		- Minor Python release
				sys_platform 	- System platform (Windows,Linux,OSX[Darwin])

Return:			result 			- Python string to run Python3 in shell
"""
def check_python_version(major_release, minor_release, sys_platform):

	# Function Variables
	py_ver = ("%d.%d" % (major_release,minor_release))
	path = ""
	py3_str = ""
	py2_str = ""
		
	# Check if user is running python 2
	if major_release == 2:

		# Check if Python3 exists in System path
		# Execute based on system platform
		if sys_platform == 'Windows':

			# Windows command sets
			path = run_cmd("echo %PATH%")
			py3_str = "Python3"
			py2_str = "Python2"
			
		elif sys_platform == 'Darwin':

			# OSX command sets
			path = run_cmd("whereis python")
			py3_str = "python3"
			py2_str = "python2"

		elif sys_platform == 'Linux':

			# Linux command sets
			path = run_cmd("whereis python")
			py3_str = "python3"
			py2_str = "python2"

		else:

			# Only Windows, OSX, and Linux supported by this script - other platforms are unsupported.
			print(u"\tYou are running %s, this is an unsupported platform.\n\tPlease run a Windows, OSX, or Linux environment.")
			return False
		
		# Check if Python 3 exists in System Path
		if py3_str in path[0]:
			
			# Adjust py3_str to match --version output
			py3_str = "Python 3."

			# Check for other common python path names (py or python3)
			response = run_cmd("py --version")
			if len(response) > 0:
				if py3_str in response[0]:		
					print(u"\tYou are running python version %s, to run %s execute \'%s\' from cmd\n" % (text_colour(py_ver,"green"), response[0].rstrip('\n'), text_colour("py","blue")))
					return "py"

			response = run_cmd("python3 --version")
			if len(response) > 0:
				if py3_str in response[0]: 
					print(u"\tYou are running python version %s, to run %s execute \'%s\' from cmd\n" % (text_colour(py_ver,"green"), response[0].rstrip('\n'), text_colour("python3","blue")))
					return "python3"

		else:

			# Python 3 not found - Check if Python2 exists in System Path
			if py2_str in path[0]:
				print(u"\tPython 2 is found in the system path, Python 3 is required...\n")

			# Provide instructions to remediate missing Python3
			print(u"\tPython 3 not found in the system path:\n")
			print(u"\t\t1. Run the Python 3 Installation exe again")
			print(u"\t\t2. Click Modify")
			print(u"\t\t3. Click Next on Optional Features page")
			print(u"\t\t4. Tick \'Add Python to environment variables\' and then click install")
			print(u"\n\tRerun this script after taking above action to verify installation\n")
			return False

	elif major_release == 3:

		# Check Python Minor release is at least .5
		if minor_release < 5:

			# Advise remediation
			print(u"\tYou are running %s release, please upgrade to at least Python 3.5" % (text_colour("Python " + py_ver,"red")))
			return False

		else:

			# User is running correct version of Python, return True
			print(u"\tYou are running %s, this satisfies the minimum requirements" % (text_colour("Python " + py_ver,"green")))

			# Execute based on system platform
			if sys_platform == 'Windows':
				return "python"
			elif sys_platform == 'Darwin':
				return "python3"
			elif sys_platform == 'Linux':
				return "python3"
			else:

				# Only Windows, OSX, and Linux supported by this script - other platforms are unsupported.
				print(u"You are running %s, this is an unsupported platform.\n\tPlease run a Windows, OSX, or Linux environment.\n")
				return False 





"""
Function: 		check_python_libraries

Description:	Takes in a list of Python library names and attempts to install whichever are missing.
				If a virtual environment is defined, libraries will be installed for that virtual environment.

Arguments:		majorRelease 	- Major Python Release i.e 2 or 3
				minorRlease		- Minor Python release
				venv_pip_str 	- String with path to pip contained in virtual environment

Return:			result 			- Boolean value (currently unused)
"""
def check_python_libraries(required_libraries, sys_platform, venv_pip_str=False):

	# Function Variables
	py3_str = "python 3."
	py2_str = "python 2."
	pip_str = ""
	response = ""

	# Check pip version
	if venv_pip_str:

		# Condition is true if running in a virtual environment
		response = run_cmd(u"%s --version" % venv_pip_str)

		# Check if response was returned from the shell
		if len(response) > 0:

			# Check if running pip for python 3 or python 2
			if py3_str in response[0]:		
				print(u"\t\'pip\' in PATH is for Python version 3.x\n")
				pip_str = venv_pip_str
			elif py2_str in response[0]:
				print(u"\t\'pip\' in PATH is for Python version 2.x\n")

	else:
		response = run_cmd("pip --version")
		if len(response) > 0:
			if py3_str in response[0]:		
				pip_str = "pip"
			elif py2_str in response[0]:
				print(u"\t\'pip\' in PATH is for Python version 2.x\n")

	if not venv_pip_str:
		response = run_cmd("pip3 --version")
		if len(response) > 0:
			if py3_str in response[0]:		
				pip_str = "pip3"
			elif py2_str in response[0]:
				print(u"\t\'pip\' in PATH is for Python version 2.x\n")

	if pip_str == "":
		print(u"\tPip installation not found...\n\tPlease install pip or add to PATH as \'pip\' or \'pip3\'.")
		print(u"\tTry running %s from terminal." % text_colour("sudo apt-get update && sudo apt-get install python3-pip","yellow"))
		return False

	# Upgrade pip installation
	if REMEDIATION:
		response = run_cmd(u"%s install --upgrade pip" % pip_str)
		print("\tChecking for pip updates...")
		if len(response) > 0:

			if "up-to-date" in response[0]:
				print(u"\tPip is already up-to-date")
				print("\t%s\n" % text_colour("SUCCESS","green"))
			elif "Successfully installed pip" in response[0]:
				print(u"\tPip updates installed successfully")
				print("\t%s\n" % text_colour("SUCCESS","green"))
			else:
				print(u"\t%s\n" % text_colour("FAIL","red"))

			for each in response:
				print(each)



	# Check library installation using pip
	response = run_cmd("%s list" % pip_str)

	if len(response) < 1:

		# Unable to find pip
		print(u"\tUnable to find pip installation")
		return False

	# Check for each package
	for library in required_libraries:

		# Install each required library by default
		install = True

		# Check whether libraries already installed
		for each in response:
			if each.startswith(library):

				# Library already exists - do not install this library
				print(u"\t%s package already installed" % text_colour(library,"blue"))
				print("\t%s\n" % text_colour("SUCCESS","green"))
				install = False
				break

		# Install missing package
		if install:
			if REMEDIATION:
				print(u"\t%s package is missing, attempting install..." % text_colour(library,"blue"))
				pip_install = run_cmd("%s install %s" % (pip_str, library))

				# Verify Successful install
				response_inner = run_cmd("%s list" % pip_str)
				install_success = False
				for each in response_inner:
					if each.startswith(library):
						install_success = True
						print("\t%s\n" % text_colour("SUCCESS","green"))
				if not install_success:
					print(u"\t%s\n" % text_colour("FAIL","red"))
					print(u"\t%s package installation was unsuccessful.\n" % library)

					# Remediation advice based on platform
					if sys_platform == 'Linux':

						# Common failure is missing openssl library
						print(u"\tTry running %s from terminal" % text_colour("sudo pip3 install virtualenv","yellow"))
						print(u"\tAlso then try running %s from terminal\n" % text_colour("sudo apt-get update && sudo apt-get install libssl-dev","yellow"))

					elif sys_platform == 'Darwin':

						# Common failure is missing xcode tools
						print(u"\tWere you prompted to install %s? This is required, try installing %s and rerun this script\n" % (text_colour("Xcode","yellow"),text_colour("Xcode","yellow")))
			else:
				print(u"\t%s package is missing." % text_colour(library,"blue"))
				print(u"\t%s\n" % text_colour("FAIL","red"))

	return True





"""
Function: 		create_virt_env

Description:	Creates a Python Virtual Environemnt

Arguments:		virt_env_name 	- Name of virtual environment (passed from batch/sh script)
				sys_platform	- Windows, Linux, OSX[Darwin]
				python_str 		- Python interpreter to run when creating virtual environment

Return:			result 			- Boolean value
"""
def create_virt_env(virt_env_name, sys_platform, python_str):

	# Function variables
	venv_script_path = ""
	venv_exists = False
	venv_success = False
	work_dir = ""
	list_contents = ""
	pwd = ""
	dir_delim = ""
	activate_dir = ""

	# Execute based on system platform
	if sys_platform == 'Windows':
		
		# Windows command sets
		list_contents = "dir"
		pwd = "cd"
		dir_delim = "\\"
		activate_dir = "Scripts"	

	elif sys_platform == 'Darwin':
		
		# OSX command sets
		list_contents = "ls"
		pwd = "pwd"
		dir_delim = "/"
		activate_dir = "bin"

	elif sys_platform == 'Linux':
		
		# Linux command sets
		list_contents = "ls"
		pwd = "pwd"
		dir_delim = "/"
		activate_dir = "bin"

	else:

		# Unsupported OS
		print(u"You are running %s, this is an unsupported platform.\n\tPlease run a Windows, OSX, or Linux environment.\n")
		return False

	# Check if current directory contains virtual environment
	result = run_cmd(list_contents)
	for entry in result:
		if str(virt_env_name) in entry:
			venv_script_path = str(virt_env_name) + dir_delim + activate_dir

	# Check if in virtual environment
	result = run_cmd(pwd)

	if len(result) > 0:

		work_dir = result[0]
		wd = result[0].split(dir_delim)
		wd_str = wd[-1]

		if str(wd_str) == str(virt_env_name):
			venv_script_path = activate_dir


	# Get Python Path
	python_path = run_cmd("%s -c \"import sys; print(sys.executable)\"" % python_str)

	# Check if virtual environment already exists
	result = run_cmd("%s %s" % (list_contents,venv_script_path))
	python_exists = False
	activate_exists = False
	pip_exists = False
	for entry in result:
		if "python" in entry:
			python_exists = True
		if "activate" in entry:
			activate_exists = True
		if "pip" in entry:
			pip_exists = True

	# Must include Python, Pip, and Activate to count as valid installation
	if python_exists and activate_exists and pip_exists:
		
		result = run_cmd("%s%spip list" % (venv_script_path,dir_delim))
		print(u"\tVirtual Environment already exists...")
		print(u"\t%s\n" % text_colour("SUCCESS","green"))
		venv_exists = True
		return str(venv_script_path) + dir_delim + "pip"

	if REMEDIATION:
		# Virtual Environment does not yet exist - need to create one
		print(u"\tCreating %s Virtual Environment..." % text_colour(virt_env_name,"blue"))
		print(u"\tPython string is %s\n" % text_colour(python_str,"cyan"))

		# Different commands for different system platforms to create virtual environment
		if sys_platform == 'Windows':
			result = run_cmd(python_str + (" -m venv %s" % virt_env_name))
		elif sys_platform == 'Darwin':
			#result = run_cmd("virtualenv %s" % virt_env_name)
			result = run_cmd(python_str + (" -m virtualenv %s" % virt_env_name))
		elif sys_platform == 'Linux':
			#result = run_cmd("virtualenv %s" % virt_env_name)
			result = run_cmd(python_str + (" -m virtualenv %s" % virt_env_name))	

		# Check if Virtual Environment installation was successful
		result = run_cmd("%s %s%s%s" % (list_contents, virt_env_name, dir_delim, activate_dir))
		python_exists = False
		activate_exists = False
		pip_exists = False
		for entry in result:
			if "python" in entry:
				python_exists = True
			if "activate" in entry:
				activate_exists = True
			if "pip" in entry:
				pip_exists = True

		# Return validation of success or failure
		if python_exists and activate_exists and pip_exists:
			venv_success = True
			print(u"\t%s\n" % text_colour("SUCCESS","green"))
			print(u"\tVirtual Environment successfully created...")
			return (u"%s%s%s%spip" % (virt_env_name,dir_delim,activate_dir,dir_delim))
		else:
			print("\tVirtual Environment creation failed...")
			return False
	else:
		# No virtual environment found
		print(u"\tVirtual Environment not found...")
		print(u"\t%s\n" % text_colour("FAIL","red"))
		print(u"%s\n" % text_colour("Will continue checking Python environment outside of Virtual Environment...","magenta"))
		time.sleep(1)





"""
Function: 		check_spark

Description:	Attempts to create a Cisco Spark room using user-supplied Spark authentication token.
				If room creation is successful, posts a message into room to verify.
				Depends on spark.py import.

Arguments:		spark_token 	- Cisco Spark REST API Authentication Token

Return:			result 			- Boolean value
"""
def check_spark(spark_token):

	try:

		# Create a new room
		print(u"\tCreating a new Spark room...")
		room_title = "Devnet Express v2 Preparation Script"
		room_id = spark.post_spark_create_room(room_title, spark_token)
		if room_id:
			print(u"\t%s\n" % text_colour("SUCCESS","green"))
		else:
			print(u"\t%s\n" % text_colour("FAIL","red"))
			return False

		# Post a message to the new room
		print(u"\tPosting message to new Spark room...")
		message = "Congratulations! Your Spark Token is working with the Cisco Spark REST APIs"
		response = spark.post_spark_message(message,room_id,spark_token)
		response_json = response.json()
		if response_json['text'] == message:
			print(u"\t%s\n" % text_colour("SUCCESS","green"))
		else:
			print(u"\t%s\n" % text_colour("FAIL","red"))
		return True

	except Exception as e:

		print(u"\t%s\n" % text_colour("FAIL","red"))
		return False




"""
Function: 		check_git

Description:	Checks if git is installed on underlying OS.
				If git is installed, will clone or pull updates for supplied repo url.

Arguments:		git_repo 		- Repository to pull
				repository_name	- Folder to clone or pull into the git repo. 
				virt_env_name 	- Virtual environment name, used to check working directory
				sys_platform 	- System Operating System (Windows, Linux, OSX[Darwin])

Return:			result 			- Boolean value
"""
def check_git(git_repo, repository_name, virt_env_name, sys_platform):

	# Function variables
	list_contents = ""
	pwd = ""
	dir_delim = ""
	work_dir = ""
	repo_name = repository_name

	# Execute based on system platform
	if sys_platform == 'Windows':
		
		# Windows command sets
		list_contents = "dir"
		pwd = "cd"
		dir_delim = "\\"

	elif sys_platform == 'Darwin':
		
		# OSX command sets
		list_contents = "ls"
		pwd = "pwd"
		dir_delim = "/"


	elif sys_platform == 'Linux':
		
		# Linux command sets
		list_contents = "ls"
		pwd = "pwd"
		dir_delim = "/"


	# Check if user has git installed
	print(u"\tChecking for git installation...")
	response = run_cmd("git --version")

	# Check if response was provided by shell
	if len(response) > 0:

		# Git should provide version information if exists
		if "git version" in response[0]:
			print(u"\t%s\n" % text_colour("SUCCESS","green"))

			if REMEDIATION:
				# Check which directory we are working in
				response = run_cmd(pwd)

				# Check if response was provided by shell
				if len(response) > 0:
					for each in response:
						if virt_env_name in each:
							work_dir = ""
						else:
							work_dir = virt_env_name + dir_delim

				# Check if Git Repository has already been pulled
				response = run_cmd(list_contents + " " + work_dir)

				# Check if response was provided by shell
				if len(response) > 0:

					repo_found = False

					for entry in response:
						if repo_name in entry:
							repo_found = True

					# Repository was found
					if repo_found:

						# Update the repo
						print(u"\tRepository found locally, attempting to pull updates...")
						response = run_cmd("git -C " + work_dir + dir_delim + repo_name + " pull")

						# Verify the update - lazy here, need to fix
						response = run_cmd(list_contents + " " + work_dir)

						# Check if response was provided by shell
						if len(response) > 0:

							repo_found = False

							for entry in response:
								if repo_name in entry:
									repo_found = True

							if repo_found:
								print(u"\t%s\n" % text_colour("SUCCESS","green"))
							else:
								print(u"\t%s\n" % text_colour("FAIL","red"))

					else:

						# Clone the repo
						print(u"\tPulling remote repository...")
						response = run_cmd("git clone " + git_repo + " " + work_dir + repo_name)

						# Verify the update - lazy here, need to fix
						response = run_cmd(list_contents + " " + work_dir)

						# Check if response was provided by shell
						if len(response) > 0:

							repo_found = False

							for entry in response:
								if repo_name in entry:
									repo_found = True

							if repo_found:
								print(u"\t%s\n" % text_colour("SUCCESS","green"))
							else:
								print(u"\t%s\n" % text_colour("FAIL","red"))

		else:

			# Git does not exist
			print(u"\t%s\n" % text_colour("FAIL","red"))

	else:

		# Git does not exist
		print(u"\t%s\n" % text_colour("FAIL","red"))

	return False




#####################################################################
#						Main Exectuion								#
#####################################################################
if __name__ == "__main__":

	# Environment Variables 
	python_str = "python"			# Used to execute python interpreter
	pip_str = "pip"
	virt_env_name = ""
	repo_name = "devnet-express-code-samples"
	if len(sys.argv) > 1:
		virt_env_name = sys.argv[1]
	if len(sys.argv) > 2 and sys.argv[2] == "-v":
		verbose_logging = True

	# Check Network Connectivity
	print(u"\nChecking Network Connectivity...\n")
	net_connected = check_network(REMOTE_SERVER, REMOTE_PORT)
	if not net_connected:
		exit()

	# Check Python Installation
	print(u"\nChecking Python installation...\n")
	python_str = check_python_version(userPython.major, userPython.minor, userPlatform)
	if python_str == False:
		exit()

	if REMEDIATION:
		# Check for Python Libraries required for Virtual Environment Installation
		print(u"\nChecking for Virtual Environment Python Library...\n")
		required_libraries = ["virtualenv","requests","wheel"]
		virt_env_installed = check_python_libraries(required_libraries, userPlatform, False)

		# Condition if pip not installed, virtual environment creation failed
		if not virt_env_installed:
			# Logging not yet implemented
			#print(u"\nLogfile name is %s" % text_colour(log_file,"blue"))
			exit()

	# Create Virtual Environment
	print(u"\nChecking for Python Virtual Environment...\n")
	
	pip_path = create_virt_env(virt_env_name, userPlatform, python_str)
	if pip_path:
		print(u"\nPIP PATH = %s\n" % text_colour(pip_path,"magenta"))

	# Check Python Libraries Installation
	required_libraries = ["wheel",
							"requests",
							"netaddr",
							"pyang",
							"ncclient",
							"cffi",
							"cryptography",
							"enum34",
							"idna",
							"ipaddress",
							"lxml",
							"netaddr",
							"paramiko",
							"pyasn1",
							"pycparser",
							"setuptools",
							"six"]
	print(u"\nChecking Python Libraries...\n")
	libraries_installed = check_python_libraries(required_libraries, userPlatform, pip_path)

	# Check Cisco Spark APIs
	if SPARK_TOKEN:
		try: 
			import spark
			print(u"\nChecking Cisco Spark...\n")
			check_spark(SPARK_TOKEN)
		except Exception as e:
			print(e)

	# Check Git installed and repository up to date
	print(u"\nChecking Git Installation and DevNet Express Repository...\n")
	git_installed = check_git(GIT_REPO, repo_name, virt_env_name, userPlatform)

	# Logging not yet implemented
	#print(u"\nLogfile name is %s" % text_colour(log_file,"blue"))
