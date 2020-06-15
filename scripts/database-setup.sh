echo -e ""
echo -e "\e[1m**************************************************************************************************"
echo -e "\e[1mStarting the MYSQL installation and database creation..."
echo -e "\e[1m**************************************************************************************************"
echo -e ""

sudo apt-get update

echo -e "\e[1mInstalling packages..."
sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev
sudo apt-get install libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev python3.6-dev

echo -e ""
echo -e "\e[1m**************************************************************************************************"
echo -e "\e[1mStarting MYSQL Installation..."
echo -e "\e[1mYou will be asked to enter password for MYSQL. Please enter the following password: onlinepayment"
echo -e "\e[1m**************************************************************************************************"
echo -e ""
sudo mysql_install_db
sudo mysql_secure_installation

echo -e "\e[1mCreating a new database named onlinepayment"
mysql -uroot -ponlinepayment -e "CREATE DATABASE onlinepayment CHARACTER SET UTF8"

echo -e "\e[1mCreating a user named onlinepayment for database access..."
mysql -uroot -ponlinepayment -e "CREATE USER onlinepayment@localhost IDENTIFIED BY 'onlinepayment';"

echo -e "\e[1mGranting all access and privilages to the new user..."
mysql -uroot -ponlinepayment -e "GRANT ALL PRIVILEGES ON onlinepayment.* TO onlinepayment@localhost;"
mysql -uroot -ponlinepayment -e "FLUSH PRIVILEGES;"

echo -e ""
echo -e "\e[1m************************************************************************************"
echo -e "\e[1mMYSQL Installation Complete!"
echo -e "\e[1mA new database named onlinepayment has been created successfully!"
echo -e "\e[1mHAPPY CODING!"
echo -e "\e[1m************************************************************************************"