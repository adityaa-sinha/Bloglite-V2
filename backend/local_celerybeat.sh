#! /bin/sh
echo "======================================================================"
echo "CELERY BEAT RUN." 
echo "----------------------------------------------------------------------"
if [ -d "venv" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. venv/bin/activate
export ENV=development
export SECRET_KEY="fd017a9e9a3e4d1eb6169b0ee9b11aa1"
export SECURITY_PASSWORD_SALT="48dcb0ffab5e48939866ac0e58fe5de6"
celery -A main.celery beat --max-interval 1 -l info
deactivate