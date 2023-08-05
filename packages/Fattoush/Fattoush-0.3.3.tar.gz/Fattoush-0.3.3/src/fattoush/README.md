Fattoush
========

Fattoush is a package that combines lettuce, webdriver and sauce to make a tasty UI testing salad.


Running
-------

Fattoush provides its own test runner which invokes lettuce such that it can run in saucelabs, with
support of parallel test runs.

    $ fattoush --parallel=webdriver

By default Fattoush will run sets of tests in series, but there is support for running lettuce in a
separate process for each webdriver configuration. Another default is that webdriver configuration
should be read from environmental variables as described at
[http://saucelabs.com/teamcity/3](http://saucelabs.com/teamcity/3). Alternatively the browser
configuration can be read from a json file.

    $ fattoush --config-file

Fattoush validates all json, whether from a file or from the environment, against a schema, which
can be printed from Fattoush using `--print-schema`. An example valid configuration can be printed
using `--print-example-config`.

For an example of how to run Fattoush, navigate to the test directory within this project, and run

    $ fattoush --config-file chrome_local.json

Usage
-----

Just write your lettuce tests as normal, but in your terrain file add

    from fattoush import Driver, hooks

and in each step definition module you are able to add

    from fattoush import Driver

The hooks module simply uses `lettuce.before` and `lettuce.after` to set up `lettuce.world` for each
test feature, scenario, and step, ensuring that each scenario gets a fresh webdriver session and
that each step is correctly logged.

`fattoush.Driver` is a subclass of WebDriver with a class method instance(step_or_scenario). Within
any step or hook you can call this class method to get the appropriate Driver instance. This driver
instance will also have a property driver_instance.sauce which provides an object inheriting
fattoush.driver.sauce.SauceInterface. This may be an instance of fattoush.driver.sauce.Sauce in
which case it will interact with sauce using its REST api as well as holding information such as
authentication credentials and publicly viewable links. If on the other hand it is an instance of
fattoush.driver.sauce.Local, calling any of the methods of this interface shall just log that it
was called, and potentially return canned information as if running in saucelabs. Which of these is
returned is dictated by whether fattoush knows that it is running against saucelabs rather than a
local selenium server.


License
-------
© 2014 Mind Candy Ltd. All Rights Reserved. 
Licensed under the MIT License; you may not use this file except in compliance with the License. 
You may obtain a copy of the License at http://opensource.org/licenses/MIT.


Possible Future Work
--------------------
 - Page abstract class
 - More hooks
 - More parallel options (per feature or per scenario)
