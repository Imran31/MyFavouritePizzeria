from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        return BaseSerializer(**validated_data)


class OrderSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'cost': instance.cost,
            'customer_id': instance.customer_id,
            'status': instance.status,
            'created': instance.created_at,
        }

class CustomerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'mobile_number': instance.mobile_number,
        }

class PizzaGenericSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
        }


class PizzaSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'pizza_id': instance.pizza.id,
            'pizza_base': instance.pizza.pizza_base.name,
            'cheese': instance.pizza.cheese.name,
            'topping': instance.topping.name
        }


    