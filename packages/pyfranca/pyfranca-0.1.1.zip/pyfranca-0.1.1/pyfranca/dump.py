
def dump_namespace(namespace):
    if namespace.typedefs:
        print("\t\tTypedefs:")
        for item in namespace.typedefs.values():
            print("\t\t\t- {} is {}".format(item.name, item.type.name))
    if namespace.enumerations:
        print("\t\tEnumerations:")
        for item in namespace.enumerations.values():
            print("\t\t\t- {}".format(item.name))
    if namespace.structs:
        print("\t\tStructs:")
        for item in namespace.structs.values():
            print("\t\t\t- {}".format(item.name))
    if namespace.arrays:
        print("\t\tArrays:")
        for item in namespace.arrays.values():
            print("\t\t\t- {}".format(item.name))
    if namespace.maps:
        print("\t\tMaps:")
        for item in namespace.maps.values():
            print("\t\t\t- {}".format(item.name))


def dump_interface(interface):
    if interface.attributes:
        print("\t\tAttributes:")
        for item in interface.attributes.values():
            print("\t\t\t- {}".format(item.name))
    if interface.methods:
        print("\t\tMethods:")
        for item in interface.methods.values():
            print("\t\t\t- {}()".format(item.name))
    if interface.broadcasts:
        print("\t\tBroadcasts:")
        for item in interface.broadcasts.values():
            print("\t\t\t- {}".format(item.name))
    dump_namespace(interface)


def dump_package(package):
    print("- {} ({})".format(package.name, package.file))
    if package.imports:
        print("\tImports:")
        for imp in package.imports:
            print("\t- {} from {}".format(imp.namespace, imp.file))
    if package.interfaces:
        print("\tInterfaces:")
        for interface in package.interfaces.values():
            if interface.version:
                version_str = " (v{}.{})".format(interface.version.major,
                                                 interface.version.minor)
            else:
                version_str = ""
            print("\t- {}{}".format(interface.name, version_str))
            dump_interface(interface)
    if package.typecollections:
        print("\tType Collections:")
        for typecollection in package.typecollections.values():
            if typecollection.version:
                version_str = " (v{}.{})".format(typecollection.version.major,
                                                 typecollection.version.minor)
            else:
                version_str = ""
            print("\t- {}{}".format(typecollection.name, version_str))
            dump_namespace(typecollection)


def dump_packages(packages):
    print("Packages:")
    for package in packages:
        dump_package(package)
