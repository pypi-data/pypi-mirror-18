===================
PumpWood Exceptions
===================

Extends Django and Rest FrameWork exceptions in order to give a better detail over model miss-especification and permit serialization of the error data to facilitate front-end debug.

Quick start
-----------

1. Add "pumpwood-exceptions" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'pumpwood-exceptions',
    ]
