objectClassFileType = {
    'binary.unpacked.zip': 'unp.zip',
    'binary.unpacked': 'unp.exe',
    'binary.pe32': 'exe',
    "archive.zip": "zip",
    "archive.tar": "tar",
    "archive.tgz": "tgz",
    "archive.7z" : "7z",
    "archive.gz" : "gz",
    "json.juice" : "juice.json",
    "json.strings": "strings.json",
    "json.apiflowgraph":"apiflowgraph.json",
    "dot.callgraph":"callgraph.dot"
}

def is_original_class (object_class):
    return 'binary.pe' in object_class or 'archive' in object_class or 'unhandled' in object_class

def is_malware_class (object_class):
    return 'binary' in object_class or 'archive' in object_class

def is_binary_class (object_class):
    return 'binary.pe' in object_class or 'binary.unpacked' in object_class


