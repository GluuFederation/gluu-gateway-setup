#!/usr/bin/python

import subprocess
import traceback
import time
import os
import sys
import socket
import random
import string
import shutil
import requests
import json
import getpass
import urllib3
import platform
import pwd
import glob
try:
    import distro
except:
    print ('Unable to find `distro` package hence using `platform`')
    distro = platform

class Distribution:
    Ubuntu = "ubuntu"
    Debian = "debian"
    CENTOS = "centos"
    RHEL = "red"

class KongSetup(object):
    def __init__(self):
        self.host_name = ''
        self.ip = ''
        self.cert_folder = './certs'
        self.template_folder = './templates'
        self.output_folder = './output'
        self.system_folder = './system'
        self.tmp_folder = '/tmp'

        self.log_error = 'gluu-gateway-setup_error.log'
        self.log = 'gluu-gateway-setup.log'

        self.cmd_mkdir = '/bin/mkdir'
        self.openssl_command = '/usr/bin/openssl'
        self.cmd_chown = '/bin/chown'
        self.cmd_chmod = '/bin/chmod'
        self.cmd_ln = '/bin/ln'
        self.host_name = '/bin/hostname'
        self.cmd_touch = '/bin/touch'
        self.cmd_mv = '/bin/mv'
        self.cmd_cp = '/bin/cp'
        self.cmd_rm = '/bin/rm'
        self.cmd_node = '/usr/bin/node'
        self.cmd_update_rs_d = '/usr/sbin/update-rc.d'
        self.cmd_sh = '/bin/sh'
        self.cmd_bash = '/bin/bash'
        self.cmd_update_alternatives = 'update-alternatives'
        self.cmd_chkconfig = 'chkconfig'
        self.cmd_alternatives = 'alternatives'
        self.cmd_echo = '/bin/echo'
        self.cmd_service = 'service'
        self.cmd_systemctl = os.popen('which systemctl').read().strip()
        self.cmd_rpm = '/bin/rpm'
        self.cmd_echo = '/bin/echo'
        self.cmd_dpkg = '/usr/bin/dpkg'
        self.cmd_kong = '/usr/local/bin/kong'

        self.country_code = ''
        self.state = ''
        self.city = ''
        self.org_name = ''
        self.admin_email = ''

        self.kong_custom_plugins = 'gluu-oauth-auth,gluu-uma-auth,gluu-uma-pep,gluu-oauth-pep,gluu-metrics,gluu-openid-connect,gluu-opa-pep'
        self.kong_ssl_cert = ''
        self.kong_ssl_key = ''
        self.pg_pwd = 'admin'
        self.kong_admin_listen_ssl_port = '8445'
        self.kong_admin_listen_port = '8001'
        self.kong_lua_ssl_trusted_certificate = ''
        self.kong_lua_ssl_verify_depth = 3
        self.gluu_prometheus_server_ip = '104.131.17.150'
        self.gluu_prometheus_server_host = 'license.gluu.org'
        self.gluu_customer_registration_endpoint = 'https://%s:%s' % (self.gluu_prometheus_server_host, '4040/metrics/registration')
        self.dist_kong_config_folder = '/etc/kong'
        self.dist_kong_config_file = '%s/kong.conf' % self.dist_kong_config_folder
        self.dist_lua_folder = '/usr/local/share/lua/5.1'
        self.dist_gluu_lua_folder = '%s/gluu' % self.dist_lua_folder
        self.dist_kong_plugins_folder = '%s/kong/plugins' % self.dist_lua_folder

        self.opt_folder = '/opt'
        self.dist_gluu_gateway_folder = '%s/gluu-gateway' % self.opt_folder
        self.dist_gluu_gateway_ui_folder = '%s/gluu-gateway-ui' % self.opt_folder
        self.dist_gluu_gateway_setup_folder = '%s/gluu-gateway-setup' % self.opt_folder
        self.dist_gluu_gateway_ui_assest_folder = '%s/assets' % self.dist_gluu_gateway_ui_folder
        self.dist_gluu_gateway_ui_config_folder = '%s/config' % self.dist_gluu_gateway_ui_folder
        self.dist_gluu_gateway_ui_config_file = '%s/config/local.js' % self.dist_gluu_gateway_ui_folder
        self.gg_plugins_folder = '%s/lib/kong/plugins' % self.dist_gluu_gateway_folder
        self.disable_plugin_list = ['ldap-auth', 'key-auth', 'basic-auth', 'jwt', 'oauth2', 'hmac-auth']
        self.gg_comman_folder = '%s/lib/gluu' % self.dist_gluu_gateway_folder

        self.dist_oxd_server_folder = '%s/oxd-server' % self.opt_folder
        self.dist_oxd_server_config_folder = '%s/conf' % self.dist_oxd_server_folder
        self.dist_oxd_server_config_file = '%s/oxd-server.yml' % self.dist_oxd_server_config_folder

        self.gg_service = 'gluu-gateway'
        self.oxd_server_service = 'oxd-server' # change this when oxd-server-4.0 is released

        # oxd kong Property values
        self.gluu_gateway_ui_port = '1338'
        self.gluu_gateway_ui_policy_type = 'uma_rpt_policy'
        self.gluu_gateway_ui_oxd_id = ''
        self.gluu_gateway_ui_op_host = ''
        self.gluu_gateway_ui_client_id = ''
        self.gluu_gateway_ui_client_secret = ''
        self.gluu_gateway_ui_oxd_web = ''
        self.gluu_gateway_ui_kong_admin_web_url = 'http://localhost:%s' % self.kong_admin_listen_port
        self.gluu_gateway_ui_oxd_version = '4.2.2'
        self.gg_version = '4.2.2'
        self.postgres_version = '10.x'

        # oxd licence configuration
        self.generate_client = True
        self.gluu_gateway_ui_redirect_uri = 'localhost'

        # JRE setup properties
        self.jre_version = '162'
        self.jre_destination_path = '/opt/jdk1.8.0_%s' % self.jre_version
        self.gg_dist_folder = '%s/dist' % self.dist_gluu_gateway_folder
        self.gg_dist_app_folder = '%s/app' % self.gg_dist_folder
        self.jre_home = '/opt/jre'
        self.jre_sh_file_name = 'jre-gluu.sh'
        self.is_prompt = True
        self.license = False
        self.init_parameters_from_json_argument()

        # OS types properties
        self.os_types = ['centos', 'red', 'ubuntu']
        self.os_type = None
        self.os_version = None
        self.os_initdaemon = None

        # log-rotate kong config file
        self.dist_kong_log_rotate_config_path = '/etc/logrotate.d'
        self.kong_log_rotate_config_file = 'kong_logrotate'

        # PostgreSQL config file path
        self.dist_pg_hba_config_path = '/var/lib/pgsql/10/data'
        self.dist_pg_hba_config_file = '%s/pg_hba.conf' % self.dist_pg_hba_config_path

        # dependency zips
        self.gg_node_modules_folder = "%s/node_modules" % self.dist_gluu_gateway_ui_folder
        self.gg_bower_modules_folder = "%s/bower_components" % self.dist_gluu_gateway_ui_assest_folder
        self.gg_node_modules_archive = 'gg_node_modules.tar.gz'
        self.gg_bower_modules_archive = 'gg_bower_components.tar.gz'

        # third party lua library
        self.oxd_web_lua_file_path = '%s/third-party/oxd-web-lua/oxdweb.lua' % self.dist_gluu_gateway_folder
        self.json_logic_file_path = '%s/third-party/json-logic-lua/logic.lua' % self.dist_gluu_gateway_folder
        self.lrucache_files_path = '%s/third-party/lua-resty-lrucache/lib/resty' % self.dist_gluu_gateway_folder
        self.lsession_files_path = '%s/third-party/lua-resty-session/lib/resty' % self.dist_gluu_gateway_folder
        self.jwt_files_path = '%s/third-party/lua-resty-jwt/lib/resty/.' % self.dist_gluu_gateway_folder
        self.hmac_files_path = '%s/third-party/lua-resty-hmac/lib/resty/.' % self.dist_gluu_gateway_folder
        self.prometheus_file_path = '%s/third-party/nginx-lua-prometheus/prometheus.lua' % self.dist_gluu_gateway_folder

        # kong package file names
        self.ubuntu18_kong_file = "kong-2.2.1.bionic.amd64.deb"
        self.centos7_kong_file = "kong-2.2.1.el7.amd64.rpm"
        self.rhel7_kong_file = "kong-2.2.1.rhel7.amd64.rpm"

        # db names
        self.dist_konga_db_file = "%s/templates/konga.sql" % self.dist_gluu_gateway_setup_folder
        self.dist_kong_db_file = "%s/templates/kong.sql" % self.dist_gluu_gateway_setup_folder

    def init_parameters_from_json_argument(self):
        if len(sys.argv) > 1:
            self.is_prompt = False
            data = json.loads(sys.argv[1])
            self.license = data['license']
            self.ip = data['ip']
            self.host_name = data['host_name']
            self.country_code = data['country_code']
            self.state = data['state']
            self.city = data['city']
            self.org_name = data['org_name']
            self.admin_email = data['admin_email']
            self.pg_pwd = data['pg_pwd']
            self.gluu_gateway_ui_redirect_uri = data['gluu_gateway_ui_redirect_uri']
            self.gluu_gateway_ui_op_host = 'https://' + data['gluu_gateway_ui_op_host']
            self.gluu_gateway_ui_oxd_web = data['gluu_gateway_ui_oxd_web']
            self.generate_client = data['generate_client']

            if not self.generate_client:
                self.gluu_gateway_ui_oxd_id = data['gluu_gateway_ui_oxd_id']
                self.gluu_gateway_ui_client_id = data['gluu_gateway_ui_client_id']
                self.gluu_gateway_ui_client_secret = data['gluu_gateway_ui_client_secret']

    def configure_postgres(self):
        print ("Configuring postgres...")
        self.log_it('Configuring postgres...')
        print ('Configuring postgres...')

        if self.os_type == Distribution.Ubuntu:
            self.run(['/etc/init.d/postgresql', 'start'])
            os.system('sudo -iu postgres /bin/bash -c "psql -c \\\"ALTER USER postgres WITH PASSWORD \'%s\';\\\""' % self.pg_pwd)
            os.system('sudo -iu postgres /bin/bash -c "psql -U postgres -tc \\\"SELECT 1 FROM pg_database WHERE datname = \'kong\'\\\" | grep -q 1 || psql -U postgres -c \\\"CREATE DATABASE kong;\\\""')
            os.system('sudo -iu postgres /bin/bash -c "psql -U postgres -tc \\\"SELECT 1 FROM pg_database WHERE datname = \'konga\'\\\" | grep -q 1 || psql -U postgres -c \\\"CREATE DATABASE konga;\\\""')
            os.system('sudo -iu postgres /bin/bash -c "psql konga < %s"' % self.dist_konga_db_file)
            os.system('sudo -iu postgres /bin/bash -c "psql kong < %s"' % self.dist_kong_db_file)

        if self.os_type in [Distribution.CENTOS, Distribution.RHEL] and self.os_version == '7':
            # Initialize PostgreSQL first time
            self.run([self.cmd_ln, '/usr/lib/systemd/system/postgresql-10.service', '/usr/lib/systemd/system/postgresql.service'])
            self.run(['/usr/pgsql-10/bin/postgresql-10-setup', 'initdb'])
            self.render_template_in_out(self.dist_pg_hba_config_file, self.template_folder, self.dist_pg_hba_config_path)
            self.run([self.cmd_systemctl, 'enable', 'postgresql'])
            self.run([self.cmd_systemctl, 'start', 'postgresql'])
            os.system('sudo -iu postgres /bin/bash -c "psql -c \\\"ALTER USER postgres WITH PASSWORD \'%s\';\\\""' % self.pg_pwd)
            os.system('sudo -iu postgres /bin/bash -c "psql -U postgres -tc \\\"SELECT 1 FROM pg_database WHERE datname = \'kong\'\\\" | grep -q 1 || psql -U postgres -c \\\"CREATE DATABASE kong;\\\""')
            os.system('sudo -iu postgres /bin/bash -c "psql -U postgres -tc \\\"SELECT 1 FROM pg_database WHERE datname = \'konga\'\\\" | grep -q 1 || psql -U postgres -c \\\"CREATE DATABASE konga;\\\""')
            os.system('sudo -iu postgres /bin/bash -c "psql konga < %s"' % self.dist_konga_db_file)
            os.system('sudo -iu postgres /bin/bash -c "psql kong < %s"' % self.dist_kong_db_file)


    def enable_service_at_start(self, serviceName, startSequence=None, stopSequence=None, action='enable'):
        # Enable service autoload on Gluu-Server startup
        if self.os_type in [Distribution.CENTOS, Distribution.RHEL]:
            if self.os_initdaemon == 'systemd':
                self.run([self.cmd_systemctl, action, serviceName])
            else:
                self.run(["/sbin/chkconfig", serviceName, "on" if action=='enable' else 'off'])

        elif self.os_type+self.os_version in ('ubuntu18','debian9'):
            self.run([self.cmd_systemctl, action, serviceName])

        elif self.os_type in [Distribution.Ubuntu, Distribution.Debian]:
            cmd_list = ["/usr/sbin/update-rc.d", serviceName, 'defaults']

            if startSequence and stopSequence:
                cmd_list.append(str(startSequence))
                cmd_list.append(str(stopSequence))

            self.run(cmd_list)

    def detect_host_name(self):
        detected_host_name = None
        try:
            detected_host_name = socket.gethostbyaddr(socket.gethostname())[0]
        except:
            try:
                detected_host_name = os.popen("/bin/hostname").read().strip()
            except:
                self.log_it("No detected hostname", True)
                self.log_it(traceback.format_exc(), True)
        return detected_host_name

    def gen_cert(self, service_name, password, user='root', cn=None):
        self.log_it('Generating Certificate for %s' % service_name)
        key_with_password = '%s/%s.key.orig' % (self.cert_folder, service_name)
        key = '%s/%s.key' % (self.cert_folder, service_name)
        csr = '%s/%s.csr' % (self.cert_folder, service_name)
        public_certificate = '%s/%s.crt' % (self.cert_folder, service_name)
        self.run([self.openssl_command,
                  'genrsa',
                  '-des3',
                  '-out',
                  key_with_password,
                  '-passout',
                  'pass:%s' % password,
                  '2048'
                  ])
        self.run([self.openssl_command,
                  'rsa',
                  '-in',
                  key_with_password,
                  '-passin',
                  'pass:%s' % password,
                  '-out',
                  key
                  ])

        cert_cn = cn
        if cert_cn == None:
            cert_cn = self.host_name

        self.run([self.openssl_command,
                  'req',
                  '-new',
                  '-key',
                  key,
                  '-out',
                  csr,
                  '-subj',
                  '/C=%s/ST=%s/L=%s/O=%s/CN=%s/emailAddress=%s' % (
                      self.country_code, self.state, self.city, self.org_name, cert_cn, self.admin_email)
                  ])
        self.run([self.openssl_command,
                  'x509',
                  '-req',
                  '-days',
                  '365',
                  '-in',
                  csr,
                  '-signkey',
                  key,
                  '-out',
                  public_certificate
                  ])
        self.run([self.cmd_chown, '%s:%s' % (user, user), key_with_password])
        self.run([self.cmd_chmod, '700', key_with_password])
        self.run([self.cmd_chown, '%s:%s' % (user, user), key])
        self.run([self.cmd_chmod, '700', key])

    def get_pw(self, size=12, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def gen_kong_ssl_certificate(self):
        self.gen_cert('gluu-gateway', self.get_pw())
        self.kong_ssl_cert = self.dist_gluu_gateway_setup_folder + '/certs/gluu-gateway.crt'
        self.kong_ssl_key = self.dist_gluu_gateway_setup_folder + '/certs/gluu-gateway.key'

    def get_ip(self):
        test_ip = None
        detected_ip = None
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            detected_ip = [(test_socket.connect(('8.8.8.8', 80)),
                            test_socket.getsockname()[0],
                            test_socket.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        except:
            self.log_it("No detected IP address", True)
            self.log_it(traceback.format_exc(), True)
        if detected_ip:
            test_ip = self.get_prompt("Enter IP Address", detected_ip)
        else:
            test_ip = self.get_prompt("Enter IP Address")
        if not self.is_ip(test_ip):
            test_ip = None
            print ('ERROR: The IP Address is invalid. Try again\n')
        return test_ip

    def get_prompt(self, prompt, default_value=None):
        try:
            if default_value:
                user_input = input("%s [%s] : " % (prompt, default_value)).strip()
                if user_input == '':
                    return default_value
                else:
                    return user_input
            else:
                _input = False
                while not _input:
                    user_input = input("%s : " % prompt).strip()
                    if user_input != '':
                        _input = True
                        return user_input
        except KeyboardInterrupt:
            sys.exit()
        except:
            return None

    def install_plugins(self):
        print ("Installing kong plugins...")
        self.log_it('Installing kong plugins...')

        # json-logic-lua
        self.run([self.cmd_mkdir, '-p', '%s/rucciva' % self.dist_lua_folder])
        self.run([self.cmd_cp, self.json_logic_file_path, '%s/rucciva/json_logic.lua' % self.dist_lua_folder])

        # lua-resty-lrucache
        self.run([self.cmd_cp, '-R', '%s/lrucache' % self.lrucache_files_path, '%s/resty' % self.dist_lua_folder])
        self.run([self.cmd_cp, '%s/lrucache.lua' % self.lrucache_files_path, '%s/resty' % self.dist_lua_folder])

        # lua-resty-session
        self.run([self.cmd_cp, '-R', '%s/session' % self.lsession_files_path, '%s/resty' % self.dist_lua_folder])
        self.run([self.cmd_cp, '%s/session.lua' % self.lsession_files_path, '%s/resty' % self.dist_lua_folder])

        # lua-resty-jwt
        self.run([self.cmd_cp, '-a', self.jwt_files_path, '%s/resty' % self.dist_lua_folder])

        # lua-resty-hmac
        self.run([self.cmd_cp, '-a', self.hmac_files_path, '%s/resty' % self.dist_lua_folder])

        # Prometheus
        self.run([self.cmd_cp, self.prometheus_file_path, self.dist_lua_folder])

        # gluu plugins
        for plugin in self.kong_custom_plugins.split(","):
            self.run([self.cmd_cp, '-R', "%s/%s" % (self.gg_plugins_folder, plugin), self.dist_kong_plugins_folder])

        # gluu plugins common file
        self.run([self.cmd_cp, '-R', '%s' % self.gg_comman_folder, self.dist_lua_folder])

        # oxd-web-lua
        self.run([self.cmd_cp, self.oxd_web_lua_file_path, self.dist_gluu_lua_folder])

        # Disable kong stock auth plugins
        for plugin in self.disable_plugin_list:
            self.run([self.cmd_cp, '-R', '%s/disable-plugin-handler.lua' % self.gg_comman_folder, "%s/%s/handler.lua" % (self.dist_kong_plugins_folder, plugin)])
            if plugin == "ldap-auth":
                continue
            self.run([self.cmd_rm, '-rf', '%s/%s/migrations' % (self.dist_kong_plugins_folder, plugin)])
            self.run([self.cmd_rm, '-R', '%s/%s/daos.lua' % (self.dist_kong_plugins_folder, plugin)])

    def install_jre(self):
        self.log_it("Installing server JRE 1.8 %s..." % self.jre_version)
        jre_archive = 'server-jre-8u%s-linux-x64.tar.gz' % self.jre_version

        try:
            self.log_it("Extracting %s into %s/%s" % (jre_archive, self.gg_dist_app_folder, jre_archive))
            self.run(['tar', '-xzf', '%s/%s' % (self.gg_dist_app_folder, jre_archive), '-C', '/opt/', '--no-xattrs', '--no-same-owner', '--no-same-permissions'])
        except:
            self.log_it("Error encountered while extracting archive %s" % jre_archive)
            self.log_it(traceback.format_exc(), True)

        self.run([self.cmd_ln, '-sf', self.jre_destination_path, self.jre_home])
        self.run([self.cmd_chmod, '-R', '755', '%s/bin/' % self.jre_destination_path])
        with open('/etc/environment', 'a') as f:
            f.write('JAVA_HOME=/opt/jre')
        if self.os_type in [Distribution.Ubuntu, Distribution.Debian]:
            self.run([self.cmd_update_alternatives, '--install', '/usr/bin/java', 'java', '%s/bin/java' % (self.jre_home), '1'])
        elif self.os_type in [Distribution.CENTOS, Distribution.RHEL]:
            self.run([self.cmd_alternatives, '--install', '/usr/bin/java', 'java', '%s/bin/java' % (self.jre_home), '1'])

    def config_gluu_gateway_ui(self):
        self.log_it('Installing gluu_gateway_ui node packages...')
        print ('Installing gluu_gateway_ui node packages...')

        if not os.path.exists(self.cmd_node):
            self.run([self.cmd_ln, '-s', '`which nodejs`', self.cmd_node])

        try:
            self.run([self.cmd_mkdir, '-p', self.gg_node_modules_folder])
            self.log_it("Extracting %s into %s" % (self.gg_node_modules_archive, self.gg_node_modules_folder))
            self.run(['tar', '--strip', '1', '-xzf', '%s/%s' % (self.gg_dist_folder, self.gg_node_modules_archive), '-C', self.gg_node_modules_folder, '--no-xattrs', '--no-same-owner', '--no-same-permissions'])
        except:
            self.log_it("Error encountered while extracting archive %s" % self.gg_node_modules_archive)
            self.log_it(traceback.format_exc(), True)

        try:
            self.run([self.cmd_mkdir, '-p', self.gg_bower_modules_folder])
            self.log_it("Extracting %s into %s" % (self.gg_bower_modules_archive, self.gg_bower_modules_folder))
            self.run(['tar', '--strip', '1', '-xzf', '%s/%s' % (self.gg_dist_folder, self.gg_bower_modules_archive), '-C', self.gg_bower_modules_folder, '--no-xattrs', '--no-same-owner', '--no-same-permissions'])
        except:
            self.log_it("Error encountered while extracting archive %s" % self.gg_bower_modules_archive)
            self.log_it(traceback.format_exc(), True)

        if self.generate_client:
            msg = 'Creating OXD OP client for Gluu Gateway GUI used to call oxd-server endpoints...'
            self.log_it(msg)
            print (msg)
            oxd_registration_endpoint = self.gluu_gateway_ui_oxd_web + '/register-site'
            redirect_uri = 'https://' + self.gluu_gateway_ui_redirect_uri + ':' + self.gluu_gateway_ui_port
            payload = {
                'op_host': self.gluu_gateway_ui_op_host,
                'redirect_uris': [redirect_uri],
                'post_logout_redirect_uris': [redirect_uri],
                'scope': ['openid', 'oxd', 'permission', 'username'],
                'grant_types': ['authorization_code', 'client_credentials'],
                'client_name': 'KONGA_GG_UI_CLIENT'
            }

            oxd_registration_response = self.http_post_call(oxd_registration_endpoint, payload)
            self.gluu_gateway_ui_oxd_id = oxd_registration_response['oxd_id']
            self.gluu_gateway_ui_client_secret = oxd_registration_response['client_secret']
            self.gluu_gateway_ui_client_id = oxd_registration_response['client_id']

        # Render gluu_gateway_ui property
        self.run([self.cmd_touch, os.path.split(self.dist_gluu_gateway_ui_config_file)[-1]],
                 self.dist_gluu_gateway_ui_config_folder, os.environ.copy(), True)
        self.render_template_in_out(self.dist_gluu_gateway_ui_config_file, self.template_folder, self.dist_gluu_gateway_ui_config_folder)

        # konga db migration
        self.run(['npm', 'run', 'db-migrate', 'postgres://postgres:%s@localhost:5432/konga' % self.pg_pwd], self.dist_gluu_gateway_ui_folder, os.environ.copy(), True)

    def is_ip(self, address):
        try:
            socket.inet_aton(address)
            return True
        except socket.error:
            return False

    def log_it(self, msg, error_log=False):
        if error_log:
            f = open(self.log_error, 'a')
            f.write('%s %s\n' % (time.strftime('%X %x'), msg))
            f.close()
        f = open(self.log, 'a')
        f.write('%s %s\n' % (time.strftime('%X %x'), msg))
        f.close()

    def make_boolean(self, c):
        if c in ['t', 'T', 'y', 'Y']:
            return True
        if c in ['f', 'F', 'n', 'N']:
            return False
        self.log_it("make_boolean: invalid value for true|false: " + c, True)

    def make_folders(self):
        try:
            self.run([self.cmd_mkdir, '-p', self.cert_folder])
            self.run([self.cmd_mkdir, '-p', self.output_folder])
        except:
            self.log_it("Error making folders", True)
            self.log_it(traceback.format_exc(), True)

    def prompt_for_properties(self):
        # Certificate configuration
        self.ip = self.get_ip()
        self.host_name = self.get_prompt('Enter Hostname', self.detect_host_name())
        print ('The next few questions are used to generate the Kong self-signed HTTPS certificate')
        self.country_code = self.get_prompt('Enter two letter Country Code')
        self.state = self.get_prompt('Enter two letter State Code')
        self.city = self.get_prompt('Enter your city or locality')
        self.org_name = self.get_prompt('Enter Organization Name')
        self.admin_email = self.get_prompt('Enter Email Address')

        # Postgres configuration
        msg = """
If you already have a postgres user and database in the
Postgres DB, then enter existing password, otherwise enter new password: """
        print (msg)
        pg = self.get_pw()
        self.pg_pwd = getpass.getpass(prompt='Password [%s] : ' % pg) or pg

        # We are going to ask for 'OP host_name' regardless of whether we're installing oxd or not
        self.gluu_gateway_ui_op_host = 'https://' + self.get_prompt('OP Server Host')

        # Konga Configuration
        msg = """
The next few questions are used to configure Konga.
If you are connecting to an existing oxd server from other the network,
make sure it's available from this server."""
        print (msg)

        self.gluu_gateway_ui_oxd_web = self.get_prompt('Enter your existing OXD server URL')

        self.generate_client = self.make_boolean(self.get_prompt("Generate client credentials to call oxd-server API's? (y - generate, n - enter existing client credentials manually)", 'y'))

        if not self.generate_client:
            self.gluu_gateway_ui_oxd_id = self.get_prompt('OXD Id')
            self.gluu_gateway_ui_client_id = self.get_prompt('Client Id')
            self.gluu_gateway_ui_client_secret = self.get_prompt('Client Secret')

    def install_config_kong(self):
        # Install Kong
        kong_package_file = ''
        install_kong_cmd = []

        if self.os_type == Distribution.Ubuntu and self.os_version == '18':
            kong_package_file = "%s/%s" % (self.gg_dist_app_folder, self.ubuntu18_kong_file)
            install_kong_cmd = [self.cmd_dpkg, '--install', kong_package_file]

        if self.os_type == Distribution.CENTOS and self.os_version == '7':
            kong_package_file = "%s/%s" % (self.gg_dist_app_folder, self.centos7_kong_file)
            install_kong_cmd = [self.cmd_rpm, '--install', '--verbose', '--hash', kong_package_file]

        if self.os_type == Distribution.RHEL and self.os_version == '7':
            kong_package_file = "%s/%s" % (self.gg_dist_app_folder, self.rhel7_kong_file)
            install_kong_cmd = [self.cmd_rpm, '--install', '--verbose', '--hash', kong_package_file]

        if not os.path.exists(kong_package_file):
            self.log_it("%s is not found" % kong_package_file)
            sys.exit(0)

        self.run(install_kong_cmd)

        if self.os_type == Distribution.Ubuntu and self.os_version in ['18']:
            self.kong_lua_ssl_trusted_certificate = "/etc/ssl/certs/ca-certificates.crt"

        if self.os_type in [Distribution.CENTOS, Distribution.RHEL]:
            self.kong_lua_ssl_trusted_certificate = "/etc/ssl/certs/ca-bundle.crt"

        self.render_template_in_out(self.dist_kong_config_file, self.template_folder, self.dist_kong_config_folder)

    def render_template_in_out(self, file_path, template_folder, output_folder):
        self.log_it("Rendering template %s" % file_path)
        fn = os.path.split(file_path)[-1]
        f = open(os.path.join(template_folder, fn))
        template_text = f.read()
        f.close()
        newFn = open(os.path.join(output_folder, fn), 'w+')
        newFn.write(template_text % self.__dict__)
        newFn.close()

    def run(self, args, cwd=None, env=None, use_wait=False, shell=False):
        self.log_it('Running: %s' % ' '.join(args))
        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env, shell=shell)
            if use_wait:
                code = p.wait()
                self.log_it('Run: %s with result code: %d' % (' '.join(args), code))
            else:
                output, err = p.communicate()
                if output:
                    self.log_it(output)
                if err:
                    self.log_it(err, True)
        except:
            self.log_it("Error running command : %s" % " ".join(args), True)
            self.log_it(traceback.format_exc(), True)

    def migrate_kong(self):
        print ("Migrating kong db...")
        self.log_it("Migrating kong db...")
        self.run([self.cmd_kong, "migrations", "up"])
        self.run([self.cmd_kong, "migrations", "finish"])

    def start_gg_service(self):
        print ("Starting %s..." % self.gg_service)
        self.log_it("Starting %s..." % self.gg_service)
        if self.os_type == Distribution.Ubuntu and self.os_version in ['18']:
            self.run([self.cmd_systemctl, 'stop', self.gg_service])
            self.run([self.cmd_systemctl, 'start', self.gg_service])
            self.run([self.cmd_systemctl, 'enable', self.gg_service])
        elif self.os_type in [Distribution.CENTOS, Distribution.RHEL]:
            self.run([self.cmd_systemctl, 'stop', self.gg_service])
            self.run([self.cmd_systemctl, 'start', self.gg_service])
            self.run([self.cmd_systemctl, 'enable', self.gg_service])

    def copy_file(self, in_file, dest_folder):
        try:
            shutil.copy(in_file, dest_folder)
            self.log_it("Copied %s to %s" % (in_file, dest_folder))
        except:
            self.log_it("Error copying %s to %s" % (in_file, dest_folder), True)
            self.log_it(traceback.format_exc(), True)

    def disable_warnings(self):
        if self.os_type in [Distribution.Ubuntu, Distribution.CENTOS, Distribution.RHEL, Distribution.Debian]:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def choose_from_list(self, list_of_choices, choice_name="item", default_choice_index=0):
        return_value = None
        choice_map = {}
        chosen_index = 0
        print ("\nSelect the number for the %s from the following list:" % choice_name)
        for choice in list_of_choices:
            choice_map[chosen_index] = choice
            chosen_index += 1
            print ("  [%i]   %s" % (chosen_index, choice))
        while not return_value:
            choice_number = self.get_prompt("Please select a number listed above", str(default_choice_index + 1))
            try:
                choice_number = int(choice_number) - 1
                if (choice_number >= 0) & (choice_number < len(list_of_choices)):
                    return_value = choice_map[choice_number]
                else:
                    print ('"%i" is not a valid choice' % (choice_number + 1))
            except:
                print ('Cannot convert "%s" to a number' % choice_number)
                self.log_it(traceback.format_exc(), True)
        return return_value

    def detect_os_type(self):
        try:
            p = distro.linux_distribution()
            self.os_type = p[0].split()[0].lower()
            self.os_version = p[1].split('.')[0]
        except:
            self.os_type, self.os_version = self.choose_from_list(self.os_types, "Operating System")
        self.log_it('OS Type: %s OS Version: %s' % (self.os_type, self.os_version))

    def detect_initd(self):
        self.os_initdaemon = open(os.path.join('/proc/1/status'), 'r').read().split()[1]

    def http_post_call(self, endpoint, payload):
        response = None
        try:
            response = requests.post(endpoint, data=json.dumps(payload), headers={'content-type': 'application/json'},  verify=False)
            response_json = json.loads(response.text)

            if response.ok:
                return response_json
            else:
                message = """Error: Failed Not Ok Endpoint: %s 
                Payload %s
                Response %s 
                Response_Json %s
                Please check logs.""" % (endpoint, payload, response, response_json)
                self.exit(message)

        except requests.exceptions.HTTPError as e:
            message = """Error: Failed Http Error:
                Endpoint: %s 
                Payload %s
                Response %s
                Error %s 
                Please check logs.""" % (endpoint, payload, response, e)
            self.exit(message)
        except requests.exceptions.ConnectionError as e:
            message = """Error: Failed to Connect:
                Endpoint: %s 
                Payload %s
                Response %s
                Error %s 
                Please check logs.""" % (endpoint, payload, response, e)
            self.exit(message)
        except requests.exceptions.RequestException as e:
            message = """Error: Failed Something Else:
                Endpoint %s 
                Payload %s
                Response %s
                Error %s 
                Please check logs.""" % (endpoint, payload, response, e)
            self.exit(message)

    def http_get_call(self, endpoint):
        response = None
        try:
            response = requests.get(endpoint, headers={'content-type': 'application/json'}, verify=False)

            response_json = json.loads(response.text)
            return response_json

        except requests.exceptions.HTTPError as e:
            message = """Error: Failed Http Error:
                Endpoint: %s 
                Response %s
                Error %s 
                Please check logs.""" % (endpoint, response, e)
            self.exit(message)
        except requests.exceptions.ConnectionError as e:
            message = """Error: Failed to Connect:
                Endpoint: %s 
                Response %s
                Error %s 
                Please check logs.""" % (endpoint, response, e)
            self.exit(message)
        except requests.exceptions.RequestException as e:
            message = """Error: Failed Something Else:
                Endpoint %s 
                Response %s
                Error %s 
                Please check logs.""" % (endpoint, response, e)
            self.exit(message)

    def exit(self, message):
        print (message)
        self.log_it(message, True)
        sys.exit()

    def configure_kong_rotate(self):
        self.log_it("Configuring log rotate for kong")
        self.run([self.cmd_cp, '%s/%s' % (self.template_folder, self.kong_log_rotate_config_file), "%s/kong" % self.dist_kong_log_rotate_config_path])

    def check_root(self):
        try:
            user = pwd.getpwuid(os.getuid()).pw_name
            print (user)
            if user != "root":
                msg="Your user is not root user, Run setup script in root user."
                print (msg)
                self.log_it(msg, True)
                sys.exit()
        except Exception as err:
            self.log_it("Failed to execute `pwd.getpwuid(os.getuid()).pw_name` %s " % err, True)

if __name__ == "__main__":
    kongSetup = KongSetup()
    kongSetup.check_root()
    try:
        if kongSetup.is_prompt:
            kongSetup.license = kongSetup.make_boolean(kongSetup.get_prompt('Do you acknowledge that use of the Gluu Gateway is under the Apache 2.0 License? (y|N)', 'N'))
            print ("")
        if kongSetup.license:
            kongSetup.make_folders()
            if kongSetup.is_prompt:
                kongSetup.prompt_for_properties()
            print ("\n")
            print ("-----------------------".ljust(30) + "-----------------------".rjust(35) + "\n")
            cnf = 'Host'.ljust(30) + kongSetup.host_name.rjust(35) + "\n" \
                  + 'Organization'.ljust(30) + kongSetup.org_name.rjust(35) + "\n" \
                  + 'City'.ljust(30) + kongSetup.city.rjust(35) + "\n" \
                  + 'State'.ljust(30) + kongSetup.state.rjust(35) + "\n" \
                  + 'Country'.ljust(30) + kongSetup.country_code.rjust(35) + "\n" \
                  + 'OXD Server URL'.ljust(30) + kongSetup.gluu_gateway_ui_oxd_web.rjust(35) + "\n" \
                  + 'OP Host'.ljust(30) + kongSetup.gluu_gateway_ui_op_host.rjust(35) + "\n"

            if not kongSetup.generate_client:
                cnf += 'OXD Id'.ljust(30) + kongSetup.gluu_gateway_ui_oxd_id.rjust(35) + "\n" \
                       + 'Client Id'.ljust(30) + kongSetup.gluu_gateway_ui_client_id.rjust(35) + "\n" \
                       + 'Client Secret'.ljust(30) + kongSetup.gluu_gateway_ui_client_secret.rjust(35) + "\n"
            else:
                cnf += 'Generate Client Credentials?'.ljust(30) + repr(kongSetup.generate_client).rjust(35) + "\n"

            print (cnf)
            kongSetup.log_it(cnf)

            if kongSetup.is_prompt:
                proceed = kongSetup.make_boolean(kongSetup.get_prompt('Proceed with these values (Y|n)', 'Y'))
            else:
                proceed = True

            if proceed:
                kongSetup.detect_os_type()
                kongSetup.detect_initd()
                kongSetup.disable_warnings()
                kongSetup.gen_kong_ssl_certificate()
                kongSetup.install_jre()
                kongSetup.configure_kong_rotate()
                kongSetup.configure_postgres()
                kongSetup.install_config_kong()
                kongSetup.install_plugins()
                kongSetup.migrate_kong()
                kongSetup.config_gluu_gateway_ui()
                kongSetup.start_gg_service()
                print ("\n\nGluu Gateway configuration is successful!!! https://localhost:%s\n\n" % kongSetup.gluu_gateway_ui_port)
            else:
                print ("Exit")
        else:
            print ("Exit")
    except:
        kongSetup.log_it("***** Error caught in main loop *****", True)
        kongSetup.log_it(traceback.format_exc(), True)
        print ("Installation failed. See: \n  %s \n  %s \nfor more details." % (kongSetup.log, kongSetup.log_error))
