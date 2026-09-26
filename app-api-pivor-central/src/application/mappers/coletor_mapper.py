from application.schemas import ColetorSchema
from domain.value_objects.coletor import Coletor


def coletor_schema_to_entity(schema: ColetorSchema) -> Coletor:
    return Coletor(**schema.model_dump())


def coletor_entity_to_schema(entity: Coletor) -> ColetorSchema:
    return ColetorSchema.model_validate(entity.__dict__)
