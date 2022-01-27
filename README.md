# fasten-pypi-plugin
A Python plugin that can be used to analyze and report issues about a module dependencies at build time.

To get this plugin running:

1. Run the [docker-python-pipeline](https://github.com/fasten-project/fasten-docker-deployment) first:
	```
	sudo docker-compose --profile python up -d
	```

2. Feed the database with the [testPackages.txt](https://github.com/fasten-project/fasten-pypi-plugin/blob/development/testPackages.txt)-file:
	```
	cat testPackages.txt | sudo docker-compose exec -T kafka kafka-console-producer.sh --broker-list kafka:9092 --topic fasten.PyPI.releases --property 'parse.key=true' --property 'key.separator=|'
	```

3. Check if the pipeline is fed (will take a while):
 * via curl:
   ```
   curl -X GET localhost:9080/api/pypi/packages
   ```
 * via the `metadata-db` container:
	* exec inside the container:
   ```
	 sudo docker-compose exec metadata-db /bin/bash
	 ```
	* query the database:
	 ```
	 PGPASSWORD=fasten1234 psql --host localhost --port 5432 --username fasten fasten_python --command="SELECT * FROM packages;"
	 ```

4. Activate your python virtual environment (if you use one):
	```
	source pypi-Plugin-venv/bin/activate
	```

5. Make sure that you have the packages [`pycg`](https://github.com/vitsalis/pycg), [`pycg-stitch`](https://github.com/fasten-project/pycg-stitch) installed. \
   To install them run the following inside the pycg / pycg-stitch folder (assuming you are using a virtual environment):
	 ```
	 sudo pypi-Plugin-venv/bin/python3.9 setup.py install
	 ```

6. Run the pypi-plugin from inside the `fasten-pypi-plugin/src/fasten`-folder to create a Call Graph for the plugin itself:
	```
	python3 main.py
		--product fasten-pypi-plugin \
		--pkg_name fasten-pypi-plugin \
		--project_path ./ \
		--timestamp 42 \
		--version 1.0 \
		--requirements ../../requirements.txt 
	```

7. The Call-Graphs can be found inside the `fasten-pypi-plugin/src/fasten/callGraphs`-folder.
