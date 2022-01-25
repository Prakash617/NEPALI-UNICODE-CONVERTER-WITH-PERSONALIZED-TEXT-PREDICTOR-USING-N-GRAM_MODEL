
s1.ipynb contains 
	OBJECTIVE: to create map.json
	-code to convert the nepali words into roman english equivalent
	-uses file sabdakosh-words.txt
	-eg. 	नेपाली- nepali
		पानी - pani
		साथी - sathi
	-creates map.json containing reverse dictionary
	i.e, { "nepali": नेपाली  ,   "pani":"पानी", ..........  }
	- contains some test cases

s2.ipynb contains
	OBJECTIVE: to convert roman eng to nepali unicode
	- hardcoded rules for converting roman english to nepali unicode
	- suggest function to get nepali unicode for given text using those rules
	- also uses previously created map.json file to get nepali unicode if available.

UI folder:
**********
main_p.py
	is python file same as the s2.ipynb

map.json
	is same file created above (copied version)

next.py
	-imports suggest function from main_p.py
	-imports pynput module
	-contain UI components using PyQt5

ui sample.png
