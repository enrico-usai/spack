# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Chai(CMakePackage, CudaPackage):
    """Copy-hiding array interface for data migration between memory spaces"""

    homepage = "https://github.com/LLNL/CHAI"
    url      = "https://github.com/LLNL/CHAI.git"

    version('develop', branch='develop', submodules='True')
    version('master', branch='master', submodules='True')
    version('1.2.0', tag='v1.2.0', submodules='True')
    version('1.1.0', tag='v1.1.0', submodules='True')
    version('1.0', tag='v1.0', submodules='True')

    depends_on('cmake@3.8:', type='build')
    depends_on('umpire')

    depends_on('cmake@3.9:', type='build', when="+cuda")
    depends_on('umpire+cuda', when="+cuda")

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))

        else:
            options.append('-DENABLE_CUDA=Off')

        options.append('-Dumpire_DIR:PATH='
                       + spec['umpire'].prefix + "/share/umpire/cmake")

        return options
