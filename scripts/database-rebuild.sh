echo -e ""
echo -e "\e[1m**************************************************************************************************"
echo -e "\e[1mThis script will drop the existing database and create a new one."
echo -e "\e[1m**************************************************************************************************"
echo -e ""

echo -e "\e[1mDroping existing database..."
mysql -uonlinepayment -ponlinepayment -e "DROP DATABASE onlinepayment"

echo -e "\e[1mCreating a new database named onlinepayment"
mysql -uonlinepayment -ponlinepayment -e "CREATE DATABASE onlinepayment CHARACTER SET utf8mb4"

python manage.py migrate


echo -e ""
echo -e "\e[1m************************************************************************************"
echo -e "\e[1mA new database named onlinepayment has been created successfully!"
echo -e "\e[1mHAPPY CODING!"
echo -e "\e[1m************************************************************************************"