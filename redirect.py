import os

# Define a context manager to suppress stdout and stderr for internal libraries
# solution inspired by https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
class redirect_stdout_stderr:
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
    '''
    def __init__(self):
        # Open a pair of null files
        self.redirect_fds =  [os.open("stdout.log", os.O_RDWR | os.O_CREAT), os.open("stderr.log", os.O_RDWR | os.O_CREAT)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.redirect_fds[0], 1)
        os.dup2(self.redirect_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.redirect_fds + self.save_fds:
            os.close(fd)