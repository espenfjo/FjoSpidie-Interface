#!/bin/bash
set_config() {
    key="$1"
    value="${*:2}"

    sed -ri "s/%$key%/$value/" SpidieFace/settings.py

}

if [ ! -z "$MONGO_HOST" ] && [ ! -z "$MONGO_PORT_27017_TCP_ADDR" ]; then
    echo "This FjoSpidie container is linked to a MongoDB Docker container, and given MONGO_HOST environment variable. Using linked MongoDB at $MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT"
    exit 1
fi
if [ -z "$MONGO_HOST" ] && [ -z "$MONGO_PORT_27017_TCP_ADDR" ]; then
    echo "Not linked to a MongoDB container, or 'MONGO_HOST' not given as an environment variable"
    exit 1;
fi

if [ -z "$MONGO_PORT" ] && [ -z "$MONGO_PORT_27017_TCP_PORT" ]; then
    MONGO_PORT=27017
fi

if [ ! -z "$MONGO_PORT_27017_TCP_ADDR" ]; then
    MONGO_HOST=$MONGO_PORT_27017_TCP_ADDR
fi
if [ ! -z "$MONGO_PORT_27017_TCP_PORT" ]; then
    MONGO_PORT=$MONGO_PORT_27017_TCP_PORT
fi


NET=$(ip a show dev eth0 |grep -w inet| awk '{print $2}' | sed "s/[0-9]*\/16/0\/16/") # Hack to replace IP with .0 :(
bpf="not ip6 and not net $NET"


pw=$(dd if=/dev/urandom bs=1 count=32 2>/dev/null | base64 -w 0 | rev | cut -b 2- | rev)
export SECRET_KEY=$(dd if=/dev/urandom bs=1 count=62 2>/dev/null | base64 -w 0 | rev | cut -b 2- | rev)
export MONGO_HOST
export MONGO_PORT

echo "from django.contrib.auth.models import User; exit(User.objects.count())" | python manage.py shell
if [ $? == 0 ]; then
    echo -e "from django.contrib.auth.models import User; u = User(username='admin');u.set_password(\"$pw\");u.is_superuser = True;u.is_staff = True;u.save()" | python manage.py shell
    echo "Admin user/pass is: admin/$pw"
else
    echo "User(s) already present in database"
fi

python manage.py runserver 0.0.0.0:8080
