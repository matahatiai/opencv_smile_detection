// @author : fajarlabs

#include <LiquidCrystal_I2C.h>
#include <TimedAction.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
unsigned long lastMillis = 0;
int dataSerial = 0;
int LED = 13;
bool lockLCD = false;

void processSerial() {
  if(dataSerial == '1') {
    if(!lockLCD) {
      clearLCDLine(1);
      lcd.print(">> BUKA");
      digitalWrite(LED, HIGH); // sets the LED on
      lockLCD = !lockLCD;
    }
  } else {
    if(lockLCD){
      clearLCDLine(1);
      lcd.print(">> TUTUP");
      digitalWrite(LED, LOW); // sets the LED on
      lockLCD = !lockLCD;
    }
  }
}

TimedAction timedAction = TimedAction(100,processSerial);

void setup() { 
  lcd.begin();
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite (LED, LOW);
  Serial.println("Halo, ini adalah pesan dari arduino!");
  lcd.setCursor(0,1);
  lcd.print(">> TUTUP");
  lcd.setCursor(0,0);
  lcd.print("SENYUM DONG :)");
}

void loop() {
   timedAction.check();
  while (Serial.available()) {
    dataSerial = Serial.read();
  }
}

void clearLCDLine(int line){
 for(int n = 0; n < 20; n++) { // 20 indicates symbols in line. For 2x16 LCD write - 16
   lcd.setCursor(n,line);
   lcd.print(" ");
 }
 lcd.setCursor(0,line); // set cursor in the beginning of deleted line
}