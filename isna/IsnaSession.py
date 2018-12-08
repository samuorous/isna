import os


class IsnaSession:
    def __init__(self, data_dir, unknown_tag='O'):
        self.unknown_tag = unknown_tag
        self.data_dir = data_dir
        self.sentences = list()
        self.tags = list()
        self.tag_map = list()
        self.num_sentences = -1
        self.sentences_file = os.path.join(self.data_dir, 'sentences.txt')
        self.tags_file = os.path.join(self.data_dir, 'tags.txt')
        self.available_tags_file = os.path.join(self.data_dir, 'available_tags.txt')
        self.load_data()

    def load_data(self):
        """ Load data from sentences, tags, available-tags files.

        """
        with open(self.sentences_file, encoding='utf-8') as f:
            for sentence in f.read().splitlines():
                self.sentences.append([word for word in sentence.split(' ')])

        # Init a plain tags file if none exists.
        if not os.path.isfile(self.tags_file):
            self.generate_tags_file()

        with open(self.tags_file, encoding='utf-8') as f:
            for tag_string in f.read().splitlines():
                self.tags.append([tag.strip() for tag in tag_string.split(' ') if len(tag.strip()) > 0])

        # Init a available_tags file from the tags file if it does not exist.
        if not os.path.isfile(self.available_tags_file):
            self.generate_available_tags_file()

        with open(self.available_tags_file, encoding='utf-8') as f:
            for tag in f.read().splitlines():
                tag = tag.strip()
                if len(tag) > 0:
                    self.tag_map.append(tag)

        # Check if unknown_tag is available.
        if self.unknown_tag not in self.tag_map:
            with open(self.available_tags_file, encoding='utf-8', mode='a') as f:
                f.write('\n{}'.format(self.unknown_tag))
            self.tag_map.append(self.unknown_tag)

        # Consistency checks.
        self.num_sentences = len(self.sentences)
        assert self.num_sentences == len(self.tags)

        for i in range(self.num_sentences):
            assert len(self.sentences[i]) == len(self.tags[i])

    def tag_sentence(self, sent_id, start, end, tag_id):
        """ Tag a (part) sentence

        :param sent_id: the position in the sentence file
        :param start: start position of tagging.
        :param end: end position of tagging
        :param tag_id: tag id to be used.
        """
        self.tags[sent_id][start:end + 1] = [self.tag_map[tag_id]] * (1 + end - start)

    def store(self):
        """ Store current session to data folder.

        """
        lines = '\n'.join([' '.join(sentence) for sentence in self.sentences])
        with open(self.sentences_file, mode='w', encoding='utf-8') as f:
            f.writelines(lines)

        lines = '\n'.join([' '.join(tags) for tags in self.tags])
        with open(self.tags_file, mode='w', encoding='utf-8') as f:
            f.write(lines)

    def gets(self):
        """ Return dict of
            {
              sentences: list of all sentences,
              tags: current assoc tags for the sentences,
              available_tags: available tags from available_tags.txt,
              unknown_tag: the tag to be used to mark unknown sentences
            }

        """
        result = dict()
        result['sentences'] = self.sentences
        result['tags'] = self.tags
        result['available_tags'] = self.tag_map
        result['unknown_tag'] = self.unknown_tag

        return result

    def update(self, tags):
        """ Update this session given a list of lists.
            [
             [tag_id_for_word_0, ...], # list of tags assoc with the first sentence
             ...
            ]

        :param tags: list
        """
        for i, tags in enumerate(tags):
            for k, tag_id in enumerate(tags):
                self.tag_sentence(i, k, k, int(tag_id))
        self.store()

    def generate_tags_file(self):
        """ Generate an plain Tags (all tags set to unknown) file.

        :return:
        """
        lines = '\n'.join([' '.join([self.unknown_tag] * len(sentence)) for sentence in self.sentences])
        with open(self.tags_file, mode='w', encoding='utf-8') as f:
            f.writelines(lines)

    def generate_available_tags_file(self):
        """ Generate an initial available_tags.txt file by collecting used tags in tags.txt.

        """
        available_tags = set()
        available_tags.add(self.unknown_tag)
        with open(self.tags_file, encoding='utf-8') as f:
            for tag_string in f.read().splitlines():
                available_tags.update([tag for tag in tag_string.split(' ')])

        lines = '\n'.join(available_tags)

        with open(self.available_tags_file, mode='w', encoding='utf-8') as f:
            f.writelines(lines)
