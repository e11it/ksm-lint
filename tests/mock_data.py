MOCK_DATA = '''
KafkaPrincipal,ResourceType,PatternType,ResourceName,Operation,PermissionType,Host
User:dsfsdfgsdfgsdfg,Topic,LITERAL,sdfgsdfgsdfgsdfg,Read,Allow,*
User:sdfgsdfgdfsgsf,Topic,LITERAL,sdfgsdfgsdfgsdfgsdfg,Read,Allow,*
User:hjghdfghdfhfgh,Group,PREFIXED,dfghdfghdfghdfghdfh,All,Allow,*
User:dfghdfghdfghdfgh,Topic,PREFIXED,dfghdfghdfgh,All,Allow,*
User:asdfasdfasdf,Cluster,LITERAL,kafka-cluster,DESCRIBE,Allow,*
User:fgdhfgbdgfhfh,Cluster,LITERAL,kafka-cluster,IdempotentWrite,Allow,*
User:dfgnbcvb45tdfgdf@app-nl-st-ibakfk,TRANSACTIONALID,PREFIXED,dfghdfghdfghdfghd,All,Allow,*
User:dgfh4hdfgfgh,Group,PREFIXED,dfghfghdfghdfghdfh,All,Allow,*
User:dgndgh4g,Topic,PREFIXED,0dfghdfghd.,Read,Allow,*
'''.strip()