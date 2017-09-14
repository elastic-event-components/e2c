# Installing E2C on Ubuntu
The following guides explain how to install a version 
of E2C on Ubuntu that enables you to write applications in Python.

We recommend the virtualenv installation. 
Virtualenv is a virtual Python environment isolated from other Python development, 
incapable of interfering with or being affected by other Python programs on the same machine.
During the virtualenv installation process, you will install not only TensorFlow but also all the packages that TensorFlow requires.
To start working with E2C, you simply need to "activate" the virtual environment. 
All in all, virtualenv provides a safe and reliable mechanism for installing and running E2C.
 
# Installing with virtualenv
Take the following steps to install E2C with Virtualenv:

1. Change to source directory: 'source/python'
```shell
$ cd source/python
```
2. Start the install shell script 'install.sh':
```shell
$ sudo ./install.sh 
```
3. Activate the virtualenv environment by issuing the following commands:
```shell
$ source venv/bin/activate
```
The preceding source command should change your prompt to the following:
```shell
$ (venv)$ 
```
When you are finish using E2C, you may deactivate the environment by invoking the deactivate function as follows:
```shell
$ (venv)$ deactivate 
```

# Validate the installation
To validate your E2C installation, do the following:

1. Ensure that your environment is prepared to run the test suite.
2. Run a short E2C program.

## Run the tests
1. Start a terminal.
2. Activate your virtualenv environment.
3. Navigate to the directory 'source/python' and run the following:
```shell
$ (venv)$ pytest tests
```

## Run a short E2C program
1. Navigate to the directory 'source/python/examples/quick_start1' and run the following:
```shell
$ (venv)$ python app.py
```

If the system outputs the following, then you are ready to start writing E2C programs:
```shell
$ Hello, E2C
```
    