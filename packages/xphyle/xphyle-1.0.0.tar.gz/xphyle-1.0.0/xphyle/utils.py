# -*- coding: utf-8 -*-
"""A collection of convenience methods for reading, writing, and otherwise
managing files. All of these functions are 'safe', meaning that if you pass
``errors=False`` and there is a problem opening the file, the error will be
handled gracefully.
"""
from collections import OrderedDict, Iterable
import copy
import csv
import io
from itertools import cycle
import os
import shutil
import sys

from xphyle import *
from xphyle.formats import *
from xphyle.paths import *

# Reading data from/writing data to files

## Raw data

def read_lines(path : 'str|file', convert : 'callable' = None,
               strip_linesep : 'bool' = True, **kwargs) -> 'generator':
    """Iterate over lines in a file.
    
    Args:
        path: Path to the file, or a file-like object
        convert: Function to call on each line in the file
        strip_linesep: Whether to strip off trailing line separators
        kwargs: Additional arguments to pass to open_
    
    Returns:
        Iterator over the lines of a file, with line endings stripped.
    """
    with open_(path, **kwargs) as f:
        if f is None:
            return ()
        itr = f
        if strip_linesep:
            itr = (line.rstrip() for line in itr)
        if convert:
            itr = (convert(line) for line in itr)
        for line in itr:
            yield line

def read_bytes(path : 'str|file', chunksize : 'int,>0' = 1024,
               **kwargs) -> 'generator':
    """Iterate over a file in chunks. The mode will always be overridden
    to 'rb'.
    
    Args:
        path: Path to the file, or a file-like object
        chunksize: Number of bytes to read at a time
        kwargs: Additional arguments to pass top ``open_``
    
    Yields:
        Chunks of the input file as bytes. Each chunk except the last should
        be of size ``chunksize``.
    """
    kwargs['mode'] = 'rb'
    with open_(path, **kwargs) as f:
        if f is None:
            return ()
        for chunk in iter_file_chunked(f, chunksize):
            yield chunk

def write_lines(iterable : 'iterable', path : 'str|file',
                linesep : 'str' = '\n', convert : 'callable' = str,
                **kwargs) -> 'int':
    """Write delimiter-separated strings to a file.
    
    Args:
        iterable: An iterable
        path: Path to the file, or a file-like object
        linesep: The delimiter to use to separate the strings, or
            ``os.linesep`` if None (defaults to '\\n')
        convert: Function that converts a value to a string
        kwargs: Additional arguments to pass top ``open_``
    
    Returns:
        Total number of bytes written, or -1 if ``errors=False`` and there was
        a problem opening the file.
    """
    if linesep is None:
        linesep = os.linesep
    if 'mode' not in kwargs:
        kwargs['mode'] = 'wt'
    written = 0
    with open_(path, **kwargs) as f:
        if f is None:
            return -1
        for s in iterable:
            if written > 0:
                written += f.write(linesep)
            written += f.write(convert(s))
    return written

def to_bytes(x, encoding='utf-8'):
    """Convert an arbitrary value to bytes.
    
    Args:
        x: Some value
        encoding: The byte encoding to use
    
    Returns:
        x converted to a string and then encoded as bytes
    """
    if isinstance(x, bytes):
        return(x)
    return str(x).encode(encoding)

def write_bytes(iterable : 'iterable', path : 'str|file', sep : 'bytes' = b'',
                convert : 'callable' = to_bytes, **kwargs) -> 'int':
    """Write an iterable of bytes to a file.
    
    Args:
        iterable: An iterable
        path: Path to the file, or a file-like object
        sep: Separator between items
        convert: Function that converts a value to bytes
        kwargs: Additional arguments to pass top ``open_``
    
    Returns:
        Total number of bytes written, or -1 if ``errors=False`` and there was
        a problem opening the file.
    """
    if sep is None:
        sep = convert(os.linesep)
    if 'mode' not in kwargs:
        kwargs['mode'] = 'wb'
    written = 0
    with open_(path, **kwargs) as f:
        if f is None:
            return -1
        for b in iterable:
            if written > 0:
                written += f.write(sep)
            written += f.write(convert(b))
    return written

# key=value files

