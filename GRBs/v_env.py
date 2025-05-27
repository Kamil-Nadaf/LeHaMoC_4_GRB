from tqdm.auto import tqdm
import subprocess
import sys
import os

def setup_environment_quietly():
    steps = [
        ("Clear PYTHONPATH", "export PYTHONPATH="),
        ("Install virtualenv", "pip install virtualenv"),
        ("Create virtualenv", "virtualenv LeHaMoc_env"),
        ("Download Miniconda", "wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"),
        ("Make Miniconda executable", "chmod +x Miniconda3-latest-Linux-x86_64.sh"),
        ("Install Miniconda", "./Miniconda3-latest-Linux-x86_64.sh -b -f -p /usr/local"),
        ("Install Python 3.9 + ujson", "conda install -q -y --prefix /usr/local python=3.9 ujson"),
        ("Install pip packages", 
         "pip install --quiet numpy==1.21.5 astropy==5.0.4 matplotlib==3.5.1 pandas==1.4.2 tqdm==4.64.0 shapely==1.7.1 scipy==1.7.3")
    ]

    progress = tqdm(total=len(steps), desc="Setting up environment", ncols=100)
    for description, cmd in steps:
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            tqdm.write(f"❌ Failed: {description}")
            raise
        progress.set_description(f"✅ {description}")
        progress.update(1)

    # Python-side path updates after setup
    sys.path.append('/usr/local/lib/python3.9/site-packages/')
    os.environ['CONDA_PREFIX'] = '/usr/local/envs/LeHaMoc_env'

    progress.set_description("Environment is Ready!")
    progress.close()

setup_environment_quietly()
