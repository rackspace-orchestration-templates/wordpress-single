class Chef::Recipe::WordPress

  # Determine whether or not we want to configure SSL for a site
  def self.use_ssl(key, cert, override)
    # key = SSL key attribute
    # cert = SSL cert attribute
    # override = use_ssl override in case no key/cert provided
    if key && cert
      return true
    elsif override
      return true
    else
      return false
    end
  end

end
