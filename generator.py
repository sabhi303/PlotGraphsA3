import configparser
import numpy as np
import csv


# this will return all the read parameters in the dictionary format
def parse_config(config_file) -> dict:
    # print('in parse config')
    cp = configparser.ConfigParser()
    cp.read(config_file)

    config = {}
    # what I am doing is parsing the parameters for each distributions
    # as mentioned in the configuration file, i.e. for each section of the config file
    for section in cp.sections():
        config[section] = dict(cp.items(section=section))

    return config


# convert all values to integer or floating of the dictionary
# and convert keys to lowercase
def convert_to_float(dictionary) -> dict:
    int_dictionary = {}
    for key, value in dictionary.items():
        int_dictionary[key.lower()] = dict(
            map(
                lambda x: (x[0].lower(), float(x[1]) if "." in x[1] else int(x[1])),
                value.items(),
            )
        )

    return int_dictionary


# inverse transform sampling functions for Dagum and Skellam distributions
def distribution_dagum(alpha, beta, p, seed=None, size=1):
    if alpha <= 0 or beta <= 0 or p <= 0:
        raise ValueError("Parameters alpha, beta, and p must be greater than 0.")
    if seed is not None:
        np.random.seed(seed=seed)
    u = np.random.uniform(0, 1, size)
    data = beta * ((1 - np.power(u, -1/alpha)) ** (-1/p) - 1)
    return data


def distribution_skellam(mu1, mu2, seed, size=1):
    np.random.seed(seed=seed)
    pois1 = np.random.poisson(mu1, size)
    pois2 = np.random.poisson(mu2, size)
    data = pois1 - pois2
    return data


def generate_data(parameters):
    # modify the key values to correct datatype and case format
    parameters = convert_to_float(parameters)
    # will seed the random data
    # print("Parameter", parameters)
    seed = parameters.get("rng").get("seed")
    np.random.seed(seed=seed)
    del parameters["rng"]  # as this is not required further

    generated_data = {}

    for distribution, dist_params in parameters.items():
        distributed_data = []
        if distribution == "gamma":
            distributed_data = np.random.gamma(
                dist_params.get("shape1"),
                dist_params.get("shape2"),
                dist_params.get("size"),
            )
        elif distribution == "exponential":
            distributed_data = np.random.exponential(
                scale=dist_params.get("scale"), size=dist_params.get("size")
            )
        elif distribution == "gaussian":
            distributed_data = np.random.normal(
                scale=dist_params.get("scale"), size=dist_params.get("size")
            )
        elif distribution == "dag":
            distributed_data = distribution_dagum(
                alpha=dist_params.get("alpha"),
                beta=dist_params.get("beta"),
                p=dist_params.get("p"),
                size=dist_params.get("size"),
                seed=seed,
            )
        elif distribution == "geometric":
            distributed_data = np.random.geometric(
                p=dist_params.get("p"), size=dist_params.get("size")
            )

        elif distribution == "poisson":
            distributed_data = np.random.poisson(
                lam=dist_params.get("lam"), size=dist_params.get("size")
            )
        elif distribution == "skellam":
            distributed_data = distribution_skellam(
                mu1=dist_params.get("mu1"),
                mu2=dist_params.get("mu2"),
                size=dist_params.get("size"),
                seed=seed,
            )

        # this will maintain both the data and the parameters which
        # have been used to generate the data
        generated_data[distribution] = {
            "data": distributed_data,
            "parameters": tuple(dist_params.values()),
        }

    return generated_data


def write_to_csv(filename, generated_data) -> bool:
    # print("Generated Data here: ", generated_data)
    with open(filename, "w", newline="") as file:
        csv_writer = csv.writer(file)
        for distribution, data in generated_data.items():
            # this will store the data in the format:
            # distribution_name (its parameters), ditribution
            csv_writer.writerow(
                [f"{distribution} {str(data.get('parameters'))}"]
                + data.get("data").tolist()
            )
    return True
