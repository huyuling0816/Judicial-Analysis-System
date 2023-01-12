# Explanatory Document on Judicial Data Analysis

[TOC]

## 1 Code file introduction

### 1.1 Tool version

| Python        | **3.6**     |
| ------------- | ----------- |
| **Django**    | **3.2.10**  |
| **Gensim**    | **4.1.2**   |
| **jieba**     | **0.42.1**  |
| **pyltp**     | **0.2.1**   |
| **pyperclip** | **1.8.2**   |
| **PyAutoGUI** | **0.9.53**  |
| **selenium**  | **3.141.0** |

### 1.2 Project structure

```python
djangoProject1
│  .gitignore.txt
│  chromedriver.exe
│  crf_learn.exe
│  database.db		   #database
│  crf_test.exe        #crf test method
│  database_process.py #database processing
│  feature.py          #crf extraction of feature elements
│  get_data.py         #crf main method
│  libcrfpp.dll
│  ltp_true.py         #word segmentation
│  model               #model file
│  output1             #trainint file
│  result              #training result
│  template01          #crf model file
│  manage.py
│  utils.p
│  views.py
│  __init__.py
│
├─.idea
│
├─__pycache__
│
├─APP1					#crawler
│
├─APP2					#word segmentation
│
├─APP3					#save annotation
│
├─APP4					#similar cases
│
├─appHTML				#frontend
│
├─djangoProject1		#main path
│
├─HTML					#frontend code
│
├─Lib					
│
├─Scripts
│
├─templates
│
├─word2evc				 #toolkit
│
├─分词					#toolkit
│
└─特征提取				   #toolkit
```

### 1.3 Overall framework

This project uses Django as the Web framework to assign url paths for APP1-APP4 and appHTML (front page) to realize the front end data transfer. To run, you need to start the Django project, which defaults to http://127.0.0.1:8000/.

```python
│  asgi.py
│  settings.py
│  urls.py
│  wsgi.py
│  __init__.py
│
└─__pycache__
```

urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('APP1/', include('APP1.urls')),   
    path('APP2/', include('APP2.urls')),    
    path('APP3/', include('APP3.urls')),    
    path('APP4/', include('APP4.urls')),    
    path('appHTML/', include('appHTML.urls')),  
]
```

#### 1.3.1 Backend implementation

APP3 (function saves case annotations) is an example, and other subprojects are similar.

```python
APP3
│  admin.py
│  apps.py
│  models.py
│  tests.py
│  urls.py    #the url of APP3
│  views.py   #View functions that accept and respond to requests and perform appropriate functions
│  __init__.py
│
├─migrations
│      __init__.py
│
└─__pycache__
```

urls.py

```python
from django.urls import path
from . import views

urlpatterns=[
    path('', views.fun)
]
```

views.py

```python
from django.http import JsonResponse
import json
import os

def fun(request):
    #save the annotations to a local Json file
    return JsonResponse({"path": path})
```

When the corresponding event is triggered on the front end (path: http://localhost:8000/appHTML/), it sends a data transfer request to http://localhost:8000/APP3/时, executes the content in the fun function, returns the path of the folder to the front end, and then the front end displays it on the page.

#### 1.3.2 Frontend implementation

```javascript
$.ajax({
    url: 'http://localhost:8000/APP3/',
    type: 'post',
    data: JSON.stringify($(jsonLabel)),
    dataType: 'json',
    contentType: 'application/json',
    success: function (data){
        alert("保存成功！文件已保存至"+data.path);
    },
    error: function () {
        alert("error");
    }
})
```

Here using Ajax asynchronous request, front and back-end interaction does not need to refresh the page. The code uses Jquery, it is neat and beautiful.



### 1.4 Introduction to the functionalities

#### 1.4.1 Crawler tools (APP1)

##### Function

Get the front-end page to pass time, keywords, and quantity, establish the connection with database, if there are enough number of cases in the database, take out the cases from the database and save them to local, if the number of instruments in the database is not enough, then automatically download them from the instruments network to the database and save them to local. The crf feature elements are extracted when the case instruments are put into the database, and the vectors, subword results and feature elements are calculated and stored in the database to provide reference for finding similar cases in the subsequent process.

##### Key Codes

feature.py

```python
from 特征提取 import utils

def remove_duplicate_elements(l):	# Removes duplicate elements from a list while keeping the relative order unchanged

def func(file_name):	# Combine words that are elements of the same event
    
def get_patterns_from_dict(event_elements):		#Convert the extracted event elements into features
    
def feature(filename):		#Pass in the file and return the feature elements
    
```

views.py

```python
def fun(request):	#Front and back-end interaction
    
def databaseEntry(path,word):	#Database processing
    