def read_dict(path: 'str|file', sep : 'str' = '=', convert : 'callable' = None,
              ordered : 'bool' = False, **kwargs) -> 'dict':
    """Read lines from simple property file (key=value). Comment lines (starting
    with '#') are ignored.
    
    Args:
        path: Property file, or a list of properties.
        sep: Key-value delimiter (defaults to '=')
        convert: Function to call on each value
        ordered: Whether to return an OrderedDict
        kwargs: Additional arguments to pass top ``open_``
    
    Returns:
        An OrderedDict, if 'ordered' is True, otherwise a dict.
    """
    def parse_line(line):
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            return None
        return line.split(sep)
    lines = filter(None, read_lines(path, convert=parse_line, **kwargs))
    if convert:
        lines = ((k, convert(v)) for k, v in lines)
    return OrderedDict(lines) if ordered else dict(lines)

def write_dict(d : 'dict', path : 'str', sep : 'str' = '=',
               linesep : 'str' = '\n', convert : 'callable' = str, **kwargs):
    """Write a dict to a file as name=value lines.
    
    Args:
        d: The dict
        path: Path to the file
        sep: The delimiter between key and value (defaults to '=')
        linesep: The delimiter between values, or ``os.linesep`` if None
            (defaults to '\\n')
        convert: Function that converts a value to a string
    """
    if linesep is None:
        linesep = os.linesep
    write_lines(
        ("{}{}{}".format(k, sep, convert(v)) for k, v in d.items()),
        path, linesep=linesep, **kwargs)

## Other delimited files

def read_delimited(path : 'str', sep : 'str' = '\t',
                   header : 'bool|iterable' = False,
                   converters : 'callable|iterable' = None,
                   yield_header : 'bool' = True,
                   row_type : 'str|callable' = 'list',
                   **kwargs) -> 'generator':
    """Iterate over rows in a delimited file.
    
    Args:
        path: Path to the file, or a file-like object
        sep: The field delimiter
        header: Either True or False to specifiy whether the file has a header,
            or an iterable of column names.
        converters: callable, or iterable of callables, to call on each value
        yield_header: If header == True, whether the first row yielded should be
            the header row
        row_type: The collection type to return for each row:
            tuple, list, or dict
        kwargs: additional arguments to pass to ``csv.reader``
    
    Yields:
        Rows of the delimited file. If ``header==True``, the first row yielded
        is the header row, and its type is always a list. Converters are not
        applied to the header row.
    """
    if row_type == 'dict' and not header:
        raise ValueError("Header must be specified for row_type=dict")
    
    with open_(path, **kwargs) as f:
        if f is None:
            return ()
        
        reader = csv.reader(f, delimiter=sep, **kwargs)
        
        if header is True:
            header_row = next(reader)
            if yield_header:
                yield header_row
        
        if converters:
            if not is_iterable(converters):
                if callable(converters):
                    converters = cycle([converters])
                else:
                    raise ValueError("'converters' must be iterable or callable")
            
            reader = (
                [fn(x) if fn else x for fn, x in zip(converters, row)]
                for row in reader)
        
        if row_type == 'tuple':
            reader = (tuple(row) for row in reader)
        elif row_type == 'dict':
            reader = (dict(zip(header_row, row)) for row in reader)
        elif callable(row_type):
            reader = (row_type(row) for row in reader)
        
        for row in reader:
            yield row

def read_delimited_as_dict(path : 'str', sep : 'str' = '\t',
                           header : 'bool|iterable' = False,
                           key : 'int,>=0|callable' = 0, **kwargs) -> 'dict':
    """Parse rows in a delimited file and add rows to a dict based on a a
    specified key index or function.
    
    Args:
        path: Path to the file, or a file-like object
        sep: Field delimiter
        key: The column to use as a dict key, or a function to extract the key
          from the row. If a string value, header must be specified. All values
          must be unique, or an exception is raised.
        kwargs: Additional arguments to pass to ``read_delimited``
    
    Returns:
        A dict with as many element as rows in the file
    
    Raises:
        Exception if a duplicte key is generated
    """
    itr = None
    
    if isinstance(key, str):
        if not header:
            raise ValueError(
                "'header' must be specified if 'key' is a column name")
        if header is True:
            kwargs['yield_header'] = True
            itr = read_delimited(path, sep, True, **kwargs)
            header = next(itr)
        key = header.index(key)
    
    if isinstance(key, int):
        keyfn = lambda row: row[key]
    elif callable(key):
        keyfn = key
    else:
        raise ValueError("'key' must be an column name, index, or callable")
    
    if itr is None:
        kwargs['yield_header'] = False
        itr = read_delimited(path, sep, header, **kwargs)
    
    d = {}
    for row in itr:
        k = keyfn(row)
        if k in d:
            raise Exception("Duplicate key {}".format(k))
        d[k] = row
    return d

