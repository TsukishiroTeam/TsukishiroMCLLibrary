class McMirrorInfo:
    def __init__(
            self,
            piston_meta_v1: str,
            piston_meta_v2: str,
            java_index: str,
            libraries: str,
            resource_server: str
            ):
        self.piston_meta_v1 = piston_meta_v1
        self.piston_meta_v2 = piston_meta_v2
        self.java_index = java_index
        self.libraries = libraries
        self.resource_server = resource_server