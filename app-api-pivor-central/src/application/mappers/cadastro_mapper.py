from application.schemas import CadastroPivoSchema
from domain.entities.avaliacao import CadastroPivo


def cadastro_schema_to_entity(schema: CadastroPivoSchema) -> CadastroPivo:
    data = schema.model_dump()
    canhao = data.get("canhao")
    if canhao is not None:
        data["canhao"] = canhao.value if hasattr(canhao, "value") else canhao
    return CadastroPivo(**data)


def cadastro_entity_to_schema(entity: CadastroPivo) -> CadastroPivoSchema:
    return CadastroPivoSchema.model_validate(entity.__dict__)
