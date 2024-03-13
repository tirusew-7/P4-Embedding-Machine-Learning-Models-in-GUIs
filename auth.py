import yaml

def authenticate(username, password):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    user_info = config.get('credentials', {}).get('usernames', {}).get(username, {})
    return user_info.get('password') == password

def save_config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

def create_account(new_username, new_password):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    if new_username in config['credentials']['usernames']:
        return False, "Username already exists. Please choose a different username."
    else:
        config['credentials']['usernames'][new_username] = {'full_name': '', 'email': '', 'logged_in': False, 'name': new_username, 'password': new_password}
        save_config(config)
        return True, "Account created successfully. You can now log in."
