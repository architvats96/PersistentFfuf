import subprocess
import importlib.util
import os

# Functions

def check_dependency(wordlist_dict):
    # Checking Dependencies

    ## Checking installation status of gobuster
    print(colored("Checking Dependencies", "blue"))
    print(colored("\nChecking gobuster", "blue"))
    status = subprocess.call("which gobuster".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if (status == 0 ):
        print(colored("Gobuster is already installed", "green"))
    else:
        print(colored("Installing Gobuster", "blue"))
        subprocess.call("sudo apt-get update --yes".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("sudo apt-get install gobuster".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status = subprocess.call("which gobuster".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status == 0):
            print(colored("Gobuster has been successfully installed", "green"))
        else:
            print(colored("Unable to install gobuster. Please install it and try again", "red"))
            exit()


    ## Checking installation status of gowitness
    print(colored("\nChecking gowitness", "blue"))
    status = subprocess.call("which gowitness".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if (status == 0 ):
        print(colored("Gowitness is already installed", "green"))
    else:
        print(colored("Installing Gobuster", "blue"))
        status2 = status = subprocess.call("which go".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status2 != 0):
            subprocess.call("sudo apt-get install gobuster".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("export GOPATH=$HOME/go >> ~/.bashrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("export GOPATH=$HOME/go >> ~/.zshrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("export PATH=$PATH:$GOPATH/bin >> ~/.bashrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("export PATH=$PATH:$GOPATH/bin >> ~/.zshrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("source ~/.bashrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("source ~/.zshrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("go install github.com/sensepost/gowitness@latest".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status = subprocess.call("which gobuster".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status == 0):
            print(colored("Gobuster has been successfully installed", "green"))
        else:
           print(colored("Unable to install gobuster. Please install it and try again", "red"))
           exit()

    ## Checking status of wordlists
    print(colored("\nChecking wordlists", "blue"))
    check = 0
    for element in wordlist_dict:
        wordlist_dict_value = wordlist_dict[f"{element}"]
        if (os.path.exists(f"{wordlist_dict_value}") == False):
            print(colored(f"{wordlist_dict_value} does not exist"))
            check = check + 1
    if (check == 0):
        print(colored("Wordlists exists", "green"))
    else:
        print(colored("Wordlists do not exist", "blue"))
        print(colored("Installing wordlists now", "blue"))
        status = subprocess.call("sudo apt-get install seclists".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status == 0):
            print(colored("Wordlists have been successfully installed", "green"))
        else:
            print("Unable to install wordlists. Exiting the program now", "red")
            exit()
    print(colored("\nAll dependencies have been successfully satisfied", "green"))


# This function runs gobuster with the provided url and wordlist
def run_gobuster(url, wordlist):
    print(colored("\nRunning Gobuster\n", "green"))
    temp_object = open("gobuster_output.txt", "w+")
    gobuster_output_object = open("gobuster_output.txt", "a")
    subprocess.call(f"gobuster dir --url http://{url} --wordlist {wordlist} --threads 100 --extensions .php,.html,.txt --no-error --output gobuster_output.txt".split(), stderr=subprocess.DEVNULL)


# This function converts the output of gobuster to gowitness's understandable format
def file_handling(url):
    temp_file_object = open("gobuster_output.txt", "r+")
    url_file_object = open(f"{url}.txt", "a")
    # {url}.txt contains the accessible URL's of the domain

    while True:
        str = temp_file_object.readline()
        if (str == ""):
            temp_file_object.close()
            url_file_object.close()
            break
        else:
            newstr = str.split(" ")
            url_file_object.write("http://" + url + newstr[0] + "\n")


def generate_wordlist(url, wordlist):
    url_object = open(f"{url}.txt", "r")
    url_wordlist_object = open(f"{url}_wordlist.txt", "w+")
    new_wordlist_object = open("new_wordlist.txt", "w")
    wordlist_object = open(f"{wordlist}", "r")

    while True:
        str = url_object.readline()
        if (str == ""):
            url_object.close()
            break
        else:
            str = str.split(f"{url}")
            url_wordlist_object.write(str[1])

    while True:
        str = wordlist_object.readline()
        if(str == ""):
            url_wordlist_object.close()
            new_wordlist_object.close()
            wordlist_object.close()
            break
        else:
            if(str in url_wordlist_object):
                continue
            else:
                new_wordlist_object.write(str)
    
    return "new_wordlist.txt"



# This function runs gowitness with the provided url
def run_gowitness(url):
    print(colored("Running Gowitness\n", "green"))
    #subprocess.call("source ~/.zshrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #subprocess.call("source ~/.bashrc".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(f"gowitness file --file {url}.txt".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(colored(f"Generated file: {url}.txt", "green"))
    print(colored(f"Generated folder: screenshots", "green"))




# Main program begins
## Checking dependencies for banner
check = ["pyfiglet", "termcolor"]
for element in check:
    package = importlib.util.find_spec(element)
    if package is None:
        subprocess.call(f"pip install {element}".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
import pyfiglet
from termcolor import colored

## CREATING BANNER
print("---------------------------------------------------------------------------------")
banner = pyfiglet.figlet_format("GoDirEnum")
print(colored(banner, "green"))
print(colored("By Archit Vats","green"))
print("---------------------------------------------------------------------------------")
print("\n\n")

wordlist = ""
wordlist_dict = {"1":"/usr/share/seclists/Discovery/Web-Content/Apache.fuzz.txt",
"2":"/usr/share/seclists/Discovery/Web-Content/apache.txt",
"3":"/usr/share/seclists/Discovery/Web-Content/big.txt",
"4":"/usr/share/seclists/Discovery/Web-Content/common.txt",
"5":"/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-big.txt",
"6":"/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
"7":"/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt",
"8":"/usr/share/seclists/Discovery/Web-Content/dirsearch.txt",
"9":"/usr/share/seclists/Discovery/Web-Content/tests.txt"}

check_dependency(wordlist_dict)

url = input("\nPlease enter the URL: ")

while True:
    while True:
        print("\n1) Apache.fuzz.txt")
        print("2) apache.txt")
        print("3) big.txt")
        print("4) common.txt")
        print("5) directory-list-2.3-big.txt")
        print("6) directory-list-2.3-medium.txt")
        print("7) directory-list-2.3-small.txt")
        print("8) dirsearch.txt")
        print("9) tests.txt")
        print("0) Custom Wordlist")


        # Deciding wordlist
        wordlist_choice = input("Which wordlist would you like to use: ")
        if (wordlist_choice in wordlist_dict):
            wordlist = wordlist_dict[f"{wordlist_choice}"]
            break
        elif (wordlist_choice == "0"):
            wordlist = input("Please enter the path to your custom wordlist: ").strip()
            if (os.path.exists(f"{wordlist}") == True):
                break
            else:
                print(colored(f"\n{wordlist} doesn't exist. Please try again", "red"))
        else:
            print(colored("\nInvalid wordlist choice. Please try again.", "red"))
            
    # Deciding whether the process is running for the first time or resuming
    if (os.path.exists(f"{url}.txt") == True):               # The process is resuming
        print(colored("Resuming process", "green"))
        wordlist = generate_wordlist(url, wordlist)
                                                       # The process is running for the first time
        

    run_gobuster(url, wordlist)
    file_handling(url)
    #run_gowitness(url)

    # Cleanup
    os.remove("gobuster_output.txt")
    #os.remove("gowitness.sqlite3")
    if (os.path.exists(f"{url}_wordlist.txt") == True):
        os.remove(f"{url}_wordlist.txt")
    if (os.path.exists("new_wordlist.txt") == True):
        os.remove("new_wordlist.txt")

    while True:
        choice = input("Would you like to combine the results with another directory enumeration (y/n): ")
        if (choice == "y"):
            break
        elif (choice == "n"):
            print(colored("\nThe program has been successfully executed. Exiting now", "green"))
            exit()
        else:
            print("\nUnknown choice. Please try again")
