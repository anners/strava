# strava scripts 

daily-milage.py is a script to write out strava activites after a certain date to a csv file
I created this for a work running challenge b/c I didn't want to manually update a spreadsheet 

**This was heavily influnced by the work [Matt Ambrogi](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde)**

# Usage 
To get your client_id, client_secret and refresh_token follow the instructions [here](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde)

I used os.getenv to read the client_id, client_secret and refresh_token from environmental variables which you can set like:\
`export CLIENT_ID="XXXX"`\
`export CLIENT_SECRET="a1XXXXXX"`\
`export REFRESH_TOKEN="XXXXXXX865736"`\

Modify the code if you want to use a different start date or csv filename the defaults are:\
`2023-11-01`\
`date-distance.csv`

to run the script:\
`python3 ./daily-milage.py`