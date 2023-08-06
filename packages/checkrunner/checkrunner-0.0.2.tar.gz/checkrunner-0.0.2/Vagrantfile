#@IgnoreInspection BashAddShebang
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/debian-8.6"

  # config.vm.box_check_update = false
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.synced_folder ".", "/home/vagrant/src/", type: "virtualbox"

  config.vm.provider "virtualbox" do |vb|
  #   vb.gui = true
      vb.memory = "512"
  end

  config.vm.provision "shell", inline: <<-SHELL
    touch /etc/is_vagrant_vm
    echo 'en_GB.UTF-8 UTF-8' >> /etc/locale.gen
    localedef -i en_GB -f UTF-8 en_GB.UTF-8
    locale-gen en_GB.UTF-8 en_US.UTF-8

    apt-get update
    sudo apt-get -y --force-yes install \
      git \
      python \
      python-all \
      python-dev \
      python-distutils-extra \
      python-pip \
      python3 \
      python3-all \
      python3-dev \
      python3-distutils-extra \
      python3-pip \
      vim \

    pip install --upgrade pip setuptools
    pip install --upgrade virtualenv setuptools-scm pytest

    sudo -u vagrant virtualenv /home/vagrant/venvs/dev
    echo 'source /home/vagrant/venvs/dev/bin/activate' >> /home/vagrant/.profile

    # Setup our project
    cd /home/vagrant/src
    sudo -u vagrant /home/vagrant/venvs/dev/bin/pip install -U .
    sudo -u vagrant /home/vagrant/venvs/dev/bin/python setup.py develop
  SHELL
end
