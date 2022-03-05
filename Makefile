build:
	docker build -f dockerfiles/python36.Dockerfile -t test_grep_py3.6 .
	docker build -f dockerfiles/python27.Dockerfile -t test_grep_py2.7 .
run:
	docker run -it test_grep_py3.6
	docker run -it test_grep_py2.7