## Compressed files

def compress_file(source_file : 'str|file', compressed_file : 'str|file' = None,
                  compression : 'bool|str' = None,
                  keep : 'bool' = True, compresslevel : 'int' = None,
                  use_system : 'bool' = True, **kwargs) -> 'str':
    """Compress an existing file, either in-place or to a separate file.
    
    Args:
        source_file: Path or file-like object to compress
        compressed_file: The compressed path or file-like object. If None,
            compression is performed in-place. If True, file name is determined
            from ``source_file`` and the uncompressed file is retained.
        compression: If True, guess compression format from the file
            name, otherwise the name of any supported compression format.
        keep: Whether to keep the source file
        compresslevel: Compression level
        use_system: Whether to try to use system-level compression
        kwargs: Additional arguments to pass to the open method when
            opening the compressed file
    
    Returns:
        The path to the compressed file
    """
    if not isinstance(compression, str):
        if compressed_file:
            compression = guess_compression_format(compressed_file
                if isinstance(compressed_file, str) else compressed_file.name)
        else:
            raise ValueError(
                "'compressed_file' or 'compression' must be specified")
    
    fmt = get_compression_format(compression)
    return fmt.compress_file(
        source_file, compressed_file, keep, compresslevel, use_system, **kwargs)

def uncompress_file(compressed_file : 'str|file', dest_file : 'str|file' = None,
                    compression : 'bool|str' = None,
                    keep : 'bool' = True, use_system : 'bool' = True,
                    **kwargs) -> 'str':
    """Uncompress an existing file, either in-place or to a separate file.
    
    Args:
        compressed_file: Path or file-like object to uncompress
        dest_file: Path or file-like object for the uncompressed file.
            If None, file will be uncompressed in-place. If True, file will be
            uncompressed to a new file (and the compressed file retained) whose
            name is determined automatically.
        compression: None or True, to guess compression format from the file
            name, or the name of any supported compression format.
        keep: Whether to keep the source file
        use_system: Whether to try to use system-level compression
        kwargs: Additional arguments to pass to the open method when
            opening the compressed file
    
    Returns:
        The path of the uncompressed file
    """
    if not isinstance(compression, str):
        source_path = compressed_file
        if not isinstance(compressed_file, str):
            source_path = compressed_file.name
        compression = guess_compression_format(source_path)
    fmt = get_compression_format(compression)
    return fmt.uncompress_file(
        compressed_file, dest_file, keep, use_system, **kwargs)

def transcode_file(source_file : 'str|file', dest_file : 'str|file',
                   source_compression : 'str|bool' = True,
                   dest_compression : 'str|bool' = True,
                   use_system : 'bool' = True,
                   source_open_args : 'dict' = {},
                   dest_open_args : 'dict' = {}):
    """Convert from one file format to another.
    
    Args:
        source_file: The path or file-like object to read from. If a file, it
            must be opened in mode 'rb'.
        dest_file: The path or file-like object to write to. If a file, it
            must be opened in binary mode.
        source_compression: The compression type of the source file. If True,
            guess compression format from the file name, otherwise the name of
            any supported compression format.
        dest_compression: The compression type of the dest file. If True,
            guess compression format from the file name, otherwise the name of
            any supported compression format.
        source_open_args: Additional arguments to pass to xopen for the source
            file
        dest_open_args: Additional arguments to pass to xopen for the
            destination file
    """
    src_args = copy.copy(source_open_args)
    if 'mode' not in src_args:
        src_args['mode'] = 'rb'
    dst_args = copy.copy(dest_open_args)
    if 'mode' not in dst_args:
        dst_args['mode'] = 'wb'
    with open_(source_file, compression=source_compression,
               use_system=use_system, **src_args) as src, \
            open_(dest_file, compression=dest_compression,
                  use_system=use_system, **dst_args) as dst:
        for chunk in iter_file_chunked(src):
            dst.write(chunk)

# FileEventListeners

class CompressOnClose(FileEventListener):
    """Compress a file after it is closed."""
    def execute(self, path, *args, **kwargs):
        self.compressed_path = compress_file(path, *args, **kwargs)

class MoveOnClose(FileEventListener):
    """Move a file after it is closed.."""
    def execute(self, path, dest):
        shutil.move(path, dest)

class RemoveOnClose(FileEventListener):
    """Remove a file after it is closed.."""
    def execute(self, path):
        os.remove(path)

# Replacement for fileinput, plus fileoutput

