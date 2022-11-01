String text = "";

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {

if (Serial.available()) {
    text = Serial.readString();
  
  }

if(check("test")){

    Serial.println("test detected");
    //Your code
}

if(check("hello")){

    Serial.println("hello detected");
    //Your code
}


    

}



boolean check( String cmp){
  text.trim();
  if(text.equals(cmp)){
    text ="";
    return true;
  
  }
  
  return false;
  
}
