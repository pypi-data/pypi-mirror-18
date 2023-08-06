gazelleapi
==========
This project provides a simple way to access and use a Gazelle based tracker from Python. This is available for
both python 2 and 3 for the time being.

It is based on [whatapi](https://github.com/isaaczafuta/whatapi) and [xanaxbetter](https://github.com/rguedes/xanaxbetter)

Installation
-------------
pip:
```bash
pip install gazelleapi
```

source:
```bash
git clone https://github.com/itismadness/gazelleapi
cd gazelleapi
python setup.py install
```

Example Usage
-------------
```
>>> from gazelleapi import GazelleAPI
>>> api = GazelleAPI(username='me', password='secret', hostname='tracker.me')
>>> api.get_torrent(1234567)
```

To avoid undue stress on the server, it is suggested that you utilize cookies to save/load session information
across usages of the API using something like pickle:
```
>>> from gazelleapi import GazelleAPI
>>> import pickle
>>> cookies = pickle.load(open('cookies.dat', 'rb'))
>>> api = GazelleAPI(username='me', password='secret', hostname='tracker.me', cookies=cookies)
...
>>> pickle.dump(api.session.cookies, open('cookies.dat', 'wb'))
```

