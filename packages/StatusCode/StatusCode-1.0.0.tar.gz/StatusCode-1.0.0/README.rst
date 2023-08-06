==========
StatusCode
==========

Python Status Code based on ``kkconst``

Installation
============

::

    pip install StatusCode


Usage
=====

::

    from StatusCode import BaseStatusCode, StatusCodeField

    class ProfileStatusCode(BaseStatusCode):
        """ 4000xx - Profile Relative Status Code """
        PROFILE_NOT_FOUND = StatusCodeField(410000, 'Profile Not Found', description=u'用户不存在')

    ProfileStatusCode.PROFILE_NOT_FOUND
    # 410001

    ProfileStatusCode.PROFILE_NOT_FOUND.message
    # u'Profile Not Found'

    ProfileStatusCode.PROFILE_NOT_FOUND.description
    # u'\u7528\u6237\u4e0d\u5b58\u5728'


Requirement
===========

::

    <require all letters capital>　= StatusCodeField(<require no duplicated value>, <message>, <description>)

