from setuptools   import setup

setup( 
	name='eg-pypackage',    
    version='0.1.2',                          
    scripts=['script/hello'],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.service','service/*'],
    },
    data_files=[
		('/usr/lib/systemd/system/', [
			'service/hello.service'
		]) ]     
)