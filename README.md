PyYeelight
===================

![YeelightBulb](http://www.yeelight.com/yeelight2016/i/image/newindex/topic2.png)

### <i class="icon-book"></i> Library

**PyYeelight** :bulb: is a simple python3 library for the Yeelight wifi bulb.

  - This library is under development but still usable on your local network only
  - This library has been developed using this [documentation](http://www.yeelight.com/download/Yeelight_Inter-Operation_Spec.pdf) available on the official [Yeelight Website](http://www.yeelight.com/en_US/)
  - The tests are only made with the [YLDP03YL](http://www.yeelight.com/en_US/product/wifi-led-c) model which is the color wifi model. If you have any other bulb that can match with this library please feel free to PR.
  - Thanks to [Marc Pabst](https://github.com/mxtra) for his work on Yeelight. His work helped me a lot !

### <i class="icon-lightbulb"></i> Tests

Tests are only made with a YLDP03YL model. Because it's the only hardware model I own. If you have bugs with another kind of model, you could open an issue and propose some code to make the library available on all models

### <i class="icon-check"></i>TODO

- [ ] Add test coverage
- [x] Add the library to Pypi
- [ ] Add sleep timer API call (using cron)
- [ ] Add color flow API call (using start_cf)
- [ ] Add music mode
- [ ] Add scene API call
- [ ] Correct some bugs (see TODO in code)
- [ ] Handle Notifications send by bulb (to discover bulbs and adjust properties
- [ ] .... and lots of things !

### <i class="icon-cog"></i> How-To

1. You have to setup your bulb using Yeelight app. ( [Android](https://play.google.com/store/apps/details?id=com.yeelight.cherry&hl=fr), [IOS](https://itunes.apple.com/us/app/yeelight/id977125608?mt=8) ).
2. In the bulb property, you have to enable "Developer Mode"
3. Determine your bulb ip (using router, software, ping and so on)
4. Open your favorite python3 console
```
>>> import pyyeelight
>>> bulb = pyyeelight.YeelightBulb("192.168.1.25")
>>> bulb.set_rgb_color(255,0,0)
```

### <i class="icon-plus"></i>What can I add ?

  - PR are welcome
  - Advices on library structure are welcome too, this is one of my first python library and I'm still a noob on Python code
  - If you want to contact me : <i class="icon-twitter"></i> @hydreliox on Twitter
