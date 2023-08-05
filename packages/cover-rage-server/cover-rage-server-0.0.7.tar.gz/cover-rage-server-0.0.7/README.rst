===================
Cover Rage - server
===================
.. image:: https://badge.fury.io/py/cover-rage-server.svg
    :target: https://badge.fury.io/py/cover-rage-server
.. image:: https://circleci.com/gh/alexryabtsev/cover_rage_server/tree/master.svg?style=shield
    :target: https://circleci.com/gh/alexryabtsev/cover_rage_server/tree/master
.. image:: https://cover-rage.doomatel.com/api/badge/ZV2EKP1xsZRHDtMA0XVevw/
    :target: https://cover-rage.doomatel.com/api/badge/ZV2EKP1xsZRHDtMA0XVevw/

Server for `Cover Rage`_.

1. Handle checks of test coverage for the last commit / pull request initiated by web-hook on Github / Bitbucket and you CI-server.
2. Keeps your overall coverage percentage for badge.

All settings should be defined in environment variables. Available settings are:

- *RAGE_SRV_REDIS_HOST* - Redis host
- *RAGE_SRV_REDIS_PORT* - Redis port
- *RAGE_SRV_REDIS_DB* - Redis database
- *RAGE_SRV_SCHEME* - http or https
- *RAGE_SRV_HOST* - domain name of your Cover Rage server
- *RAGE_SRV_MIN_GOOD_COVERAGE_PERCENTAGE* - min good coverage percentage for badge

To add a project you should run *run_cli* console script:

*./rage_cli.py gh|bb <account> <repo> <access token>*

where:

- *gh* is Github, *bb* is Bitbucket,
- *account* is your account name on Github / Bitbucket
- *repo* is your repo name on Github / Bitbucket
- *access token* is an API access token from Github / Bitbucket

This command will create a web-hook on Github / Bitbucket and generate you public and private Cover Rage tokens. Use them when you'll configuring your CI-server.

To run server inside Docker container you can use this command:

*docker-compose --file docker-compose.yml --project-name cover_rage_server up*

.. _cover rage: https://github.com/alexryabtsev/cover_rage
