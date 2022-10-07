import argparse

parser = argparse.ArgumentParser()

parser.add_argument("bob", type=int)
parser.add_argument("--a", "--bob-bobodfdsfsdf", "--bodfb-bo", "-b", type=int)

args = vars(parser.parse_args())
print(f"{args}")
