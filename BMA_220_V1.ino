#include <BMA220.h>

BMA220 bma;
int quick[100], quickx[100], quicky[100];
float HighValues, HighValuesx, HighValuesy, Most, Mostx, Mosty;
float data, datax, datay;

void setup() {
  Serial.begin(9600);
  if (!bma.begin()) {
    Serial.println(F("No valid BMA220 sensor found, check wiring"));
    //        while (true):  // stop here, no reason to go on...
    //            ;
  }
  bma.setRegister(SENSITIVITY_REG, SENS_2g);
  bma.setRegister(FILTER_REG, FILTER_500Hz);
  HighValues = 0;
  Most = 0;
}

void loop() {
  //    Serial.print("x-axis: ");
  //   Serial.print(bma.readAcceleration(XAXIS));
  //    Serial.print("\t");
  //    Serial.print("y-axis: ");
  //   Serial.print(bma.readAcceleration(YAXIS));
  //  Serial.print("\t");
  //    Serial.print("z-axis: ");
  //    Serial.println(bma.readAcceleration(ZAXIS));
  for (int n = 0; n<5; n++) {
    for (int i = 0; i<50; i++) {
      quickx[i] = abs(bma.readAcceleration(XAXIS));
      Mostx = max(quickx[i],Mostx);
      quicky[i] = abs(bma.readAcceleration(YAXIS));
      Mosty = max(quicky[i],Mosty);
      quick[i] = abs(bma.readAcceleration(ZAXIS));
      Most = max(quick[i],Most);
      //delay(1);      
    }
    HighValues = Most + HighValues;
    HighValuesx = Mostx + HighValuesx;
    HighValuesy = Mosty + HighValuesy;
    Most = Mostx = Mosty = 0;
  }
  data = HighValues/5;
  datax = HighValuesx/5;
  datay = HighValuesy/5;
  Serial.print("Accelerator Reading: ");
//  Serial.print(datax);
//  Serial.print("\t");
//  Serial.print(datay);
//  Serial.print("\t");
  Serial.println(data);
  
  
  HighValues = HighValuesx = HighValuesy = 0;
}
