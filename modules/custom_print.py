class Colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def print_error(msg):
	print(Colors.FAIL + msg + Colors.ENDC)


def print_warning(msg):
	print(Colors.WARNING + msg + Colors.ENDC)

def print_info(msg):
	print(Colors.OKCYAN + msg + Colors.ENDC)

def print_ok(msg):
	print(Colors.OKGREEN + msg + Colors.ENDC)
