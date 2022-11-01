
//Output to motor driver
int dOut[5]={A0,A1,A2,A3,A4};

//Release timing
int tgap = 2000;

//Release flashing led pin
int wLed = 13;


/*Serial Output Details
 *=====================
 * left - 0
 * up - 1
 * right - 2
 * down - 3
 * release - 4
 * no detection - 5
 */
/*Ultrasound Sensors
 * =================
 * left   sensor (trig-2,echo-3)
 * right  sensor (trig-4,echo-5)
 * up     sensor (trig-6,echo-7)
 * down   sensor (trig-8,echo-9)
 * relese sensor (trig-10,echo-11)
 */

 /*Output Pins
  * Left    - A0
  * Right   - A1
  * Up      - A2
  * Down    - A3
  * Release - A4
  * Flashing Led For Release Timing - D13
  */

//Sensor Detection Limit In CM
int detect_limit = 8;

#include <Ultrasonic.h>

Ultrasonic ultrasonic1(2, 3,5000UL);  // Left
Ultrasonic ultrasonic2(4, 5,5000UL);  // Right
Ultrasonic ultrasonic3(6, 7,5000UL);  // Up
Ultrasonic ultrasonic4(8, 9,5000UL);  // Down
Ultrasonic ultrasonic5(10, 11,5000UL);  // Release



void setup() {
  Serial.begin(115200);
  pinMode(wLed,OUTPUT);
  //Define Outputs

  for(int i = 0;i<5;i++){
    pinMode(dOut[i],OUTPUT);
    /*
    digitalWrite(dOut[i],HIGH);
    delay(100);
    digitalWrite(dOut[i],LOW);
    delay(100);
    */
  }

  
}

void loop() {

//Left Sensor
while(rSensor(1)<detect_limit){
  Serial.println("0");
  setOutput(0);
}

//Right Sensor
while(rSensor(2)<detect_limit){
  Serial.println("2");
  setOutput(1);
}

//Up Sensor
while(rSensor(3)<detect_limit){
  Serial.println("1");
  setOutput(2);
}

//Down Sensor
while(rSensor(4)<detect_limit){
  Serial.println("3");
  setOutput(3);
}



//Release Sensor
long t = millis();

while(rSensor(5)<detect_limit){

  
  while(rSensor(5)< detect_limit && tgap > millis()-t){
    setOutput(5);
    digitalWrite(wLed,HIGH);
    delay(100);
    digitalWrite(wLed,LOW);
    delay(100);
     
  }

  
  if(millis()-t > tgap){
    Serial.println("4");
    setOutput(4);
    digitalWrite(wLed,HIGH);
    
  }
}


//No Sensor Detections

digitalWrite(wLed,LOW);
setOutput(5);
Serial.println("5");




}




int rSensor(int a){
if(a==1)
return constrain(ultrasonic1.read(), 0, 30);
else if(a==2)
return constrain(ultrasonic2.read(), 0, 30);
else if(a==3)
return constrain(ultrasonic3.read(), 0, 30);
else if(a==4)
return constrain(ultrasonic4.read(), 0, 30);
else if(a==5)
return constrain(ultrasonic5.read(), 0, 30);
else
return 0;

}


void printReadings(){
int x1=rSensor(1);
int x2=rSensor(2);
int x3=rSensor(3);
int x4=rSensor(4);
int x5=rSensor(5);
 
Serial.print(x1);
Serial.print(",");
Serial.print(x2);
Serial.print(",");
Serial.print(x3);
Serial.print(",");
Serial.print(x4);
Serial.print(",");
Serial.print(x5);
Serial.println(); 
}


void setOutput(int a){

  for(int i = 0;i<5;i++){
    if(i == a){
      digitalWrite(dOut[i],HIGH);
      delay(100);
    }

    else{
      digitalWrite(dOut[i],LOW);
    }
  }
}
