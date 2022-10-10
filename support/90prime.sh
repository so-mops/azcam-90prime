AZCAM_DATAROOT="/home/lesser/data"
export AZCAM_DATAROOT
echo AzCam data root is $AZCAM_DATAROOT

echo Activating azcam virtual environment
source ~/azcam/venvs/azcam/bin/activate

ipython --profile azcamserver -i -c "import azcam_90prime.server; from azcam.cli import *"
