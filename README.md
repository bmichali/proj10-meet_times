# README #
## Author: ##
 Benjamin (Ben) Michalisko , bmichali@uoregon.edu 
## Description: ##
Allows users to create possible meeting times and add them to data base
based on their google calendars. After adding first possible meetings, 
gives user a token which can be passed to others so that they can add their
free times and find overlapping timeblocks becoming the new possible meeting
times. Users who are given a token can't change primary information about the
meeting, which includes date range, beginning and end time, but are able to 
select calendars and submit their freetimes.
## Not Finished: ##
1. Finding overlapping times using database entries
2. Displaying information from database of meeting datarange/begin & end times 
for users using token
## How to run: ##
```
move credentials.ini into meetings folder
move client secrets file into meetings folder
make install
make run
Ctrl+C to quit
```

