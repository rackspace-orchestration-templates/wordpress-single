# Support whyrun
def whyrun_supported?
  true
end

action :add do
  run_context.include_recipe 'htpasswd'

  htpasswd "vsftpd password for user #{new_resource.user}" do
    file node['vsftpd']['config']['user_passwd_file']
    user new_resource.user
    password new_resource.password
    type 'crypt'
    new_resource.updated_by_last_action(true)
  end

  file ::File.join(node['vsftpd']['config']['user_config_dir'], new_resource.user) do
    owner 'root'
    group 'root'
    mode 0644
    root = "local_root=#{new_resource.root.sub(%r{/\./.*}, '')}\n"
    user = "guest_username=#{new_resource.local_user}\n" unless new_resource.local_user.to_s.empty?
    content "#{root}#{user}"
    notifies :restart, 'service[vsftpd]'
    new_resource.updated_by_last_action(true)
  end
end

action :remove do
  run_context.include_recipe 'htpasswd'

  htpasswd "Remove vsftpd user #{new_resource.user}" do
    file node['vsftpd']['config']['user_config_dir']
    user new_resource.user
    new_resource.updated_by_last_action(true)
  end

  file ::File.join(node['vsftpd']['config']['user_config_dir'], new_resource.user) do
    action :delete
    notifies :restart, 'service[vsftpd]'
    new_resource.updated_by_last_action(true)
  end
end

def initialize(*args)
  super
  @run_context.include_recipe 'vsftpd'
end
