import argparse
import subprocess
import importlib.util
import os
import csv

# Functions

## This function is used to create a banner
def func_banner():
    print("---------------------------------------------------------------------------------")
    banner = figlet_format("PersistentFFuF")
    print(colored(banner, "green"))
    print(colored("By Archit Vats","green"))
    print("---------------------------------------------------------------------------------")
    print("\n\n")


## This function is used to generate wordlist
def func_generate_wordlist():
    wordlist_dict = {
        1:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/Apache.fuzz.txt", "size":""},
        2:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/apache.txt", "size":""},
        3:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/big.txt", "size":""},
        4:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/common.txt", "size":""},
        5:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-big.txt", "size":""},
        6:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt", "size":""},
        7:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt", "size":""},
        8:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/dirsearch.txt", "size":""},
        9:{"name":"", "location":"/usr/share/seclists/Discovery/Web-Content/tests.txt", "size":""}
    }

    wordlist_dict_name = []
    maxlen = 0
    for i in range(1,len(wordlist_dict)+1):
        file_size = str(round(((os.path.getsize(wordlist_dict[i]["location"]))/1000),2)) + "KB"
        wordlist_dict[i]["size"] = file_size
        wordlist_dict[i]["name"] = wordlist_dict[i]["location"].split("/")[-1]
        wordlist_dict_name.append(wordlist_dict[i]["name"])
        length = len(wordlist_dict[i]["name"])
        if (length > maxlen):
            maxlen = length + 5
            
    return wordlist_dict, maxlen

## This function is used to input URL and wordlist from the user
def func_input(wordlist_dict, maxlen):
    ### Creating an augument parser for URL and wordlist
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=False)
    parser.add_argument('--wordlist', type=str, required=False)
    argument = parser.parse_args()

    ### Entering URL
    location = ""
    if (argument.url == None):                  ### If the user hasn't provided URL
        url = input("\nPlease enter the URL: ")
        location = ""
        for i in url.split("/")[1:]:
            location = location + "/" + i
        if (location == ""):
            location = "/"
        url = {                                 ### Creating a dictionary for URL consisting of domain_name and location
            "domain_name":url.split("/")[0],
            "location":location
        }
    else:                                       ### If the user has provided the URL
        for i in argument.url.split("/")[1:]:
            location = location + "/" + i
        if (location == ""):
            location = "/"
        url = {                                 ### Creating a dictionary for URL consisting of domain_name and location
            "domain_name":argument.url.split("/")[0],
            "location":location
        }

    ### Entering wordlist
    if (argument.wordlist == None):
        while True:                                 # This loop runs until a wordlist is decided
            for i in range(1,len(wordlist_dict)+1):
                print(f"%d) %-{maxlen}s %-{maxlen}s" %(i, wordlist_dict[i]["name"], wordlist_dict[i]["size"]))
            print(f"{0}) Custom wordlist")
    
            # Deciding wordlist
            wordlist_choice = input("Which wordlist would you like to use: ")
            if (wordlist_choice in wordlist_dict):
                wordlist = wordlist_dict[wordlist_choice]["location"]
                break
            elif (wordlist_choice == "0"):
                wordlist = input("Please enter the path to your custom wordlist: ").strip()
                if (os.path.exists(f"{wordlist}") == True):
                    break
                else:
                    func_printer(f"{wordlist} doesn't exist. Please try again", "error")
            else:
                func_printer("Invalid wordlist choice. Please try again.", "error")
    
    else:
        wordlist = argument.wordlist
    
    ### Creating a dictionary for wordlist consisting of name and location
    wordlist = {
        "wordlist_name":wordlist.split("/")[-1],
        "wordlist_location":wordlist
        }

    return url,wordlist
    

## This function is used to handle all of the printing in the entire program
def func_printer(text, comment):
    # The comments can be info, success or error
    if (comment == "info"):
        print(colored(f"[#] {text}","yellow"))
    elif (comment == "success"):
        print(colored(f"[+] {text}","green"))
    elif (comment == "error"):
        print(colored(f"[-] {text}","red"))
    else:
        print(colored("PRINTING ERROR","red"))

