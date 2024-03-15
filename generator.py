import configparser
import numpy as np
import csv

# this will return all the read parameters in the dictionary format
def parse_config(config_file) -> dict:
    # print('in parse config')
    cp = configparser.ConfigParser()
    cp.read(config_file)

    # ata ithe fkt key value pairs banavayachya aahet
    config = {}
    for section in cp.sections():
        config[section] = dict(cp.items(section=section))

    return config    

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    seed = int(lines[0].strip())
    num_samples = int(lines[1].strip())
    
    distributions = []
    for line in lines[2:]:
        parts = line.strip().split()
        dist_name = parts[0].lower()
        dist_params = list(map(float, parts[1:]))
        distributions.append((dist_name, dist_params))

        return seed, num_samples, distributions

# convert all values to integer or floating of the dictionary
# and convert keys to lowercase
def convert_to_float(dictionary) -> dict:
     int_dictionary = {}
     for key, value in dictionary.items():
        int_dictionary[key.lower()] = dict(map(lambda x: (x[0].lower(), float(x[1]) if '.' in x[1] else int(x[1])), value.items()))

     return int_dictionary

# Define the inverse transform sampling functions for Dagum and Skellam distributions
def inverse_transform_dagum(alpha, beta, p, size=1):
    u = np.random.random(size)
    return (1 / beta) * ((1 - (1 - u) ** (1 / alpha)) ** (1 / p))

def inverse_transform_skellam(mu1, mu2, size=1):
    x = np.zeros(size)
    for i in range(size):
        p = mu1 / (mu1 + mu2)
        s = np.random.poisson((mu1 + mu2) / 2)
        s1 = np.random.binomial(s, p)
        s2 = s - s1
        x[i] = s1 - s2
    return x

def generate_data(parameters):

    # modify the key values to correct datatype and case format
    parameters = convert_to_float(parameters)
    # will seed the random data
    np.random.seed(parameters.get("rng").get("seed"))
    del parameters["rng"] #as this is not required further

    generated_data = {}

    for distribution, dist_params in parameters.items():
        distributed_data = []
        if distribution == 'gamma':
            distributed_data = np.random.gamma(
                    dist_params.get("shape1"),
                    dist_params.get("shape2"),  
                    dist_params.get("size")
            )
        elif distribution == 'exponential':
            distributed_data = np.random.exponential(
                scale=dist_params.get("scale"),
                size = dist_params.get("size")
            )
        elif distribution == 'gaussian':
            distributed_data = np.random.normal(
                scale=dist_params.get("scale"),
                size = dist_params.get("size")
            )
        elif distribution == 'dag':
            distributed_data = inverse_transform_dagum(
                alpha = dist_params.get("alpha"), 
                beta = dist_params.get("beta"), 
                p = dist_params.get("p"), 
                size= dist_params.get("size")
            )
        elif distribution == 'geometric':
            distributed_data = np.random.geometric(
                p = dist_params.get("p"), 
                size=dist_params.get("size")
                )
            
        elif distribution == 'poisson':
            distributed_data = np.random.poisson(
                lam= dist_params.get("lam"), 
                size=dist_params.get("size")
                )
        elif distribution == 'skellam':
            distributed_data = inverse_transform_skellam(
                mu1 = dist_params.get("mu1"), 
                mu2 = dist_params.get("mu2"), 
                size= dist_params.get("size")
                )
            
        generated_data[distribution] = distributed_data
    
    return generated_data


def write_to_csv(filename, generated_data) -> bool:
    print("Generated Data here: ", generated_data)
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for distribution, data in generated_data.items():
            csv_writer.writerow([f"{distribution} {data.shape[0]}"] + data.tolist())
    return True