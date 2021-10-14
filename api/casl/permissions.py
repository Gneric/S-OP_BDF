from casl import AbilityBuilder
from api.utils.hasura_api import checkPermissions

def ability_for(user):
    permissions = checkPermissions(user)
    # Buscar en Hasura si existe usuario
        # Si no existe return error
    # Tomar las permissions del usuario enviado
    # crear un build de abilities con las permissions del Hasura
    # retornar las abilities y en los endpoints si el usuario 
    # no cuenta con los permisos para hacer algo devuelve error
    ability_builder = AbilityBuilder()
    for p in permissions:
        ability_builder.can(p['action'], p['subject'])
    return ability_builder.build()
