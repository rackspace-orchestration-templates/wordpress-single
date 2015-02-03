from fabric.api import env, task
from envassert import detect, file, port, process, service, user
from hot.utils.test import get_artifacts, http_check


@task
def check():
    env.platform_family = detect.detect()

    assert file.exists('/var/www/vhosts/example.com/xmlrpc.php'),\
        'xmlrpc.php did not exist'

    assert port.is_listening(21), 'port 21/vsftpd is not listening'
    assert port.is_listening(80), 'port 80/varnishd is not listening'
    assert port.is_listening(3306), 'port 3306/mysqld is not listening'
    assert port.is_listening(6082), 'port 6082/varnishd is not listening'
    assert port.is_listening(8080), 'port 8080/apache2 is not listening'
    assert port.is_listening(11211), 'port 11211/memcached is not listening'

    assert user.exists('ftp'), 'ftp user does not exist'
    assert user.exists('varnish'), 'varnish user does not exist'
    assert user.exists('varnishlog'), 'varnishlog user does not exist'
    assert user.exists('mysql'), 'mysql user does not exist'
    assert user.exists('memcache'), 'memcache user does not exist'
    assert user.exists('wp_user'), 'wp_user user does not exist'

    assert process.is_up('apache2'), 'apache2 is not running'
    assert process.is_up('mysqld'), 'mysqld is not running'
    assert process.is_up('varnishd'), 'varnishd is not running'
    assert process.is_up('memcached'), 'memcached is not running'
    assert process.is_up('vsftpd'), 'vsftpd is not running'

    assert service.is_enabled('apache2'), 'apache2 service not enabled'
    assert service.is_enabled('mysql'), 'mysql service not enabled'
    assert service.is_enabled('varnish'), 'varnish service not enabled'
    assert service.is_enabled('varnishlog'), 'varnishlog service not enabled'
    assert service.is_enabled('memcached'), 'memcached service not enabled'
    assert service.is_enabled('vsftpd'), 'vsftpd service not enabled'

    assert http_check('http://localhost/', 'Powered by WordPress')


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
