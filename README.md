# PersistentFfuf
[![CodeQL](https://github.com/architvats96/PersistentFfuf/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/architvats96/PersistentFfuf/actions/workflows/codeql.yml)
---
## Description
This is a directory enumeration tool which uses ffuf for its working. However, it saves the output generated by a wordlist. This eases the usage of another wordlist on the same domain name as it would be parsed through all previously used wordlists and only the unique data will be provided to ffuf. By doing so, the pentester can not only save time but also obtain all the results at a centralized location. Additionally, it also detects and notifies the user if a wordlist has previously been used on the domain name.

## Working
To understand its working, allow me to take you on a deeper dive into it. This tool creates a save file for every wordlist that you've tried. This is used for every subsequent usage where the chosen wordlist is parsed through the previously used wordlists and only the uniquely identified content is provided to ffuf. This makes sure that only the essential data is passed to ffuf which results with a saving on time. Moreover, the results are combined in a CSV file for easier working.

## Requirements
python3

## Usage
The tool can be used in two ways:
- Either provide the url and wordlist while running it
```python3 PersistentFfuf.py --url <URL> --wordlist <wordlist_location>```
- or simply run the tool and provide them when asked
```python3 PersistentFfuf.py```

For Example: 
```python3 PersistentFfuf.py --url 0.0.0.0 --wordlist /usr/share/seclists/Discovery/Web-Content/common.txt```

Upon a successful execution of the program, it will generate two files as follows:
- **PersistentFfuf_Output.csv**: This consists of the output generated by ffuf in a csv format for easier viewing.
- **PersistentFfuf_SaveFile.csv**: This is the save file which tracks the wordlist usage upon a domain.

# Video Walkthrough
https://user-images.githubusercontent.com/43727792/197153752-9c72c5a3-0306-402b-a9a1-3cf87d65b2af.mp4
