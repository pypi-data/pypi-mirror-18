from setuptools   import setup

setup( 
	name='eg-pypackage',    
    version='0.1.1',                          
    scripts=['script/hello'],
    data_files=[
		('/usr/lib/systemd/system/', [
			'service/hello.service'
			]) ]     
)