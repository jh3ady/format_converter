import csv
import io
import json
import yaml
from abc import ABC, abstractmethod


class SerializationError(Exception):
    pass


class DeserializationError(Exception):
    pass


class InvalidSerializerError(Exception):
    pass


class Serializer(ABC):
    serializers = {}

    def __init_subclass__(cls, **kwargs):
        if isinstance(kwargs["formats"], tuple):
            for format in kwargs["formats"]:
                if format not in Serializer.serializers:
                    cls.serializers[format] = cls()
        else:
            if kwargs["formats"] not in Serializer.serializers:
                cls.serializers[kwargs["formats"]] = cls()

    @abstractmethod
    def serialize(self, value: object) -> str:
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self, value: str) -> object:
        raise NotImplementedError()


class JsonSerializer(Serializer, formats="json"):
    def __init__(self):
        super().__init__()

    def serialize(self, value: object) -> str:
        return json.dumps(value)

    def deserialize(self, value: str) -> object:
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError as exc:
            raise DeserializationError(exc)


class JsonLinesSerializer(Serializer, formats="json_lines"):
    def __init__(self):
        super().__init__()

    def serialize(self, value: object) -> str:
        if isinstance(value, dict):
            return json.dumps(value)
        elif isinstance(value, list):
            return "\n".join([json.dumps(item) for item in value])
        else:
            raise SerializationError()

    def deserialize(self, value: str) -> object:
        try:
            return [json.loads(line) for line in value.split("\n")]
        except json.decoder.JSONDecodeError as exc:
            raise DeserializationError(exc)


class YamlSerializer(Serializer, formats=("yml", "yaml")):
    def __init__(self):
        super().__init__()

    def serialize(self, value: object) -> str:
        return yaml.safe_dump(value)

    def deserialize(self, value: str) -> object:
        return yaml.safe_load(value)


class CsvSerializer(Serializer, formats="csv"):
    def __init__(self):
        super().__init__()

    def serialize(self, value: object) -> str:
        fd = io.StringIO()
        if isinstance(value, dict):
            fieldnames = value.keys()
            writer = csv.DictWriter(fd, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerow(value)
        elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            fieldnames = value[0].keys()
            writer = csv.DictWriter(fd, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(value)
        else:
            raise SerializationError()
        return fd.getvalue()

    def deserialize(self, value: str) -> object:
        items = []
        fd = io.StringIO(value)

        reader = csv.DictReader(fd)

        for row in reader:
            items.append({column: row[column] for column in row})

        return items

