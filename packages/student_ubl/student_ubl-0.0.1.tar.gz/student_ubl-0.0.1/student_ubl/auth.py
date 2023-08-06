# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import requests
from student_ubl.urls import URL


class MahasiswaAuth(object):

	INPUT_NAME = 'txtinput[]'
	SUBMIT_NAME = 'btninput'
	VAL_SUBMIT_NAME = 'LogIn'

	def __init__(self, *args, **kwargs):
		self._nim = kwargs['nim']
		self._password = kwargs['password']
		self._data = {
			self.INPUT_NAME: [self._nim, self._password],
			self.SUBMIT_NAME: self.VAL_SUBMIT_NAME,
		}

		self._session = None

	def _login(self):
		self._session = requests.Session()
		self._session.post(URL['login'], self._data)
		return self._session