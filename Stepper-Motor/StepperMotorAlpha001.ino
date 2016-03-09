#include <Stepper.h>
 
 const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
                          // for your motor
 float pasi = 20;         //PASI PE COMANDA
 int comanda = 0; 
 int comandafin = 0;
 float speed = 2;        //VITEZA PE COMANDA
 //int Stanga;
 //int Dreapta;
 //int Sus;
 //int Jos;
 
 // initialize the stepper library on the motor shield
 Stepper myStepperX(stepsPerRevolution, 9, 10, 11 ,12);
 Stepper myStepperZ(stepsPerRevolution, 3, 4, 5, 6); 
 
 // give the motor control pins names:
 const int En2A = 2; 
 const int En2B = 7;
 const int EnA = 8;
 const int EnB = 13;
 

void setup() {
 Serial.begin(9600);
 // set the PWM and brake pins so that the direction pins  // can be used to control the motor:
 pinMode(EnA, OUTPUT);
 pinMode(EnB, OUTPUT);
 pinMode(En2A, OUTPUT);
 pinMode(En2B, OUTPUT);
 Serial.println("Use Numpad 2-4-6-8 to move motors!");
 
 //digitalWrite(EnA, HIGH);
 //digitalWrite(EnB, HIGH);
 //digitalWrite(En2A, HIGH);
//digitalWrite(En2B, HIGH);
 // initialize the serial port:

 // set the motor speed (for multiple steps only):
 myStepperX.setSpeed(speed);
 myStepperZ.setSpeed(speed);
 }

 
 void loop() {
 
  //myStepper.step(500);
  //delay(500);
  //myStepper.step(-500);
  //myStepper2.step(500);
  //delay(500);
  //myStepper2.step(-500);
 
 
 
 }
 void serialEvent()
 {
   if(Serial.available() )
  {
    comanda = Serial.read();
    comandafin = comanda - '0';
    Serial.print("Received: ");
    Serial.print(comandafin);
    motorsStart();
    if (comandafin == 4)
    {
      MotorSt();
      Serial.println(" =>  Stanga");
    }
   
    if (comandafin == 6)
    {
      MotorDr();
      Serial.println(" =>  Dreapta");
    }
   
    if (comandafin == 8)
    {
      MotorFt();
      Serial.println(" =>  Fata");
    }
    
    if(comandafin == 2)
    
    {
      MotorSp();
      Serial.println(" =>  Spate");
    }
    
    if(comandafin == 7)
    {
      SusSt(25);
      Serial.println(" => Stanga Fata");
    }
    if(comandafin == 9)
    {
      SusDr(25);
      Serial.println(" => Dreapta Fata");
    }
    
    if(comandafin == 3)
    {
      JosDr(25);
      Serial.println(" => Dreapta Spate");
    }
    
    if(comandafin == 1)
    {
      JosSt(25);
      Serial.println(" => Stanga Spate");
    }
    
    if(comandafin == 0)
    {
    desenPatrat(50);
    }
    
    if(comandafin == 49){
    parabola(-50, 50);
    }
    
    if(comandafin == 50){
    parabolaX3(-20, 20);
    }
    
    if(comandafin == 51){
    parabolaX4(-10, 10);
    }
    
     motorsStop();
  }
}
//============================= Simplu
void MotorDr()
{
  myStepperZ.step(-pasi);
}

void MotorSt()
{
  myStepperZ.step(pasi);
}


void MotorFt()
{
  myStepperX.step(pasi);
}

void MotorSp()
{
  myStepperX.step(-pasi);
}

//============================== Parametri
void pMotorDr(int parametru)
{
  myStepperZ.step(-parametru);
}

void pMotorSt(int parametru)
{
  myStepperZ.step(parametru);
}


void pMotorFt(int parametru)
{
  myStepperX.step(parametru);
}

void pMotorSp(int parametru)
{
  myStepperX.step(-parametru);
}
//============================= Diagonale 
void SusSt(int parametru){
 for(int i = 1; i <= parametru; i++){
  pMotorFt(1);
  pMotorSt(1); 
  }
}

void SusDr(int parametru){
 for(int i = 1; i <= parametru; i++){
  pMotorFt(1);
  pMotorDr(1); 
  }
}
void JosSt(int parametru){
 for(int i = 1; i <= parametru; i++){
  pMotorSp(1);
  pMotorSt(1); 
  }
}
void JosDr(int parametru){
 for(int i = 1; i <= parametru; i++){
  pMotorSp(1);
  pMotorDr(1); 
  }
}
//============================== Patrat
void desenPatrat(int marime){
 pMotorDr(marime);
 pMotorFt(marime);
 pMotorSt(marime);
 pMotorSp(marime);
}
//============================== Parabola X^2

void parabola(int xStart, int xFin){
  for(int i = xStart; i <= xFin; i++){
  pMotorSp(1);
  pMotorDr((2*i + 1)/ 10 );
  Serial.println((2*i + 1)/10); 
  }
}
//============================== Parabola X^3

void parabolaX3(int xStart, int xFin){
  for(int i = xStart; i <= xFin; i++){
  pMotorSp(1);
  int calculMiscare = (6*i + 1)/ 10;
  int movement = pow(calculMiscare, 2) ;
  int movementAbsolut = pow(movement, 0.5);
  pMotorDr(-movementAbsolut);
  Serial.println("Parabola X^3");
  Serial.println(movementAbsolut); 
  }
}
//============================== Parabola X^4

void parabolaX4(int xStart, int xFin){
  for(int i = xStart; i <= xFin; i++){
  pMotorSp(2);
  pMotorDr((24*i + 1)/ 10 );
  Serial.println((24*i + 1)/10); 
  }
}
void motorsStart(){
  digitalWrite(EnA, HIGH);
  digitalWrite(EnB, HIGH);
  digitalWrite(En2A, HIGH);
  digitalWrite(En2B, HIGH);
}

void motorsStop(){
  digitalWrite(EnA, LOW);
  digitalWrite(EnB, LOW);
  digitalWrite(En2A, LOW);
  digitalWrite(En2B, LOW);
}
   
