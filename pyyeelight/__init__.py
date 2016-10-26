from .yeelightAPICall import YeelightAPICall
from voluptuous import Schema, All, Any, Range


class YeelightBulb:
    """
     TODO : check every method with bulb off (software off) to see if the command is allowed

    """

    POWER_OFF = "off"
    POWER_ON = "on"

    EFFECT_SUDDEN = "sudden"
    EFFECT_SMOOTH = "smooth"

    MIN_TRANSITION_TIME = 30

    PROPERTY_NAME_POWER = "power"
    PROPERTY_NAME_BRIGHTNESS = "bright"
    PROPERTY_NAME_COLOR_TEMPERATURE = "ct"
    PROPERTY_NAME_RGB_COLOR = "rgb"
    PROPERTY_NAME_HUE = "hue"
    PROPERTY_NAME_SATURATION = "sat"
    PROPERTY_NAME_COLOR_MODE = "color_mode"
    PROPERTY_NAME_FLOW = "flowing"
    PROPERTY_NAME_SLEEP_REMAINING = "delayoff"
    PROPERTY_NAME_FLOW_PARAMETERS = "flow_params"
    PROPERTY_NAME_MUSIC_IS_ON = "music_on"
    PROPERTY_NAME_BULB_NAME = "name"

    ADJUST_ACTION_INCREASE = "increase"
    ADJUST_ACTION_DECREASE = "decrease"
    ADJUST_ACTION_CIRCLE = "circle"

    ADJUST_PROPERTY_BRIGHTNESS = "bright"
    ADJUST_PROPERTY_COLOR_TEMPERATURE = "ct"
    ADJUST_PROPERTY_COLOR = "color"

    def __init__(self, ip, port=55443):
        self.api_call = YeelightAPICall(ip, port)
        self.property = dict.fromkeys([self.PROPERTY_NAME_POWER, self.PROPERTY_NAME_BRIGHTNESS,
                                       self.PROPERTY_NAME_COLOR_TEMPERATURE, self.PROPERTY_NAME_RGB_COLOR,
                                       self.PROPERTY_NAME_HUE, self.PROPERTY_NAME_SATURATION,
                                       self.PROPERTY_NAME_COLOR_MODE, self.PROPERTY_NAME_FLOW,
                                       self.PROPERTY_NAME_SLEEP_REMAINING, self.PROPERTY_NAME_FLOW_PARAMETERS,
                                       self.PROPERTY_NAME_MUSIC_IS_ON, self.PROPERTY_NAME_BULB_NAME])
        self.refresh_property()

    def is_on(self):
        return self.property[self.PROPERTY_NAME_POWER] == self.POWER_ON

    def is_off(self):
        return self.property[self.PROPERTY_NAME_POWER] == self.POWER_OFF

    def get_property(self, property_name):
        try:
            return self.property[property_name]
        except KeyError:
            print("This property '{}' is not available".format(property_name))
            return None

    def get_all_properties(self):
        return self.property

    def refresh_property(self):
        # Generate a list of str where each str is a property name
        prop_list = []
        for prop in self.property.keys():
            prop_list.append(prop)
        # Send command to the bulb
        self.api_call.operate_on_bulb("get_prop", prop_list)
        # Affect each result to the right property dict keys
        for i in range(len(prop_list)):
            self.property[prop_list[i]] = self.api_call.get_response()[i]

    def set_color_temperature(self, temperature, effect=EFFECT_SUDDEN, transition_time=MIN_TRANSITION_TIME):
        """
            Set the white color temperature. The bulb must be switched on.

            :param temperature: color temperature to set. It can be between 1700 and 6500 K
            :param effect: if the change is made suddenly or smoothly
            :param transition_time: in case the change is made smoothly, time in ms that change last

            :type temperature: int
            :type effect: str
            :type transition_time : int
        """
        # Check bulb state
        if self.is_off():
            raise Exception("set_color_temperature can't be used if the bulb is off. Turn it on first")
        # Input validation
        schema = Schema({'temperature': All(int, Range(min=1700, max=6500)),
                         'effect': Any(self.EFFECT_SUDDEN, self.EFFECT_SMOOTH),
                         'transition_time': All(int, Range(min=30))})
        schema({'temperature': temperature, 'effect': effect, 'transition_time': transition_time})
        # Send command
        params = [temperature, effect, transition_time]
        self.api_call.operate_on_bulb("set_ct_abx", params)
        # Update property
        self.property[self.PROPERTY_NAME_COLOR_TEMPERATURE] = temperature

    def set_rgb_color(self, red, green, blue, effect=EFFECT_SUDDEN, transition_time=MIN_TRANSITION_TIME):
        """
            Set the color of the bulb using rgb code. The bulb must be switched on.

            :param red: Red component of the color between 0 and 255
            :param green: Green component of the color between 0 and 255
            :param blue: Blue component of the color between 0 and 255
            :param effect: if the change is made suddenly or smoothly
            :param transition_time: in case the change is made smoothly, time in ms that change last

            :type red: int
            :type green: int
            :type blue: int
            :type effect: str
            :type transition_time : int
        """
        # Check bulb state
        if self.is_off():
            raise Exception("set_rgb_color can't be used if the bulb is off. Turn it on first")
        # Input validation
        schema = Schema({'red': All(int, Range(min=0, max=255)),
                         'green': All(int, Range(min=0, max=255)),
                         'blue': All(int, Range(min=0, max=255)),
                         'effect': Any(self.EFFECT_SUDDEN, self.EFFECT_SMOOTH),
                         'transition_time': All(int, Range(min=30))})
        schema({'red': red, 'green': green, 'blue': blue,  'effect': effect, 'transition_time': transition_time})
        # Send command
        rgb = (red*65536) + (green*256) + blue
        params = [rgb, effect, transition_time]
        self.api_call.operate_on_bulb("set_rgb", params)
        # Update property
        self.property[self.PROPERTY_NAME_RGB_COLOR] = rgb

    def set_hsv_color(self, hue, saturation, effect=EFFECT_SUDDEN, transition_time=MIN_TRANSITION_TIME):
        """
            Set the color of the bulb using hsv code. The bulb must be switched on.
            TODO : Resolve bug found trying to set hue to 100 and sat to 100 (General error)

            :param hue: Hue component of the color between 0 and 359
            :param saturation: Saturation component of the color between 0 and 100
            :param effect: if the change is made suddenly or smoothly
            :param transition_time: in case the change is made smoothly, time in ms that change last

            :type hue: int
            :type saturation: int
            :type effect: str
            :type transition_time : int
        """
        # Check bulb state
        if self.is_off():
            raise Exception("set_hsv_color can't be used if the bulb is off. Turn it on first")
        # Input validation
        schema = Schema({'hue': All(int, Range(min=0, max=359)),
                         'saturation': All(int, Range(min=0, max=100)),
                         'effect': Any(self.EFFECT_SUDDEN, self.EFFECT_SMOOTH),
                         'transition_time': All(int, Range(min=30))})
        schema({'hue': hue, 'saturation': saturation, 'effect': effect, 'transition_time': transition_time})
        # Send command
        params = [hue, saturation, effect, transition_time]
        self.api_call.operate_on_bulb("set_hsv", params)
        # Update property
        self.property[self.PROPERTY_NAME_HUE] = hue
        self.property[self.PROPERTY_NAME_SATURATION] = saturation

    def set_brightness(self, brightness, effect=EFFECT_SUDDEN, transition_time=MIN_TRANSITION_TIME):
        """
            This method is used to change the brightness of a smart LED

            :param brightness: is the target brightness. The type is integer and ranges from 1 to 100. The
                               brightness is a percentage instead of a absolute value. 100 means maximum brightness
                               while 1 means the minimum brightness.
            :param effect: if the change is made suddenly or smoothly
            :param transition_time: in case the change is made smoothly, time in ms that change last

            :type brightness: int
            :type effect: str
            :type transition_time : int
        """
        # Check bulb state
        if self.is_off():
            raise Exception("set_brightness can't be used if the bulb is off. Turn it on first")
        # Input validation
        schema = Schema({'brightness': All(int, Range(min=1, max=100)),
                         'effect': Any(self.EFFECT_SUDDEN, self.EFFECT_SMOOTH),
                         'transition_time': All(int, Range(min=30))})
        schema({'brightness': brightness, 'effect': effect, 'transition_time': transition_time})
        # Send command
        params = [brightness, effect, transition_time]
        self.api_call.operate_on_bulb("set_bright", params)
        # Update property
        self.property[self.PROPERTY_NAME_BRIGHTNESS] = brightness

    def turn_on(self, effect=EFFECT_SUDDEN, transition_time=MIN_TRANSITION_TIME):
        """
            This method is used to switch on the smart LED (software managed on).

            :param effect: if the change is made suddenly or smoothly
            :param transition_time: in case the change is made smoothly, time in ms that change last

            :type effect: str
            :type transition_time : int
        """
        # Check bulb state
        if self.is_on():
            return
        else:
            # Input validation
            schema = Schema(
                {'effect': Any(self.EFFECT_SUDDEN, self.EFFECT_SMOOTH), 'transition_time': All(int, Range(min=30))})
            schema({'effect': effect, 'transition_time': transition_time})
            # Send command
            params = ["on", effect, transition_time]
            self.api_call.operate_on_bulb("set_power", params)
            # Update property
            self.property[self.PROPERTY_NAME_POWER] = self.POWER_ON

    def turn_off(self, effect=EFFECT_SUDDEN, transition_time=MIN_TRANSITION_TIME):
        """
            This method is used to switch off the smart LED (software managed off).

            :param effect: if the change is made suddenly or smoothly
            :param transition_time: in case the change is made smoothly, time in ms that change last

            :type effect: str
            :type transition_time : int
        """
        # Check bulb state
        if self.is_off():
            return
        else:
            # Input validation
            schema = Schema(
                {'effect': Any(self.EFFECT_SUDDEN, self.EFFECT_SMOOTH), 'transition_time': All(int, Range(min=30))})
            schema({'effect': effect, 'transition_time': transition_time})
            # Send command
            params = ["off", effect, transition_time]
            self.api_call.operate_on_bulb("set_power", params)
            # Update property
            self.property[self.PROPERTY_NAME_POWER] = self.POWER_OFF

    def toggle(self):
        """
            This method is used to toggle the smart LED (software managed off).
            This method is defined because sometimes user may just want to flip the state without knowing the
            current state
        """
        # Send command
        self.api_call.operate_on_bulb("toggle")
        # Update property
        if self.is_on():
            self.property[self.PROPERTY_NAME_POWER] = self.POWER_OFF
        elif self.is_off():
            self.property[self.PROPERTY_NAME_POWER] = self.POWER_ON

    def save_state(self):
        """
            This method is used to save current state of smart LED in persistent memory. So if user powers off and
            then powers on the smart LED again (hard power reset), the smart LED will show last saved state.

            For example, if user likes the current color (red) and brightness (50%) and want to make this state as a
            default initial state (every time the smart LED is powered), then he can use save_state to do a snapshot.

            Only accepted if the smart LED is currently in "on" state.
        """
        # Check bulb state
        if self.is_off():
            raise Exception("save_state can't be used if the bulb is off. Turn it on first")
        # Send command
        self.api_call.operate_on_bulb("set_default")

    def adjust(self, action, prop):
        """
            This method is used to change brightness, CT or color of a smart LED without knowing the current value,
            it's main used by controllers.

            :param action: The direction of the adjustment. The valid value can be:
                                ADJUST_ACTION_INCREASE: increase the specified property
                                ADJUST_ACTION_DECREASE : decrease the specified property
                                ADJUST_ACTION_CIRCLE : increase the specified property, after it reaches the max value,
                                                       go back to minimum value.
            :param prop: The property to adjust. The valid value can be:
                                ADJUST_PROPERTY_BRIGHTNESS: adjust brightness.
                                ADJUST_PROPERTY_COLOR_TEMPERATURE: adjust color temperature.
                                ADJUST_PROPERTY_COLOR: adjust color. (When “prop" is “color", the “action" can only
                                                       be “circle", otherwise, it will be deemed as invalid request.)

            :type action: str
            :type prop: str
        """
        # Input validation
        schema = Schema(
            {'action': Any(self.ADJUST_ACTION_CIRCLE, self.ADJUST_ACTION_DECREASE, self.ADJUST_ACTION_INCREASE),
             'prop': Any(self.ADJUST_PROPERTY_BRIGHTNESS, self.ADJUST_PROPERTY_COLOR,
                         self.ADJUST_PROPERTY_COLOR_TEMPERATURE)})
        schema({'action': action, 'prop': prop})
        # Send command
        params = [action, prop]
        self.api_call.operate_on_bulb("set_adjust", params)
        # Update property
        self.refresh_property()  # TODO : do more test to handle property change without sending another command

    # WARNING : This method is in the API documentation but after some test the method is not supported by Bulbs
    # def set_name(self, name):
    #     """
    #         This method is used to name the device. The name will be stored on the device and reported in
    #         discovering response. User can also read the name through “get_property” method.
    #
    #         NOTE: When using Yeelight official App, the device name is stored on cloud. This method instead store
    #         the name on persistent memory of the device, so the two names could be different.
    #
    #         :param name: name stored in the device memory
    #
    #         :type name: str
    #     """
    #     # Input validation
    #     schema = Schema({'name': str })
    #     schema({'name': name})
    #     # Send command
    #     self.api_call.operate_on_bulb("set_name", [name])
    #     # Update property
    #     #self.property[self.PROPERTY_NAME_BRIGHTNESS] = brightness
