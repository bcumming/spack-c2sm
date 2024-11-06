from spack.pkg.builtin.icon import Icon as SpackIcon


class IconMch(SpackIcon):
    git = 'git@gitlab.dkrz.de:icon/icon-nwp.git'

    maintainers("dominichofer")

    version('master', submodules=True)
    version('icon-2.6.6-mch2b', submodules=True)
    version('icon-2.6.6-mch2a', submodules=True)

    # Model Features:
    variant('dace',
            default=False,
            description='Enable the DACE modules for data assimilation')
    requires("+mpi", when="+dace")

    variant('emvorado',
            default=False,
            description='Enable the radar forward operator EMVORADO')
    requires("+mpi", when="+emvorado")

    # Infrastructural Features:
    variant('async-io-rma',
            default=True,
            description='Enable remote memory access (RMA) for async I/O')
    variant('realloc-buf',
            default=False,
            description='Enable reallocatable communication buffer')

    # Optimization Features:
    variant(
        'pgi-inlib',
        default=False,
        description=
        'Enable PGI/NVIDIA cross-file function inlining via an inline library')

    # MCH specific features:
    variant(
        'eccodes-definitions',
        default=False,
        description=
        'Enable extension of eccodes with center specific definition files')

    depends_on('cosmo-eccodes-definitions',
               type='run',
               when='+eccodes-definitions')

    with when('+emvorado'):
        depends_on('eccodes +fortran')
        depends_on('hdf5 +szip +hl +fortran')
        depends_on('zlib')

    def configure_args(self):
        args = super().configure_args()
        super_libs = args.pop()

        libs = LibraryList([])

        for x in [
                'dace',
                'emvorado',
                'async-io-rma',
                'realloc-buf',
                'pgi-inlib',
        ]:
            args += self.enable_or_disable(x)

        if '+emvorado' in self.spec:
            libs += self.spec['eccodes:fortran'].libs
            libs += self.spec['hdf5:fortran,hl'].libs
            libs += self.spec['zlib'].libs

        args.append(f"{super_libs} {libs.link_flags}")
        return args