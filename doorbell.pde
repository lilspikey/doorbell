#include <Servo.h>

#define DOORBELL_PIN 5
#define SERVO_PIN 9

#define ANALOG_START 14

#define STATE_INIT_POSITION 0
#define STATE_WAITING 1
#define STATE_BELL_FORWARD 2
#define STATE_BELL_BACKWARD 3
#define STATE_FINISH 4

#define DOORBELL_THRESHOLD 400

#define DOORBELL_INIT_ANGLE 70
#define DOORBELL_BACKWARD_ANGLE 90
#define DOORBELL_FORWARD_ANGLE 180


Servo servo;
int state;
unsigned long prev_millis;
unsigned int duration;
unsigned int start_count;
unsigned int ring_count;
unsigned int finish_count;


void next_state(int nstate, unsigned int nduration=0) {
  state = nstate;
  prev_millis = millis();
  duration = nduration;
}

void same_state() {
  prev_millis = millis();
  duration = 100;
}

void ring_bell() {
  // ensure servo attached again
  servo.attach(SERVO_PIN);
  ring_count = 3;
  Serial.println("DING DONG");
  next_state(STATE_BELL_FORWARD);
}

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  // enable pullup resistor
  pinMode(ANALOG_START + DOORBELL_PIN, INPUT);
  digitalWrite(ANALOG_START + DOORBELL_PIN, HIGH);
  next_state(STATE_INIT_POSITION);
}

void loop() {
  if ( Serial.available() ) {
    char c = Serial.read();
    
    // run command
    if ( c == 'T' ) {
      if ( state == STATE_WAITING ) {
        ring_bell();
      }
    }
  }
  
  if ( (millis() - prev_millis) > duration ) {
    switch(state) {
      case STATE_INIT_POSITION: {
        start_count = 0;
        servo.write(DOORBELL_INIT_ANGLE);
        next_state(STATE_WAITING, 1000);
      }
      break;
      case STATE_WAITING: {
        int v = analogRead(DOORBELL_PIN);
        if ( v <= DOORBELL_THRESHOLD ) {
          start_count++;
          if ( start_count > 2 ) {
            ring_bell();
          }
          else {
            same_state();
          }
        }
        else {
          start_count = 0;
          if ( servo.attached() ) {
            // turn off servo
            // so to avoid buzzing from it being
            // overloaded
            servo.detach();
          }
          same_state();
        }
      }
      break;
      case STATE_BELL_FORWARD: {
        if ( ring_count ) {
          servo.write(DOORBELL_FORWARD_ANGLE);
          next_state(STATE_BELL_BACKWARD, 500);
        }
        else {
          finish_count = 0;
          next_state(STATE_FINISH);
        }
      }
      break;
      case STATE_BELL_BACKWARD: {
        servo.write(DOORBELL_BACKWARD_ANGLE);
        ring_count--;
        next_state(STATE_BELL_FORWARD, 900);
      }
      break;
      case STATE_FINISH: {
        int v = analogRead(DOORBELL_PIN);
        if ( v > DOORBELL_THRESHOLD ) {
          // keep track and see if pin stays
          // raised for several loops in a row
          finish_count++;
          if ( finish_count < 5 ) {
            same_state();
          }
          else {
            next_state(STATE_INIT_POSITION);
          }
        }
        else {
          // doorbell voltage not raised yet
          // or dropped to 0 again, so want to avoid ringing
          // until signal has clearly finished
          finish_count = 0;
          same_state();
        }
      }
      break;
    }
  }
}
