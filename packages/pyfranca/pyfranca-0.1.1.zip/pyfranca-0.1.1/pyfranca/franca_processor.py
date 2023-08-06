
import os
from pyfranca import franca_parser
from pyfranca import ast


class ProcessorException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Processor:

    def __init__(self):
        self.package_paths = ["."]
        self.files = {}
        self.packages = {}

    def _basename(self, namespace):
        dot = namespace.rfind(".")
        if dot == -1:
            return namespace
        else:
            return namespace[dot + 1:]

    def _packagename(self, namespace):
        dot = namespace.rfind(".")
        if dot == -1:
            return None
        else:
            return namespace[0:dot]

    def _import_namespace_types(self, types, namespace):
        for item in namespace.typedefs.values():
            types[item.name] = item
        for item in namespace.enumerations.values():
            types[item.name] = item
        for item in namespace.structs.values():
            types[item.name] = item
        for item in namespace.arrays.values():
            types[item.name] = item
        for item in namespace.maps.values():
            types[item.name] = item

    def _import_interface_types(self, types, interface):
        # if interface.attributes:
        #     for item in interface.attributes.values():
        #         types[item.name] = item.type
        # if interface.methods:
        #     for item in interface.methods.values():
        #         types[item.name] = item
        # if interface.broadcasts:
        #     for item in interface.broadcasts.values():
        #         types[item.name] = item
        # self._import_namespace_types(types, interface)
        pass

    def _build_package_type_list(self, package):
        package.types = {}

        for imp in package.imports:
            if imp.namespace and imp.namespace.endswith(".*"):
                namespace = imp.namespace[:-2]
                type = self._basename(namespace)
                packagename = self._packagename(namespace)
                if packagename not in self.packages:
                    raise ProcessorException("Unknown package {}".format(packagename))
                if type not in self.packages[packagename].typecollections:
                    raise ProcessorException("Type {} not in {}".format(type, packagename))
                self._import_interface_types(package.types, self.packages[packagename].typecollections)
            else:
                raise NotImplementedError("No support for model imports.")

        for interface in package.interfaces.values():
            self._import_interface_types(package.types, interface)
        for typecollection in package.typecollections.values():
            self._import_namespace_types(package.types, typecollection)

    def _verify_type(self, package, type):
        if isinstance(type, ast.PrimitiveType):
            return "OK"
        elif isinstance(type, ast.ComplexType):
            return "OK2"
        elif isinstance(type, ast.CustomType):
            if type in package.types:
                return "OK3"
            else:
                return "oops"
        else:
            return "???"

    def _verify_package_type_list(self, package):
        for typecollection in package.typecollections.values():
            for typedef in typecollection.typedefs.values():
                res = self._verify_type(package, typedef.type)
                print(typedef.name, res)

    def _import_package(self, fspec, references):
        if not os.path.exists(fspec):
            for path in self.package_paths:
                temp_fspec = os.path.join(path, fspec)
                if os.path.exists(temp_fspec):
                    fspec = temp_fspec
                    break
            else:
                raise ProcessorException("{} not found.".format(fspec))

        parser = franca_parser.Parser()
        package = parser.parse_file(fspec)

        if package.name in references:
            raise ProcessorException("Circular dependency for package \"{}\".".
                                     format(package.name))

        self.packages[package.name] = package
        self.files[fspec] = package

        for package_import in package.imports:
            self._import_package(package_import.file,
                                 references + [package.name])

        self._build_package_type_list(package)
        self._verify_package_type_list(package)

        return package

    def read_file(self, fspec):
        package = self._import_package(fspec, [])
        return package
