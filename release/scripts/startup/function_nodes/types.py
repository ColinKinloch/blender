from . sockets import (
    FloatSocket,
    IntegerSocket,
    VectorSocket,
    CustomColoredSocket,
)

class SocketBuilder:
    def build(self, node_sockets, name):
        raise NotImplementedError()

class UniqueSocketBuilder(SocketBuilder):
    def __init__(self, socket_cls):
        self.socket_cls = socket_cls

    def build(self, node_sockets, name, identifier):
        return node_sockets.new(
            self.socket_cls.bl_idname,
            name,
            identifier=identifier)

class ColoredSocketBuilder(SocketBuilder):
    def __init__(self, color):
        self.color = color

    def build(self, node_sockets, name, identifier):
        socket = node_sockets.new(
            "fn_CustomColoredSocket",
            name,
            identifier=identifier)
        socket.color = self.color
        return socket

class DataTypesInfo:
    def __init__(self):
        self.data_types = set()
        self.builder_by_data_type = dict()
        self.list_by_base = dict()
        self.base_by_list = dict()

    def insert_data_type(self, data_type, builder):
        assert data_type not in self.data_types
        assert isinstance(builder, SocketBuilder)

        self.data_types.add(data_type)
        self.builder_by_data_type[data_type] = builder

    def insert_list_relation(self, base_type, list_type):
        assert self.is_data_type(base_type)
        assert self.is_data_type(list_type)
        assert base_type not in self.list_by_base
        assert list_type not in self.base_by_list

        self.list_by_base[base_type] = list_type
        self.base_by_list[list_type] = base_type

    def is_data_type(self, data_type):
        return data_type in self.data_types

    def is_base(self, data_type):
        return data_type in self.list_by_base

    def is_list(self, data_type):
        return data_type in self.base_by_list

    def to_list(self, data_type):
        assert self.is_base(data_type)
        return self.list_by_base[data_type]

    def to_base(self, data_type):
        assert self.is_list(data_type)
        return self.base_by_list[data_type]

    def to_builder(self, data_type):
        assert self.is_data_type(data_type)
        return self.builder_by_data_type[data_type]

    def build(self, data_type, node_sockets, name, identifier):
        builder = self.to_builder(data_type)
        socket = builder.build(node_sockets, name, identifier)
        socket.data_type = data_type
        return socket

    def get_data_type_items(self):
        items = []
        for data_type in self.data_types:
            items.append((data_type, data_type, ""))
        return items

    def get_base_type_items(self):
        items = []
        for data_type in self.list_by_base.keys():
            items.append((data_type, data_type, ""))
        return items

    def get_data_type_items_cb(self):
        def callback(_1, _2):
            return self.get_data_type_items()
        return callback


type_infos = DataTypesInfo()

type_infos.insert_data_type("Float", UniqueSocketBuilder(FloatSocket))
type_infos.insert_data_type("Vector", UniqueSocketBuilder(VectorSocket))
type_infos.insert_data_type("Integer", UniqueSocketBuilder(IntegerSocket))
type_infos.insert_data_type("Float List", ColoredSocketBuilder((0, 0.3, 0.5, 0.5)))
type_infos.insert_data_type("Vector List", ColoredSocketBuilder((0, 0, 0.5, 0.5)))
type_infos.insert_data_type("Integer List", ColoredSocketBuilder((0.3, 0.7, 0.5, 0.5)))

type_infos.insert_list_relation("Float", "Float List")
type_infos.insert_list_relation("Vector", "Vector List")
type_infos.insert_list_relation("Integer", "Integer List")