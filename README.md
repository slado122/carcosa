![[Version 0.1](https://github.com/slado122)](http://img.shields.io/badge/version-v1.2-orange.svg)
![[Python 3.6](https://github.com/slado122)](http://img.shields.io/badge/python-3.6-blue.svg)
![[GPL-3.0 License](https://github.com/slado122)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)



# carcosa
Carcosa (**Before Outset PaSsword CRacKing**) is a tool to **assist** in all the **previous process of password cracking**. By now, it's able to generate smart and powerful wordlists.   
  

The idea is inspired by **bopscrk** of R3nt0n. I don't pretend to create this all from scratch. I just changed the logic a bit, added some syntactic sugar and optimized it. Also I recoded **bopscrk** from Python 2.7 to Python 3.6. So now the program runs much faster. 


## How it works
+ You have to **provide** some **words** which will act as a **base**.
+ The tool will generate **all possible combinations** between them.
+ To generate more combinations, it will add some **common separators** (e.g. "-", "_", "."), **random numbers** and **special chars**.
+ You can enable **leet** and **case transforms** to increase your chances.
+ You can provide wordlists that you already tried against the target in order to exclude all this words from the resultant wordlist (`-x`). 
 

## Requirements
+ Python 3.6


## Usage
```

  -h, --help         show this help message and exit
  -i, --interactive  interactive mode, the script will ask you about target
  -w                 words to combine comma-separated (non-interactive mode)
  --min              min length for the words to generate (default: 4)
  --max              max length for the words to generate (default: 32)
  -c, --case         enable case transformations
  -l, --leet         enable leet transformations
  -n                 max amount of words to combine each time (default: 2)
  -x , --exclude     exclude all the words included in other wordlists
                     (several wordlists should be comma-separated)
  -o , --output      output file to save the wordlist (default: tmp.txt)


```
 

## Tips
+ Fields can be left **empty**.
+ Words have to be written **without accents**, just normal characters.
+ In the others field you can write **several words comma-separated**. *Example*: 2C,Flipper.
+ Using the **non-interactive mode**, you should provide years in the long and short way (1970,70) to get the same result than the interactive mode.
+ You have to be careful with **-n** argument. If you set a big value, it could result in **too huge wordlists**. I recommend values between 2 and 5.


## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.
