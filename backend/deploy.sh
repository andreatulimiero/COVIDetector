echo -e "[\x1b[35m*\x1b[0m] Deploying ..."
# Backend
cd backend

## Virtualenv 
if ls env >/dev/null ; then : ;
else
  echo -e "[\x1b[35m*\x1b[0m] Creating virtualenv ..."
  python3 -m venv -p python3 env;
fi
source env/bin/activate
source .env
## Dependecies
echo -e "[\x1b[35m*\x1b[0m] Installing dependencies ..."
pip install -r requirements.txt > /dev/null
## Cronjob
## crontab < cronjob

## Debug check
SETTINGS_PATH=covidetector/settings.py 
mv $SETTINGS_PATH $SETTINGS_PATH.bak
cat $SETTINGS_PATH.bak | sed 's/^DEBUG\s*=\s*True$/DEBUG = False/' > $SETTINGS_PATH
mv $SETTINGS_PATH $SETTINGS_PATH.bak
cat $SETTINGS_PATH.bak | sed 's/^SESSION_COOKIE_SECURE\s*=\s*False$/SESSION_COOKIE_SECURE = True/' > $SETTINGS_PATH

## DB
echo -e "[\x1b[35m*\x1b[0m] Updating DB ..."
python manage.py migrate

echo -e "[\x1b[33m+\x1b[0m] Deploy complete ..."
