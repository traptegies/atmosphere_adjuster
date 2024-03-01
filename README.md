# atmosphere_adjuster
A simple python script to make themesongs more enjoyable to play in the background

## What does it?
- Scan the given directory for .mp3 files
- Read the metadata (tag comments) to check if the file was already adjusted in the past
- If it needs to be adjusted, the general volume of the file will be reduced by twice the average decibel relative to full scale, a 5 seconds fade in effect and a 3 seconds fade out effect is added.
- Afterwards the comment `atmosphered` is added to the metadata

## Usage
### Necessary Adjustment
Change the following line:

`lib_dir = r'/path/to/your/mp3files/parent/dir'`

To match your parent directory of mp3 files you want to get adjusted. Be aware, the script will search through **all** subdirectories for MP3 files only.

### Automating it (tested on Debian 12)
I personally use this script with a cronjob to scan my themesong collection once a day.
If you plan on doing the same, don't forget to make the file executable:

`chmod +x /path/to/atmosphere_adjuster.py`

Then you can add the following line to your crontab (`crontab -e`) to run it everyday at 3:00 AM:

`0 3 * * * /usr/bin/python3 /path/to/atmosphere_adjuster.py`