class FileManager(object):
    """Dict-like container for files. Files are opened lazily (upon first
    request) using ``xopen``.
    
    Args:
        files: An iterable of files to add. Each item can either be a string
            path or a (key, fileobj) tuple.
        kwargs: Default arguments to pass to xopen
    """
    def __init__(self, files=None, **kwargs):
        self._files = OrderedDict()
        self._paths = {}
        self.default_open_args = kwargs
        if files:
            self.add_all(files)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.close()
    
    def __del__(self):
        self.close()
    
    def __len__(self):
        return len(self._files)
    
    def __getitem__(self, key : 'str|int'):
        f = self.get(key)
        if not f:
            raise KeyError(key)
        return f
    
    def __setitem__(self, key : 'str', f : 'str|file'):
        """Add a file.
        
        Args:
            key: Dict key
            f: Path or file object. If this is a path, the file will be
                opened with mode 'r'.
        """
        self.add(f, key)
    
    def __contains__(self, key : 'str'):
        return key in self._files
        
    def add(self, f, key : 'str' = None, **kwargs):
        """Add a file.
        
        Args:
            f: Path or file object. If this is a path, the file will be
                opened with the specified mode.
            key: Dict key. Defaults to the file name.
            kwargs: Arguments to pass to xopen. These override any keyword
                arguments passed to the FileManager's constructor.
        """
        if isinstance(f, str):
            path = f
            f = copy.copy(self.default_open_args)
            f.update(kwargs)
        else:
            path = f.name
        if key is None:
            key = path
        if key in self._files:
            raise ValueError("Already tracking file with key {}".format(key))
        self._files[key] = f
        self._paths[key] = path
    
    def add_all(self, files, **kwargs):
        """Add all files from an iterable or dict.
        
        Args:
            files: An iterable or dict of files to add. If an iterable, each
                item can either be a string path or a (key, fileobj) tuple.
            kwargs: Additional arguments to pass to ``add``
        """
        if isinstance(files, dict):
            for key, f in files.items():
                self.add(f, key=key)
        else:
            for f in files:
                if isinstance(f, str):
                    self.add(f, **kwargs)
                else:
                    self.add(f[1], key=f[0], **kwargs)
    
    def get(self, key : 'str|int'):
        """Get the file object associated with a path. If the file is not
        already open, it is first opened with ``xopen``.
        """
        f = self._files.get(key, None)
        if f is None:
            if isinstance(key, int) and len(self) > key:
                key = list(self.keys)[key]
                f = self._files[key]
            else:
                return None
        if isinstance(f, dict):
            path = self._paths[key]
            f = xopen(path, **f)
            self._files[key] = f
        return f
    
    def get_path(self, key : 'str'):
        """Returns the file path associated with a key.
        
        Args:
            key: The key to resolve
        """
        if isinstance(key, int) and len(self) > key:
            key = list(self.keys)[key]
        return self._paths[key]
    
    @property
    def keys(self):
        """Returns a list of all keys in the order they were added.
        """
        return self._files.keys()
    
    @property
    def paths(self):
        """Returns a list of all paths in the order they were added.
        """
        return list(self._paths[key] for key in self.keys)
    
    def iter_files(self):
        """Iterates over all (key, file) pairs in the order they were added.
        """
        keys = list(self.keys)
        for key in keys:
            yield (key, self.get(key))
    
    def close(self):
        """Close all files being tracked.
        """
        for fh in self._files.values():
            if fh and not (isinstance(fh, dict) or fh.closed):
                fh.close()

