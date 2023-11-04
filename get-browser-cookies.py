#! /usr/bin/python

#print("Starting...")

import browser_cookie3
import json
import os
import sys


NAME = "Get Browser Cookies"
VERSION = "1.0.0"
VERSION_DATE = "30.10.2023 @ 2 am"
AUTHOR = "Sowtyy"

#print(f"Author: {AUTHOR}. Version: {VERSION}. Date: {VERSION_DATE}.\n")


def parse_args(args: list, *, acceptable_args: list, special_arg_str: str = "--"):
  args_len = len(args)
  new_args = {}

  for i in range(args_len):
    if not args[i].startswith(special_arg_str):
      continue
    arg_filtered = args[i].replace(special_arg_str, "", 1)

    new_name = None
    new_value = None

    if arg_filtered not in acceptable_args:
      continue
    new_name = arg_filtered

    i_plus = i + 1

    if i_plus < args_len:
      next_arg = args[i_plus]

      if not next_arg.startswith(special_arg_str):
        new_value = args[i_plus]

    if new_name:
      new_args[new_name] = new_value

  return new_args

def setTitle(title : str):
  title = "title " + title

  try:
    os.system(title)
  except Exception as e:
    pass

  return

def writeJson(filename : str, data):
  with open(filename, "w", encoding = "utf-8") as file:
    json.dump(data, file, indent = 2)
  
  return

def printCookies(data : dict):
  for browser in data:
    #print(f"{browser[0].upper()}{browser[1:]}:", end = "")
    print(f"{browser.upper()}:", end = "")

    #cookies = data[browser]
    domains = data[browser]

    #if cookies == {}:
    if domains == {}:
      print("  ---")
      continue
    else:
      print()

    for domain in domains:
      print(f"    {domain}:")

      cookies = domains[domain]

      for name in cookies:
        value = cookies[name]

        print(f">>      {name}: {value}")
    
    print()
  
  return

def getCookies(methods : list):
  found = {}

  for method in methods:
    try:
      found[method.__name__] = method()
    except browser_cookie3.BrowserCookieError:
      pass
    except Exception as e:
      print("-- Error trying to get browser cookies:", repr(e))

  return found

def filterCookies(data, *, names : list = [], domains : list = []):
  filtered = {}

  for browser in data:
    filtered[browser] = {}

    cookies = data[browser]

    for cookie in cookies:
      toContinue = False

      if len(domains) > 0:
        for domain in domains:
          if domain in cookie.domain:
            break
        else:
          toContinue = True
        
      if toContinue: continue
      
      if len(names) > 0:
        for name in names:
          if name in cookie.name:
            break
        else:
          toContinue = True
      
      if toContinue: continue

      if cookie.domain not in filtered[browser]:
        filtered[browser][cookie.domain] = {}

      filtered[browser][cookie.domain][cookie.name] = cookie.value

      #print(cookie.domain)

  return filtered

def main():
  setTitle(f"{NAME} {VERSION}   by {AUTHOR}   at {VERSION_DATE}")

  acceptableArgs = ["names", "domains", "filename"]
  argsDict = parse_args(sys.argv, acceptable_args = acceptableArgs)

  methods = [
    browser_cookie3.chrome,
    browser_cookie3.chromium,
    browser_cookie3.opera,
    browser_cookie3.opera_gx,
    browser_cookie3.brave,
    browser_cookie3.edge,
    browser_cookie3.vivaldi,
    browser_cookie3.firefox,
    browser_cookie3.safari
  ]
  domains = argsDict.get("domains").split(" ") if argsDict.get("domains") else []
  names = argsDict.get("names").split(" ") if argsDict.get("names") else []
  filename = argsDict.get("filename") or "cookies.json"

  print(f"Searching for: {', '.join(names)}...")
  print(f"Domains: {', '.join(domains)}.")

  cookiesRaw = getCookies(methods)
  cookies = filterCookies(cookiesRaw, names = names, domains = domains)

  print("\n")
  printCookies(cookies)

  inp = input(f"\nEnter '/s' to save cookies to {filename} file or anything else to exit: ")
  if inp == "/s":
    writeJson(filename, cookies)
  
  return

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    input(f"-- Exception in main: {repr(e)}")
