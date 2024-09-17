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