class FileInput(FileManager):
    """Similar to python's ``fileinput`` that uses ``xopen`` to open files.
    Currently only support sequential line-oriented access via ``next`` or
    ``readline``.
    """
    def __init__(self, files=None, mode='t', encoding='utf-8'):
        if 'r' not in mode:
            mode = 'r' + mode
        super(FileInput, self).__init__(mode=mode)
        for m in mode:
            if m not in ('r', 't', 'b', 'U'):
                raise ValueError("Invalid mode: {}".format(mode))
        self._is_binary = 'b' in mode
        self.fileno = -1
        self._startlineno = 0
        self.filelineno = 0
        self._pending = True
        if files:
            self.add_all(files)
    
    @property
    def filekey(self):
        if self.fileno < 0:
            return None
        return list(self.keys)[self.fileno]
    
    @property
    def filename(self):
        """Returns the name of the file currently being read.
        """
        if self.fileno < 0:
            return None
        return self.get_path(self.fileno)
    
    @property
    def lineno(self):
        return self._startlineno + self.filelineno
    
    @property
    def finished(self):
        return self.fileno >= len(self)
    
    def add(self, f, key : 'str' = None):
        """Overrides FileManager.add() to prevent file-specific open args.
        """
        # If we've already finished reading all the files,
        # put us back in a pending state
        if self.finished:
            self._pending = True
            self.fileno -= 1
        super(FileInput, self).add(f, key)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while True:
            if not self._ensure_file():
                raise StopIteration()
            try:
                line = self._nextline()
                #if not line:
                #    raise StopIteration()
                self.filelineno += 1
                return line
            except StopIteration:
                self._pending = True
    
    def _ensure_file(self):
        if self._pending:
            self.fileno += 1
            self._startlineno += self.filelineno
            self.filelineno = 0
            if not self.finished:
                # set the _nextline method
                curfile = self.get(self.fileno)
                if is_iterable(curfile):
                    self._nextline = lambda: next(curfile)
                #elif hasattr(curfile, 'readline'):
                #    self._nextline = curfile.readline
                else: # pragma: no-cover
                    raise Exception("File associated with key {} is not "
                                    "iterable and does not have a 'readline' "
                                    "method".format(self.filekey))
            self._pending = False
        return not self.finished
    
    def readline(self):
        """Read the next line from the current file (advancing to the next
        file if necessary and possible).
        
        Returns:
            The next line, or the empty string if ``self.finished==True``
        """
        try:
            return next(self)
        except StopIteration:
            return b'' if self._is_binary else ''

def fileinput(files=None, mode='t', encoding='utf-8'):
    """Convenience method that creates a new ``FileInput``.
    
    Args:
        files: The files to open. If None, files passed on the command line are
            used, or STDIN if there are no command line arguments.
        mode: The default read mode ('t' for text or 'b' for binary)
        encoding: The default character encoding
    
    Returns:
        A FileInput instance
    """
    if not files:
        files = sys.argv[1:] or (STDIN,)
    elif isinstance(files, str):
        files = (files,)
    return FileInput(files, mode, encoding)

class FileOutput(FileManager):
    """Base class for file manager that writes to multiple files.
    """
    def __init__(self, files=None, mode='t', linesep=os.linesep, encoding='utf-8'):
        if not any(m in mode for m in ('w', 'a', 'x')):
            mode = 'w' + mode
        super(FileOutput, self).__init__(mode=mode)
        for m in mode:
            if m not in ('w', 'a', 'x', 't', 'b', 'U'):
                raise ValueError("Invalid mode: {}".format(mode))
        self.encoding = encoding
        self.num_lines = 0
        self._is_binary = 'b' in mode
        if self._is_binary and isinstance(linesep, str):
            self.linesep = linesep.encode(encoding)
        else:
            self.linesep = linesep
        self._linesep_len = len(linesep)
        if files:
            self.add_all(files)
    
    def writelines(self, lines : 'iterable', newlines : 'bool' = True):
        """Write an iterable of lines to the output(s).
        
        Args:
            lines: An iterable of lines to write
            newlines: Whether to add line separators after each line
        """
        for line in lines:
            self.writeline(line, newline=newlines)
    
    def writeline(self, line : 'str' = None, newline : 'bool' = True):
        """Write a line to the output(s).
        
        Args:
            line: The line to write
            newline: Whether to also write a line separator. If None (the
                default), the line will be checked to see if it already has a
                line separator, and one will be written if it does not.
        """
        if self.num_lines == 0:
            self.num_lines += 1
        sep = None
        if newline:
            self.num_lines += 1
            sep = self.linesep
        self._writeline(self._encode(line), sep)
    
    def _writeline(self, line : 'str', sep : 'str'):
        """Does the work of writing a line to the output(s). Must be implemented
        by subclasses.
        """
        raise NotImplemented()
    
    def _encode(self, line):
        is_binary = isinstance(line, bytes)
        if self._is_binary and not is_binary:
            line = line.encode(self.encoding)
        elif not self._is_binary and is_binary:
            line = line.decode(self.encoding)
        return line
    
    def _write_to_file(self, f, line, sep):
        """Writes a line to a file, gracefully handling the (rare? nonexistant?)
        case where the file has a ``writelines`` but not a ``write`` method.
        """
        try:
            if line:
                f.write(line)
            if sep:
                f.write(sep)
        except: # pragma: no-cover
            if sep:
                line += sep
            f.writelines((line,))

