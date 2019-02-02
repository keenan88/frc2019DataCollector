Required setup:

Python must be installed.

dataCollectorClient.py requires the pillow module, which does not come with default python. run "pip install pillow" in the command prompt to install pillow.

Delete deleteMe.csv from localCSVData and serverCSVData folders.

------------------------------------------------------------------------------

User Manual:

The project contains two python scripts, dataCollectorClient.py and server.py

To host a server, simply double click the python server.py script. The server's IP and Port will be stated in the console.

To run a client, run the dataCollectorClient.py script. Enter the appropriate server's IP and Port to authenticate connection to server. 
All data which is saved by the client will be sent to the server, and saved in the servers "serverCSVData" folder. If a client cannot communicate
which the server, it will save locally to its "localCSVData" folder.

All information is saved in csv format, such that information can be easily entered into excel or google sheets.

NOTE: Server and client must be on the same network to communicate.

------------------------------------------------------------------------------

Any questions can be directed to the developer, keenanburke@outlook.com.

