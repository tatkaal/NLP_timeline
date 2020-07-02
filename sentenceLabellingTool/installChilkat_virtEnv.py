import sys, site, shutil, os, platform

try:
    USER_BASE
except NameError:
    USER_BASE = None

try:
    USER_SITE
except NameError:
    USER_SITE = None

try:
    PREFIXES
except NameError:
    PREFIXES = ["/usr"]


if os.path.exists("2.6"):
    print("----")
    print(sys.path)
    print("---- Python 2.6 requires a manual install.")
    print("---- To install the Chilkat module, copy chilkat.py and _chilkat.so to the Python 2.6 site packages directory.")
    print("---- One of the above listed directories is the site-packages directory.")
    exit()


# Copy of sysconfig._getuserbase()

def _getuserbase():
    env_base = os.environ.get("PYTHONUSERBASE", None)
    if env_base:
        return env_base

    def joinuser(*args):
        return os.path.expanduser(os.path.join(*args))

    if os.name == "nt":
        base = os.environ.get("APPDATA") or "~"
        return joinuser(base, "Python")

    if sys.platform == "darwin" and sys._framework:
        return joinuser("~", "Library", sys._framework,
                        "%d.%d" % sys.version_info[:2])

    print("_getuserbase result: " +joinuser("~", ".local"))
	
    return joinuser("~", ".local")


def getuserbase():
    """Returns the `user base` directory path.
    The `user base` directory can be used to store data. If the global
    variable ``USER_BASE`` is not initialized yet, this function will also set
    it.
    """
    global USER_BASE
    if USER_BASE is None:
        USER_BASE = _getuserbase()
    return USER_BASE

# Same to sysconfig.get_path('purelib', os.name+'_user')
def _get_path(userbase):
    version = sys.version_info

    if os.name == 'nt':
        return userbase + '\\Python' + str(version[0]) + str(version[1]) + '\\site-packages'

    if sys.platform == 'darwin' and sys._framework:
        return userbase + '/lib/python/site-packages'

    return userbase + '/lib/python' + str(version[0]) + "." + str(version[1]) + '/site-packages'


def getusersitepackages():
    """Returns the user-specific site-packages directory path.

    If the global variable ``USER_SITE`` is not initialized yet, this
    function will also set it.
    """
    global USER_SITE
    userbase = getuserbase() # this will also set USER_BASE

    if USER_SITE is None:
        USER_SITE = _get_path(userbase)

    return USER_SITE



def getsitepackages(prefixes=None):
    """Returns a list containing all global site-packages directories.
    For each directory present in ``prefixes`` (or the global ``PREFIXES``),
    this function will find its `site-packages` subdirectory depending on the
    system environment, and will return a list of full paths.
    """
    sitepackages = []
    seen = set()

    if prefixes is None:
        prefixes = PREFIXES

    for prefix in prefixes:
        if not prefix or prefix in seen:
            continue
        seen.add(prefix)

        if os.sep == '/':
            sitepackages.append(os.path.join(prefix, "lib",
                                        "python%d.%d" % sys.version_info[:2],
                                        "site-packages"))
        else:
            sitepackages.append(prefix)
            sitepackages.append(os.path.join(prefix, "lib", "site-packages"))

    return sitepackages

# make sure we are installing Chilkat for the correct
# Python version, the correct architecture (32-bit/64-bit/...),
# and the correct operating system (Linux, Windows, ...).
pyMajorVersion = sys.version_info.major
pyMinorVersion = sys.version_info.minor
pyVersion = str(pyMajorVersion) + "." + str(pyMinorVersion)
print("This Python version " + pyVersion)

print("os.name: " + os.name)
print("site.PREFIXES: ")
for prefix in site.PREFIXES:
    print(prefix)
print("----")

# Make sure this Chilkat download is for the correct Python version.
if not os.path.exists(pyVersion):
    print("This Python version does not match the downloaded Chilkat module.\n")
    exit()

# system can be Linux, Darwin, Windows, SunOS
mySystem = platform.system()
print("This system: " + mySystem)

# machine can be x86_64, i686, i386, AMD64, sun4u, ia64, ppc64, armv6l
# sun4u is a SPARC, ia64 is Itanium, ppc64 is PowerPC
myMachine = platform.machine()
print("This processor: " + myMachine)

# coalesce all ARM architectures into "arm"
if "arm" in myMachine:
    myMachine = "arm"

if myMachine == "AMD64":
    myMachine = "x86_64"

if myMachine == "amd64":
    myMachine = "x86_64"

if myMachine == "i386":
    myMachine = "i686"

# If this is a 64-bit Windows machine, skip the architecture check because
# 32-bit Python could be used.
skipArchCheck = False
if (mySystem == "Windows") and (myMachine == "x86_64"):
    skipArchCheck = True
if (mySystem == "SunOS"):
	skipArchCheck = True
	
# Make sure this Chilkat download is for the correct processor architecture
if not skipArchCheck:
    if not os.path.exists(myMachine):
        print("This processor architecture does not match the downloaded Chilkat module.\n")
        exit()

# Make sure this Chilkat download is for the correct operating system
if not os.path.exists(mySystem):
    print("This operating system does not match the downloaded Chilkat module.\n")
    exit()


bGlobalInstall = False

if len(sys.argv) > 1:
    opt = sys.argv[1]
    if opt == '-g':
        bGlobalInstall = True
        print("Installing globally...\n")


if bGlobalInstall:
    spList = getsitepackages()
    print(spList)
    spDir = spList[0]
    if not "site-packages" in spDir:
        # prefer the first directory having "site-packages" in the name.
        for d in spList:
            if "site-packages" in d:
                spDir = d
                break

else:
    spDir = getusersitepackages()

print("Installing to site-packages directory: " + spDir)

# if the spDir does not exist, create it.
if not os.path.exists(spDir):
    print("creating directory " + spDir)
    os.makedirs(spDir)

print("copying chilkat.py to " + spDir)
shutil.copy("chilkat.py",spDir)

if mySystem == "Windows":
    print("copying _chilkat.pyd to " + spDir)
    shutil.copy("_chilkat.pyd",spDir)
else:
    print("copying _chilkat.so to " + spDir)
    shutil.copy("_chilkat.so",spDir)

print("The Chilkat Python module is ready to be used.")
print("Success.")




