# Amazon Detail Grabber

This python script grabs the details of all the items of a particular product and stores in a file in json format.<br/>
It grabs product ID, title, price, url, and seller
 ```
 Note: This tracker specfically designed for amazon.in so, may or may not work for other urls 
```
## Usage
After forking and cloning the repo in your machine, just run the command
```
pip install -r req.txt
```
It simply installs all the required packages in your device

You can change the searched item and price filter in amazon_config.py file to search for the according to your requirement\
You can remove comment in the set_headless() method in the tracker.py file method to make the browser headless i.e the browser will run internally


