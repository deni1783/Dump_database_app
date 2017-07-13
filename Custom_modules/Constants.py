PATH_TO_DIALECTS_LIST_JSON = r'Dialects/supported_dialects.json'
PATH_TO_PROFILE_SETTINGS_JSON = r'Settings/connection_profiles.json'
PATH_TO_DEFAULT_OBJECTS_JSON = r'Settings/default_objects.json'
PATH_TO_CUSTOM_SETTINGS_JSON = r'Settings/custom_settings.json'

# Для этого списка диалектов, в запросах нужно изменять БАЗУ в параметрах подключения
DIALECTS_FOR_CHANGE_DB_IN_QUERIES = ['postgresql', 'greenplum']
# DIALECTS_FOR_CHANGE_DB_IN_QUERIES = ['postgresql']