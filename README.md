While interning at Enertiv, I created this flask web app to run on the free pythonanywhere hosting service - that way, all my coworkers and fellow interns could use it. The purpose of this program is to convert the metadata of the equipment we track using sensors, that we retireve from our REST API, into a fully formatted mechanical schedule as a .xlsx file. The REST API originally yields the data in a JSON format, almost always upwards of 10,000 lines.  
  
This program adds value both internally and to our cutomers; most mechanical schedules are over 40-years-old, faded, sloppy, as well as out of date. This program gives the client a brand new mechanical schedule, properly formatted (rows and columns) in a .xlsx file, and it provides the same for our internal records. Additionally, since the .xslx is formatted identically to the original schedules, it lets us easily compare the metadata between the two to quickly locate any errors or updates.   
  
The website design is very simple, because it's purpose is purely functional rather than visual. A form takes input of the JSON file generated by our REST API and instantly outputs the newly generated excel file as an attachment.  
  
To try it out locally, download the repo and cd into mysite (the directory containing app.py). Run python app.py and upload one of the two try me files. You will recieve back an attachment in both your browser and the mysite directory. 
