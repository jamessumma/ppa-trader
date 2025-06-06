# this is where the data is controlled and held, for now. Long term this will likely be where we query data. 
lets design a pipeline. I'm thinking this:
a config file that determines what values we wish to query for, the ones we wish to derive, and some schemes by which we encode string data to me input to the ml model, and the process of labelling our data.

data-manager.py will manage everything, it will handle the call to get data and the call to get the processed data out
data-scraper.py will query alpaca at the request of the data-manager for the data we want (the data we want is determined by the config file) and put it in a folder named pre-processed-data as a csv and signal to the data-manager when it is done
once data-scraper.py is done, data-factory.py will take the preprocessed data from the folder named pre-processed-data, it will look at the config file to decide while values to derive will construct a csv accordingly, placing that into the folder named derived-data as a csv and signal to the data-manager when it is done
data-ml-prep.py will then take the csv with all of the raw and derived values, it will take any strings and ecode them the way you described earlier so they can be used as features in the neural network. It will look at the config file to see if, for a particular value, it will choose One-Hot Encoding, label encoding, or cyclical encoding. it will be put as a csv into a folder named "prepped data"
data-ml-labeling.py will label our data according to whatever labeling schema, i'm thinking about calling this labeling-factory because we may have different labeling paradigms we want to use. the finalized labeled data will be put into a folder named "labeled data"
And then we are done!