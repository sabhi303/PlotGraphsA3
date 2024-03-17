import argparse
import glob as glob
from generator import parse_config, generate_data, write_to_csv
from plotter import plot_graphs
import os


# this will retrive all the configuration files
# in the current directory (i.e. files ending with cfg)
def get_configs(config_folder) -> list:
    configs = glob.glob(f"{config_folder}/*cfg")
    return configs if len(configs) > 0 else False


def main(args):
    # following is the logic to get all configuration files and
    # later the generator will parse them, and create sequences as per the
    # configuration provided inside them

    if not os.path.isdir(args.config_folder):
        print("Invalid folder path!")
        exit(-3)

    config_files = get_configs(args.config_folder)

    # is anything related to argparse needs to be done?

    # if none configs are found
    if not config_files:
        print("Unable to print config files in the current directory")
        print("Exiting!")
        exit(-1)

    for config_file in config_files:

        print(f"Processing {config_file} ...")
        # parse the files, from the function in generator
        parsed_config = parse_config(config_file)
        # print(parsed_config)

        # generate the sequence
        generated_data = generate_data(parsed_config)
        # print(generated_data)

        # remove the config folder path from it
        config_file = config_file.replace(args.config_folder, ".")

        # change the filename & write that into csv
        op_filename = config_file.replace(".cfg", "-data.csv")
        if not   write_to_csv(op_filename, generated_data):
            print("Failed to write data in the csv file")

        # now the logic to plot this data
        plot_graphs(f"{op_filename.replace('-data.csv', ' ')}", generated_data)

    print("Done")
    return


if __name__ == "__main__":

    # Parsing command line arguments
    parser = argparse.ArgumentParser(description="Get the foldername which has config files with .cfg extension")
    parser.add_argument("config_folder", help="Path to the folder containing .cfg files")
    args = parser.parse_args()

    main(args)
