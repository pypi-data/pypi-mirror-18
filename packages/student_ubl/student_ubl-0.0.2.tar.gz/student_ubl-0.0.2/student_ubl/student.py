# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json
from bs4 import BeautifulSoup
from student_ubl.auth import MahasiswaAuth
from student_ubl.urls import URL


class ClassBasedStudentUBL(object):

	RESULT_FORMAT_JSON = 'json'
	RESULT_FORMAT_BUILTIN = 'dict'

	def _json_data(self, key, hasil):
		return json.dumps({key: hasil})

	def _split_list(list, chunk_size):
		return [list[offs:offs+chunk_size] for offs in range(0, len(list), chunk_size)]


class BiodataAPI(MahasiswaAuth, ClassBasedStudentUBL):

	KEY_TOLERANT_NIM = 'N I M'
	KEY_REPLACE_NIM = 'nim'
	
	def __init__(self, *args, **kwargs):
		super(BiodataAPI, self).__init__(*args, **kwargs)
		self._login()

	def is_student(self):
		return bool(self.get_profile(result_format=self.RESULT_FORMAT_BUILTIN))
		
	def get_profile(self, result_format='dict'):
		try:
			html_doc = self._session.get(URL['data_mhs'])
			soup = BeautifulSoup(html_doc.text, 'html.parser')
			tag_table = soup.find_all('tr')

			# Mencari data mahasiswa
			tag_table = soup.table.find_all('tr')
			data_mahasiswa = [tag.text.replace('\xa0', '').split(':') for tag in tag_table[:-1]]
			data_mahasiswa = [(" ".join(data[0].split()), " ".join(data[1].split())) for data in data_mahasiswa]
			hasil = {}

			for k, v in data_mahasiswa:
				if k == BiodataAPI.KEY_TOLERANT_NIM:
					hasil[BiodataAPI.KEY_REPLACE_NIM] = v
				else:
					hasil[k.lower().replace(' ', '_')] = v

			if result_format == self.RESULT_FORMAT_JSON:
				return self._json_data('biodata', hasil)

			if result_format == self.RESULT_FORMAT_BUILTIN:
				return hasil
		except:
			return None


class AkademikAPI(MahasiswaAuth, ClassBasedStudentUBL):

	def __init__(self, *args, **kwargs):
		super(AkademikAPI, self).__init__(*args, **kwargs)
		self._login()


	def get_tahun_ajaran(self, result_format='dict'):
		try:
			html_doc = self._session.get(URL['data_akademik'])
			soup = BeautifulSoup(html_doc.text, 'html.parser')
			tag_option = soup.find_all('option')
			tahun_ajaran = [s['value'] for s in tag_option[:-2]]
			semester = [(s['value'], s.text) for s in tag_option[-2:]]
			hasil = {'tahun_ajarn': tahun_ajaran, 'semester': dict(semester)}

			if result_format == self.RESULT_FORMAT_JSON:
				return self._json_data('tahun_ajaran_semester', hasil)
			else:
				return hasil
		except:
			return None


	def get_nilai_semester(self, tahun_ajaran, semester, result_format='dict'):
		# try:
		payloads = {
			self.INPUT_NAME: ['Nilai Semester', tahun_ajaran, semester],
			self.SUBMIT_NAME: 'Tampilkan!',
		}


		html_doc = self._session.post(URL['post_nilai_semester'], payloads)
		soup = BeautifulSoup(html_doc.text, 'html.parser')
		tag_td = soup.find_all('td')[16:]

		step = 9
		header = [i.text for i in tag_td[:9]]
		del tag_td[:9]
		result = []

		# Mengambil text dan menghapus format hex unicode
		for i in range(9):
			if tag_td:
				result.append([i.text.replace('\xa0', '') for i in tag_td[:step]])
				del tag_td[:step]

		# Mengubah data menjadi key-value pairs terhadap header
		result_copy = result
		result = []
		for i in result_copy[:]:
			result.append(dict(list(zip(header,i))))

		result_copy = result
		result = []
		x = {}

		# Mengubah data menjadi integer jika nilainya instance dari class int
		for index, data in enumerate(result_copy):
			for k, v in data.items():
				if v.isnumeric():
					x[k.lower().replace(' ', '_')] = int(v)
				else:
					x[k.lower().replace(' ', '_')] = v

			result.append(x)
			x = {}


		result_copy = result
		# oncom = {}
		result = {}

		for i in result_copy:
			kode = i['kode']
			# for k, v in i.items():
			del i['kode']
			result[kode] = i
			# print(i)
		# result = oncom

		if result_format == self.RESULT_FORMAT_BUILTIN:
			return result
		if result_format == self.RESULT_FORMAT_JSON:
			return self._json_data('nilai_semester', result)
		# except:
		# 	return None

	def get_hsk(self, result_format='dict'):
		html_doc = self._session.get(URL['hsk_online'])
		soup = BeautifulSoup(html_doc.text, 'html.parser')
		tag_td = soup.find_all('td')[16:]
		chunks_awal = 4
		chunks_prestasi = 4
		tag_head = [i.text.lower().replace(' ', '_') for i in tag_td[:chunks_awal]]
		del tag_td[:chunks_awal]

		tag_prestasi = [i.text.lower().replace(' ', '_') for i in tag_td[:chunks_prestasi]]
		del tag_td[:chunks_prestasi]

		tag_data = [i.text.lower() for i in tag_td]
		result = []

		# Mengambil data dengan pemotongan step 7 pada data tabel
		# 0 	 ['1', 'kp002', 'algoritma dan struktur data 1*', '3', '3', '9', 'b']
		# 1 	 ['2', 'kp003', 'algoritma dan struktur data 2*', '3', '2', '6', 'c']
		# ............
		chunks_standar = 7
		while True:
			if tag_data:
				result.append([x.replace('\xa0', '') for x in tag_data[:chunks_standar]])
				del tag_data[:chunks_standar]
			else:
				break

		# melakukan filter agar hanya data yang nilai-nilai saja yang diambil dari tabel hsk
		result_copy = result
		result = []
		for i in result_copy:
			if i[0].isnumeric():
				i[0] = int(i[0])
				i[3] = float(i[3])
				i[4] = float(i[4])
				i[5] = float(i[5])
				result.append(dict(list(zip(tag_head,i[:3]))+[('index_prestasi',dict(list(zip(tag_prestasi, i[3:]))))]))
				

		if result_format == self.RESULT_FORMAT_BUILTIN:
			return result
		if result_format == self.RESULT_FORMAT_JSON:
			return self._json_data('hsk', result)

		return result

class FacadeStudentUBL(object):

	def authenticated(self, nim, password):
		self.__nim = nim
		self.__password = password

	def akademik_api(self):
		return AkademikAPI(nim=self.__nim, password=self.__password)

	def biodata_api(self):
		return BiodataAPI(nim=self.__nim, password=self.__password)


def main():

	student_ubl = FacadeStudentUBL()
	student_ubl.authenticated(nim='', password='')

	akademik = student_ubl.akademik_api()
	biodata = student_ubl.biodata_api()

	from pprint import pprint
	print(akademik.get_tahun_ajaran())
	print(biodata.is_student())
	print(akademik.get_nilai_semester('20152016', 'O'))
	# print(akademik.get_hsk('json'))


# main()

