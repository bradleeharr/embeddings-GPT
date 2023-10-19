from data_to_csv import *

element_data_fp = "element_data"
github_data_fp = "github_data"


def main():
    element_to_csv(element_data_fp)
    github_to_csv(github_data_fp)


if __name__ == "__main__":
    main()