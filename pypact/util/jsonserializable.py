import json


class JSONSerializable(object):

    def json_serialize(self):
        def obj_dict(obj):
            new_dict = {}
            for k, v in obj.__dict__.items():
                if '__' not in k:
                    new_dict[k] = v
            return new_dict

        return json.dumps(self, default=obj_dict, indent=4, sort_keys=False)

    def json_deserialize(self, j, objtype=object):
        """
        Read the JSON file into the JSONSerializable data objects

        :param j: The JSON dump
        :param key: The key/member variable name
        :param objtype: The type of object to be added to the list
        :return:
        """
        d = json.loads(j)
        for key, value in self.__dict__.items():
            if key in d:
                if isinstance(value, JSONSerializable):
                    value.json_deserialize(json.dumps(d[key]))
                elif isinstance(d[key], dict):
                    self.json_deserialize(json.dumps(d[key]))
                elif isinstance(value, list):
                    self.json_deserialize_list(json.dumps(d[key]), key, objtype=objtype)
                else:
                    setattr(self, key, d[key])

    def json_deserialize_list(self, j, key, objtype):
        """
        This is a little hack, but I cannot think of a better way to deserialize a
        list of objects

        :param j: The JSON dump
        :param key: The key/member variable name
        :param objtype: The time of object to be added to the list
        :return:
        """
        d = json.loads(j)

        def do_append(a):
            # for the standard case of a list of str, int or floats
            if isinstance(a, (int, float, str)):
                self.__dict__[key].append(a)
                return

            # for the unique case of a list of JSONSerializable objects
            t = objtype()
            if isinstance(t, JSONSerializable):
                t.json_deserialize(json.dumps(a))
                self.__dict__[key].append(t)

        if key in d:
            for i in d[key]:
                if isinstance(self.__dict__[key], list):
                    do_append(i)
        else:
            if isinstance(d, list):
                for l in d:
                    do_append(l)
