mkdir zabbix_istall
cd zabbix_istall

touch addr.txt

# Ввод переменных через ;
echo "Введите значения переменных в формате VAR1;VAR2:"
read input_variables

# Разделяем введенные значения по символу ;
IFS=";" read VAR1 VAR2 <<< "$input_variables"

# Вывод значений переменных
echo "VAR1 = $VAR1"
echo "VAR2 = $VAR2"

# Запись переменных в файл addr.txt
echo "$VAR1;$VAR2" > addr.txt

curl -l https://raw.githubusercontent.com/YAbl0K0/Zabbix_test/main/Import_zabbix.py
chmod +x Import_zabbix.py
./import_zabbix.py

#Install
wget https://repo.zabbix.com/zabbix/5.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.4-1+ubuntu20.04_all.deb
sudo dpkg -i zabbix-release_5.4-1+ubuntu20.04_all.deb
sudo apt update


sudo apt install zabbix-agent
# Путь к файлу Zabbix.cnf
file_path="/etc/zabbix/zabbix_agentd.conf"

# Используем команду sed для замены значения переменной Server на значение VAR1 в файле
sed -i "s/^ServerActive=.*/ServerActive=$VAR1/" "$file_path"
sed -i "s/^HostName=.*/HostName=$VAR2/" "$file_path"
#Start
service zabbix-agent start
#Check
systemctl status zabbix-agent.service
