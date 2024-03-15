import glob as glob
from generator import parse_config,generate_data, write_to_csv
from plotter import plot_graphs


# this will retrive all the configuration files
# in the current directory (i.e. files ending with cfg)
def get_configs() -> list:
    configs = glob.glob("./*cfg")
    return configs if len(configs)> 0 else False

def main():

    # following is the logic to get all configuration files and 
    # later the generator will parse them, and create sequences as per the 
    # configuration provided inside them

    config_files = get_configs()

    # if none are found
    if not config_files:
        print("Unable to print config files in the current directory")
        print("Exiting!")
        exit(-1)
    
    for config_file in config_files:
        # parse the files, from the function in generator
        # printing it for now
        parsed_config = parse_config(config_file)
        print (parsed_config)

        # generate the sequence
        generated_data = generate_data(parsed_config)
        print(generated_data)
        
        # write that into csv
        # change the filename
        op_filename = config_file.replace('.cfg', '-data.csv')
        if(write_to_csv(op_filename, generated_data)):
            print("Data written Successfully")
        else:
            print("Failed to write data in the csv file")
        # okay, done
            
        # now the logic to plot this data
        # okay, ata tatpurata asach thevtoy, like csv read nai karate, direct data pass krto
        plot_graphs(f"{op_filename.replace('-data.csv', ' plot')}", generated_data)

    return

if __name__ == '__main__':
    main()