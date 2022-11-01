int x;

int out[5] = {8,9,10,11,12};

bool state = true;
void setup() {

 for(int i =0;i<5;i++)
  pinMode(out[i],OUTPUT);
  
 Serial.begin(115200);
 Serial.setTimeout(1);

 pinMode(13,OUTPUT);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 Serial.print(x);

 if(x ==1){
  digitalWrite(13,state);
  //delay(10);
  state = !state;
 }

 output(x);
}



void output(int i){

for(int k = 0;k<5;k++){
  if(k == i)
    digitalWrite(out[k],HIGH);

  else
    digitalWrite(out[k],LOW);

}
}
