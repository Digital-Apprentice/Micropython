"""the classes that supports switch operations including simple incremental rotary encoder as a rotary switch"""
# copyright Tomasz Zgrys (Digital-Apprentice) - 2022 - MIT license 


##Class Button (switches used as a buttons)
### button_pin - GPIO Pin of the switch (button)
### powering - powering of switch: GND - connected to ground, POS - connected do 3.3V 
### click_interval - the maximum time beyond which the next click will be a separate operation [in milliseconds]
### long_press_time - time after which state of button will be recognized as long press [in milliseconds]
### example of use: b = Button(18,'POS',250,2000)
### Methods:
###         powering - checks or sets new powering method, GND - connected to ground, POS - connected do 3.3V
###         button_value - checks and returns present GPIO value
###         state_value - checks or sets (set 0 after handling procedure) new value of present state, it gives the number of clicks, takes values > 0,
###                       for multiple clicks, each click within the click_interval time will be counted as a multiple click
###         is_pressed - returns True if pressed or False if released, e.g. helpful for handling long press operations
###         is_released - returns True if released or False if pressed, e.g. helpful for handling multiple clicks
###         click_interval - checks or sets the time of click interval
###         long_press_time - checks or sets the time of long press operation


##Class RotaryEncoder (simple incremental rotary encoder)
### pin_a - first GPIO Pin of the encoder
### pin_b - second GPIO Pin of the encoder
### switch_pin - GPIO Pin of the switch in encoder, powered the same as whole encoder, after initialization possible to change it separately, uses methods from Button class
### powering - powering of encoder: GND - connected to ground, POS - connected do 3.3V
### start_val - start value at which counting is to start
### step - value (step), by which the encoder value is to change
### direction - the direction in which you want the increment to take place: CW - clockwise increment, CCW - counterclockwise increment
### example of use: r = RotaryEncoder(16,17,switch_pin=None,powering='GND',start_val=100,step=10,direction='CW')
### Methods:
###          value - check or set new base value
###          action - information about the type of operation - addition or subtraction during rotation
###          direction - check or set new increment direction
###          step - check or set new step value
    

from machine import Pin
import time


class Button(object):
    
    def __init__(self, button_pin, powering='GND',click_interval = 200, long_press_time = 1500):
        
        self.powering(button_pin, powering)
        self.button_pin.irq(handler = self._button_handler)  
        self._click_interval = click_interval    # time in ms
        self._long_press_time = long_press_time  # time in ms       
        
        self.pressed = False
        self.released = False
        self._state = 0
        self._last_state = 0
        
        self._pressing_time = 0
        self._time_of_state = 0        
        self._time_of_last_state = 0
        self._time_of_last_clicked = 0
            
    def _button_handler(self, pin):
        
        self._button_value = pin.value()
        if self._button_value != self._last_button_value:
            self._time_of_state = time.ticks_ms()           
            if self._button_value != self._base_button_value:
                self.pressed = True
                self.released = False
            else:
                self._pressing_time = time.ticks_diff(self._time_of_state,self._time_of_last_state)
                if self.pressed == True:
                    if 25 < self._pressing_time < self._long_press_time:                      
                        click_interval = time.ticks_diff(self._time_of_state,self._time_of_last_clicked)                       
                        if self._last_state >= 1 and click_interval < self._click_interval:
                            self._state += 1
                        else:
                            self._state = 1
                        print('state',self._state,'click interval',click_interval)
                        self._last_state = self._state
                        self._time_of_last_clicked = time.ticks_ms()
                    elif self._pressing_time >= self._long_press_time:
                        self._state = -1
                        self._last_state = self._state
                    
                    self.pressed = False
                    self.released = True
                    
            self._time_of_last_state = self._time_of_state
            self._last_button_value = self.button_value

    def powering(self, button_pin=None, powering=None):
        if (button_pin and powering) != None:
            self._powering = powering                # 'GND' = negative, connected to ground, 'POS' = positive, connected to 3.3V
            self.button_pin = Pin(button_pin, Pin.IN, Pin.PULL_UP if self._powering == 'GND' else Pin.PULL_DOWN)
            if self._powering == 'GND':
                self._base_button_value = 1          # pin pulled-up for sensing low state (logic '0')
            else:
                self._base_button_value = 0          # pin pulled-down for sensing high state (logic '1')
            self._last_button_value = self._base_button_value
            print(self.button_pin, self._powering)
            
        else:
            return self._powering
    
    def button_value(self):                          
        return self.button_pin.value()
    
    def state_value(self, state = None):
        if state == None:
            return self._state
        else:
            self._state = state
            
    def is_pressed(self):
        return self.pressed
    
    def is_released(self):
        return self.released
    
    def click_interval(self, click_interval = None):
        if click_interval == None:
            return self._click_interval
        else:
            self._click_interval = click_interval
            
    def long_press_time(self, long_press_time = None):
        if long_press_time == None:
            return self._long_press_time
        else:
            self._long_press_time = long_press_time
              

class RotaryEncoder(object, Button):
    
    def __init__(self, pin_A, pin_B,switch_pin=None, powering='GND',start_val=0,step=1,direction='CW'):
        self.pin_A = Pin(pin_A,Pin.IN,Pin.PULL_UP if powering == 'GND' else Pin.PULL_DOWN) 
        self.pin_B = Pin(pin_B,Pin.IN,Pin.PULL_UP if powering == 'GND' else Pin.PULL_DOWN)
        self.pin_A.irq(handler=self.__encoder_handler)
        self.__last_pin_A_value = self.pin_A.value()
        if switch_pin:
            super().__init__(switch_pin, powering)
        self.value(start_val)
        self.step(step)
        self.direction(direction)
        self._action = None
                
    def __encoder_handler(self, pin):
        pin_A_value = self.pin_A.value()
        if self._direction == 'CW':
            __step_value = self._step
        else:
            __step_value = -self._step       
        if pin_A_value != self.__last_pin_A_value:
            if self.pin_B.value() != pin_A_value:
                self._encoder_value += __step_value
                if self._direction == 'CW':                    
                    self._action = '+'
                else:
                    self._action = '-'
            else:
                self._encoder_value -= __step_value
                if self._direction == 'CW':
                    self._action = '-'
                else:
                    self._action = '+'
        self.__last_pin_A_value = self.pin_A.value()  
       
    def value(self, value=None):
        if value == None:
            return self._encoder_value
        else:
            self._encoder_value = value
    
    def step(self, step=None):
        if step == None:
            return self._step
        else:
            self._step = step
    
    def direction(self, direction=None):
        if direction == None:
            return self._direction
        else:
            if direction == ('CW' or 'CCW'):
                self._direction = direction
            else:
                self._direction = 'CW'
                
    def action(self):
        return self._action
        

