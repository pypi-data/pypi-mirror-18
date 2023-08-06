.. install_ext_trackapps:

TrackApps
=========

You have 2 options how to install TrackApps extension.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

Filename after PIP download contains version, adapt sample code.

  .. code-block:: bash
  
     $ sudo pip download hydratk-ext-trackapps
     $ sudo pip install hydratk-ext-trackapps.tar.gz 
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-ext-trackapps
     
  .. note::
  
     Use PIP to install package from local file for correct installation.
     When installed from remote repository, PIP sometimes doesn't call setup.py.       

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-ext-trackapps.git
     $ cd ./hydratk-ext-trackapps
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://python.org/pypi/hydratk-ext-trackapps -O hydratk-ext-trackapps.tar.gz
     $ tar -xf hydratk-ext-trackapps.tar.gz
     $ cd ./hydratk-ext-trackapps
     $ sudo python setup.py install
     
  .. note::
  
     Source is distributed with Sphinx (not installed automatically) documentation in directory doc. 
     Type make html to build local documentation however is it recommended to use up to date online documentation.       
  
Requirements
^^^^^^^^^^^^     
     
The extension requires hydratk, hydratk-lib-network.  
     
Installation
^^^^^^^^^^^^

See installation example, Python 2.7.

  .. code-block:: bash
  
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_ext_trackapps.egg-info
     writing requirements to src/hydratk_ext_trackapps.egg-info/requires.txt
     writing src/hydratk_ext_trackapps.egg-info/PKG-INFO
     writing top-level names to src/hydratk_ext_trackapps.egg-info/top_level.txt
     writing dependency_links to src/hydratk_ext_trackapps.egg-info/dependency_links.txt
     writing entry points to src/hydratk_ext_trackapps.egg-info/entry_points.txt
     writing manifest file 'src/hydratk_ext_trackapps.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk_ext_trackapps.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_ext_trackapps.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     creating build/lib.linux-x86_64-2.7/hydratk/extensions
     copying src/hydratk/extensions/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions
     creating build/lib.linux-x86_64-2.7/hydratk/extensions/trackapps
  
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_trackapps-0.1.1-py2.7.egg
     Processing dependencies for hydratk-ext-trackapps==0.1.1
     Searching for hydratk-lib-network==0.2.0
     Best match: hydratk-lib-network 0.2.0
     Processing hydratk_lib_network-0.2.0-py2.7.egg
     hydratk-lib-network 0.2.0 is already the active version in easy-install.pth

     Using /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.2.0-py2.7.egg
     Searching for hydratk==0.4.0
     Best match: hydratk 0.4.0
     Processing hydratk-0.4.0-py2.7.egg
     hydratk 0.4.0 is already the active version in easy-install.pth
     Installing htkprof script to /usr/local/bin
     Installing htk script to /usr/local/bin

     Using /usr/local/lib/python2.7/dist-packages/hydratk-0.4.0-py2.7.egg
     Finished processing dependencies for hydratk-ext-trackapps==0.1.1
    
    
Application installs following (paths depend on your OS configuration)

* trackapps command in /usr/local/bin/trackapps
* modules in /usr/local/lib/python2.7/dist-packages/hydratk_ext_trackapps-0.1.1-py2.7.egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-trackapps.conf     
       
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-trackapps module is installed.   

  .. code-block:: bash
  
     $ pip list | grep hydratk-ext-trackapps
     
     hydratk-ext-trackapps (0.1.1)
     
Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     TrackApps: TrackApps v0.1.1 (c) [2016 Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>]
     
