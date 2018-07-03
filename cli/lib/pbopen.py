from contextlib import contextmanager
from os.path import getsize, basename

import sys
from tqdm import tqdm

@contextmanager
def pbopen(filename):
    total = getsize(filename)
    pb = tqdm(total=total, unit="B", unit_scale=True,
              desc=basename(filename), miniters=1,
              ncols=80, ascii=True)

    def wrapped_line_iterator(fd):
        processed_bytes = 0
        for line in fd:
            processed_bytes += len(line)
            # update progress every MB.
            if processed_bytes >= 1024 * 1024:
                pb.update(processed_bytes)
                processed_bytes = 0
            yield line

        # finally
        pb.update(processed_bytes)
        pb.close()
    with open(filename) as fd:
        yield wrapped_line_iterator(fd)

if __name__ == "__main__":
    pbopen(sys.argv)
