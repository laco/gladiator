CURRENT_VERSION=$(shell python3 -c "from gladiator import get_version; print(get_version())")
# NEXT_VERSION=$(shell python3 -c "from gladiator import next_version; print(next_version())")


build:
	python3 setup.py sdist

test:
	tox


clean:
	rm -rf Gladiator.egg-info
	rm -f dist/*.tar.gz

# inc_version:
# 	perl -i -pe 's/$(CURRENT_VERSION)/$(NEXT_VERSION)/' gladiator/__init__.py
# 	echo "New vesion is: $(NEXT_VERSION)"

git_tag:
	git tag $(CURRENT_VERSION)

pypi_upload:
	python3 setup.py sdist upload -r pypi

pypi_register:
	python3 setup.py register -r pypi

pypitest_upload:
	python3 setup.py sdist upload -r pypitest

pypitest_register:
	python3 setup.py register -r pypitest

release: clean test build
	echo "1. runnint tests"
	echo "2. Change version"
	echo "3. commit and create tag"
	echo "4. git push --tags"
	echo "5. setup.py upload"

