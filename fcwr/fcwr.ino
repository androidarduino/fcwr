#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN 7

// How many NeoPixels are attached to the Arduino?
#define BRIDES 12
#define NUMPIXELS 25
#define OFF 0
#define ON 1
#define FLASH 2
#define FAVORITE 3
#define MUSIC 4
#define UP 5
#define DOWN 6
#define BURST 7
// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(BRIDES * NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 500; // delay for half a second
int state = OFF;
unsigned int c[BRIDES];
int leds[BRIDES];

void setup() {
  Serial.begin(115200);
  pixels.begin(); // This initializes the NeoPixel library.
  for (int i=0;i<BRIDES;i++) {
    leds[i]=OFF;
    c[i]=0;
    setAll(i,128,128,0);
  }
}

/*states: OFF, ON, FLASH, SETTING
transitions: OFF-short->ON, ON-long->FLASH, ON-short->OFF, OFF-long->SETTING, FLASH-short->OFF, SETTING-short-...-short-long->OFF

off->on: water filling effect
on: breathing effect
on->flash: explode effect
flash: flashing color effect
off: all black effect
*/

void loop() {
  //Receive command from serial port
  //update LED segments accordingly
  //call LED segments' processing unit with their counters
   while (Serial.available() > 0) {
      int oldStatus = Serial.parseInt();
      int newStatus = Serial.parseInt();
      int object = Serial.parseInt() - 1;
      if (Serial.read() == '\n') {
        Serial.println("200");
        if (object > BRIDES) return;
        if (object == -1) {
          allLights(newStatus);
          updateLEDs();
          delay(20);
          return;
        }
        if (oldStatus == OFF && newStatus == ON) leds[object] = UP;
        if (oldStatus == ON && newStatus == FLASH) leds[object] = BURST;
        if (oldStatus != OFF && newStatus == ON) leds[object] = ON;
        if (newStatus == OFF) leds[object] = newStatus;
        if (newStatus == FAVORITE) {
          for(int i=0;i<BRIDES;i++) leds[i]=OFF;
          leds[object] = FAVORITE;
        }
      }
   }
   updateLEDs();
   delay(20);
}

void allLights(int newStatus) {
  for(int i=0;i<BRIDES;i++) {
    leds[i] = newStatus;
    c[i]=0;
  }  
}

void updateLEDs() {
  for(int i=0;i<BRIDES;i++) {
      if (leds[i] == UP) {
        waterFilling(++c[i], i);
      }
      if (leds[i] == ON) {
        breathing(++c[i], i);
      }
      if (leds[i] == OFF) {
        off(++c[i], i);
      }
      if (leds[i] == BURST) {
        explode(++c[i], i);
      }
      if (leds[i] == FLASH) {
        flash(++c[i], i);
      }
      if (leds[i] == FAVORITE) {
        favorite(++c[i], i);
      }
      if (leds[i] == MUSIC) {
        music(++c[i], i);
      }
      if (c[i]>60000) c[i]-=60000;
  }
  pixels.show();
}

void favorite(int counter, int base) {
  // favorite girl, display yellow for base, all other lights off
  for(int i=0;i<BRIDES;i++) 
    if(i==base)
      setAll(base, 255,255,0);
    else
      off(0,i);
}

void music(int counter, int base) {
  // TODO: get mic input, set lights based on input value as a shift register
  return;
}

//counter++ every 50ms, this function will be called every 50ms too. return true when the process has finished.
bool waterFilling(int counter, int base) {
  int Counter = counter;
  //Fill the strip within 25 loops, which is 1.25s
  counter = counter % NUMPIXELS;
  for (int i= base * NUMPIXELS;i< base*NUMPIXELS + NUMPIXELS;i++) {
    if (i <= base*NUMPIXELS + counter)
      pixels.setPixelColor(i, pixels.Color(255,50,50));
    else
      pixels.setPixelColor(i, pixels.Color(0,0,0));
    //pixels.show();    
  }
  if (Counter % NUMPIXELS == NUMPIXELS - 1) {
    leds[base] = ON;
    return true;
  }
  return false;
}

bool breathing(int counter, int base) {
  //Breath in red, interval 3s
  int INTERVAL = 3000/50;
  counter = counter % INTERVAL;
  if (counter > INTERVAL/2) counter = INTERVAL-counter;
  counter = counter * (200*2/INTERVAL) + 55;
  setAll(base, counter, 20, 20);
  //Always return false, never end the loop
  return false;
}

bool explode(int counter, int base) {
  //Show bright white explosion for 0.5s
  int Counter = counter;
  int INTERVAL = 500/50;
  counter = counter % INTERVAL;
  if (counter > INTERVAL) counter = INTERVAL-counter;
  counter = counter * (255*2/INTERVAL);
  setAll(base, counter, counter, counter);
  if (Counter % INTERVAL == 0) {
    leds[base] = FLASH;
    return true;
  }
  return false;
}

bool flash(int counter, int base) {
  //Change pattern every 0.15s
  counter = counter % (300/100);
  if (counter == 0) {
    for(int i= base*NUMPIXELS;i<base*NUMPIXELS + NUMPIXELS;i++) {
      pixels.setPixelColor(i, pixels.Color(random(255),random(255),random(255)));
      //pixels.show();
    }
  }
  return false;
}

bool off(int, int base) {
  
  setAll(base, 0,0,0);
  return true;
}

void setAll(int base, int R, int G, int B) {
  for(int i=base*NUMPIXELS;i<base*NUMPIXELS+NUMPIXELS;i++){
    pixels.setPixelColor(i, pixels.Color(R,G,B));
    //pixels.show();
  }
}

