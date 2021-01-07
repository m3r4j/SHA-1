# sha1.py


# Function is used to left rotate i by n
def left_rotate(i, n):
    return ((i << n) & 0xffffffff) | (i >> (32 - n))


# The main function to generate the hash
def generate_hash(data):
	# Pre-defined variables / Constants
	h0 = 0x67452301
	h1 = 0xEFCDAB89
	h2 = 0x98BADCFE
	h3 = 0x10325476
	h4 = 0xC3D2E1F0


	# Make a data_arr
	data_arr = []


	# Convert to decimal and then convert to 8-bit binary and save it to 'data_arr'
	for x in data:
		data_arr.append(format(ord(x), '08b'))


	# Join the binaries into a string and add an extra '1' bit to it
	stream = ''.join(data_arr)
	stream += '1'


	# Keep adding 0s to the stream until the length is exactly 448 bits long
	while len(stream) % 512 != 448:
		stream += '0'


	# This is the required 64-bit value that is added to the end of the stream which contains the length of the original message in bits
	length = format(len(data) * 8, '064b')
	stream += length


	# Divide the block into 16 chunks of 32-bit words
	chunks = []
	res = ''

	for x in stream:
		res += x

		if len(res) == 32:
			chunks.append(res)
			res = ''


	# Extend chunks so that their is 80 32-bit words in it
	for t in range(16, 80):
		chunk = (int(chunks[t - 3], 2) ^ int(chunks[t - 8], 2) ^ int(chunks[t - 14], 2) ^ int(chunks[t - 16], 2)) & 2**32-1
		chunk = left_rotate(chunk, 1)
		chunk = format(chunk, 'b')
		chunks.append(chunk)


	# Initialize the hash values
	a = h0
	b = h1
	c = h2
	d = h3
	e = h4


	# Run the mainloop
	for i in range(80):
		if 0 <= i <= 19:
			f = (b & c) ^ (~b & d)
			k = 0x5A827999

		elif 20 <= i <= 39:
			f = b ^ c ^  d
			k = 0x6ED9EBA1

		elif 40 <= i <= 59:
			f = (b & c) ^ (b & d) ^ (c & d)
			k = 0x8F1BBCDC

		elif 60 <= i <= 79:
			f = b ^ c ^ d
			k = 0xCA62C1D6


		temp = left_rotate(a, 5) + f + e + k + int(chunks[i], 2) & 2**32-1
		e = d
		d = c
		c = left_rotate(b, 30) & 2**32-1
		b = a
		a = temp


	# Add the hash values of a-e together with hash values of h0-h4
	h0 = (h0 + a) & 2**32-1
	h1 = (h1 + b) & 2**32-1
	h2 = (h2 + c) & 2**32-1
	h3 = (h3 + d) & 2**32-1
	h4 = (h4 + e) & 2**32-1


	# Join them up and return result
	hash_list = [h0, h1, h2, h3, h4]
	res = ''

	for x in hash_list:
		res += format(x, '0x')

	return res


# Input the string
data = input('Enter string to hash: ')


# If the length of the message * 8 is less than 512 than continue else show an error
if len(data) * 8 <= 512:
	result = generate_hash(data)
	print(result)
else:
	print('Length must be less than or equal to 512.')

