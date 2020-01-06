#!/usr/bin/env python3
import math
import time
import threading


class blind():
	NUMBERS = list(map(chr, range(ord("0"), ord("9") + 1)))
	LOWERCASE = list(map(chr, range(ord("a"), ord("z") + 1)))
	UPPERCASE = list(map(chr, range(ord("A"), ord("A") + 1)))
	SINGLE_BYTE = list(map(chr, range(1, 0x100)))
	MULTI_BYTES = list(map(chr, range(1, 0x110000)))


	def __init__(self):
		return


	def leak(self, compare_function, start_index = 0, max_length = 100, letter_table = MULTI_BYTES, use_logging = True, use_asynchronous = True):
		self.compare_function = compare_function
		self.captured_letters = ["\u3000"] * max_length
		self.letter_table = ["\x00"] + letter_table + ["\x00"]
		self.use_logging = use_logging
		self.use_asynchronous = use_asynchronous

		if self.use_asynchronous:
			thread_list = []

			for i in range(start_index, max_length):
				t = threading.Thread(target = self.capture_letter, args = (i, ))
				t.start()
				thread_list.append(t)

			# wait until close all threads
			while 1:
				time.sleep(0.001)
				is_end = True

				while len(thread_list) > 0:
					if thread_list[0].is_alive():
						is_end = False
						break
					else:
						thread_list.pop(0)
				if is_end:
					break

			del thread_list

		else:
			for i in range(start_index, max_length):
				if self.capture_letter(i) == "\x00":
					break

		return self.get_captured_letters()


	def get_captured_letters(self):
		res = "".join(self.captured_letters)

		# split null byte
		null_idx = res.find("\x00")
		if null_idx > -1:
			res = res[:null_idx]

		return res


	def capture_letter(self, i):
		c = self.__binary_search(i, 0, len(self.letter_table) - 1)
		self.captured_letters[i] = c

		if self.use_logging and c != "\x00":
			print("[+] LEAK - %s" % (self.get_captured_letters()))

		return c


	def __binary_search(self, i, left, right):
		mid = math.ceil((left + right) / 2)

		try:
			res = self.compare_function(i, self.letter_table[mid - 1])
		except:
			res = False

		if (right - left) <= 1:
			return self.letter_table[int(right if res else left)]

		if res:
			return self.__binary_search(i, mid, right)
		else:
			return self.__binary_search(i, left, mid)



if __name__ == "__main__":

	pass