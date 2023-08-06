#!/usr/bin/env python

from __future__ import print_function
from colorama import *

init(autoreset=True)


################################################################################
results = {
    "total": 0,
    "bad": 0
}

# report
# NONE -> NONE
# produce pass or fail result
def reportResult():
    total = results["total"]
    bad = results["bad"]
    passed = total - bad
    if (passed <= 1 and total <= 1):
        print(Fore.LIGHTWHITE_EX + "Of " + str(total) + " tests run, " + str(bad) +
              " failed, and " + str(passed) + " passed.")
    if (passed <= 1 and total <= 1):
        print(Fore.YELLOW + "Of " + str(total) + " tests run, " + Fore.RED + str(bad) +
              " failed, " + Fore.GREEN + "and " + str(passed) + " passed.")
    else:
        print(Fore.GREEN + "Of " + str(total) + " tests, " + Fore.RED + str(bad) +
              " failed, " + Fore.GREEN + str(passed) + " passed.")
    print(Style.RESET_ALL)


# checkExpect
# object param object string -> NONE
# produce pass or fail when the input function under test is invoked using
# param and expected value
# param can be of any data type
# expected value can be of any data type
def checkExpect(f, a, expected, name=None):
    result = f(a)
    if (name is not None):
        print(Fore.WHITE + "> for unit test: " + name)
    else:
        print(Fore.WHITE + "> for unit test: " + "unknown description test")

    if (result != expected):
        print("test: " + Fore.RED + "failed")
        print(Fore.RED + "Expected " + str(expected) + ", but was " + str(result))
        print("info: " + Fore.LIGHTYELLOW_EX + "Algorithm design is not well formed!")
        print("")
        print(Style.RESET_ALL)
        results['bad'] += 1
        results['total'] += 1
    else:
        print("test: " + Fore.GREEN + "passed")
        print("Function: " + f(a) + " consumed the following argument(s) " + str(a) +
              ", and produced " + str(result) + ", which matches " + str(expected) + " the expected result.")
        print("info: " + Fore.LIGHTBLUE_EX + "Algorithm is well formed!")
        print("")
        print(Style.RESET_ALL)
        results['total'] += 1

    reportResult()

