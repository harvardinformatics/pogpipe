user = new RCUserModel()
user.username
user.email
user.first_name
etc...

Portal_User_Factory::exists_in_AD(newuser)    # This checks the username and the email.
Portal_User_Factory::username_exists_in_ID(username)
Portal_User_Factory::email_exists_in_ID(email)

Portal_User_Factory::make_username(newuser):

  # Takes some combination of initial/lastname/number and returns an
    unused username

Portal_User_Factory::check_user(newuser)

  # Does stuff like checks for caps, odd characters

Portal_User_Factory::compare_to_AD(newuser)

  # Gets the AD user (by username/email??) 
  
Portal_User_Factory::make_home_directory(newuser)

Portal_User_Factory::make_user_lab_directory(newuser,group)

Portal_User_Factory::get_new_uid()   # Should we do this when we save?

  #Makes user to reserve the id?

Portal_Group_Factory::get_groups_by_username(newuser)

Portal_User_Factory::save_AD_User(newuser)

  # Gets uid if needed
  # Generates the AD attributes from the user object
  # Saves to AD


Portal_User_Factory::set_user_state(newuser,state)





  
  