def Rep(startTime,endTime,num,word):
    # Pass in the parameters and create a subfolder to store the download data
    
    connection = sqlite3.connect('D:\\DATA SCIENCE\\djangoProject1\\database.db')  #Creating a connection to the database
    cur = connection.cursor()	#Create a cursor
    
    if length>=num:		# If there are enough instruments in the database, then they can be taken directly from the database and saved locally
        for i in range(0,num):
            title = titles[i][0] + '.txt'
            content = contents[i][0]
            thisPath = os.path.join(filename,title)
            file = open(thisPath,'w')
            file.write(content)
    else:	# Insufficient number of instruments in the database, download directly from the instruments website
        download(startTime,endTime,num,word)
        sleep(15)
        fileProcess('D:\数据科学爬取案件\\',filename,word)
```

#### 1.4.2 Participle method(APP2)

##### Function

Receive the case content from the front-end, use a variety of word separation methods for word annotation and feature element extraction, and return the results to the front-end.

##### Key Codes

views.py

```python
def fun(request):	
    
    jsonDict = nlp_method.cut(text)
    dict_feature, pattern = get_data.word_process_text(text)
    result_dict = {					#type: nested dictionaries
        "cut": jsonDict,			#Participle annotation
        "feature": dict_feature		#Characteristic elements
    }
    return JsonResponse(result_dict)
```

nlp_method.py

```python
def cut(content):     #Total participle method
    
def ltp_cut(content):	#Chinese participle
def ltp_pos(words):		#word marking
def dict_wordpos(words,postags):		#Generate dictionaries of participles and lexemes
def delete_POS(words,postags,list):		#Delete fixed-word words in the dictionary
def select_POS(words,postags,list):		#Screening for words that develop wordiness
	
def find_all(list,dict):					#Find all words with the specified attributes
def find_continuous(list,words,postags):	#Find consecutive specified words words
def remove_repeat(continuous_list):			#Remove repetitive words

def ltp_net(words,postags):			#Named Entity Identification
def dict_wordnet(words,postags):	#Generate a named entity dictionary
def get_net(list,words,postags):	#Entity identification of certain specific properties
def stopwords():					#Add to deactivation thesaurus
def self_dic():						#Add custom dictionaries
def jieba_exact(content, filepath3):	# jieba participle exact mode
def jieba_pos(content):					# jieba lexical annotation
def tfidf(content, topK, withWeight, list):			# Keyword extraction based on tfidf algorithm
def textrank(content, topK, withWeight, list):		# Keyword extraction based on textrank algorithm
def get_pos(content, pos):							# Get the participle of the corresponding attribute
```

#### 1.4.3 Marking preservation(APP3)

That is, APP3, which is used as an example in the front and back-end interaction, is not repeated here.

#### 1.4.4 Similarity analysis(APP4)

##### Function

Accept the keywords and text content from the front-end, calculate the vector, compare it with the vector of related cases in the database, and return the case with the highest similarity from the database to the front-end.

##### Key codes

views.py

```python
def find_max(searchword,text):		# Find the case with the greatest similarity
    """
    :param searchword（i.e. the search keyword entered by the user when crawling
           text（The front end passes over paperwork that needs to find similar cases）
    :return: Returns a list where the 0th element is the title and the 1st element is the body content
    """
    # Iterate through the database to get the vector for each case
    # Use vector--similarity method to calculate the maximum value
    # Take out the corresponding case
```

#### 1.4.5 Frontend pages(appHTML)

```python
HTML
│  htmlfile.html	#Frontend code files
```

##### Function

html+CSS+JavaScript. Users send requests and submit data in this page. Show the result of word separation, similar cases.

##### Key codes

htmlfile.html

```html
<script src={% static 'Jquery/jquery-3.3.0.min.js' %}></script>		<!--Introducing Jqurey files-->
<script>
	function change(temp)			
	function change_extra(temp)		//Toggle bar switch
	function FileWord(files)		//Display the contents of the uploaded file in a text box
	$(document).ready(function ())		//Bind the listening events after the page is loaded to achieve front and back-end interaction
</script>	
```



## 2 Cautions

### 2.1 Version Compatibility

It is recommended that all tool versions are the same as those listed in the code file introduction, and that you do not use newer versions of tools, which are prone to compatibility problems. All imported packages should be imported into the virtual environment where the project is located.

### 2.2 File Directory

Project content is more, file references, method calls are rich, static folder content is very important, the description of all the directory only select the more critical content to display.

### 2.3 Local Address

The project is written to run at D:\DATA SCIENCE\djangoProject1, the path of some of the tools involved in the run, in addition, the crawler tool to get the case is located in D:\Data Science Crawl Case, the case annotation saved at D:\Data Science Crawl Case\Case Annotation folder, it is recommended to create the same folder when running or make changes to the corresponding address, otherwise errors may occur.

### 2.4 Network lag

Due to the lag in the network of the magistrate's office, the crawler tool may have a long waiting event when downloading documents, or even crawl failure, etc. Please wait patiently, or click on the front end to run the program again when the network is clear.

### 2.5 Removed files

Some data and model files are not uploaded due to the size limitation of github repository. Please contact me if you need them.



## 3 Copyright Notice

This project is only for Nanjing University Data Science Big Assignment submission, not for any commercial use.