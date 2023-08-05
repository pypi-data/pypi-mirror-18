============== 
Juta_cms_icons 
============== 

New Icon Admin Field. 

Detailed documentation is in the "docs" directory. 

Quick start 
----------- 
1. pip install juta-icons 


2. Add "juta_cms_icons" to your INSTALLED_APPS setting like this:: 

INSTALLED_APPS = [ 
... 
'juta_cms_icons', 
] 

3. Start the development server and visit http://127.0.0.1:8000/admin/ 
to create a poll (you'll need the Admin app enabled). 

4. To use the Iconfield do as follows: 
*in App's models.py import the library 
from juta_cms_icons.fields import IconField 

class GoogleIcon(models.Model): 
icon_field = IconField() 

5. To Add new fonts You will need to reinstall the selected.json file with the icons library  
