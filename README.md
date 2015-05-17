# VAPy
###The Voat API wrapper for Python3  
---  
#####IN PROGRESS - ALL CLAIMS SUBJECT TO CHANGE
---  



VAPy is intended to provide a simple, highly explicit Python interface to the Voat API.  

While VAPy makes Submission and Comment classes available to the user, they are not used as part of the VAPy internal data structure. VAPy encourages a more functional approach and consists largely of simple functions and methods designed to make is easier for users to chain those functions together in meaningful ways.

VAPy provides the Profiles component, which when run from IDLE provides a simple user agent and API key management system. Profiles work with a VAPy application, providing secure local persistence and renewal serivces for API tokens. Profiles uses [SQLite3](https://www.sqlite.org/) and [simplecrypt](https://github.com/andrewcooke/simple-crypt).


#####Subverse Information

**get_subverse_creation_date(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns string "YYY-MM-DDDOWHH:MM:SS:MSS"  

**get_subverse_subscriber_count(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns int value of number of subverse subscribers

**get_subverse_rated_adult(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns boolean value of adult content (NSFW) flag

**get_subverse_sidebar(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns raw (html) sidebar text

**get_submission_type(**submission_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns 'url' or 'formattedContent'