from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from glob import glob
import shutil


class ThreadedFileRemover:
    def __init__(self, *paths, num_threads=None):
        """
        Uses threaded operations to delete folders and files listed as
        glob `paths`.  Number of threads defaults to 2 x cpu_count 
        when `num_threads` is 0 or None.
        """
        self.paths = []
        for p in paths:
            self.paths.extend(glob(p))
        self.num_threads = num_threads if num_threads else 2*cpu_count()
        
    @staticmethod
    def _rmtree(d):
        shutil.rmtree(d)
        return d

    def prune_paths(self):
        with ThreadPoolExecutor(self.num_threads) as pool:
            threads = [pool.submit(self._rmtree, d) for d in dirs]
            for f in as_completed(threads):
                try:
                    d = f.result()
                except Exception as e:
                    print('Error occured: ', e)
                else:
                    print(f'REMOVED: {d}')
        return True
