For smooth work, make sure that the hostname of the vantage point does not have dots in it
When running the script for the first time you can follothese steps to configure the script:
```
sudo apt update -y && apt install -y git python3 python python-rrdtool python-webpy curl
git clone 'https://version.aalto.fi/gitlab/vikbere2/pytomo'
cd pytomo
mkdir sources
curl https://raw.githubusercontent.com/EErikas/CS-E4260-Assignment-1-scripts/master/sources/part1urls.txt --output sources/part1
curl https://raw.githubusercontent.com/EErikas/CS-E4260-Assignment-1-scripts/master/sources/part2urls.txt --output sources/part2
curl https://raw.githubusercontent.com/EErikas/CS-E4260-Assignment-1-scripts/master/vantage_point/read_db.py --output read_db.py
python3 read_db.py
```
