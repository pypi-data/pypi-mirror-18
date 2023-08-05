myjscss
==========

The js css combine compress cache  and distribute to differnt client 

Introduction
-------------

JsCssBaseService
provides combine,compress js,css by different target like mobile,pc
js config file like  app.json:
{
    "client": [
      "mobile",
      "pc"
    ],
    "caption": "core lib",
    "index": 5,
    "type": "js",
    "files": [
      "/static/common/start.js",
      "/static/common/common.js",
      "/static/common/controller.js",
      "/static/common/directive/directive.js",
      "/static/common/filter.js"
    ]
  }

will compress files to a single js for different target client
for example:
app.json  client is mobile and pc
"/static/common/start.js" is a js relate path
when compute mobile  find /static/common/start.js  and /static/common/start.mobile.js two files, and combine compress it
when compute pc will find /static/common/start.js and /static/common/start.pc.js two files and combine  compress it
you can define many file config like app.json

this service also cache compress lib ,you must provide cache_get(key) cachet_set(key,value)
you can define many config like app.json in one folder
config_path is your config folder path
js_path is your js file folder path js_path+'/static/common/start.js' can find your js file


css config like flex_css.json
{
    "type": "css",
    "client": [
      "pc",
      "mobile",
      "admin"
    ],
    "caption": "style lib",
    "index": 18,
    "files": [
      "/static/common/directive/directive.css",
      "/static/common/directive/templates/employee_selector.css",
      "/static/common/directive/templates/department_selector.css",
      "/static/common/components/base/base.scss"
    ]
  }

Documentation
-------------

License
-------

myjscss is distributed under the `MIT license
<http://www.opensource.org/licenses/mit-license.php>`_.

