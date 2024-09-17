# Development setup

I call this a development setup, because it is clearly not ready for production.

```sh
sudo apt install python3 python3-pip python3-venv tree
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Server

It's a simple flask with 2 API POST endpoints (/api/load and /api/predict).
To run it:

```sh
python server.py
```

## Client

This will access the server's POST endpoints and deliver the predictions:

```sh
python client.py -n 2 -o outputs -u 127.0.0.1:5000
tree outputs
```

## Cleanup

```sh
# kill the server if it is running in background and you need to kill it
# I hope you don't have any other python instances you need to run
sudo pkill python 

deactivate
rm -rf venv

rm -rf outputs
```

# Excuses

- There is no authentication or other security.
- There are not enough comments in the code and this readme is light.
- I know you will find a way to make it crash. I already know a couple ways myself (e.g. add one more line in stock_price_data_files/BAD_CSVS/CORRUPTED_CSV.csv the whole thing becomes unusable due to internal error). But I know how I should fix them.
- This is not ready for production.
- This is the best I can do in 2 hours.