class TeeFileOutput(FileOutput):
    """Write output to mutliple files simultaneously.
    """
    def _writeline(self, line=None, sep=None):
        for key, f in self.iter_files():
            self._write_to_file(f, line, sep)

class CycleFileOutput(FileOutput):
    def __init__(self, files=None, mode='t', n=1, **kwargs):
        super(CycleFileOutput, self).__init__(files=files, mode=mode, **kwargs)
        self._cur_file_idx = 0
    
    def _writeline(self, line=None, sep=None):
        self._write_to_file(self.get(self._cur_file_idx), line, sep)
        self._cur_file_idx = (self._cur_file_idx + 1) % len(self)
        
class NCycleFileOutput(FileOutput):
    """Alternate output lines between files. The ``n`` argument specifies how
    many lines to write to a file before moving on to the next file.
    """
    def __init__(self, files=None, mode='t', n=1, **kwargs):
        super(NCycleFileOutput, self).__init__(files=files, mode=mode, **kwargs)
        self.n = n
        self._cur_line_idx = 0
        self._cur_file_idx = 0
    
    def _writeline(self, line=None, sep=None):
        if self._cur_line_idx >= self.n:
            self._cur_line_idx = 0
            self._cur_file_idx += 1
        if self._cur_file_idx >= len(self):
            self._cur_file_idx = 0
        self._write_to_file(self.get(self._cur_file_idx), line, sep)
        self._cur_line_idx += 1

def fileoutput(files=None, mode='t', linesep=os.linesep, encoding='utf-8',
               file_output_type=TeeFileOutput, **kwargs):
    """Convenience function to create a fileoutput.
    
    Args:
        files: The files to write to
        mode: The write mode ('t' or 'b')
        linesep: The separator to use when writing lines
        encoding: The default file encoding to use
        file_output_type: The specific subclass of FileOutput to create
        kwargs: additional arguments to pass to the FileOutput constructor
    
    Returns:
        A FileOutput instance
    """
    if not files:
        files = sys.argv[1:] or (STDOUT,)
    elif isinstance(files, str):
        files = (files,)
    return file_output_type(files, mode=mode, linesep=linesep,
                            encoding=encoding, **kwargs)

class RollingFileOutput(FileOutput):
    """Write up to ``n`` lines to a file before opening the next file. File
    names are created from a pattern.
    
    Args:
    """
    def __init__(self, filename_pattern, mode='t', n=1, **kwargs):
        super(RollingFileOutput, self).__init__(mode=mode, **kwargs)
        self.filename_pattern = filename_pattern
        self.n = n
        self._cur_line_idx = 0
        self._cur_file_idx = 0
    
    def _writeline(self, line=None, sep=None):
        if self._cur_line_idx >= self.n:
            self._cur_line_idx = 0
            self._cur_file_idx += 1
        if self._cur_file_idx >= len(self):
            self._open_next_file()
        self._write_to_file(self.get(self._cur_file_idx), line, sep)
        self._cur_line_idx += 1
    
    def _open_next_file(self):
        self.add(self.filename_pattern.format(self._cur_file_idx))

# Misc

def linecount(f, linesep : 'str' = None, buffer_size : 'int' = 1024 * 1024,
              **kwargs) -> 'int':
    """Fastest pythonic way to count the lines in a file.
    
    Args:
        path: File object, or path to the file
        linesep: Line delimiter, specified as a byte string (e.g. b'\\n')
        bufsize: How many bytes to read at a time (1 Mb by default)
        kwargs: Additional arguments to pass to the file open method
    
    Returns:
        The number of lines in the file. Blank lines (including the last line
        in the file) are included.
    """
    if buffer_size < 1:
        raise ValueError("'buffer_size' must be >= ")
    if linesep is None:
        linesep = os.linesep.encode()
    if 'mode' not in kwargs:
        kwargs['mode'] = 'rb'
    elif kwargs['mode'] != 'rb':
        raise ValueError("File must be opened with mode 'rb'")
    with open_(f, **kwargs) as fh:
        if fh is None:
            return -1
        read_f = fh.read # loop optimization
        buf = read_f(buffer_size)
        if len(buf) == 0: # empty file case
            return 0
        lines = 1
        while buf:
            lines += buf.count(linesep)
            buf = read_f(buffer_size)
        return lines

def is_iterable(x):
    """Returns True if ``x`` is a non-string Iterable.
    
    Args:
        x: The object to test
    """
    return isinstance(x, Iterable) and not isinstance(x, str)
