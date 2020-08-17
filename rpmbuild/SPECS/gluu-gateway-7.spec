Name:		gluu-gateway
Version:	%VERSION%
Release:	%RELEASE%
Summary:	OAuth protected API
License:	Apache-2.0
URL:		https://www.gluu.org
Source0:	gluu-gateway-4.2.1.tar.gz
Source1:	gluu-gateway.service
Source3:	konga.service
BuildArch:      noarch
Requires:	postgresql10, postgresql10-server, nodejs, lua-cjson, unzip, python-requests, ca-certificates, logrotate, openssl, libpcre3, procps, perl

%description
The Gluu Gateway is a package which can be used to quickly
deploy an OAuth protected API gateway

%prep
%setup -q

%install
mkdir -p %{buildroot}/tmp/
mkdir -p %{buildroot}/opt/
mkdir -p %{buildroot}/lib/systemd/system/
cp -a %{SOURCE1} %{buildroot}/lib/systemd/system/gluu-gateway.service
cp -a %{SOURCE3} %{buildroot}/lib/systemd/system/konga.service
cp -a opt/gluu-gateway %{buildroot}/opt/
cp -a opt/gluu-gateway-ui %{buildroot}/opt/
cp -a opt/gluu-gateway-setup %{buildroot}/opt/

%pre
mkdir -p /opt/gluu-gateway-ui/config/locales
mkdir -p /opt/gluu-gateway-ui/config/env

%post
systemctl enable konga > /dev/null 2>&1
systemctl stop konga > /dev/null 2>&1
systemctl enable gluu-gateway > /dev/null 2>&1
systemctl stop gluu-gateway > /dev/null 2>&1
chmod +x /opt/gluu-gateway-setup/setup-gluu-gateway.py > /dev/null 2>&1
if [ `ulimit -n` -le 4095 ]; then
if ! cat /etc/security/limits.conf | grep "* soft nofile 4096" > /dev/null 2>&1; then
echo "* soft nofile 4096" >> /etc/security/limits.conf
echo "* hard nofile 4096" >> /etc/security/limits.conf
fi
ulimit -n 4096 > /dev/null 2>&1
fi

%preun
systemctl stop gluu-gateway > /dev/null 2>&1

%postun
if [ "$1" = 0 ]; then 
mkdir -p /opt/gluu-gateway-ui.rpmsavefiles  > /dev/null 2>&1
cp /opt/gluu-gateway-ui/config/*.rpmsave /opt/gluu-gateway-ui.rpmsavefiles/  > /dev/null 2>&1
rm -rf /opt/gluu-gateway-ui/* > /dev/null 2>&1
mkdir -p /opt/gluu-gateway-ui/config/  > /dev/null 2>&1
mv /opt/gluu-gateway-ui.rpmsavefiles/*.rpmsave /opt/gluu-gateway-ui/config/  > /dev/null 2>&1
rm -rf /opt/gluu-gateway-ui.rpmsavefiles  > /dev/null 2>&1
rm -rf /opt/jdk1.8.0_162 > /dev/null 2>&1
rm -rf /opt/jre > /dev/null 2>&1
systemctl start postgresql > /dev/null 2>&1
su postgres -c "psql -c \"DROP DATABASE kong;\"" > /dev/null 2>&1
su postgres -c "psql -c \"DROP DATABASE konga;\"" > /dev/null 2>&1
fi

%files
/opt/*
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/application.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/blueprints.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/bootstrap.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/connections.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/cors.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/csrf.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/globals.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/http.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/i18n.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/jwt.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/load-db.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/local_example.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/local.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/log.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/models.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/orm.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/passport.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/paths.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/policies.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/pubsub.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/routes.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/session.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/sockets.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/views.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/locales/en.json
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/locales/_README.md
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/env/development.js
%config(missingok, noreplace) /opt/gluu-gateway-ui/config/env/production.js
/lib/systemd/system/konga.service
/lib/systemd/system/gluu-gateway.service

%changelog
* Wed Jan 15 2020 Davit Nikoghosyan <davit@gluu.org> - %VERSION%-1
- Release %VERSION%
