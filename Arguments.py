params = {}

# Whether to run on GPU
params["gpu"] = False
# List of pot-scaled bet sizes to use in the tree
params["bet_sizing"] = [1, 2, 3]
# Server running the ACPC dealer
params["acpc_server"] = "localhost"
# Server port running the ACPC dealer
params["acpc_server_port"] = 20000
# The number of betting rounds in the game
params["streets_count"] = 2
# The tensor datatype used for storing DeepStack's internal data
params["Tensor"] = torch.FloatTensor  # Assuming you have torch imported
# The directory for data files
params["data_directory"] = "../Data/"
# The size of the game's ante, in chips
params["ante"] = 100
# The size of each player's stack, in chips
params["stack"] = 1200
# The number of iterations that DeepStack runs CFR for
params["cfr_iters"] = 1000
# The number of preliminary CFR iterations which DeepStack doesn't factor into the average strategy (included in cfr_iters)
params["cfr_skip_iters"] = 500
# How many poker situations are solved simultaneously during data generation
params["gen_batch_size"] = 10
# How many poker situations are used in each neural net training batch
params["train_batch_size"] = 100
# Path to the solved poker situation data used to train the neural net
params["data_path"] = "../Data/TrainSamples/PotBet/"
# Path to the neural net model
params["model_path"] = "../Data/Models/PotBet/"
# The name of the neural net file
params["value_net_name"] = "final"
# The neural net architecture
params["net"] = [
    "nn.Linear(input_size, 50)",
    "nn.PReLU()",
    "nn.Linear(50, output_size)",
]
# How often to save the model during training
params["save_epoch"] = 2
# How many epochs to train for
params["epoch_count"] = 10
# How many solved poker situations are generated for use as training examples
params["train_data_count"] = 100
# How many solved poker situations are generated for use as validation examples
params["valid_data_count"] = 100
# Learning rate for neural net training
params["learning_rate"] = 0.001

assert params["cfr_iters"] > params["cfr_skip_iters"]

# If using GPU
if params["gpu"]:
    import torch

    params["Tensor"] = torch.cuda.FloatTensor

# You can now use the 'params' dictionary in your Python code.
