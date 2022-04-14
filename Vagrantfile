Vagrant.configure("2") do |config|
    config.hostmanager.enabled = true 
    config.hostmanager.manage_host = true
    config.vm.define "dev" do |dev|
        config.vm.box = "ubuntu/focal64"
        dev.vm.hostname = "dev01"
        dev.vm.network "private_network", ip: "192.168.56.2"
        dev.vm.provision "shell", path: "dev-install.sh"  
        dev.vm.provider "virtualbox" do |vb|
            vb.cpus = 2
            vb.memory = "2048"
        end
    end
end
  