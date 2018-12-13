# as_topo_scrape
#### Worcester Polytechnic Institute
#### CS 513 Computer Networks | Fall 2018

Team members: 
* Anqi Lu
* Wei Xiong 
* Zeqian Li

Research topic: 
[AS-Level Topology Collection Through Looking Glass Servers](http://conferences.sigcomm.org/imc/2013/papers/imc037s-khanA.pdf)

The goal of our project is to replicate and compare the results from paper AS-level Topology Collection through Looking Glass Servers by Khan et al. \cite{khan2013level}. Several studies have pointed out the incompleteness of the Internet topology researchers have found and pieced together so far. In this study, we explore one of the AS-topology collection method -- Looking Glass (LG) servers with the hope to discover AS links that were not found by other AS topology collection methods. After querying LG servers we collected, we discovered 28K AS links and 5.9K ASes that were hidden from other resources. 


#### Running Insturctions
* Activate [pipenv](https://github.com/pypa/pipenv) - a virtual environment for this project
> pipenv shell
* Check pipenv is python 3. If not, switch to python 3
> pipenv --three
* Install all dependencies
> pipenv install

* Pipfile.lock is automatically populated. It contains all the packages in this project. 
* If you want to install packages, just use pip install (package name)
