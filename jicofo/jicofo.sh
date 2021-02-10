#!/bin/bash

if [[ "$1" == "--help"  || $# -lt 1 ]]; then
    echo -e "Usage:"
    echo -e "$0 [OPTIONS], where options can be:"
    echo -e "\t--host=HOST\t sets the hostname of the XMPP server (default: domain, if domain is set, localhost otherwise)"
    echo -e "\t--domain=DOMAIN\t sets the XMPP domain"
    echo -e "\t--port=PORT\t sets the port of the XMPP server (default: 5347)"
    echo -e "\t--subdomain=SUBDOMAIN\t sets the sub-domain used to bind focus XMPP component (default: focus)"
    echo -e "\t--secret=SECRET\t sets the shared secret used to authenticate focus component to the XMPP server"
    echo -e "\t--user_domain=DOMAIN\t specifies the name of XMPP domain used by the focus user to login."
    echo -e "\t--user_name=USERNAME\t specifies the username used by the focus XMPP user to login. (default: focus@user_domain)"
    echo -e "\t--user_password=PASSWORD\t specifies the password used by focus XMPP user to login. If not provided then focus user will use anonymous authentication method."
    echo
    echo -e "\tSECRET and PASSWORD can alternatively be set via the environment variables JICOFO_SECRET and JICOFO_AUTH_PASSWORD respectively."
    echo
    exit 1
fi

if [ -z "$JICOFO_MAX_MEMORY" ]; then JICOFO_MAX_MEMORY=3072m; fi

cp /etc/jicofo/sip-communicator.properties ~/
exec java -Xmx$JICOFO_MAX_MEMORY \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:HeapDumpPath=/tmp \
    -Djdk.tls.ephemeralDHKeySize=2048 \
    $JAVA_SYS_PROPS \
    -jar /usr/share/jicofo/jicofo.jar $@
