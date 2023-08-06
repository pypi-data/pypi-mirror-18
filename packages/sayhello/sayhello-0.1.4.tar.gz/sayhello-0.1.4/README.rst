===============================
sayhello
===============================


.. image:: https://img.shields.io/pypi/v/say_hello.svg
        :target: https://pypi.python.org/pypi/say_hello

.. image:: https://api.travis-ci.org/catplant/say-hello.svg?branch=master
        :target: https://travis-ci.org/catplant/say_hello


用法
----

在命令行上阅读文本和文件。调用百度 TTS 语音，目前支持支持中文、美音、英音、粤语、日语、韩语、法语、西班牙语、泰语、阿拉伯语、俄语、葡萄牙语。

.. code-block:: bash

    $ say 你好
    $ say -u hello
    $ say 黄金时代.txt


安装
----

.. code-block:: bash

    $ [sudo] pip install sayhello


依赖
----

* `docopt`_

安装：``[sudo] pip install docopt``
    
* `requests`_

安装：``[sudo] pip install requests``

* mplayer

安装：``[sudo] apt-get install mplayer``


.. _docopt: https://github.com/docopt/docopt
.. _requests: https://github.com/kennethreitz/requests

