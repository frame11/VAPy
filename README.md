# VAPy
###The Voat API wrapper for Python3  
---  
#####IN PROGRESS - ALL CLAIMS SUBJECT TO CHANGE - CURRENTLY NONFUNCTIONAL
---  



VAPy is intended to provide a simple, highly explicit Python interface to the Voat API.  

While VAPy makes Submission and Comment classes available to the user, they are not used as part of the VAPy internal data structure. VAPy encourages a more functional approach and consists largely of simple functions and methods designed to make is easier for users to chain those functions together in meaningful ways.

VAPy includes the Profiles component, which can be run as a stand alone application providing a simple user agent and API key management system. Profiles can be used with VAPy applications, providing secure local persistence and renewal for API tokens. Profiles uses [SQLite3](https://www.sqlite.org/) and [simplecrypt](https://github.com/andrewcooke/simple-crypt).

---
####GETTING STARTED  
To use VAPy you need a valid Voat.co login and api key.  


#####Initializing VAPy

All VAPy methods are available to any instance of VAPy with a properly initialized self.headers attribute. This attribute must contain a current Voat API key and token or communication with the Voat API will not be possible.

`vapy = VAPy.VAPy()`  
`vapy.load_profile(<profile>, <pwd>)`

*load_profile()* will retreive the profile named `<profile>` and create

VAPy can be used without the Profiles component with the set_headers() method:  
  
```vapy = Vapy.Vapy()  ```  
```vapy.set_headers(<uname>, <pwd>, <key>, <token>)```
  

After setting the headers all VAPy functions will work with or without use of Profiles.  

---
####VAPy METHODS  

#####Voat Content Dictionaries
Most VAPy functions take a voat content dicitonary as an argument. This is the Python dict corresponding to the json data of the API response to a GET query for a submission or comment. While some keys are shared between submission and comment dicts while others are unique to only one. As a result, some VAPy dictionary methods will only return data when passed a specific content dictionary type. For example, `get_submission_type()` will never return a result when passed a comment dictionary just as `get_parent_id()` will never return a result when passed a submission dictionary.

#####Dictionary Methods  
Accept Voat submission or comment dictionaries (or both) and return dictionary values. Intended for primary use with list comprehensions.  
  


&nbsp;&nbsp;&nbsp;&nbsp;`links = [vapy.get_links(d) for d in filter(is_url_submission, itr_of_victs)]`

#####Filter Methods  
Intended to be used primarily with filter(), VAPy filter methods accept voat content dictionaries and return a boolean value.  
&nbsp;&nbsp;&nbsp;&nbsp;`main_comments = filter  

&nbsp;&nbsp;&nbsp;&nbsp;`user_names = [vapy.get_author(d) for d in some_itr_of_voat_content_dicts]`  

#####Subverse Information Methods
Accept a subverse name as a string and return the appropriate subverse information.  

**get_subverse_creation_date(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns string "YYY-MM-DDDOWHH:MM:SS:MSS"  

**get_subverse_subscriber_count(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns int value of number of subverse subscribers

**get_subverse_rated_adult(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns boolean value of adult content (NSFW) flag

**get_subverse_sidebar(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns raw (html) sidebar text