def func_check_dependency(wordlist_dict):
    # Checking Dependencies
    print("Checking Dependencies")

    ## Checking dependencies for banner
    check = ["pyfiglet", "termcolor"]
    for element in check:
        package = importlib.util.find_spec(element)
        if package is None:
            subprocess.call(f"pip install {element}".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    global figlet_format
    global colored
    from pyfiglet import figlet_format
    from termcolor import colored

    func_banner()

    ## Checking installation status of xterm
    func_printer("Checking installation status of xterm","info")
    status = subprocess.call("which xterm".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if (status == 0 ):
        func_printer("Xterm is already installed","success")
    else:
        func_printer("Installing xterm","info")
        subprocess.call("sudo apt-get update --yes".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("sudo apt-get install xterm".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status = subprocess.call("which xterm".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status == 0):
            func_printer("Xterm has been successfully installed","success")
        else:
            func_printer("Unable to install xterm. Please install it and try again", "error")
            exit()

    ## Checking installation status of ffuf
    func_printer("Checking installation status of ffuf","info")
    status = subprocess.call("which ffuf".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if (status == 0 ):
        func_printer("Ffuf is already installed","success")
    else:
        func_printer("Installing ffuf","info")
        subprocess.call("sudo apt-get update --yes".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("sudo apt-get install ffuf".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status = subprocess.call("which ffuf".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status == 0):
            func_printer("Ffuf has been successfully installed","success")
        else:
            func_printer("Unable to install ffuf. Please install it and try again", "error")
            exit()

    ## Checking installation status of wordlists
    func_printer("Checking wordlists","info")
    check = 0
    for i in wordlist_dict:
        wordlist_name = wordlist_dict[i]["name"]
        wordlist_location = wordlist_dict[i]["location"]
        if (os.path.exists(f"{wordlist_location}") == 0):
            func_printer(f"{wordlist_name} does not exist", "error")
            check = check + 1
    if (check == 0):
        func_printer("Wordlists exists", "success")
    else:
        func_printer("Wordlists do not exist", "error")
        func_printer("Installing wordlists now", "info")
        status = subprocess.call("sudo apt-get install seclists".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (status == 0):
            func_printer("Wordlists have been successfully installed", "success")
        else:
            func_printer("Unable to install wordlists. Exiting the program now", "error")
            exit()
    func_printer("All dependencies have been successfully satisfied\n", "success")


# This function runs ffuf with the provided url and wordlist
def func_ffuf(url, wordlist_location, load_save_file):
    if (load_save_file == 0):
        print("\n")
        func_printer("Running ffuf with the provided wordlist","info")
        subprocess.call(f"xterm -e ffuf -w {wordlist_location} -u http://{url}/FUZZ -t 100 -o PersistentFfuf_Output.csv -of csv -ic".split(), stderr=subprocess.DEVNULL)
        func_printer("Ffuf has successfully executed\n", "success")
        func_printer("Your output file has been generated as: PersistentFfuf_Output.csv", "success")
    elif(load_save_file == 1):
        func_printer("Running ffuf with the optimized wordlist","info")
        subprocess.call(f"xterm -e ffuf -w {wordlist_location} -u http://{url}/FUZZ -t 100 -o temp_ffuf_output.csv -of csv -ic".split(), stderr=subprocess.DEVNULL)

        fileobj_ffuf_output = open("PersistentFfuf_Output.csv","a")
        fileobj_temp_ffuf_output = open("temp_ffuf_output.csv","r")

        file_temp_ffuf_output = fileobj_temp_ffuf_output.readline()
        if (file_temp_ffuf_output == ""):
            func_printer("Ffuf has successfully executed however no new data is found\n", "success")
            return
        else:
            while True:
                file_temp_ffuf_output = fileobj_temp_ffuf_output.readline()
                if (file_temp_ffuf_output != ""):
                    fileobj_ffuf_output.write(file_temp_ffuf_output)
                else:
                    fileobj_ffuf_output.close()
                    fileobj_temp_ffuf_output.close()
                    func_printer("Ffuf has successfully executed with the save file\n", "success")
                    func_printer("Your output file has been generated as: PersistentFfuf_Output.csv", "success")
                    break
    else:
        func_printer("Unknown status of save file. Exiting now","error")
        exit()


def func_optimize_wordlist(var_jsonData, url, new_wordlist):
    var_list_of_wordlists = []
    var_optimized_wordlist = {              # var_optimized_wordlist contains the name and location of optimized wordlist
        "wordlist_name":"",                 # new_wordlist contains the name and location of new wordlist
        "wordlist_location":""
    }
    fileobj_new_wordlist = open(new_wordlist["wordlist_location"],"r")
    set_new_wordlist = {i for i in fileobj_new_wordlist.readlines()}

    for index in var_jsonData.keys():
        if (var_jsonData[index]["domain_name"] == url["domain_name"] and var_jsonData[index]["location"] == url["location"]):
            var_list_of_wordlists.append(var_jsonData[index]["wordlist_location"])

    if (not var_list_of_wordlists):           # if (var_list_of_wordlists is empty)
        fileobj_new_wordlist.close()
        return new_wordlist
    elif (new_wordlist["wordlist_location"] in var_list_of_wordlists):                     # Reuse of wordlist
        func_printer("This wordlist has already been used with this url.","info")
        var_optimized_wordlist["wordlist_name"] = ""
        var_optimized_wordlist["wordlist_location"] = ""
        return var_optimized_wordlist
    elif (new_wordlist["wordlist_location"] not in var_list_of_wordlists):               # Unique wordlist
        func_printer("An optimized wordlist is being generated", "info")
        fileobj_optimized_wordlist = open("optimized_wordlist.txt","a+")
        set_comb_wordlist = set()
        for loop in range(len(var_list_of_wordlists)):
            fileobj_old_wordlist = open(var_list_of_wordlists[loop],"r")            # This is the old wordlist
            for i in fileobj_old_wordlist.readlines():
                set_comb_wordlist.add(i)      # All words of old wordlist are stored in a list
        
        for i in set_new_wordlist:
            if (i not in set_comb_wordlist):
                fileobj_optimized_wordlist.write(i)
        
        fileobj_new_wordlist.close()
        fileobj_optimized_wordlist.close()
        fileobj_old_wordlist.close()
        var_optimized_wordlist["wordlist_name"] = "optimized_wordlist.txt"
        var_optimized_wordlist["wordlist_location"] = "optimized_wordlist.txt"
        return var_optimized_wordlist
    else:
        func_printer("Fatal error in generating the wordlist. Exiting now", "error")


# This function is used to save progress
def func_save_progress(load_save_file):
    fileobj_progress = open("PersistentFfuf_SaveFile.csv","a")
    file_data = []

    if (load_save_file == 0):
        # For appending all keys and values of url and wordlist into file_data
        for i,j in url.keys(),wordlist.keys(),url.values(),wordlist.values():
            file_data.append(i)
            file_data.append(j)

    elif (load_save_file == 1):
        # For appending keys and values of url and wordlist into file_data except the first row
        for i,j in url.values(),wordlist.values():
            file_data.append(i)
            file_data.append(j)

    elif (load_save_file == -1):
        exit()

    else:
        func_printer("Unknown state of save file","error")
        exit()

    # For writing the data in a file named save_data.csv
    for index in range(len(file_data)):
        if (index != 3 and index != 7):
            fileobj_progress.write(file_data[index] + ",")
        else:
            fileobj_progress.write(file_data[index] + "\n")
    fileobj_progress.close()
    func_printer("Your save file has been generated as: PersistentFfuf_SaveFile.csv", "success")


def func_CSV2JSON():
    var_jsonData = {}

    var_CsvFile = open("PersistentFfuf_SaveFile.csv","r")
    var_CsvReader = csv.DictReader(var_CsvFile)

    num = 1
    for rows in var_CsvReader:
        var_jsonData[num] = rows
        num = num + 1

    var_CsvFile.close()
    return var_jsonData


# This function performs a cleanup of all the temporary files created in the process
def func_cleanup():
    '''if (os.path.exists("optimized_wordlist.txt") == True):
        os.remove("optimized_wordlist.txt")'''
    if (os.path.exists("temp_ffuf_output.csv") == True):
        os.remove("temp_ffuf_output.csv")
    if (os.path.exists("temp_ffuf_output.csv") == True):
        os.remove("temp_ffuf_output.csv")





#####################################################################
# Main program begins
#####################################################################

wordlist_dict, maxlen = func_generate_wordlist()        # Wordlist is generated
func_check_dependency(wordlist_dict)                    # Dependencies are checked
url,wordlist = func_input(wordlist_dict, maxlen)        # User input is taken
            
# Deciding whether the process is running for the first time or resuming
if (os.path.exists(f"PersistentFfuf_SaveFile.csv") == True):    ## The process is resuming
    load_save_file = 1
    print("\n")
    func_printer("A previous run of the program is found and thus the process is resumed", "success")
    
    var_jsonData = func_CSV2JSON()
    var_optimized_wordlist = func_optimize_wordlist(var_jsonData, url, wordlist)
    if (var_optimized_wordlist["wordlist_location"] == ""):
        func_printer("Thus, there's no need to run ffuf again with this wordlist","info")
        func_printer("The process has been successfully completed","success")
        load_save_file = -1
    else:
        func_ffuf(url["domain_name"] + url["location"], var_optimized_wordlist["wordlist_location"], load_save_file)
    
else:                                                           ## The process is running for the first time
    load_save_file = 0
    func_ffuf(url["domain_name"] + url["location"], wordlist["wordlist_location"], load_save_file)

func_save_progress(load_save_file)                      # Progress is saved
func_cleanup()                                          # Temporary files are deleted