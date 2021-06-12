# SaltyCoin

[![Python 3.9](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://www.python.org/downloads/release/python-390/)

**SaltyCoin** is a browser game about trading a fake currency. It's meant to be played at a convention where all players experience the same randomly generated market.

## Deployment

```bash
# install python3.9 from ppa
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9

# install pip then install numpy library
sudo apt install python3-pip
pip install numpy

# get code
cd /srv
git clone https://github.com/cbahn/SaltyCoin.git

# run server
cd /srv/SaltyCoin
python3 webserver.py
```

## Next Steps
- [ ] Clean up templating engine
- [ ] Complete Admin menu
- [ ] Make it easier to adjust the time between value changes
- [ ] Add clientside buy-sell game mechanics
- [ ] Lightly obfuscate client-side gamestate tracking
