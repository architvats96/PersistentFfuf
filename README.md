# PersistentFfuf
## Description
This is a directory enumeration tool which uses ffuf for its working. However, it saves the output generated by a wordlist. This eases the usage of another wordlist on the same domain name as it would be parsed through all previously used wordlists and only the unique data will be provided to ffuf. By doing so, the pentester can not only save time but also obtain all the results at a centralized location. Additionally, it also detects and notifies the user if a wordlist has previously been used on the domain name.

## Requirements
python3

## Usage
The tool can be used in two ways:
- Either provide the url and wordlist while running it
python3 PersistentFfuf.py --url <URL> --wordlist <wordlist_location>
- or simply run the tool and provide them when asked
python3 PersistentFfuf.py

For Example

  python3 PersistentFfuf.py --url 0.0.0.0 --wordlist /usr/share/seclists/Discovery/Web-Content/common.txt
