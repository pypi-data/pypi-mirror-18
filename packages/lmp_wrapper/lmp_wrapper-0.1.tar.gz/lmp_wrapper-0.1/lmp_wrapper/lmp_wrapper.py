from subprocess import Popen, PIPE

class LammpsError(Exception):
    pass

class Lammps:
    """Wrapper for Lammps

        What this class is for
        - Handles program calling differences between mpi and serial
          (default mpi)
        - Raises exceptions of type LammpsError when Lammps exits in error

        Example
        -------

            from lmp_wrapper import Lammps
            lmp = Lammps()
            lmp.in(input_string)
            lmp.read(file_handle)
            lmp.open(file_path)
            lmp.run(5000)
    """
    def __init__(self, version='mpi', num_threads=None, verbosity=0,
                 stdout_path='.stdout', stderr_path='.stderr'):
        """Initialize Lammps wrapper

        Parameters
        ----------
        version : str
            type of Lammps to use (default 'mpi')

        Returns
        -------
        lmp : Lammps
            class instance used to control Lammps

        Example
        -------
            with Lammps(num_threads=12) as lmp:
                lmp.open('settings.in')
                lmp.in('read_data conf.data')
                lmp.in('fix 1 all nve')
                lmp.run(5000)
        """
        self.verbosity = int(verbosity)
        self.version = version
        if num_threads is None:
            num_threads = 1
        self.num_threads = num_threads

        self.stderr_path = stderr_path
        self.stdout_path = stdout_path
            
    def __enter__(self):
        self.stdout = open(self.stdout_path, 'w')
        self.stderr = open(self.stderr_path, 'w')
        if self.version == 'mpi':
            self.p = Popen(['mpirun', '-np', str(self.num_threads), 'lmp_mpi'],
                           stdin=PIPE, stdout=self.stdout, stderr=self.stderr)
        else:
            raise NotImplementedError('No support for version {}'.format(
                                                                  self.version))
        return self

    def check_error(self):
        """Read standard error file to decide if Lammps ended in error.
        Raises an exception if Lammps ended in error.
        """
        error_flag = False
        error_msg = '\n'
        with open(self.stdout_path, 'r') as stdout:
            for line in stdout.readlines():
                if 'ERROR' in line:
                    error_flag = True
                    error_msg += line
                elif error_flag:
                    raise LammpsError(error_msg)

        if self.poll() is not None and self.poll() != 0:
            raise LammpsError('Lammps exited with code {}'.format(self.poll()))

    def inp(self, text):
        self.p.stdin.write(text)
        self.check_error()

    def open(self, path):
        with open(path) as f:
            self.p.stdin.write(f.read())
        self.check_error()

    def poll(self):
        return self.p.poll()

    def __exit__(self, type=None, value=None, traceback=None):
        self.p.communicate('\n')
        self.stdout.close()
        self.stderr.close()
        self.check_error()
