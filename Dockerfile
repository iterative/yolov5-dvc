# FROM ultralytics/yolov5:latest-cpu
FROM ultralytics/yolov5:v7.0-cpu

# Install system dependencies
RUN apt-get update && \
    apt-get install -y apt-transport-https build-essential cmake curl gcc g++ git tree sudo unzip wget

# Install the project Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Make directory models/weights in the workdir
RUN mkdir -p models/weights

# Add a group and a user
ARG USER_ID="1000"
ARG GROUP_ID="1000"
ENV USER_ID=${USER_ID}
ENV GROUP_ID=${GROUP_ID}

RUN addgroup --gid "${GROUP_ID}" "user" && \
    useradd -m user -u "${USER_ID}" -g "${GROUP_ID}" && \
    echo 'user:user' | chpasswd user && \
    echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user && \
    sudo chown -R user /usr/src/app

USER user
