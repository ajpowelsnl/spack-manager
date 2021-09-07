from spack.pkg.builtin.trilinos import Trilinos as bTrilinos

class Trilinos(bTrilinos):
    depends_on('ninja', type='build')
    generator = 'Ninja'

    # Last known working GPU commit
    #version('develop', commit='4796b92fb0644ba8c531dd9953e7a4878b05c62d')

    def setup_build_environment(self, env):
        spec = self.spec
        if '+cuda' in spec and '+wrapper' in spec:
            if '+mpi' in spec:
                env.set('OMPI_CXX', spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            else:
                env.set('CXX', spec["kokkos-nvcc-wrapper"].kokkos_cxx)
        # Workaround for segfaults with IPO
        if '%intel' in spec and '+stk' in spec:
            for cc in "CXX C F LD".split():
                env.append_flags(cc + "FLAGS", '-no-ipo')
