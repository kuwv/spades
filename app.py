#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Provide webapp start.'''

from spades import create_app

app = create_app()

# import multiprocessing
# from typing import Any, Dict
#
# from flask import Flask
# from gunicorn.app.base import BaseApplication
#
# from spades import create_app
#
#
# def number_of_workers() -> int:
#     return (multiprocessing.cpu_count() * 2) + 1
#
#
# class WebApplication(BaseApplication):
#     '''Implement web application object.'''
#
#     def __init__(self, app: Flask, options: Dict[Any, Any] = None) -> None:
#         '''Initialize web application.'''
#         self.options = options or {}
#         self.application = app
#         super().__init__()
#
#     def load_config(self) -> None:
#         '''Load web application configuration.'''
#         config = {
#             key: value
#             for key, value in self.options.items()
#             if key in self.cfg.settings and value is not None
#         }
#         for key, value in config.items():
#             self.cfg.set(key.lower(), value)
#
#     def load(self) -> Flask:
#         '''Load application for service.'''
#         return self.application
#
#
# if __name__ == '__main__':
#     options = {
#         'bind': '%s:%s' % ('127.0.0.1', '8080'),
#         'workers': number_of_workers(),
#     }
#     WebApplication(create_app(), options).run()
