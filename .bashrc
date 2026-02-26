test -f /etc/profile.dos && . /etc/profile.dos

# Some applications read the EDITOR variable to determine your favourite text
# editor. So uncomment the line below and enter the editor of your choice :-)
#export EDITOR=/usr/bin/vim
#export EDITOR=/usr/bin/mcedit

# add aliases if there is a .aliases file
test -s ~/.alias && . ~/.alias
# Command prompt show current path:
export PROMPT_DIRTRIM=4 # Trimming path to 4 directories

# ROS initialization
alias ros_pull='singularity pull ~/av/ros_jazzy.sif docker://morris2001/jazzy:latest'
alias ros_shell='singularity exec  ~/av/ros_jazzy.sif /bin/bash'
# alias ros_gpu_shell='singularity exec --nv  ~/av/ros_jazzy.sif /bin/bash'  
alias humble_pull='singularity pull ~/av/ros_humble.sif docker://morris2001/humble:latest'
alias humble_shell='singularity exec  ~/av/ros_humble.sif /bin/bash'

# Rest of ROS initialization in .rosinit  
# After typing: ros_shell
# then type: source ~/.rosinit
# Or after typing: humble_shell
# then type: source ~/.rosinit humble