Type command htk help and detailed info is displayed.
Type man trackapps to display manual page. 

  .. code-block:: bash
  
     $ htk help
     
     Commands:
         track - run trackapps command line extension
             Options:
                [--tr-dev-key <key>] - developer key, configurable, supported for app: testlink
                [--tr-domain <domain>] - domain, configurable, supported for app: qc
                [--tr-fields <list>] - requested fields, name1,name2,... , supported for action: read
                [--tr-id <num>] - record id, supported for actions: read|update|delete
                [--tr-input <filename>] - filename, content is written to ticket description, supported for actions: create|update
                [--tr-limit <num>] - limit, supported for action: read, apps: qc|bugzilla|jira
                [--tr-offset <num>] - offset, supported for action: read, apps: qc|bugzilla|jira
                [--tr-order-by <expression>] - record ordering, name1:direction,name2:direction,... , direction asc|desc, supported for action: read, app: qc
                [--tr-output <filename>] - filename, writes action output, supported for action: read
                [--tr-page <num>] - record page, supported for action: read, app: mantis
                [--tr-params <dict>] - record parameters, name1:value,name2:value,... , supported for actions: create|update
                [--tr-passw <password>] - password, configurable
                [--tr-path <path>] - directory path, dir1/dir2/... , supported for use cases: read/create folder|read/create test set|create test|read/create suite, apps: qc|testlink
                [--tr-per-page <num>] - records per page, supported for action: read, app: mantis
                [--tr-project <project>] - project, configurable, supported for apps: qc|mantis|trac|jira|testlink
                [--tr-query <expression>] - query, supported for action: read, apps: qc|bugzilla|trac|jira
                [--tr-steps <list>] - test steps delimited by |, step parameters use dictionary form, name1:value,name2:value,...|name1:value,name2:value,... , supported for action: create, app: testlink
                [--tr-type defect|test-folder|test|test-set-folder|test-set|test-instance|test-suite|test-plan|build] - entity type, default defect, supported for actions: read|create|update|delete, apps: qc|testlink
                [--tr-url <url>] - url, configurable
                [--tr-user <username>] - username, configurable
                --tr-action read|create|update|delete - action, delete supported for apps: qc|mantis|trac
                --tr-app qc|bugzilla|mantis|trac|testlink - application

           
You can run TrackApps also in standalone mode.

  .. code-block:: bash
  
     $ trackapps help
     
     TrackApps v0.1.1
     (c) 2016 Petr Rašek <bowman@hydratk.org>, HydraTK team <team@hydratk.org>
     Usage: trackapps [options] command

     Commands:
        help - prints help
        run - run trackapps command line extension
           Options:
              [--dev-key <key>] - developer key, configurable, supported for app: testlink
              [--domain <domain>] - domain, configurable, supported for app: qc
              [--fields <list>] - requested fields, name1,name2,... , supported for action: read
              [--id <num>] - record id, supported for actions: read|update|delete
              [--input <filename>] - filename, content is written to ticket description, supported for actions: create|update
              [--limit <num>] - limit, supported for action: read, apps: qc|bugzilla|jira
              [--offset <num>] - offset, supported for action: read, apps: qc|bugzilla|jira
              [--order-by <expression>] - record ordering, name1:direction,name2:direction,... , direction asc|desc, supported for action: read, app: qc
              [--output <filename>] - filename, writes action output, supported for action: read
              [--page <num>] - record page, supported for action: read, app: mantis
              [--params <dict>] - record parameters, name1:value,name2:value,... , supported for actions: create|update
              [--passw <password>] - password, configurable
              [--path <path>] - directory path, dir1/dir2/... , supported for use cases: read/create folder|read/create test set|create test|read/create suite, apps: qc|testlink
              [--per-page <num>] - records per page, supported for action: read, app: mantis
              [--project <project>] - project, configurable, supported for apps: qc|mantis|trac|jira|testlink
              [--query <expression>] - query, supported for action: read, apps: qc|bugzilla|trac|jira
              [--steps <list>] - test steps delimited by |, step parameters use dictionary form, name1:value,name2:value,...|name1:value,name2:value,... , supported for action: create, app: testlink
              [--type defect|test-folder|test|test-set-folder|test-set|test-instance|test-suite|test-plan|build] - entity type, default defect, supported for actions: read|create|update|delete, apps: qc|testlink
              [--url <url>] - url, configurable
              [--user <username>] - username, configurable
              --action read|create|update|delete - action, delete supported for apps: qc|mantis|trac
              --app qc|bugzilla|mantis|trac|testlink - application

     Global Options:
        -c, --config <file> - reads the alternate configuration file
        -d, --debug <level> - debug turned on with specified level > 0
        -e, --debug-channel <channel number, ..> - debug channel filter turned on
        -f, --force - enforces command
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available modes is specified in the docs
                                 