# SaltyCoin

[![Python 3.9](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://www.python.org/downloads/release/python-390/)

**SaltyCoin** is a browser game about trading a fake currency. It's meant to be played at a convention where all players experience the same randomly generated market.

## Deployment

1. Spin up fresh ubuntu server

2.
```sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9

sudo apt install python3-pip
pip install numpy

cd /srv
git clone https://github.com/cbahn/SaltyCoin.git
```

## Next Steps
[ ] Clean up templating engine
[ ] Complete Admin menu
[ ] Make it easier to adjust the time between value changes
[ ] Add clientside buy-sell game mechanics
[ ] Lightly obfuscate client-side gamestate tracking