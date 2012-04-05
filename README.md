## Installation ##
### Creating the environment ###
Create a virtual python enviroment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv uwc-env
```

#### For virtualenv ####
```bash
virtualenv uwc-env
cd uwc-env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone git@github.com:vasyabigi/uwc.git uwc
```

### Install requirements ###
```bash
cd uwc
pip install -r requirements.txt
```

### Configure project ###
```bash
cp uwc/local_settings.py.example uwc/local_settings.py
vi uwc/local_settings.py
```

### Sync database ###
```bash
python manage.py syncdb --all
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000
