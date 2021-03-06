#!/bin/bash -e

workspace="$( dirname $0 )"



(
	cd "$workspace"
	workspace="$(pwd)"

	if [ ! -e .contents ]
	then
		virtualenv .contents
	fi
	.contents/bin/pip install -r requirements.txt

	.contents/bin/coverage erase
	for x in *_test.py
	do
		.contents/bin/coverage run -a --omit=.contents/*,*_test.py $x
	done
	.contents/bin/coverage report

	if [ ! -e .contents_package ]
	then
		virtualenv .contents_package
	fi
	.contents_package/bin/pip install -r requirements.package.txt

	echo zip lambda.zip *.py
	zip lambda.zip *.py

	(
		cd .contents_package/lib/python2.7/site-packages
		echo zip -u -r "$workspace/lambda.zip" *
		zip -u -r "$workspace/lambda.zip" * || code=$?
	)

	echo zip lambda.zip web/*.html
	zip lambda.zip web/*.html
	echo zip lambda.zip web/js/*.js
	zip lambda.zip web/js/*.js

)
