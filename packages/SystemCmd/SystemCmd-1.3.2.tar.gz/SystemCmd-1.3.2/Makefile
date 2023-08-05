package=system_cmd

include pypackage.mk


bump-upload:
	bumpversion patch
	git push --tags
	python setup.py sdist upload
	

vulture:
	
