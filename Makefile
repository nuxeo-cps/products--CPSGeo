check:
	pychecker2 *.py

clean:
	find . "(" -name "*~" -or -name "*.pyc" -or -name "#*" -or -name ".#*" ")" -print0 | xargs -0 rm -f
	#rm -rf doc/API
	cd tests ; make clean

docs:
	happydoc -d doc/API *.py
