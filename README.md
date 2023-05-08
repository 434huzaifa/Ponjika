# Ponjika
Ponjika can store any information in the form of a playlist. And help users to organize information. Websites will use API to collect information for anime, movies, and books. without these three categories, people can insert custom items. and make custom categories. every item will have a description, link, and icon.

[Project Presentation Video](https://youtu.be/c-bvn4PxIeY)

## Prerequisite
>flask-login

>flask-mongoengine

>requests

>flask-uploads

>MongoDB

>Jikanpy

# MUST DO THIS:
The version we used of flask_uploads was not updated thats why we have to do this. 
1. Go to this director `C:\Users\%USER%\AppData\Local\Programs\Python\Python310\Lib\site-packages\flask_uploads.py`
2. open flask_uploads.py
3. find from werkzeug. import secure_filename,FileStorage
4. replace the line with 
                        from werkzeug.utils import secure_filename 
                        from werkzeug.datastructures import  FileStorage
 # How to Run
 1. Download The Repo then run main.py
 2. Make sure your cmd run location same as the main.py location
 3. See __init__.py to change database settings

![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(749).png)

![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(750).png)
![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(751).png)

![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(752).png)

![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(753).png)
![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(754).png)
![alt text](https://github.com/434huzaifa/Ponjika/blob/master/Screenshots/Screenshot%20(755).png)

## Feature
1. Create user account
2. Login to user account
3. Create a category
   - Category name
   - Category detail
4. Add item to category
   - Item name
   - Item icon
   - Item detail
5. Delete /edit category
6. Delete/edit item
7. Search an item
8. Logout 



