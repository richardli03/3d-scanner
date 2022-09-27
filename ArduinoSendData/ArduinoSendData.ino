
//      ******************************************************************
//      *                                                                *
//      *                                                                *
//      *     Example Arduino program that transmits data to a laptop    *
//      *                                                                *
//      *                                                                *
//      ******************************************************************


//
// setup function to initialize hardware and software
//
const int analogInPin = A4; 
int d = 0;
void setup()
{ 
  //
  // start the serial port
  //
  long baudRate = 9600;       // NOTE1: The baudRate for sending & receiving programs must match
  Serial.begin(baudRate);     // NOTE2: Set the baudRate to 115200 for faster communication
}



//
// main loop
//
void loop() 
{  
   //
  // loop: calculate the data, then send it from the Arduino to the phython program
  //
  while(true) {
    //
    // here is where you update the data to be sent
    //   
    //
    // transmit one line of text to phython with 4 numeric values
    // NOTE: commas are sent between values, after the last value a Newline is sent
    //
    d = analogRead(analogInPin);
    Serial.println(d);
    

    //
    // delay after sending data so the serial connection is not over run
    //
    delay(40);
  }
}
