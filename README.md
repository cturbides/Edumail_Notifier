# Edumail Notifier
It's a python written project created in order to learn how to use and apply my Google APIs knowledge. The project per se it's aimed at the new assignment emails placed in classroom, but it can be change for other kind of applications (wich send automatically emails).
Besides the focus on classroom, this project is just an example of what Gmail API allow us to do if use it in the right way.
To change to the notifier aimed (or needed), just change this code part of "edumail_notifier\apidata_access\gmailaccess.py", specifically the lines 106 and 111 (if it will be used for an educational application).

```python
if complete_sentence == " Nueva tarea:": #Modify this conditional sentence if its different'
.....
if snt[-1] == "(Classroom)": #Modify this conditional sentence if it is other application or if the application name in the mail it's in a different position.
```
In order to run it, execute __main__.py file (as default the application run itself continuesly, so I recommend run it as a background process using pythonw). 

## Requirements
- Have [notify.py](https://pypi.org/project/notify-py/) library installed, it can be done using [pip](https://pypi.org/project/pip/).
- Have Google APIs python package installed (it can be done using pip, or for more information go to [Developers Google's page](https://developers.google.com/gmail/api/quickstart/python)
- Follow all the steps described in [Developers Google's page](https://developers.google.com/gmail/api/quickstart/python), in order to get a credentials.json (it can has other name, but you have to change it for credentials.json) file which are going to be located on edumail_notifier\credentials folder
- And that's all :D

## Contributing
I accept all kind of Pull requests if they are substantiated. 
For major changes, please open an issue first to discuss what you would like to change.
## License
[MIT License](https://opensource.org/licenses/MIT)
# Created by Carlos or ty4115
