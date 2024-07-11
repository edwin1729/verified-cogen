import argparse
import logging
import os
import pathlib

from tqdm import tqdm
from typing_extensions import Optional

from helpers import pprint_stat, rename_file, tabulate_list
from llm import LLM
from modes import Mode, VALID_MODES
from runners.invariants import InvariantRunner
from runners.preconditions import PreconditionRunner
from verus import Verus

if not os.path.exists("log"):
    os.mkdir("log")
logging.basicConfig(
    level=os.environ.get("PYLOG_LEVEL", "INFO").upper(), filename="log/llm.log"
)
logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("-d", "--dir", help="directory to run on", required=False)

    parser.add_argument(
        "--insert-invariants-mode",
        help=f"insert invariants using: {', '.join(VALID_MODES)}",
        default="llm",
    )
    parser.add_argument(
        "--bench-type",
        help="benchmark type, available: {invariants, preconditions}",
        default="invariants",
    )
    parser.add_argument("--temperature", help="model temperature", default=0, type=int)
    parser.add_argument("--shell", help="shell", default=os.getenv("SHELL"))
    parser.add_argument(
        "--verus-path", help="verus path", default=os.getenv("VERUS_PATH")
    )
    parser.add_argument(
        "--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN")
    )
    parser.add_argument(
        "--llm-profile", help="llm profile", default="gpt-4-1106-preview"
    )
    parser.add_argument("--tries", help="number of tries", default=1, type=int)
    parser.add_argument("--retries", help="number of retries", default=0, type=int)
    parser.add_argument(
        "-s", "--output-style", choices=["stats", "full"], default="full"
    )
    return parser.parse_args()


def main():
    args = get_args()
    mode = Mode(args.insert_invariants_mode)
    if args.input is None and args.dir is None:
        args.input = input("Input file: ").strip()

    runner = InvariantRunner if args.bench_type == "invariants" else PreconditionRunner

    verus = Verus(args.shell, args.verus_path)
    if args.dir is not None:
        success, success_zero_tries, failed = [], [], []

        files = list(pathlib.Path(args.dir).glob("**/*.rs"))
        for file in tqdm(files):
            llm = LLM(args.grazie_token, args.llm_profile, args.temperature)

            retries = args.retries + 1
            tries = None
            while retries > 0 and tries is None:
                tries = runner.run_on_file(
                    logger, verus, mode, llm, args.tries, str(file)
                )
                retries -= 1

            name = rename_file(file)
            if tries == 0:
                logger.info(f"{name} verified without modification")
                success_zero_tries.append(name)
            elif tries is not None:
                logger.info(f"{name} verified with modification")
                success.append(name)
            else:
                logger.error(f"{name} failed")
                failed.append(name)

        if args.output_style == "full":
            success_zero_tries_tabbed = tabulate_list(success_zero_tries)
            success_tabbed = tabulate_list(success)
            failed_tabbed = tabulate_list(failed)
            if len(success_zero_tries) > 0:
                print(f"Verified without modification: {success_zero_tries_tabbed}")
            if len(success) > 0:
                print(f"Verified with modification: {success_tabbed}")
            if len(failed) > 0:
                print(f"Failed: {failed_tabbed}")

        pprint_stat(
            "Verified without modification", len(success_zero_tries), len(files)
        )
        pprint_stat("Verified with modification", len(success), len(files))
        pprint_stat("Failed", len(failed), len(files))

    else:
        llm = LLM(args.grazie_token, args.llm_profile, args.temperature)
        tries = runner.run_on_file(logger, verus, mode, llm, args.tries, args.input)
        if tries == 0:
            print("Verified without modification")
        elif tries is not None:
            print("Verified with modification on try", tries)
        else:
            print("Failed to verify")


if __name__ == "__main__":
    main()
