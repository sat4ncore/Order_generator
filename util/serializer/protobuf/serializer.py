from generator.order import OrderTuple
import util.serializer.protobuf.order_pb2 as proto


class ProtobufSerializer:
    @classmethod
    def serialize(cls, order: OrderTuple):
        proto_order = proto.Order()
        proto_order.identifier = order.identifier
        proto_order.currency_pair = order.currency_pair
        proto_order.direction = order.direction
        proto_order.status = order.status
        proto_order.timestamp = order.timestamp
        proto_order.initial_price = order.initial_price
        proto_order.filled_price = order.filled_price
        proto_order.initial_volume = order.initial_volume
        proto_order.filled_volume = order.filled_volume
        proto_order.description = order.description
        proto_order.tags = order.tags

        return proto_order.SerializeToString()

    @classmethod
    def deserialize(cls, order):
        proto_order = proto.Order()
        proto_order.ParseFromString(order)
        order = OrderTuple(proto_order.identifier,
                           proto_order.currency_pair,
                           proto_order.direction,
                           proto_order.status,
                           proto_order.timestamp,
                           proto_order.initial_price,
                           proto_order.filled_price,
                           proto_order.initial_volume,
                           proto_order.filled_volume,
                           proto_order.description,
                           proto_order.tags)
        return order

