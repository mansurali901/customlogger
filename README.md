# Python Custom Logger 
This custom logger is written on python 3.6 for kind of situations where we need to setup custom logging and emailing 
required for such purposes sometimes APM type tools doesn't so as admin i always comes up with bash scripts 

Usage :
Install Python3.x and then run dependencies 

```
pip3 install -r requirments.txt
```
Next is to update the Email template and recipient email addresses use below format 
Name emailaddress@domain.com

```
[root@localhost scripts]# cat mycontacts.txt 
Mansur mansurali901@gmail.com
```
Email template can be draft in 

```
root@localhost scripts]# cat message.txt 
Dear ${PERSON_NAME}, 

This is a test message. 
Have a great weekend! 

```

To run script 

```
python3 detectiveROB.py 
```
