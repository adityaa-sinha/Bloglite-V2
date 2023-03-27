# Bloglite^v2^

A multi-user blogging application.

## How to run the application?
Make sure to install redis and mailhog first.

 ### Start the redis server by running the following command
```bash
redis-server
```

### Start mailhog by running the following command
```bash
mailhog
```
### Running the backend code
- Open terminal at the root directory of this project and run the following command to setup environment
	```bash
	cd backend
	sh local_setup.sh
	```
- Open another terminal tab and run the following command to run the application 
	```bash
	cd backend
	sh local_run.sh
	```
- Open another terminal tab and run the following command to run celery workers
	```bash
	cd backend
	sh local_workers.sh
	```
- Open another terminal tab and run the following command to run celery beat for scheduled jobs
	```bash
	cd backend
	sh local_celerybeat.sh
	```
### Running the frontend code

`node_modules` folder is not present in this repository. Make a new VueJS project by following the VueJS documentation and copy-paste the `node_modules` folder in `bloglite-frontend` folder.

After that, open terminal at `bloglite-frontend` folder and run the following command
```bash
npm run dev
```

### Done!