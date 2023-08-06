import os
import argparse


def main():
    """Receive command line arguments, output the result accordingly."""
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="Create the path tree for the directory " +
                             "with this path. If omitted, creates for " +
                             "current directory",
                        nargs='?', default='.')
    parser.add_argument("-o", "--output",
                        help="Name of the output file " +
                             "(overwritten if present, created if not)")
    parser.add_argument("-s", "--show",
                        help="Print the output to terminal",
                        action="store_true")
    args = parser.parse_args()

    outFile = None
    if args.output:
        outFile = open(args.output, 'w')

    path = create_path(args.directory, outFile)
    if args.show:
        print ('\n'.join(path))


def create_path(dirPath='.', outFile=None, levelAligner='|',
                fileIndicator='|-'):
    """Create the path array for the specified directory.

    Keyword argumens:
    dirPath: a string representing a directory path to generate the array for.
               (defaults to current directory, '.')
    outFile: an open file object, the formatted output is written to this file.
               (defaults to None)
    levelAligner: a string representing the character that will be running
                    through the left side of the output path tree to indicate
                    the top level files. (defaults to a pipe '|')
    fileIndicator: a string that is printed right before the file names.
                     (defaults to a pipe and a hyphen '|-')

    Returns:
    An array of strings representing the path tree.
    """
    path = generate_path(dirPath, levelAligner, fileIndicator)

    if outFile is not None and not outFile.closed:
        outFile.write('\n'.join(path))
        outFile.close()
    return path


def generate_path(dirPath, levelAligner,
                  fileIndicator, level=0, pathMap=None):
    if pathMap is None:
        pathMap = []
    files = []

    # If directory, visit its contents, otherwise just return
    try:
        files = os.listdir(dirPath.strip())
    except OSError:
        return

    for file in files:
        levelLine = format_line(levelAligner, fileIndicator, file, level)
        pathMap.append(levelLine)

        # Recursively visit this entry
        generate_path(os.path.join(dirPath, file), levelAligner,
                      fileIndicator, level+1, pathMap)

    return pathMap


def format_line(levelAligner, fileIndicator, filename, level):
    aligner = levelAligner if level > 0 else ""
    return aligner + (" "*level) + fileIndicator + filename

if __name__ == "__main__":
    main()
