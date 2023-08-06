csf
---

Dependencies
============
python 2.x/3.x

[pandas](http://pandas.pydata.org/ "pandas")

Installation
============

- 1.pip install csf
- 2.python setup.py install
- 3.访问[https://pypi.python.org/pypi/csf/](https://pypi.python.org/pypi/csf/)下载安装


Upgrade
=======

	pip install csf --upgrade

Quick Start
===========
**Example1

    >>> import csf
    >>> csf.config.set_token("ACCESS_KEY","SECRET_KEY") 设置token
    >>> csf.get_stock_hist_bar(code="000001")
    
return：
>                          code   open   high    low  close      volume
    date                                                                               
    1991-01-02 00:00:00  000001   5.97   5.97   5.97   5.97     58958.0
    1991-01-03 00:00:00  000001   5.96   5.96   5.96   5.96     21240.0
    ...                     ...    ...    ...    ...    ...         ...
    2016-04-07 00:00:00  000001  10.72  10.73  10.59  10.59  37771959.0
    2016-04-08 00:00:00  000001  10.55  10.67  10.50  10.57  37655386.0