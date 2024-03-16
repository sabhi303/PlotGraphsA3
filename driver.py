import argparse
import glob as glob
from generator import parse_config, generate_data, write_to_csv
from plotter import plot_graphs


# this will retrive all the configuration files
# in the current directory (i.e. files ending with cfg)
def get_configs() -> list:
    configs = glob.glob("./*cfg")
    return configs if len(configs) > 0 else False


def main(args):
    # following is the logic to get all configuration files and
    # later the generator will parse them, and create sequences as per the
    # configuration provided inside them

    config_files = get_configs()

    # is anything related to argparse needs to be done?

    # if none configs are found
    if not config_files:
        print("Unable to print config files in the current directory")
        print("Exiting!")
        exit(-1)

    for config_file in config_files:
        # parse the files, from the function in generator
        parsed_config = parse_config(config_file)
        # print(parsed_config)

        # generate the sequence
        generated_data = generate_data(parsed_config)
        # print(generated_data)

        # return

        # change the filename & write that into csv
        op_filename = config_file.replace(".cfg", "-data.csv")
        if not   write_to_csv(op_filename, generated_data):
            print("Failed to write data in the csv file")

        # now the logic to plot this data
        # making use of the argparser
        if args.plot:
            plot_graphs(f"{op_filename.replace('-data.csv', ' plot')}", generated_data)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate data from configuration files and plot graphs"
    )
    parser.add_argument(
        "--plot", action="store_true", help="Whether to plot the generated data"
    )
    args = parser.parse_args()
    main(args)
