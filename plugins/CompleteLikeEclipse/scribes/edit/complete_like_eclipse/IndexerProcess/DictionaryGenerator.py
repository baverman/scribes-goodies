class Generator(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		self.__sigid1 = manager.connect("generate-dictionary", self.__generate_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		from re import UNICODE, compile
		self.__pattern = compile(r"[^-\w]", UNICODE)
		from dbus import Dictionary, String, Int32
		try:
			self.__empty_dict = Dictionary({}, signature="ss")
		except:
			self.__empty_dict = Dictionary({}, key_type=String, value_type=Int32)
		return

	def __generate(self, data):
		try:
			text, editor_id = data
			if not text: raise ValueError
			words = self.__generate_words(text)
			if not words: raise ValueError
			dictionary = self.__generate_dictionary(words)
			if not dictionary: raise ValueError
			self.__manager.emit("finished", (editor_id, dictionary))
		except ValueError:
			self.__manager.emit("finished", (editor_id, self.__empty_dict))
		return False

	def __generate_words(self, text):
		from re import split
		words = split(self.__pattern, text)
		words =[word for word in words if self.__filter(word)]
		return words

	def __filter(self, word):
		if len(word) < 4: return False
		if word.startswith("---"): return False
		if word.startswith("___"): return False
		return True

	def __generate_dictionary(self, words):
		dictionary = {}
		for string in words:
			if string in dictionary.keys():
				dictionary[string] += 1
			else:
				dictionary[string] = 1
		return dictionary

	def __generate_cb(self, manager, data):
		self.__generate(data)
		return False
