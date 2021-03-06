# Retro Gym

## TODOs
* Find a way to reduce state dimension
* Record own gameplay
* Train supervised model
* Train NEAT algorithm
* Train DQN model

## How to setup

### Step 1 - Create a conda environment

```
conda create --name rl-playground python=3.7
conda activate rl-playground
pip install -r requirements.txt
```
As of writing this doc retro-gym has max support for Python 3.7. \
Check [here](https://retro.readthedocs.io/en/latest/getting_started.html) for the latest version.

---

### Step 2 - Copy the ROM to retro-gym's **stable** game folder 

Due to the nature of the ROM, OpenAI does not support it by default.
```
#Linux
/home/user/.conda/envs/env_name/lib/python3.7/site-packages/retro/data/stable

#Windows
C:/Users/.conda/Miniconda3/envs/env_name/Lib/site-packages/retro/data/stable
```

### Step 3 - Test that eveything is running

Run the random agent provided
```
python random_agent.py
```

## Using the Retro Integration UI

### Step 1 - Move the exe to the folder which contains retro

You have to run `import retro; print(retro.__path__)`! It'll display a filepath and you have to move the .exe file to there and run it.

### Step 2 - Integrate the ROM 

Execute `Ctrl + Shift + O` and locate the ROM in your filesistem.

## Special thanks to

* Esteveste - **Started code for Mario Kart** - [GitHub](https://github.com/esteveste/gym-SuperMarioKart-Snes)

## Known issues

* If `01_manual_kart.py` is missing or getting deleted by Windows defender (because it contains a key listener), check the following [link](https://answers.microsoft.com/en-us/protect/forum/all/windows-defender-deleting-my-own-applications/65b96548-e411-42b0-8ce1-ae28f46eb9a1) to setup exceptions for this folder.