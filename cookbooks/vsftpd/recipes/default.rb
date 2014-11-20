package 'vsftpd'

service 'vsftpd' do
  supports :status => true, :stop => true, :start => true, :restart => true
  action :enable
end

template '/etc/vsftpd.conf' do
  owner 'root'
  group 'root'
  mode 0644
  variables :config => node['vsftpd']['config']
  notifies :restart, 'service[vsftpd]', :delayed
end

directory '/etc/vsftpd' do
  owner 'root'
  group 'root'
  mode 0755
end

if node['vsftpd']['chroot_local_user'] || node['vsftpd']['chroot_list_enable']
  include_recipe 'vsftpd::chroot_users'
end

include_recipe 'vsftpd::virtual_users' if node['vsftpd']['virtual_users_enable']
