#install mysql-server

class {'mysql::server':
	config_hash => {'root_password' => 'youwillneverknow'},
}

# Create user

class {'mysql::backup':
	backupuser => 'backup',
	backuppassword => '123456',
	backupdir => '/var/backup/',

}

