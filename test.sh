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
)
