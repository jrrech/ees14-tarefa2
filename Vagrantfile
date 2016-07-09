Vagrant.configure("2") do |config|

  config.ssh.forward_agent = true
  config.vm.box = "ubuntu/trusty32"

  config.vm.define "ees14vm", primary: true do |ees14vm|
    ees14vm.vm.network :forwarded_port, host: 42022, guest: 22
    ees14vm.vm.network :forwarded_port, host: 43000, guest: 3000
    ees14vm.vm.hostname = 'ees14vm'

    ees14vm.vm.provider "virtualbox" do |v|
      v.name = "ees14vm"
    end

    ees14vm.vm.provision 'ansible' do |ansible|
      ansible.host_key_checking = false
      ansible.playbook = "playbook.yml"
      ansible.raw_ssh_args = ['-o UserKnownHostsFile=/dev/null -o ForwardAgent=yes']
    end
  end
end
