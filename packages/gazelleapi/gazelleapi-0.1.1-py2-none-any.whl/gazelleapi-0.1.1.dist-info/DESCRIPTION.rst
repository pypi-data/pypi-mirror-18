Copyright (c) 2016 itismadness

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Description: gazelleapi
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
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
