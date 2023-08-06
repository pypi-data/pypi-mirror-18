from distutils.core import setup

requires = []

try:
	import ldap3
except:
	requires.append('ldap3')

setup(
	name="pydirectory",
	version="0.1.15",
	description="Python frameWork to managing multiples LDAP services - (gamma)",
	author="Jonas Delgado Mesa",
	author_email="jdelgado@yohnah.net",
	url="https://github.com/Wengex/PyDirectory",
	license="GPLv2",
	packages=[
		'pydirectory',
		'pydirectory.directory',
		'pydirectory.directory.settings',
		'pydirectory.directory.engine',
		'pydirectory.directory.objects',
		'pydirectory.ldap',
		'pydirectory.ldap.settings',
		'pydirectory.ldap.engine',
		'pydirectory.ldap.objects',
		'pydirectory.activedirectory',
		'pydirectory.activedirectory.settings',
		'pydirectory.activedirectory.engine',
		'pydirectory.activedirectory.objects',
	],
	long_description=open('README.txt').read(),
	install_requires = requires
)
