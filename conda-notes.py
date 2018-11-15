from conda.cli import main_search
from conda.cli import conda_argparse

p = conda_argparse.generate_parser()
args = p.parse_args(['search','pandas=0.22=py36*','--info'])
main_search.execute(args, None)

# need to copy-paste conda/cli/main_search.py::execute() to return a result...
