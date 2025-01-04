MAJOR = 4
MINOR = 6
PATCH = 0
FORK = "bad" # bad.ideas

# The VERSION.STR cannot be more than 14 total characters long.
# It gets pre-pended with "v" and postpended with "[$00]" for use in-game.
# Beta versions tack on a ".b" at the end, so you only get 12 actual characters.
# Generation will fail with
#   f4c.ff4bin.rom.RomError: Patch at 10D810 conflicts with prior patch at 10D800
# otherwise.

VERSION = (MAJOR, MINOR, PATCH, FORK)
NUMERIC_VERSION = (MAJOR, MINOR, PATCH)
VERSION_STR = f"{MAJOR}.{MINOR}.{PATCH}.{FORK}"
NUMERIC_VERSION_STR = f"{MAJOR}.{MINOR}.{PATCH}"
FORK_SOURCE_URL = ""