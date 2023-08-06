import shutil
import os
import sys
import re
import subprocess
import site

from subprocess import check_call, CalledProcessError
import shutil

dulwichInstallCmd = 'pip install dulwich --global-option="--pure"'
hggitlocation = site.getsitepackages()[0] + "/hg-git"
hggitCloneCmd = "hg clone https://bitbucket.org/durin42/hg-git \"" + hggitlocation + "\""
errorCheckMessage = "Error ocurred while checking for"
errorInstallMessage = "Error occured while installing"


def checkAndInstallHggitDependencies():
    # if the hg-git folder exists, show user an error message and exit
    if checkIfHggitExists():
        print("Hg-git already exists")
        sys.exit()
    installDulwich()
    hggitClone()


def installDulwich():
    print("installing dulwich...\n")
    try:
        check_call(dulwichInstallCmd, shell=True)
    except CalledProcessError as err:
        print(errorInstallMessage, "dulwich: ", err, end="")
        print(". Please try again later")
        sys.exit()


def checkIfHggitExists():
    return os.path.isdir(site.getsitepackages()[0]+"/hg-git")


def hggitClone():
    print("installing hg-git...\n")
    try:
        check_call(hggitCloneCmd, shell=True)
    except CalledProcessError as err:
        print("Error ocurred while cloning hggit repository: ", err, end="")
        print(". Please try again later")
        sys.exit()

    modifyHgrcFile()


def modifyHgrcFile():
    with open(os.path.expanduser("~") + "/.hgrc", "r+") as f:
        # Error handling while writing to .hgrc file
        matched = False
        s = "hggit=" + hggitlocation + "/hggit"
        try:
            for line in f:
                m = re.match(re.escape(r"[extensions]"), line)
                if m is not None and m.group() == '[extensions]':
                    f.write(s)
                    matched = True
                if not matched:
                    f.seek(0, 2)
                    f.write("\n[extensions]\n"+s)
        except KeyboardInterrupt as err:
            print("Error occurred: ", err, end="")
            sys.exit()
        except IOError as err:
            print("Error occurred: ", err, end="")
            sys.exit()


def checkExtension():
    f = open(os.path.expanduser("~") + "/.hgrc", "r")
    matched = False

    for line in f:
        if "[extensions]" in line:
            matched = True

    return matched


def checkHgrc():
    # Tests that Hg-Git was added to the extensions
    f = open(os.path.expanduser("~") + "/.hgrc", "r")
    hggit = "hggit=" + hggitlocation + "/hggit"
    matched = False

    for line in f:
        if hggit in line:
            matched = True

    return matched


def checkHgClone():
    # Tests that Hg-Git is working by running hg clone on a git repository
    subprocess.run(["hg", "clone",
                    "git://github.com/schacon/hg-git.git", "test"])
    matched = os.path.exists(os.getcwd() + "/test")
    subprocess.run(["rm", "-rf", "./test"])
    return matched


def runTests():
    assert checkExtension()
    assert checkHgrc()
    assert checkHgClone()

checkAndInstallHggitDependencies()
runTests()
